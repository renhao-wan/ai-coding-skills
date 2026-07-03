#!/usr/bin/env python3
"""
PDF to Markdown 转换驱动脚本
使用 marker-pdf 将 PDF 转换为 Markdown 格式
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def check_dependencies():
    """检查依赖是否安装"""
    missing = []

    # 检查 Python 版本
    if sys.version_info < (3, 10):
        print(f"错误：Python 版本过低 ({sys.version})，需要 >= 3.10")
        return False

    # 检查 marker-pdf
    try:
        import marker_pdf
        print(f"✓ marker-pdf 已安装")
    except ImportError:
        missing.append("marker-pdf")

    # 检查 torch
    try:
        import torch
        print(f"✓ PyTorch 已安装 ({torch.__version__})")
        if torch.cuda.is_available():
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
        else:
            print(f"  使用 CPU 模式")
    except ImportError:
        missing.append("torch")

    if missing:
        print(f"\n缺少依赖：{', '.join(missing)}")
        print(f"请运行：pip install {' '.join(missing)}")
        return False

    return True


def install_dependencies():
    """安装依赖"""
    print("正在安装 marker-pdf...")
    subprocess.run([sys.executable, "-m", "pip", "install", "marker-pdf"], check=True)
    print("安装完成！")


def convert_pdf(pdf_path, output_dir, dpi=384, page_range=None):
    """转换单个 PDF"""
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    # 检查输入文件
    if not pdf_path.exists():
        print(f"错误：文件不存在 - {pdf_path}")
        return False

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 构建命令
    cmd = [
        "marker_single",
        str(pdf_path),
        "--output_dir", str(output_dir),
        "--highres_image_dpi", str(dpi)
    ]

    if page_range:
        cmd.extend(["--page_range", page_range])

    print(f"转换中：{pdf_path.name}")
    print(f"输出目录：{output_dir}")
    print(f"DPI：{dpi}")
    print("-" * 50)

    # 执行转换
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print("-" * 50)
        print(f"✓ 转换完成！")
        return True
    else:
        print(f"✗ 转换失败")
        return False


def batch_convert(input_dir, output_dir, dpi=384):
    """批量转换目录下的 PDF"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # 查找所有 PDF
    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"未找到 PDF 文件：{input_dir}")
        return False

    print(f"找到 {len(pdf_files)} 个 PDF 文件")
    print("=" * 50)

    success = 0
    failed = 0

    for pdf in pdf_files:
        if convert_pdf(pdf, output_dir, dpi):
            success += 1
        else:
            failed += 1
        print()

    print("=" * 50)
    print(f"转换完成：成功 {success}，失败 {failed}")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="PDF to Markdown 转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 转换单个文件（高精度）
  python convert.py document.pdf -o output/

  # 批量转换
  python convert.py pdf_dir/ -o output/ --batch

  # 指定 DPI
  python convert.py document.pdf -o output/ --dpi 192

  # 只转换特定页
  python convert.py document.pdf -o output/ --pages "0-5"
        """
    )

    parser.add_argument("input", help="输入 PDF 文件或目录")
    parser.add_argument("-o", "--output", required=True, help="输出目录")
    parser.add_argument("--dpi", type=int, default=384, help="OCR 分辨率 (默认: 384)")
    parser.add_argument("--pages", help="页码范围，如 '0,5-10,20'")
    parser.add_argument("--batch", action="store_true", help="批量转换目录")
    parser.add_argument("--install", action="store_true", help="安装依赖")
    parser.add_argument("--check", action="store_true", help="检查依赖")

    args = parser.parse_args()

    # 安装依赖
    if args.install:
        install_dependencies()
        return

    # 检查依赖
    if args.check:
        check_dependencies()
        return

    # 检查依赖是否存在
    if not check_dependencies():
        print("\n是否现在安装依赖？(y/n): ", end="")
        if input().lower() == 'y':
            install_dependencies()
        else:
            sys.exit(1)

    # 执行转换
    if args.batch:
        batch_convert(args.input, args.output, args.dpi)
    else:
        convert_pdf(args.input, args.output, args.dpi, args.pages)


if __name__ == "__main__":
    main()
