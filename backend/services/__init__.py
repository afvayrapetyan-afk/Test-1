"""Services package"""
from .github_service import GitHubService

# CodeIndexer is optional (requires qdrant-client)
try:
    from .code_indexer import CodeIndexer
    __all__ = ["GitHubService", "CodeIndexer"]
except ImportError:
    __all__ = ["GitHubService"]
