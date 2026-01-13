"""
Base Agent - базовый класс для всех AI агентов с доступом к коду
"""
from typing import Dict, List, Optional
from services.github_service import GitHubService
from services.code_indexer import CodeIndexer
import ast


class BaseAgent:
    """Базовый класс для всех агентов"""

    def __init__(self, name: str = "BaseAgent"):
        """
        Инициализация агента

        Args:
            name: Имя агента
        """
        self.name = name
        self.github = GitHubService()
        self.indexer = CodeIndexer()

    def read_file(self, path: str, branch: str = "main") -> str:
        """
        Прочитать файл из репозитория

        Args:
            path: Путь к файлу
            branch: Ветка

        Returns:
            Содержимое файла
        """
        try:
            file_data = self.github.get_file_content(path, branch)
            return file_data["content"]
        except Exception as e:
            raise Exception(f"Ошибка чтения файла {path}: {e}")

    def search_code(self, query: str, semantic: bool = False, max_results: int = 10) -> List[Dict]:
        """
        Поиск по коду

        Args:
            query: Поисковый запрос
            semantic: Использовать семантический поиск (AI)
            max_results: Максимум результатов

        Returns:
            Список найденных фрагментов
        """
        if semantic:
            # Семантический поиск через embeddings
            return self.indexer.semantic_search(query, top_k=max_results)
        else:
            # Текстовый поиск через GitHub API
            return self.github.search_code(query, max_results)

    def get_file_context(self, path: str) -> Dict:
        """
        Получить контекст файла (imports, functions, classes)

        Args:
            path: Путь к файлу

        Returns:
            Словарь с контекстом
        """
        content = self.read_file(path)

        # Парсинг для Python
        if path.endswith('.py'):
            return self._parse_python_file(content)

        # Для других языков - возвращаем базовую информацию
        return {
            "language": "unknown",
            "lines": len(content.split('\n')),
            "size": len(content)
        }

    def _parse_python_file(self, content: str) -> Dict:
        """
        Парсинг Python файла

        Args:
            content: Содержимое файла

        Returns:
            Контекст (imports, functions, classes)
        """
        try:
            tree = ast.parse(content)

            context = {
                "language": "python",
                "imports": [],
                "functions": [],
                "classes": [],
                "lines": len(content.split('\n'))
            }

            for node in ast.walk(tree):
                # Imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        context["imports"].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        context["imports"].append(f"{module}.{alias.name}")

                # Functions
                elif isinstance(node, ast.FunctionDef):
                    context["functions"].append({
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node) or ""
                    })

                # Classes
                elif isinstance(node, ast.ClassDef):
                    context["classes"].append({
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or ""
                    })

            return context

        except SyntaxError as e:
            return {
                "language": "python",
                "error": f"Syntax error: {e}",
                "lines": len(content.split('\n'))
            }

    def create_branch(self, branch_name: str, from_branch: str = "main") -> bool:
        """
        Создать новую ветку

        Args:
            branch_name: Имя ветки
            from_branch: От какой ветки создать

        Returns:
            True если успешно
        """
        return self.github.create_branch(branch_name, from_branch)

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
        return self.github.commit_file(path, content, message, branch)

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
            title: Заголовок
            body: Описание
            head_branch: Ветка с изменениями
            base_branch: Базовая ветка

        Returns:
            Информация о PR
        """
        return self.github.create_pull_request(title, body, head_branch, base_branch)

    def log(self, message: str):
        """Логирование"""
        print(f"[{self.name}] {message}")
