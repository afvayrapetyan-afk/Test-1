"""
CodeAnalystAgent - агент для анализа кода
"""
from .base_agent import BaseAgent
from openai import AsyncOpenAI
import json
import os
from typing import Dict, List


class CodeAnalystAgent(BaseAgent):
    """
    Агент для анализа качества кода

    Умеет:
    - Анализировать код на баги
    - Оценивать качество (0-100)
    - Находить security уязвимости
    - Предлагать улучшения
    - Проверять best practices
    """

    def __init__(self):
        super().__init__(name="CodeAnalystAgent")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY не найден")

        self.llm = AsyncOpenAI(api_key=api_key)

    async def analyze_file(self, path: str, branch: str = "main") -> Dict:
        """
        Полный анализ файла

        Args:
            path: Путь к файлу
            branch: Ветка

        Returns:
            Детальный анализ с оценками и рекомендациями
        """
        self.log(f"Analyzing file: {path}")

        # 1. Получить код и контекст
        code = self.read_file(path, branch)
        context = self.get_file_context(path)

        # 2. Создать промпт для анализа
        prompt = self._create_analysis_prompt(path, code, context)

        # 3. Запросить LLM
        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert code reviewer with deep knowledge of software engineering best practices, security, and performance optimization."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        # 4. Парсить результат
        analysis = json.loads(response.choices[0].message.content)

        self.log(f"Analysis complete. Quality score: {analysis.get('quality_score', 0)}")

        return {
            "file": path,
            "branch": branch,
            "analysis": analysis,
            "lines_of_code": len(code.split('\n')),
            "language": context.get("language", "unknown")
        }

    async def analyze_pull_request(self, pr_number: int) -> Dict:
        """
        Анализ Pull Request

        Args:
            pr_number: Номер PR

        Returns:
            Анализ всех изменённых файлов
        """
        self.log(f"Analyzing PR #{pr_number}")

        # TODO: Implement PR analysis
        # 1. Get PR files from GitHub
        # 2. Analyze each changed file
        # 3. Generate review comments

        return {
            "pr": pr_number,
            "status": "not_implemented",
            "message": "PR analysis will be implemented in next iteration"
        }

    async def find_bugs(self, path: str) -> List[Dict]:
        """
        Поиск потенциальных багов в коде

        Args:
            path: Путь к файлу

        Returns:
            Список найденных багов
        """
        self.log(f"Searching for bugs in: {path}")

        code = self.read_file(path)

        prompt = f"""
        Analyze this code for potential bugs and issues.

        File: {path}

        Code:
        ```
        {code}
        ```

        Return JSON with:
        {{
            "bugs": [
                {{
                    "line": <line_number>,
                    "severity": "critical|high|medium|low",
                    "type": "bug_type",
                    "description": "what's wrong",
                    "fix": "how to fix it"
                }}
            ]
        }}
        """

        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        result = json.loads(response.choices[0].message.content)
        bugs = result.get("bugs", [])

        self.log(f"Found {len(bugs)} potential bugs")

        return bugs

    async def suggest_improvements(self, path: str) -> List[Dict]:
        """
        Предложить улучшения кода

        Args:
            path: Путь к файлу

        Returns:
            Список рекомендаций
        """
        self.log(f"Generating improvement suggestions for: {path}")

        code = self.read_file(path)
        context = self.get_file_context(path)

        prompt = f"""
        Review this code and suggest improvements for:
        - Performance
        - Readability
        - Maintainability
        - Best practices

        File: {path}
        Language: {context.get('language', 'unknown')}

        Code:
        ```
        {code[:2000]}  # Limit to first 2000 chars
        ```

        Return JSON with:
        {{
            "improvements": [
                {{
                    "category": "performance|readability|security|architecture",
                    "priority": "high|medium|low",
                    "description": "what to improve",
                    "example": "code example (optional)"
                }}
            ]
        }}
        """

        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.5
        )

        result = json.loads(response.choices[0].message.content)
        improvements = result.get("improvements", [])

        self.log(f"Generated {len(improvements)} improvement suggestions")

        return improvements

    async def check_security(self, path: str) -> Dict:
        """
        Проверка на security уязвимости

        Args:
            path: Путь к файлу

        Returns:
            Отчёт о безопасности
        """
        self.log(f"Security check for: {path}")

        code = self.read_file(path)

        prompt = f"""
        Perform a security audit of this code. Look for:
        - SQL injection
        - XSS vulnerabilities
        - Command injection
        - Insecure dependencies
        - Authentication issues
        - Data leaks
        - OWASP Top 10 issues

        File: {path}

        Code:
        ```
        {code}
        ```

        Return JSON with:
        {{
            "security_score": <0-100>,
            "vulnerabilities": [
                {{
                    "type": "vulnerability_type",
                    "severity": "critical|high|medium|low",
                    "line": <line_number>,
                    "description": "description",
                    "recommendation": "how to fix"
                }}
            ],
            "safe_practices": ["list of good practices found"],
            "recommendations": ["security recommendations"]
        }}
        """

        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        result = json.loads(response.choices[0].message.content)

        self.log(f"Security score: {result.get('security_score', 0)}")

        return result

    def _create_analysis_prompt(self, path: str, code: str, context: Dict) -> str:
        """Создать промпт для полного анализа"""

        return f"""
        Perform a comprehensive code review of this file.

        File: {path}
        Language: {context.get('language', 'unknown')}
        Lines: {context.get('lines', 0)}
        Functions: {len(context.get('functions', []))}
        Classes: {len(context.get('classes', []))}

        Code:
        ```
        {code[:3000]}  # First 3000 characters
        ```

        Analyze and return JSON with:
        {{
            "quality_score": <0-100>,
            "readability_score": <0-100>,
            "maintainability_score": <0-100>,
            "performance_score": <0-100>,

            "strengths": ["what's good about this code"],

            "issues": [
                {{
                    "type": "bug|smell|security|performance",
                    "severity": "critical|high|medium|low",
                    "description": "what's wrong",
                    "line": <line_number or null>,
                    "recommendation": "how to fix"
                }}
            ],

            "complexity": {{
                "cyclomatic": <estimated>,
                "cognitive": "low|medium|high"
            }},

            "best_practices": {{
                "followed": ["practices that are followed"],
                "missing": ["practices that should be added"]
            }},

            "refactoring_suggestions": [
                {{
                    "area": "what to refactor",
                    "reason": "why",
                    "impact": "high|medium|low"
                }}
            ],

            "summary": "2-3 sentence summary of the analysis"
        }}

        Be constructive and specific. Focus on actionable feedback.
        """
