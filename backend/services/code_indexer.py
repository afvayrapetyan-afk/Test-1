"""
Code Indexer - индексация кода в vector store для семантического поиска
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import ast
import hashlib
import os


class CodeIndexer:
    """Индексирует код в Qdrant для семантического поиска"""

    def __init__(self):
        """Инициализация"""
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client = QdrantClient(url=qdrant_url)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection_name = "code_snippets"

        # Создать коллекцию если не существует
        self._ensure_collection()

    def _ensure_collection(self):
        """Создать коллекцию если не существует"""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)

            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=384,  # all-MiniLM-L6-v2 dimension
                        distance=Distance.COSINE
                    )
                )
        except Exception as e:
            print(f"Warning: Could not create collection: {e}")

    def index_file(self, file_path: str, content: str, language: str = "python"):
        """
        Индексировать файл

        Args:
            file_path: Путь к файлу
            content: Содержимое
            language: Язык программирования
        """
        # Разбить на функции/классы (для Python)
        if language == "python":
            snippets = self._extract_python_snippets(content, file_path)
        else:
            # Для других языков - индексируем весь файл
            snippets = [{
                "id": self._generate_id(file_path),
                "file": file_path,
                "type": "file",
                "name": file_path,
                "code": content,
                "docstring": ""
            }]

        # Создать embeddings и сохранить
        points = []
        for snippet in snippets:
            # Создать текст для embedding (код + docstring)
            text_to_embed = f"{snippet['name']}\n{snippet['docstring']}\n{snippet['code']}"
            embedding = self.encoder.encode(text_to_embed).tolist()

            point = PointStruct(
                id=snippet["id"],
                vector=embedding,
                payload={
                    "file": snippet["file"],
                    "type": snippet["type"],
                    "name": snippet["name"],
                    "code": snippet["code"][:1000],  # Ограничить размер
                    "docstring": snippet["docstring"]
                }
            )
            points.append(point)

        # Сохранить в Qdrant
        if points:
            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
            except Exception as e:
                print(f"Error indexing file {file_path}: {e}")

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Семантический поиск по коду

        Args:
            query: Поисковый запрос (на естественном языке)
            top_k: Количество результатов

        Returns:
            Список найденных фрагментов кода
        """
        try:
            # Создать embedding для запроса
            query_embedding = self.encoder.encode(query).tolist()

            # Поиск в Qdrant
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            # Форматировать результаты
            found = []
            for result in results:
                found.append({
                    "file": result.payload["file"],
                    "type": result.payload["type"],
                    "name": result.payload["name"],
                    "code": result.payload["code"],
                    "docstring": result.payload.get("docstring", ""),
                    "score": result.score
                })

            return found

        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []

    def _extract_python_snippets(self, code: str, file_path: str) -> List[Dict]:
        """
        Извлечь функции и классы из Python кода

        Args:
            code: Python код
            file_path: Путь к файлу

        Returns:
            Список snippets (функции, классы)
        """
        snippets = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                # Функции
                if isinstance(node, ast.FunctionDef):
                    snippets.append({
                        "id": self._generate_id(f"{file_path}:{node.name}"),
                        "file": file_path,
                        "type": "function",
                        "name": node.name,
                        "code": ast.unparse(node),
                        "docstring": ast.get_docstring(node) or ""
                    })

                # Классы
                elif isinstance(node, ast.ClassDef):
                    snippets.append({
                        "id": self._generate_id(f"{file_path}:{node.name}"),
                        "file": file_path,
                        "type": "class",
                        "name": node.name,
                        "code": ast.unparse(node)[:500],  # Ограничить размер
                        "docstring": ast.get_docstring(node) or ""
                    })

        except SyntaxError:
            # Если не удалось распарсить, индексируем весь файл
            snippets.append({
                "id": self._generate_id(file_path),
                "file": file_path,
                "type": "file",
                "name": file_path,
                "code": code[:1000],
                "docstring": ""
            })

        return snippets

    @staticmethod
    def _generate_id(text: str) -> str:
        """Генерировать уникальный ID из текста"""
        return hashlib.md5(text.encode()).hexdigest()

    def delete_file(self, file_path: str):
        """
        Удалить файл из индекса

        Args:
            file_path: Путь к файлу
        """
        try:
            # TODO: Implement deletion by file path filter
            pass
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    def get_stats(self) -> Dict:
        """Получить статистику индекса"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "total_points": collection_info.points_count,
                "collection": self.collection_name,
                "vector_size": 384
            }
        except Exception as e:
            return {"error": str(e)}
