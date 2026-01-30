# SuiLight Knowledge Salon - Makefile

.PHONY: help install test run clean check run-tests

help:
	@echo "SuiLight Knowledge Salon - 命令帮助"
	@echo ""
	@echo "安装相关:"
	@echo "  make install      - 安装依赖"
	@echo "  make install-dev  - 安装开发依赖"
	@echo ""
	@echo "运行相关:"
	@echo "  make run          - 启动服务 (默认端口 8000)"
	@echo "  make run-port P=9000  - 指定端口启动"
	@echo "  make run-ui       - 仅启动 UI (不启动 API)"
	@echo "  make run-reload   - 热重载模式启动"
	@echo ""
	@echo "任务队列:"
	@echo "  make worker       - 启动 Celery Worker"
	@echo ""
	@echo "测试相关:"
	@echo "  make test         - 运行测试"
	@echo "  make test-watch   - 监听模式运行测试"
	@echo ""
	@echo "代码质量:"
	@echo "  make lint         - 代码检查"
	@echo "  make format       - 代码格式化"
	@echo "  make check        - 全面检查"
	@echo ""
	@echo "运维相关:"
	@echo "  make clean        - 清理缓存"
	@echo "  make docker       - 构建 Docker 镜像"
	@echo ""

# 安装依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
install-dev:
	pip install -r requirements.txt
	pip install black isort mypy pytest pytest-asyncio

# 运行服务
run:
	python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

run-port:
	python -m uvicorn src.main:app --host 0.0.0.0 --port $(P)

run-ui:
	@echo "UI 已内置在主服务中，直接访问 http://localhost:8000"

run-reload:
	python -m uvicorn src.main:app --reload

# 任务队列 Worker
worker:
	celery -A src.tasks worker --loglevel=info

# 测试
test:
	pytest tests/ -v

test-watch:
	ptw tests/ -- -v

# 代码质量
lint:
	black --check src/ tests/
	isort --check-only src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

check: lint test

# 清理
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache dist build *.egg-info 2>/dev/null || true

# Docker
docker:
	docker build -t suilight .
	docker run -p 8000:8000 suilight
