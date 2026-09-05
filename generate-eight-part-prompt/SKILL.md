---
name: generate-eight-part-prompt
description: 接收用户提供的八股文档主题与一组技术关键词，组装并输出一份完整可复制的「八股技术文档生成提示词」。产出物是提示词（prompt）本身，不是八股文章。当主题明确而关键词不全时，会自动罗列该主题的高频考点与重要问题供用户勾选确认后再组装。当用户提到"生成八股提示词 / 容器扩容 rehash 等专题的提问模板 / 把某主题变成可交给大模型的任务"时使用。
allowed-tools: ["Read", "Glob", "Grep", "AskUserQuestion"]
version: 1.0.0
keywords: [八股, 面试, 提示词, prompt, 容器扩容, 高并发, 后端]
---

# 八股文档生成提示词组装器

## 一、能力定位（先明确边界）

本 Skill 是一个**提示词组装器**，不是八股文档生成器：

- 输入：八股文档主题 + 技术关键词列表
- 输出：一段**完整、可直接复制粘贴给大模型**的提示词
- 不产出：八股文章本身

用户拿到输出的提示词后，复制给任一能联网、能写长文的大模型，才会得到八股技术文档。

> 反例（禁止）：直接把「容器扩容」讲一遍、或列出答案。本 Skill 只组装任务描述，不答题。

## 二、入参定义

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `document_topic` | string | 否 | 文档主题，如「各类容器扩容/rehash 机制」 |
| `tech_keywords` | array[string] | 否 | 需覆盖的技术关键词，如 `["ThreadLocal扩容", "hashmap扩容", ...]` |
| `forbid_extra_knowledge` | boolean | 否 | 是否严格禁止下游 AI 额外增加用户未指定的知识点 |

调用示例：

```
document_topic: "各类容器扩容/rehash 机制"
tech_keywords: ["ThreadLocal扩容", "hashmap扩容", "concurrenthashmap扩容", "redis的hash扩容", "list扩容"]
forbid_extra_knowledge: true
```

## 三、入参收集与校验（缺参分两级处理：先联想候选，再确认，不脑补）

按顺序检查。**关键词不全 ≠ 直接终止**，而是先进入「候选联想」让用户从清单里挑；只有信息少到无法联想时才要求用户手动补齐。

### 情形 A：连主题都不明确
追问主题，附示例，不空转：
> 请提供八股文档的主题，例如「各类容器扩容/rehash 机制」「IO 多路复用」「MySQL 索引失效场景」。

### 情形 B：主题明确，但关键词缺失 / 过少 / 过泛 → 候选联想供选择

触发条件任选其一：`tech_keywords` 为空；只给了 1~2 个宽泛词（如只写「扩容」，未指明容器/组件）；用户明说「该列哪些我不确定」。

按以下流程执行：

1. **联想候选**：围绕主题生成该主题的高频考点候选清单（宁精勿滥，一般 5~10 条），每条写成「技术点（所属组件 + 版本）」。候选必须贴合主题、是该主题面试真正会问的，禁止塞入与主题无关的充数项。示例——主题「各类容器扩容/rehash 机制」：
   - ThreadLocalMap 扩容
   - HashMap 扩容（JDK1.8）
   - ConcurrentHashMap 扩容（JDK1.8）
   - Hashtable 扩容（JDK1.8）
   - Redis hash（dict）渐进式 rehash
   - Redis list（quicklist / ziplist 连锁更新）
   - ArrayList / String 扩容（顺带一提时注明属同主题家族）
2. **分批勾选**：AskUserQuestion 每次最多 4 个选项，故按批次呈现候选（每批 4 项，`multiSelect: true`），让用户勾选要覆盖的技术点；多轮问完为止。候选外的内容用户可经「Other/自定义」补充。
3. **回退授权**：若用户表示「由你按该主题常见高频考点全权确定」，则采纳候选清单为正式关键词，视为用户已授权（等价于 `forbid_extra_knowledge: false`），并在目标 prompt 的 ② 中写明「讲解对象由助手按主题高频考点确定，清单如下」，让下游可见、可纠正。
4. **勾选汇总**：把所有已勾选 + 用户自定义条目汇总为正式 `tech_keywords`，进入组装。**未勾选的候选绝不悄悄并入。**

> 版本歧义处理：候选里若用户只给了组件名而该组件存在版本差异（HashMap 1.7 vs 1.8、Redis 3.2 前后），优先追问目标版本；用户不置可否时，在 prompt 中显式标注默认版本（如 JDK1.8 / Redis 7.x），并要求下游联网核实版本差异。

### 情形 C：未声明是否允许扩展
追问：
> 是否严格限定只覆盖你给出的技术点，禁止下游 AI 额外补充其他容器/知识点？还是允许适度扩展必要的前置概念？

