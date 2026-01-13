"""
GitHub Service - интеграция с GitHub API
"""
from github import Github, GithubException
from typing import List, Dict, Optional
import os
import base64
from datetime import datetime


class GitHubService:
    """Сервис для работы с GitHub API"""

    def __init__(self):
        """Инициализация GitHub клиента"""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN не найден в environment variables")

        self.client = Github(token)
        self.repo_name = os.getenv("GITHUB_REPO")

        if not self.repo_name:
            raise ValueError("GITHUB_REPO не найден в environment variables")

    def get_repository(self):
        """Получить репозиторий"""
        try:
            return self.client.get_repo(self.repo_name)
        except GithubException as e:
            raise Exception(f"Ошибка получения репозитория: {e}")

    def get_file_content(self, path: str, branch: str = "main") -> Dict:
        """
        Получить содержимое файла

        Args:
            path: Путь к файлу
            branch: Ветка (по умолчанию main)

        Returns:
            Dict с содержимым и метаданными
        """
        try:
            repo = self.get_repository()
            content_file = repo.get_contents(path, ref=branch)

            # Декодировать содержимое
            if isinstance(content_file, list):
                raise ValueError(f"{path} это директория, не файл")

            content = content_file.decoded_content.decode('utf-8')

            return {
                "path": path,
                "content": content,
                "size": content_file.size,
                "sha": content_file.sha,
                "url": content_file.html_url,
                "language": self._detect_language(path)
            }
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(f"Файл {path} не найден")
            raise Exception(f"Ошибка чтения файла: {e}")

    def get_directory_tree(self, path: str = "", branch: str = "main") -> List[Dict]:
        """
        Получить дерево файлов и папок

        Args:
            path: Путь к директории
            branch: Ветка

        Returns:
            Список файлов и папок
        """
        try:
            repo = self.get_repository()
            contents = repo.get_contents(path, ref=branch)

            if not isinstance(contents, list):
                contents = [contents]

            tree = []
            for content in contents:
                node = {
                    "name": content.name,
                    "path": content.path,
                    "type": content.type,  # "file" or "dir"
                    "size": content.size if content.type == "file" else 0,
                    "sha": content.sha,
                }

                # Если это директория, можно рекурсивно получить детей
                if content.type == "dir":
                    node["children"] = []  # Placeholder, загружается по требованию

                tree.append(node)

            # Сортировка: папки первыми, потом файлы
            tree.sort(key=lambda x: (x["type"] != "dir", x["name"].lower()))

            return tree

        except GithubException as e:
            if e.status == 404:
                return []
            raise Exception(f"Ошибка чтения директории: {e}")

    def search_code(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Поиск по коду

        Args:
            query: Поисковый запрос
            max_results: Максимум результатов

        Returns:
            Список найденных фрагментов
        """
        try:
            repo = self.get_repository()
            results = repo.search_code(query)

            found = []
            for idx, result in enumerate(results):
                if idx >= max_results:
                    break

                found.append({
                    "file": result.path,
                    "url": result.html_url,
                    "sha": result.sha,
                    "score": result.score,
                })

            return found

        except GithubException as e:
            raise Exception(f"Ошибка поиска: {e}")

    def get_file_history(self, path: str, max_commits: int = 10) -> List[Dict]:
        """
        История изменений файла

        Args:
            path: Путь к файлу
            max_commits: Максимум коммитов

        Returns:
            Список коммитов
        """
        try:
            repo = self.get_repository()
            commits = repo.get_commits(path=path)

            history = []
            for idx, commit in enumerate(commits):
                if idx >= max_commits:
                    break

                history.append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat(),
                    "url": commit.html_url
                })

            return history

        except GithubException as e:
            raise Exception(f"Ошибка получения истории: {e}")

    def create_pull_request(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main"
    ) -> Dict:
        """
        Создать Pull Request

        Args:
            title: Заголовок PR
            body: Описание PR
            head_branch: Ветка с изменениями
            base_branch: Базовая ветка (main)

        Returns:
            Информация о созданном PR
        """
        try:
            repo = self.get_repository()
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )

            return {
                "number": pr.number,
                "title": pr.title,
                "url": pr.html_url,
                "state": pr.state,
                "created_at": pr.created_at.isoformat()
            }

        except GithubException as e:
            raise Exception(f"Ошибка создания PR: {e}")

    def create_branch(self, branch_name: str, from_branch: str = "main") -> bool:
        """
        Создать новую ветку

        Args:
            branch_name: Имя новой ветки
            from_branch: От какой ветки создать

        Returns:
            True если успешно
        """
        try:
            repo = self.get_repository()
            source = repo.get_branch(from_branch)
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source.commit.sha
            )
            return True

        except GithubException as e:
            raise Exception(f"Ошибка создания ветки: {e}")

    def commit_file(
        self,
        path: str,
        content: str,
        message: str,
        branch: str = "main"
    ) -> Dict:
        """
        Создать или обновить файл

        Args:
            path: Путь к файлу
            content: Содержимое
            message: Commit message
            branch: Ветка

        Returns:
            Информация о коммите
        """
        try:
            repo = self.get_repository()

            # Проверить, существует ли файл
            try:
                existing = repo.get_contents(path, ref=branch)
                sha = existing.sha
            except GithubException:
                sha = None

            # Создать или обновить
            if sha:
                result = repo.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=sha,
                    branch=branch
                )
            else:
                result = repo.create_file(
                    path=path,
                    message=message,
                    content=content,
                    branch=branch
                )

            return {
                "path": path,
                "sha": result["commit"].sha,
                "url": result["commit"].html_url
            }

        except GithubException as e:
            raise Exception(f"Ошибка commit файла: {e}")

    @staticmethod
    def _detect_language(path: str) -> str:
        """Определить язык программирования по расширению"""
        extensions = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".cpp": "cpp",
            ".c": "c",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".md": "markdown",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".sh": "bash",
            ".html": "html",
            ".css": "css",
            ".sql": "sql",
        }

        for ext, lang in extensions.items():
            if path.endswith(ext):
                return lang

        return "text"
