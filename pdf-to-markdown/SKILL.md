---
name: pdf-to-markdown
description: Convert PDF files to Markdown format with high accuracy using marker-pdf. Supports complex layouts, tables, formulas, and images extraction.
allowed-tools: ["Bash", "Read", "Write", "Glob", "Grep", "AskUserQuestion"]
version: 1.0.0
keywords: [pdf, markdown, ocr, convert, extract, marker]
---

# PDF to Markdown Converter

将 PDF 文件转换为 Markdown 格式，支持复杂布局、表格、数学公式和图片提取。

**技术栈：** marker-pdf + PyTorch + surya-ocr

**适用场景：**
- 试卷/测验 PDF 转为可编辑的 Markdown
- 学术论文提取
- 技术文档转换
- 包含表格和公式的 PDF

---

## 前置条件

### 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| Python | >= 3.10 | 3.11+ |
| 内存 | 4GB | 8GB+ |
| 磁盘空间 | 3GB（模型文件） | 5GB+ |
| GPU | 无（CPU可用） | NVIDIA GPU + CUDA |

### 依赖检查

运行前必须检查以下依赖是否存在：

```bash
# 检查 Python 版本
python --version

# 检查 marker-pdf 是否安装
pip show marker-pdf

# 检查 PyTorch 是否安装
pip show torch
```

### 依赖安装

如果依赖不存在，询问用户是否安装：

```bash
# 安装 marker-pdf（会自动安装所有依赖）
pip install marker-pdf
```

**自动安装的依赖包括：**
- `torch` - 深度学习框架
- `transformers` - Hugging Face 模型库
- `surya-ocr` - OCR 识别引擎
- `pdftext` - PDF 文本提取
- `pypdfium2` - PDF 渲染
- `opencv-python-headless` - 图像处理
- `scikit-learn` - 机器学习工具
- `Pillow` - 图像处理

**首次运行会自动下载模型文件（约 2GB）到：**
- Windows: `C:\Users\<用户名>\AppData\Local\datalab\datalab\Cache\models\`
- Linux/Mac: `~/.cache/datalab/models/`

---

## 使用方法

### 基础转换

```bash
# 转换单个 PDF
marker_single "<输入PDF路径>" --output_dir "<输出目录>"

# 示例
marker_single "文档.pdf" --output_dir "output/"
```

### 高精度转换（推荐）

对于复杂布局、公式密集的 PDF，使用高 DPI 模式：

```bash
marker_single "<输入PDF路径>" --output_dir "<输出目录>" --highres_image_dpi 384
```

**DPI 参数说明：**
| DPI 值 | 精度 | 速度 | 适用场景 |
|--------|------|------|---------|
| 96 | 低 | 最快 | 简单文本 PDF |
| 192 | 中 | 快 | 普通 PDF（默认） |
| 384 | 高 | 慢 | 复杂布局、公式密集 |

### 批量转换

```bash
# 转换整个目录下的 PDF
marker "<输入目录>" --output_dir "<输出目录>"

# 示例
marker "pdf_files/" --output_dir "markdown_output/"
```

### 指定页码范围

```bash
marker_single "文档.pdf" --output_dir "output/" --page_range "0,5-10,20"
```

---

## 输出结构

```
<输出目录>/
├── <文件名>/
│   ├── <文件名>.md              # 主文档
│   ├── _page_0_Figure_1.jpeg    # 提取的图片
│   ├── _page_0_Picture_2.jpeg
│   └── ...
└── <文件名>_meta.json           # 元数据（可选）
```

---

## 完整工作流程

### 步骤 1：检查环境

```bash
# 检查 Python
python --version || echo "错误：未安装 Python"