用 AskUserQuestion 给出选项（「仅限定指定点 / 允许补充必要前置概念 / 由你按高频考点补全」），不要替用户做决定。

## 四、继承项目创作约束（组装前先扫描）

组装提示词前，用 Glob/Read 检查当前会话作用域内是否存在约束文件，路径优先级从高到低：

- `.claude/CLAUDE.md`（或当前工作目录下的 CLAUDE.md / AGENTS.md）
- `.claude/skills/` 下与本主题相关的技能文件
- 用户级 `~/.claude/CLAUDE.md`（全局规范，若与项目级冲突以项目级为准）

命中后：

1. 提取其中与「八股/技术文档创作」相关的约束，重点是：写作风格（文字为主、禁修辞化比喻）、结构要求（概念→原理→机制→FAQ）、Obsidian 双链与 Callout 规范、是否必须联网核实。
2. 把提取结果固化为目标提示词中的**规则段**，强制要求下游 AI 优先遵守（见第五步 ⑥⑦）。

若目录下不存在任何约束文件，则跳过本步，不向目标提示词注入规则段。

## 五、组装目标提示词

把以下 8 个要素按顺序拼成一段连贯的自然语言 prompt（用 markdown 代码块整体包裹）：

### ① 任务开头
固定句式：*「请生成一篇面向 Java 后端面试的技术八股文档，主题为 `<document_topic>`。」*

### ② 限定讲解对象
将 `tech_keywords` 逐条展开，写明对应的容器/组件与版本。示例：
- `hashmap扩容` → HashMap(JDK1.8)
- `concurrenthashmap扩容` → ConcurrentHashMap(JDK1.8)

若 `forbid_extra_knowledge = true`，追加一句：*「限定只讲解上述对象，不得引入题目未指定的其他容器/数据结构。」* 若允许扩展，写明仅可补充与主流程强相关的前置概念（如负载因子定义），不得跑题。

### ③ 文档格式
指定：技术八股文章、结构分层清晰、可用表格辅助对比、无闲聊、知识点严谨、面向面试背诵。若检测到项目约束文件，补一句「格式与风格以 Claude Code 项目中的创作规范为准」。

### ④ 通用覆盖维度
要求对**每个**技术点强制覆盖 6 个维度：
1. 底层结构（存储布局、用什么组织数据）
2. 核心机制（扩容/rehash 整体是怎么工作的）
3. 触发条件（什么情况下扩容、阈值是什么）
4. 关键参数（负载因子、默认容量、每次扩容倍率等）
5. 迁移流程（一次性 / 渐进式 / 多线程协助等）
6. 坑点与面试易错点

### ⑤ 关键词逐条展开
将用户传入的每个 `tech_keywords` 单独成条，写明该条必须讲透的核心细节。这一步是本 Skill 的主要工作量：keyword 太宽时要拆细、补全必须覆盖的子问题（见第六节「展开参考表」）。

### ⑥ 高频问答要求
追加：*「文末整理一组高频面试追问（Q/A），每条给出可直接背诵的严谨回答；追问必须是面试官真的会追着问的细节（如『为什么 ConcurrentHashMap 要用 sizeCtl』『为什么 Redis 渐进式 rehash 期间读写要同时查两张表』），不要泛泛而问。」*

### ⑦ 约束继承规则
若第四步命中了约束文件，追加：*「若本次对话上下文中存在 Claude Code 项目创作规范（CLAUDE.md / AGENTS.md），下游 AI 必须优先遵循其中的创作要求；两者冲突时以项目规范为准。」*

### ⑧ 输出收尾
追加：*「输出要求：纯技术八股文档，无寒暄、无过程叙述，直接给文档内容。」*

### 输出格式
整段 prompt 放入 markdown 代码块，方便一键复制。正文不得输出八股答案、不得附加无关键码。

## 六、关键词展开参考表（示意，按需增补）

以「各类容器扩容/rehash」为例，展示 ⑤ 的展开粒度：

