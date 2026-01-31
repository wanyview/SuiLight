
# ============ 讨论系统 ============

from src.discussions import router as discussions_router

app.include_router(discussions_router, prefix="/api")



# ============ 启动 ============

if __name__ == "__main__":
    import uvicorn
