# Word to Markdown 转换工具

将 Word 文档（.docx）转换为 Markdown 格式的命令行工具。

## 目录结构

```
word-to-markdown/
├── README.md       # 本文件
├── SKILL.md        # 详细说明文档
└── convert.py      # 转换驱动脚本
```

## 功能特性

- ✅ 支持 .docx 格式
- ✅ 自动提取图片
- ✅ 识别表格结构
- ✅ 保留文本格式（加粗、斜体等）
- ✅ 支持批量转换
- ✅ 简单易用的命令行界面

## 快速开始

### 安装依赖

```bash
python convert.py --install
```

### 检查依赖

```bash
python convert.py --check
```

### 转换单个文件

```bash
python convert.py document.docx -o output/
```

### 批量转换

```bash
python convert.py word_dir/ -o output/ --batch
```

### 指定图片目录

```bash
python convert.py document.docx -o output/ --images-dir images/
```

## 技术栈

| 组件             | 技术      |
| ---------------- | --------- |
| 文档解析         | mammoth   |
| HTML 转 Markdown | html2text |

## 环境要求

- Python >= 3.10
- 内存 >= 2GB（推荐 4GB）
- 磁盘空间 >= 100MB

## 输出示例

转换后的 Markdown 文件结构：

```markdown
# 文档标题

## 第一章

这里是正文内容，**加粗文本**和*斜体文本*都会保留。

### 1.1 节

- 列表项 1
- 列表项 2

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |

![图片](images/document_image_001.png)
```

## 常见问题

### Q: 支持 .doc 格式吗？

A: 不支持，仅支持 .docx 格式。如需转换 .doc 文件，请先用 Word 另存为 .docx。

### Q: 图片会保存到哪里？

A: 默认保存在输出目录下的 `images/` 文件夹中，可通过 `--images-dir` 参数自定义。

### Q: 转换后格式丢失怎么办？

A: 复杂样式可能无法完全保留，建议转换后手动检查并调整格式。

## 更多信息

详见 [SKILL.md](SKILL.md)
