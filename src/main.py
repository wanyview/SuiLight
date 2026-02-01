
"""
SuiLight Knowledge Salon - 主应用入口
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

# ============ FastAPI 应用 ============
app = FastAPI(title="SuiLight Knowledge Salon")

# ============ 讨论系统 ============
from src.discussions import router as discussions_router

app.include_router(discussions_router, prefix="/api")


# ============ 胶囊存储初始化 ============
from src.storage.capsule_storage import CapsuleStorage
import os

# 创建全局存储实例
CAPSULE_STORAGE = None


def init_storage():
    """初始化胶囊存储"""
    global CAPSULE_STORAGE
    if CAPSULE_STORAGE is None:
        db_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "capsules.db"
        )
        CAPSULE_STORAGE = CapsuleStorage(db_path)
        print(f"✅ 胶囊存储初始化完成: {db_path}")
    return CAPSULE_STORAGE


# 应用启动时初始化存储
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_storage()
    yield
    # 应用关闭时清理


# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
    
    # 初始化存储
    init_storage()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
