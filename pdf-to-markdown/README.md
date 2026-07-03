# PDF to Markdown Skill

将 PDF 文件转换为 Markdown 格式的 Claude Code Skill。

## 目录结构

```
.claude/skills/pdf-to-markdown/
├── SKILL.md        # Skill 主文档（Claude 读取）
├── convert.py      # 转换驱动脚本
└── README.md       # 本文件
```

## 功能特性

- ✅ 支持复杂布局 PDF
- ✅ 自动提取图片
- ✅ 识别数学公式（LaTeX 格式）
- ✅ 识别表格结构
- ✅ 支持多语言（中英文）
- ✅ 批量转换支持

## 快速使用

### 作为 Claude Code Skill

在 Claude Code 中，当用户提到"转换 PDF"、"PDF 转 Markdown"等关键词时，会自动加载此 Skill。

### 命令行直接使用

```bash
# 检查依赖
python convert.py --check

# 安装依赖
python convert.py --install

# 转换单个文件
python convert.py document.pdf -o output/

# 批量转换
python convert.py pdf_dir/ -o output/ --batch

# 高精度模式
python convert.py document.pdf -o output/ --dpi 384
```

## 技术栈

| 组件     | 技术                |
| -------- | ------------------- |
| 核心工具 | marker-pdf          |
| 深度学习 | PyTorch             |
| OCR 引擎 | surya-ocr           |
| PDF 解析 | pdftext + pypdfium2 |

## 环境要求

- Python >= 3.10
- 内存 >= 4GB（推荐 8GB）
- 磁盘空间 >= 3GB（模型文件）

## 更多信息

详见 [SKILL.md](SKILL.md)
