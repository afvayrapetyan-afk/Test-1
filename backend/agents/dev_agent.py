"""
DevAgent - агент для автоматической разработки
"""
from .base_agent import BaseAgent
from anthropic import AsyncAnthropic
import json
import os
from typing import Dict, List, Optional


class DevAgent(BaseAgent):
    """
    Агент для автоматической разработки кода

    Умеет:
    - Генерировать новый код по описанию
    - Создавать Pull Request
    - Добавлять фичи к существующему коду
    - Генерировать тесты
    - Рефакторить код
    """

    def __init__(self):
        super().__init__(name="DevAgent")

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY не найден")

        self.claude = AsyncAnthropic(api_key=api_key)

    async def implement_feature(
        self,
        description: str,
        target_files: Optional[List[str]] = None,
        create_pr: bool = True
    ) -> Dict:
        """
        Реализовать новую фичу

        Args:
            description: Описание фичи
            target_files: Файлы для модификации (если известны)
            create_pr: Создать PR автоматически

        Returns:
            Результат с созданными файлами и PR
        """
        self.log(f"Implementing feature: {description}")

        # 1. Найти релевантные файлы (если не указаны)
        if not target_files:
            target_files = await self._find_relevant_files(description)

        # 2. Получить контекст существующего кода
        context = await self._gather_context(target_files)

        # 3. Создать план реализации
        plan = await self._create_implementation_plan(description, context)

        # 4. Генерировать код
        generated_code = await self._generate_code(description, context, plan)

        # 5. Создать ветку и закоммитить
        branch_name = f"feature/{self._slugify(description)}"
        self.create_branch(branch_name)

        committed_files = []
        for file_info in generated_code["files"]:
            commit_result = self.commit_file(
                path=file_info["path"],
                content=file_info["content"],
                message=f"Add {file_info['description']}",
                branch=branch_name
            )
            committed_files.append(commit_result)

        # 6. Создать PR (если нужно)
        pr = None
        if create_pr:
            pr = self.create_pull_request(
                title=f"Feature: {description}",
                body=self._generate_pr_description(description, plan, generated_code),
                head_branch=branch_name,
                base_branch="main"
            )

        self.log(f"Feature implemented! Branch: {branch_name}")

        return {
            "description": description,
            "branch": branch_name,
            "files_modified": len(committed_files),
            "files": committed_files,
            "plan": plan,
            "pr": pr
        }

    async def refactor_code(self, path: str, goals: List[str]) -> Dict:
        """
        Рефакторинг кода

        Args:
            path: Путь к файлу
            goals: Цели рефакторинга (e.g., ["improve performance", "reduce complexity"])

        Returns:
            Рефакторенный код
        """
        self.log(f"Refactoring {path} with goals: {goals}")

        # Получить текущий код
        current_code = self.read_file(path)
        context = self.get_file_context(path)

        # Создать промпт
        prompt = f"""
        Refactor this code to achieve these goals:
        {chr(10).join(f"- {goal}" for goal in goals)}

        Current code:
        ```python
        {current_code}
        ```

        File context:
        - Functions: {len(context.get('functions', []))}
        - Classes: {len(context.get('classes', []))}
        - Lines: {context.get('lines', 0)}

        Requirements:
        1. Maintain existing functionality
        2. Improve code quality
        3. Add docstrings if missing
        4. Follow PEP 8 (for Python) or language best practices
        5. Keep the same public API

        Return the refactored code.
        """

        response = await self.claude.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        refactored_code = response.content[0].text

        return {
            "path": path,
            "original_lines": len(current_code.split('\n')),
            "refactored_lines": len(refactored_code.split('\n')),
            "code": refactored_code,
            "goals_addressed": goals
        }

    async def generate_tests(self, path: str) -> Dict:
        """
        Генерировать тесты для файла

        Args:
            path: Путь к файлу с кодом

        Returns:
            Сгенерированные тесты
        """
        self.log(f"Generating tests for: {path}")

        code = self.read_file(path)
        context = self.get_file_context(path)

        # Определить фреймворк для тестов
        test_framework = self._detect_test_framework(path)

        prompt = f"""
        Generate comprehensive unit tests for this code.

        Code to test:
        ```python
        {code}
        ```

        Functions to test: {[f['name'] for f in context.get('functions', [])]}
        Classes to test: {[c['name'] for c in context.get('classes', [])]}

        Requirements:
        1. Use {test_framework} testing framework
        2. Cover all public functions and methods
        3. Include edge cases and error handling
        4. Add docstrings to tests
        5. Use meaningful test names
        6. Aim for >80% code coverage

        Return the complete test file code.
        """

        response = await self.claude.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=6000,
            messages=[{"role": "user", "content": prompt}]
        )

        test_code = response.content[0].text

        # Определить путь для тестов
        test_path = self._get_test_path(path)

        return {
            "source_file": path,
            "test_file": test_path,
            "test_code": test_code,
            "framework": test_framework,
            "estimated_coverage": "80-90%"
        }

    async def fix_bug(self, path: str, bug_description: str) -> Dict:
        """
        Исправить баг в коде

        Args:
            path: Путь к файлу
            bug_description: Описание бага

        Returns:
            Исправленный код
        """
        self.log(f"Fixing bug in {path}: {bug_description}")

        code = self.read_file(path)

        prompt = f"""
        Fix this bug in the code:

        Bug description: {bug_description}

        Code:
        ```python
        {code}
        ```

        Requirements:
        1. Fix ONLY the bug, don't change unrelated code
        2. Add comments explaining the fix
        3. Ensure the fix doesn't introduce new bugs
        4. Return the complete fixed file

        Return the fixed code with explanation of what was changed.
        """

        response = await self.claude.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.content[0].text

        # Парсить ответ (код + объяснение)
        # Предполагаем что Claude возвращает код в ```python блоке

        return {
            "path": path,
            "bug_description": bug_description,
            "fixed_code": result,
            "explanation": "Fix applied"
        }

    # Helper methods

    async def _find_relevant_files(self, description: str) -> List[str]:
        """Найти релевантные файлы через semantic search"""
        results = self.search_code(description, semantic=True, max_results=5)
        return [r["file"] for r in results]

    async def _gather_context(self, files: List[str]) -> Dict:
        """Собрать контекст из файлов"""
        context = {"files": []}

        for file_path in files[:5]:  # Limit to 5 files
            try:
                content = self.read_file(file_path)
                file_context = self.get_file_context(file_path)

                context["files"].append({
                    "path": file_path,
                    "content": content[:1000],  # First 1000 chars
                    "context": file_context
                })
            except Exception as e:
                self.log(f"Error reading {file_path}: {e}")

        return context

    async def _create_implementation_plan(
        self,
        description: str,
        context: Dict
    ) -> Dict:
        """Создать план реализации"""

        files_info = "\n".join([
            f"- {f['path']}: {len(f['context'].get('functions', []))} functions"
            for f in context.get("files", [])
        ])

        prompt = f"""
        Create an implementation plan for this feature:

        Feature: {description}

        Existing codebase context:
        {files_info}

        Return JSON with:
        {{
            "steps": [
                {{
                    "step": 1,
                    "action": "what to do",
                    "files": ["files to modify or create"]
                }}
            ],
            "new_files": ["list of new files to create"],
            "modified_files": ["list of existing files to modify"],
            "estimated_complexity": "low|medium|high"
        }}
        """

        response = await self.claude.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Парсить JSON из ответа
        plan_text = response.content[0].text

        try:
            # Попытаться извлечь JSON
            plan = json.loads(plan_text)
        except:
            # Если не JSON, вернуть простой план
            plan = {
                "steps": [{"step": 1, "action": plan_text}],
                "estimated_complexity": "medium"
            }

        return plan

    async def _generate_code(
        self,
        description: str,
        context: Dict,
        plan: Dict
    ) -> Dict:
        """Генерировать код по плану"""

        context_str = "\n\n".join([
            f"File: {f['path']}\n```\n{f['content']}\n```"
            for f in context.get("files", [])[:3]
        ])

        prompt = f"""
        Implement this feature:

        Feature: {description}

        Implementation plan:
        {json.dumps(plan, indent=2)}

        Existing code context:
        {context_str}

        Generate the complete code for all new/modified files.

        Return as JSON:
        {{
            "files": [
                {{
                    "path": "path/to/file.py",
                    "content": "complete file content",
                    "description": "what this file does",
                    "is_new": true/false
                }}
            ]
        }}
        """

        response = await self.claude.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.content[0].text

        try:
            result = json.loads(result_text)
        except:
            # Fallback: создать один файл из ответа
            result = {
                "files": [{
                    "path": "generated_code.py",
                    "content": result_text,
                    "description": description,
                    "is_new": True
                }]
            }

        return result

    def _generate_pr_description(
        self,
        description: str,
        plan: Dict,
        generated_code: Dict
    ) -> str:
        """Генерировать описание PR"""

        files_list = "\n".join([
            f"- {f['path']} - {f['description']}"
            for f in generated_code["files"]
        ])

        return f"""
## Feature: {description}

### Implementation
{files_list}

### Changes
- {len(generated_code['files'])} files modified/created

### Plan
Complexity: {plan.get('estimated_complexity', 'medium')}

### Testing
- [ ] Unit tests added
- [ ] Manual testing completed
- [ ] Code review requested

---

🤖 Generated by DevAgent
"""

    @staticmethod
    def _slugify(text: str) -> str:
        """Преобразовать текст в slug для названия ветки"""
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        text = re.sub(r'^-+|-+$', '', text)
        return text[:50]

    @staticmethod
    def _detect_test_framework(path: str) -> str:
        """Определить фреймворк для тестов"""
        if path.endswith('.py'):
            return 'pytest'
        elif path.endswith('.js') or path.endswith('.ts'):
            return 'jest'
        return 'unittest'

    @staticmethod
    def _get_test_path(source_path: str) -> str:
        """Определить путь для тестового файла"""
        import os
        dir_name = os.path.dirname(source_path)
        file_name = os.path.basename(source_path)

        # Для Python: backend/module.py → backend/tests/test_module.py
        if source_path.endswith('.py'):
            test_dir = os.path.join(dir_name, 'tests')
            test_file = f"test_{file_name}"
            return os.path.join(test_dir, test_file)

        return f"tests/{file_name}"
