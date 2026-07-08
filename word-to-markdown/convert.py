#!/usr/bin/env python3
"""
Word to Markdown 转换驱动脚本
使用 mammoth + html2text 将 Word 文档转换为 Markdown 格式
支持 .docx 格式
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

    # 检查 mammoth
    try:
        import mammoth
        print(f"✓ mammoth 已安装")
    except ImportError:
        missing.append("mammoth")

    # 检查 html2text
    try:
        import html2text
        print(f"✓ html2text 已安装")
    except ImportError:
        missing.append("html2text")

    if missing:
        print(f"\n缺少依赖：{', '.join(missing)}")
        print(f"请运行：pip install {' '.join(missing)}")
        return False

    return True


def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "mammoth", "html2text"], check=True)
    print("安装完成！")


def convert_word(word_path, output_dir, images_dir=None):
    """转换单个 Word 文档"""
    import mammoth
    import html2text

    word_path = Path(word_path)
    output_dir = Path(output_dir)

    # 检查输入文件
    if not word_path.exists():
        print(f"错误：文件不存在 - {word_path}")
        return False

    # 检查文件格式
    if word_path.suffix.lower() not in ['.docx']:
        print(f"错误：不支持的格式 - {word_path.suffix}，仅支持 .docx")
        return False

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 设置图片目录
    if images_dir is None:
        images_dir = output_dir / "images"
    images_dir = Path(images_dir)
    images_dir.mkdir(parents=True, exist_ok=True)

    print(f"转换中：{word_path.name}")
    print(f"输出目录：{output_dir}")
    print("-" * 50)

    try:
        # 使用 mammoth 转换为 HTML
        with open(word_path, "rb") as docx_file:
            # 配置图片处理
            def convert_image(image):
                with image.open() as image_bytes:
                    image_data = image_bytes.read()
                    # 生成图片文件名
                    image_name = f"{word_path.stem}_image_{hash(image_data) & 0xFFFFFFFF:08x}.png"
                    image_path = images_dir / image_name
                    # 保存图片
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_data)
                    return {"src": f"images/{image_name}"}

            result = mammoth.convert_to_html(
                docx_file,
                convert_image=mammoth.images.img_element(convert_image)
            )
            html_content = result.value
            messages = result.messages

        # 使用 html2text 转换为 Markdown
        h = html2text.HTML2Text()
        h.body_width = 0  # 不自动换行
        h.unicode_snob = True  # 使用 Unicode
        h.ignore_emphasis = False  # 保留强调
        h.ignore_links = False  # 保留链接
        h.ignore_images = False  # 保留图片
        h.ignore_tables = False  # 保留表格
        h.mark_code = True  # 标记代码

        markdown_content = h.handle(html_content)

        # 生成输出文件名
        output_file = output_dir / f"{word_path.stem}.md"

        # 写入 Markdown 文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {word_path.stem}\n\n")
            f.write(markdown_content)

        print(f"✓ 转换完成：{output_file}")

        # 显示警告信息
        if messages:
            print(f"\n转换警告：")
            for msg in messages:
                print(f"  - {msg}")

        return True

    except Exception as e:
        print(f"✗ 转换失败：{e}")
        return False


def batch_convert(input_dir, output_dir):
    """批量转换目录下的 Word 文档"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # 查找所有 Word 文档
    word_files = list(input_dir.glob("*.docx"))

    if not word_files:
        print(f"未找到 Word 文档：{input_dir}")
        return False

    print(f"找到 {len(word_files)} 个 Word 文档")
    print("=" * 50)

    success = 0
    failed = 0

    for word in word_files:
        if convert_word(word, output_dir):
            success += 1
        else:
            failed += 1
        print()

    print("=" * 50)
    print(f"转换完成：成功 {success}，失败 {failed}")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="Word to Markdown 转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 转换单个文件
  python convert.py document.docx -o output/

  # 批量转换
  python convert.py word_dir/ -o output/ --batch

  # 指定图片目录
  python convert.py document.docx -o output/ --images-dir images/
        """
    )

    parser.add_argument("input", help="输入 Word 文件或目录")
    parser.add_argument("-o", "--output", required=True, help="输出目录")
    parser.add_argument("--images-dir", help="图片输出目录（默认在输出目录下的 images/）")
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
        batch_convert(args.input, args.output)
    else:
        convert_word(args.input, args.output, args.images_dir)


if __name__ == "__main__":
    main()
