"""
Punto de entrada de la plataforma web.
Uso: python -m web.main   o   python web/main.py
"""

import argparse
import asyncio
import os
import sys

import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Smart Robot Monitor — Plataforma Web")
    parser.add_argument("--host", default="0.0.0.0", help="Host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Puerto (default: 8080)")
    parser.add_argument("--reload", action="store_true", help="Auto-reload en desarrollo")
    args = parser.parse_args()

    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║   Smart Robot Monitor — Plataforma Web              ║")
    print(f"  ║   http://{args.host}:{args.port}                              ║")
    print("  ║   Ctrl+C para salir                                 ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()

    uvicorn.run(
        "web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
