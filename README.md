# ai-coding-skills

收集用于 AI 辅助编程的 Skill 配置，适配 OpenCode/Kiro/Cursor 等 AI 编程工具。

## 目录结构

```
ai-coding-skills/
├── apache-license/                    # Apache 许可证生成
├── generate-eight-part-prompt/        # 八股文档生成提示词组装
├── generate-exam-prep/                # 试卷/备考资料生成
├── github-release-note-generator/     # GitHub Release 公告生成
├── internship-log/                    # 实习日志
├── java-javadoc-auto-generator/       # Java Javadoc 自动生成
├── java-wheel-doc-generator/          # Java 轮子库文档生成
├── oss-release-sop/                   # 开源项目发布 SOP
├── readme-generator/                  # README 自动生成
└── word-to-markdown/                  # Word 转 Markdown
```

## Skill 说明

| Skill | 功能 | 适用场景 |
|-------|------|----------|
| **readme-generator** | 分析代码结构自动生成 README.md | 项目文档初始化 |
| **github-release-note-generator** | 生成中英双语 GitHub Release 公告 | 版本发布 |
| **java-javadoc-auto-generator** | 自动为 Java 代码生成 Javadoc 注释 | 代码文档化 |
| **java-wheel-doc-generator** | 为 Java 工具库生成使用文档 | 库文档编写 |
| **word-to-markdown** | Word 转 Markdown | 文档格式转换 |
| **generate-eight-part-prompt** | 组装八股技术文档生成提示词 | 面试备考 |
| **generate-exam-prep** | 生成试卷/备考资料 | 教育场景 |
| **apache-license** | 生成 Apache 2.0 许可证文件 | 开源项目 |
| **oss-release-sop** | 开源项目发布标准操作流程 | 项目发布 |
| **internship-log** | 逐条提问整理当天实习工作并写入日志 | 实习记录 |

## 使用方式

将对应的 Skill 目录复制到项目的 `.opencode/skills/`、`.kiro/skills/` 或 `.claude/skills/` 目录下，AI 工具会自动识别并加载。

## License

各 Skill 许可证详见各自目录下的 SKILL.md 文件。
