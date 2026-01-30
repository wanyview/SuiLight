#!/usr/bin/env python3
"""
SuiLight Knowledge Salon - 启动入口

Usage:
    python -m suilight              # 启动服务 (默认端口 8000)
    python -m suilight --port 9000  # 指定端口
    python -m suilight --reload     # 热重载模式
    python -m suilight --help       # 查看帮助
"""

import argparse
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(
        description="SuiLight Knowledge Salon - 多智能体知识协作平台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m suilight              # 启动服务
  python -m suilight --port 9000  # 端口 9000
  python -m suilight --reload     # 热重载模式
  python -m suilight --api-only   # 仅启动 API (无 UI)
        """
    )
    
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="服务端口 (默认: 8000)"
    )
    
    parser.add_argument(
        "--host", "-H",
        type=str,
        default="0.0.0.0",
        help="绑定地址 (默认: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--reload", "-r",
        action="store_true",
        help="启用热重载 (开发模式)"
    )
    
    parser.add_argument(
        "--api-only",
        action="store_true",
        help="仅启动 API 服务 (不显示 UI)"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    # 启动服务
    from src.main import app
    import uvicorn
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🧠 SuiLight Knowledge Salon                            ║
║   多智能体知识协作平台                                     ║
║                                                           ║
║   Web UI: http://localhost:{port}                         ║
║   API Docs: http://localhost:{port}/docs                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """.format(port=args.port))
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
