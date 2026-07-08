# Word to Markdown Converter

将 Word 文档（.docx）转换为 Markdown 格式，支持复杂布局、表格、图片提取。

**技术栈：** mammoth + html2text

**适用场景：**

- 试卷/测验等 Word 文档转为可编辑的 Markdown
- 学术论文提取
- 技术文档转换
- 包含表格和图片的 Word 文档

---

## 前置条件

### 系统要求

| 项目     | 最低要求 | 推荐配置 |
| -------- | -------- | -------- |
| Python   | >= 3.10  | 3.11+    |
| 内存     | 2GB      | 4GB+     |
| 磁盘空间 | 100MB    | 500MB+   |

### 依赖检查

运行前必须检查以下依赖是否存在：

```bash
# 检查 Python 版本
python --version

# 检查 mammoth 是否安装
pip show mammoth

# 检查 html2text 是否安装
pip show html2text
```

### 依赖安装

如果依赖不存在，询问用户是否安装：

```bash
# 安装依赖
pip install mammoth html2text
```

**自动安装的依赖包括：**

- `mammoth` - Word 文档解析库
- `html2text` - HTML 转 Markdown 工具

---

## 使用方法

### 基础转换

```bash
# 转换单个 Word 文档
python convert.py "<输入Word路径>" -o "<输出目录>"

# 示例
python convert.py "文档.docx" -o "output/"
```

### 批量转换

```bash
# 转换整个目录下的 Word 文档
python convert.py "<输入目录>" -o "<输出目录>" --batch

# 示例
python convert.py "word_files/" -o "markdown_output/" --batch
```

### 指定图片目录

```bash
python convert.py "文档.docx" -o "output/" --images-dir "images/"
```

---

## 输出结构

```
<输出目录>/
├── <文件名>.md              # 主文档
└── images/                  # 图片目录（如果文档包含图片）
    ├── <文件名>_image_001.png
    ├── <文件名>_image_002.png
    └── ...
```

---

## 完整工作流程

### 步骤 1：检查环境

```bash
# 检查 Python
python --version || echo "错误：未安装 Python"

# 检查依赖
python convert.py --check
```

如果依赖未安装，询问用户：

> "mammoth 或 html2text 未安装，是否现在安装？"

### 步骤 2：确认输入文件

```bash
# 列出待转换的 Word 文档
ls -la "<输入目录>"/*.docx
```

### 步骤 3：执行转换

```bash
# 创建输出目录
mkdir -p "<输出目录>"

# 执行转换
python convert.py "<Word文件>" -o "<输出目录>"
```

### 步骤 4：验证输出

```bash
# 检查生成的 Markdown 文件
ls -la "<输出目录>"/

# 检查图片是否提取成功
ls -la "<输出目录>/images/"
```

### 步骤 5：整理格式

转换完成后，可以进一步整理 Markdown 格式：

- 统一标题层级
- 修复表格格式
- 补充缺失的格式
- 添加分隔线提高可读性

---

## 参数说明

| 参数             | 说明         | 默认值               |
| ---------------- | ------------ | -------------------- |
| `-o, --output` | 输出目录     | 必填                 |
| `--images-dir` | 图片输出目录 | 输出目录下的 images/ |
| `--batch`      | 批量转换模式 | false                |
| `--install`    | 安装依赖     | -                    |
| `--check`      | 检查依赖     | -                    |

---

## 常见问题排查

### 问题 1：转换后格式丢失

**原因：** Word 文档使用了复杂的样式

**解决：** 目前工具会尽量保留格式，但某些复杂样式可能需要手动调整

### 问题 2：图片未提取

**原因：** Word 文档中的图片格式不支持

**解决：** 检查 Word 文档中的图片是否为嵌入式图片

### 问题 3：表格格式混乱

**原因：** Word 中表格格式复杂

**解决：** 可能需要手动调整表格格式

### 问题 4：中文乱码

**原因：** 编码问题

**解决：** 确保输入文件是标准的 .docx 格式

---

## 使用示例

### 示例 1：转换单个试卷

```bash
python convert.py "单元测验.docx" -o "markdown版/"
```

### 示例 2：批量转换所有试卷

```bash
python convert.py "word版/" -o "markdown版/" --batch
```

### 示例 3：指定图片目录

```bash
python convert.py "文档.docx" -o "output/" --images-dir "assets/"
```

---

## 性能参考

| Word 文档大小 | 转换时间 |
| ------------- | -------- |
| < 1MB         | 1-5 秒   |
| 1-5MB         | 5-15 秒  |
| 5-10MB        | 15-30 秒 |
| > 10MB        | 30+ 秒   |

*实际时间取决于文档复杂度和图片数量*

---

## 与其他工具对比

| 工具              | 精度       | 速度 | 表格 | 图片 | 格式保留   |
| ----------------- | ---------- | ---- | ---- | ---- | ---------- |
| **mammoth** | ⭐⭐⭐⭐   | 快   | ✅   | ✅   | ⭐⭐⭐⭐   |
| python-docx       | ⭐⭐⭐     | 快   | ✅   | ❌   | ⭐⭐⭐     |
| pandoc            | ⭐⭐⭐⭐⭐ | 中   | ✅   | ✅   | ⭐⭐⭐⭐⭐ |
| LibreOffice       | ⭐⭐⭐⭐   | 慢   | ✅   | ✅   | ⭐⭐⭐⭐   |

**mammoth 是轻量级且易于使用的选择，适合大多数场景。**

---

## 注意事项

1. **仅支持 .docx 格式**，不支持旧版 .doc 格式
2. **复杂样式**可能无法完全保留
3. **图片**会自动提取并保存到指定目录
4. **表格**会尽量转换为 Markdown 表格格式
5. **输出文件**使用 UTF-8 编码