| 用户关键词 | 展开为必须覆盖的核心细节 |
|-----------|------------------------|
| ThreadLocal 扩容 | ThreadLocalMap 底层（开放寻址的 Entry 数组）、触发条件（size ≥ threshold）、扩容为 2 倍、负载因子 2/3、扩容前的过期 Entry 清理（清理脏 Entry 后再判断）、线性探测 + 探测公式（idx 与 step 的选取）、内存泄漏链（弱引用 key + 强引用 value） |
| HashMap 扩容（JDK1.8） | 底层 Node 数组 + 链表/红黑树、扩容触发（size > threshold = capacity × loadFactor）、负载因子默认 0.75、扩容为 2 倍、一次性 rehash、迁移时按 (e.hash & oldCap) 拆成 lo/hi 两条链挂到新桶、为什么桶下标只可能是 i 或 i+oldCap、树化/退化阈值（TREEIFY_THRESHOLD=8 / UNTREEIFY_THRESHOLD=6 / MIN_TREEIFY_CAPACITY=64） |
| ConcurrentHashMap 扩容（JDK1.8） | 结构（Node + CAS + synchronized 锁桶）、sizeCtl 的多重含义（-1 初始化、负数表示扩容中、正数为阈值）、扩容触发（sizeCtl 由 put 后 size 超过阈值触发）、transfer() 协助迁移、ForwardingNode 标记（hash = MOVED）、多线程如何按 stride 领取任务桶迁移、扩容中的读（命中 ForwardingNode 转去新表）与写（协助扩容或锁桶）、helpTransfer 时机 |
| Redis hash 扩容（dict rehash） | 双哈希表结构 ht[0]/ht[1]、扩容/缩容触发（used/buckets 比例 + dict_can_resize 与持久化期间禁止 resize）、新表容量计算（首次 ≥ used×2、每次 power2 增长）、为什么必须渐进式 rehash（避免大字典一次性迁移阻塞单线程事件循环）、rehashidx 游标机制、渐进式期间增删改查的「双表查询 + 新数据只进新表」规则、期间并发修改与游标推进的边界 |
| Redis list（quicklist/压缩列表） | Redis 3.2 后 listpack 与更早 quicklist+ziplist 的差异、ziplist 连续内存与连锁更新（cascade update）问题、为什么用 ziplist 时要限制节点数、list-max-ziplist-size 参数、各版本参数演进需联网核实版本号 |

> 展开规则：关键词是「组件 + 动作」时，补全动作的**触发→参数→流程→坑**全链路；关键词含糊时先回第三步入参校验追问，不要自己猜一个容器替用户做主。

## 七、端到端示例

**输入**

```
document_topic: "各类容器扩容/rehash 机制"
tech_keywords: ["ThreadLocal扩容", "hashmap扩容", "concurrenthashmap扩容", "redis的hash扩容", "list扩容"]
forbid_extra_knowledge: true
```

**输出（示意 prompt，缩略）**

```text
请生成一篇面向 Java 后端面试的技术八股文档，主题为「各类容器扩容/rehash 机制」。
限定讲解对象：ThreadLocalMap、HashMap(JDK1.8)、ConcurrentHashMap(JDK1.8)、Redis hash(dict rehash)、Redis list(quicklist/ziplist→listpack)，不得额外引入其他容器或数据结构。
文档格式：技术八股文章，分层清晰，可用表格辅助对比；风格以当前对话上下文中 Claude Code 项目创作规范为准。
每个技术点必须覆盖：底层结构、核心机制、触发条件、关键参数、数据迁移流程（一次性/渐进式/多线程协助）、坑点与面试易错点。
需要覆盖的内容点：
1. ThreadLocalMap：开放寻址 Entry 数组、2 倍扩容、负载因子 2/3、扩容前清理过期 Entry、弱引用 key + 强引用 value 的内存泄漏链。
2. HashMap(1.8)：负载因子 0.75、2 倍扩容、一次性 rehash、按 hash&oldCap 拆链迁移、桶下标 i 或 i+oldCap、树化/退化阈值。
3. ConcurrentHashMap(1.8)：sizeCtl 多重含义、transfer 协助迁移、ForwardingNode 与 MOVED、扩容期间的读写规则。
4. Redis dict hash：双哈希表 ht[0]/ht[1]、渐进式 rehash 触发条件、rehashidx 游标、为何不能一次性 rehash、期间双表查询与新增数据落新表。
5. Redis list：quicklist/ziplist 结构、连锁更新问题、版本演进（联网核实 3.2 前后差异）。
文末给出高频面试追问及可直接背诵的严谨回答。
若存在项目创作规范，优先遵循；输出纯技术八股文档，无寒暄。
```

**把它给大模型后**才会产出真正的八股文档——本 Skill 到此为止，不越界生成正文。

## 八、自检清单

输出 prompt 前逐项核对：

- [ ] 八股主题明确出现在任务开头
- [ ] 用户每个关键词都展开成了具体覆盖细节，无遗漏
- [ ] 已按用户决定写入「禁止扩展 / 允许有限扩展」约束
- [ ] 6 个通用维度（结构/机制/触发/参数/流程/坑点）已要求覆盖
- [ ] 已追加「高频面试问答」与「遵守项目创作约束」两条指令
- [ ] 全文无任何八股答案正文
- [ ] 整段 prompt 被代码块包裹，可一键复制
- [ ] 若关键词由「候选联想 + 勾选」而来，已确保未把用户未勾选项并入
- [ ] 若过程中出现缺参，已追问或已提供候选清单供选择，而非自行脑补
