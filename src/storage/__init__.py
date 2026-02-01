"""
SuiLight Storage Module
"""

from .capsule_storage import CapsuleStorage, get_storage
from . import capsule_storage  # 导出旧版 StorageManager

# 为了向后兼容
StorageManager = capsule_storage.CapsuleStorage

__all__ = ["CapsuleStorage", "get_storage", "StorageManager"]