# 检查 marker-pdf
pip show marker-pdf > /dev/null 2>&1 || echo "警告：未安装 marker-pdf"
```

如果 marker-pdf 未安装，询问用户：
> "marker-pdf 未安装，是否现在安装？（需要约 2GB 磁盘空间）"

### 步骤 2：确认输入文件

```bash
# 列出待转换的 PDF 文件
ls -la "<输入目录>"/*.pdf
```

### 步骤 3：执行转换

```bash
# 创建输出目录
mkdir -p "<输出目录>"

# 执行转换（高精度模式）
marker_single "<PDF文件>" --output_dir "<输出目录>" --highres_image_dpi 384
```

### 步骤 4：验证输出

```bash
# 检查生成的 Markdown 文件
ls -la "<输出目录>"/

# 检查图片是否提取成功
ls -la "<输出目录>/<文件名>/"*.jpeg
```

### 步骤 5：整理格式

转换完成后，可以进一步整理 Markdown 格式：
- 统一标题层级
- 修复识别错误的公式
- 补充缺失的选项
- 添加分隔线提高可读性

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--highres_image_dpi` | OCR 分辨率 | 192 |
| `--output_format` | 输出格式 (markdown/json/html/chunks) | markdown |
| `--page_range` | 页码范围 | 全部 |
| `--disable_image_extraction` | 不提取图片 | false |
| `--llm_service` | LLM 辅助服务 | 无 |
| `--disable_ocr` | 禁用 OCR | false |
| `--disable_multiprocessing` | 禁用多进程 | false |

---

## 常见问题排查

### 问题 1：首次运行很慢

**原因：** 正在下载模型文件（约 2GB）

**解决：** 等待下载完成，后续运行会使用缓存

### 问题 2：内存不足

**症状：** `RuntimeError: CUDA out of memory` 或进程被杀死

**解决：**
```bash
# 使用 CPU 模式
marker_single "文档.pdf" --output_dir "output/" --disable_multiprocessing
```

### 问题 3：公式识别错误

**原因：** OCR 对复杂数学符号识别有限

**解决：**
1. 使用高 DPI 模式：`--highres_image_dpi 384`
2. 使用 LLM 辅助（需要 API key）：`--use_llm`
3. 手动修正识别结果

### 问题 4：表格识别混乱

**原因：** PDF 中表格格式复杂

**解决：** 高 DPI 模式通常能改善，否则需要手动调整

### 问题 5：中文识别错误

**原因：** 训练数据偏向英文

**解决：** 使用高 DPI 模式可改善

---

## 使用示例

### 示例 1：转换单个试卷

```bash
marker_single "单元测验.pdf" --output_dir "markdown版/" --highres_image_dpi 384
```

### 示例 2：批量转换所有试卷

```bash
for pdf in pdf版/*.pdf; do
  marker_single "$pdf" --output_dir "markdown版/" --highres_image_dpi 384
done
```

### 示例 3：只转换特定页

```bash
marker_single "长文档.pdf" --output_dir "output/" --page_range "0-5"
```

---

## 性能参考

| PDF 页数 | 普通模式 (DPI 192) | 高精度模式 (DPI 384) |
|---------|-------------------|---------------------|
| 1-5 页 | 1-2 分钟 | 3-5 分钟 |
| 5-10 页 | 2-5 分钟 | 5-10 分钟 |
| 10-20 页 | 5-10 分钟 | 10-20 分钟 |

*实际时间取决于 PDF 复杂度和硬件配置*

---

## 与其他工具对比

| 工具 | 精度 | 速度 | 表格 | 公式 | 图片 |
|------|------|------|------|------|------|
| **marker-pdf** | ⭐⭐⭐⭐⭐ | 中 | ✅ | ✅ | ✅ |
| PyMuPDF | ⭐⭐⭐ | 快 | ❌ | ❌ | ❌ |
| pdfplumber | ⭐⭐⭐⭐ | 中 | ✅ | ❌ | ❌ |
| Tesseract OCR | ⭐⭐⭐ | 慢 | ❌ | ❌ | ❌ |

**marker-pdf 是目前开源方案中精度最高的选择。**

---

## 注意事项

1. **首次运行**会下载约 2GB 模型文件，请确保网络畅通
2. **高 DPI 模式**会显著增加处理时间和输出文件大小
3. **复杂公式**仍可能识别错误，建议核对原 PDF
4. **扫描件 PDF** 识别效果取决于图片质量
5. **输出图片**会保存在与 Markdown 同级的目录中
