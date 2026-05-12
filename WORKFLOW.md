# 数据生产工作流 (Day 1 手工批量模式)

> 用 Trae 内置免费模型批量生产 1000+ 条训练数据

---

## 🎯 总览

| 步骤 | 工具 | 耗时 | 产出 |
|------|------|------|------|
| 1. 生成种子问题 | Trae + DeepSeek-V4-Pro | 5-10 min | 1000 条种子 |
| 2. 三模型收集回答 | Trae + GLM/DS/Qwen | 1.5-2 h | 1000 × 3 回答 |
| 3. Meta-Judge 标注 | Trae + Kimi-K2.6 | 1 h | 1000 条风险标签 |
| 4. 解析 + 验证 | 本地脚本 | 5 min | 标准训练数据 |

---

## 📋 Step 1: 生成种子问题

### 操作步骤

1. Trae 里新开对话，选 **DeepSeek-V4-Pro**
2. 复制粘贴 `prompts/01_seed_generation.md` 的完整内容
3. 等模型输出 JSONL（大约 1000 行）
4. 全选复制，保存为 `data/seeds.jsonl`

### 验收标准
- 行数 ≥ 950（允许 5% 丢失）
- 5 个领域每个 ≥ 150 条
- 每行是合法 JSON（可用 `python -c "import json; [json.loads(l) for l in open('data/seeds.jsonl')]"` 验证）

### 翻车预防
- 如果中途被截断：让它 "continue from question N+1, same format"
- 如果输出质量下降：分 2 次生成，每次 500 条

---

## 📋 Step 2: 三模型并行收集回答

### 操作步骤

1. **打开 3 个 Trae 对话**：
   - 对话 A：DeepSeek-V4-Pro
   - 对话 B：GLM-5.1
   - 对话 C：Qwen3.6-Plus

2. **每个对话先发系统提示词**（复制 `prompts/02_response_system.md`），等模型回 "READY"

3. **批量发问题**（每批 30 条，共 34 批）：
   - 从 `seeds.jsonl` 里挑 30 行
   - 按 `prompts/02_batch_template.md` 格式化成一条用户消息
   - **同时粘到 3 个对话里**（Ctrl+V × 3）
   - 等 3 个对话都回复完
   - 把三组答案按 JSONL 格式保存到 `data/responses_batch_XX.jsonl`

4. **每 5 批做一次 quick check**：
   - 有没有某个模型开始偷懒（答案变短 / 重复）
   - 如果发现，新开对话重发系统提示词

### 验收标准
- 每批 30 个回答都齐全（允许 1-2 个缺失）
- 回答长度 80-200 字（过长过短都是质量信号）
- 没有出现 "I need more context" 等拒答

### 翻车预防
- **模型敷衍**：新开对话 + 重发系统提示词
- **中文/英文错位**：系统提示词强调 "reply in same language as question"
- **编号乱了**：要求模型用 `A1:` `A2:` 开头，解析脚本自动对齐

---

## 📋 Step 3: Meta-Judge 标注

### 操作步骤

1. Trae 里新开对话，选 **Kimi-K2.6**
2. 粘贴 `prompts/03_judge_system.md`，等回 "JUDGE READY"
3. 按 `prompts/03_judge_batch.md` 格式，每次粘 10 组数据进去
4. 模型输出 10 行 JSON，每行一个判断
5. 追加到 `data/labels.jsonl`
6. 重复直到 1000 条全部判完（100 次）

### 验收标准
- `labels.jsonl` 行数 = 数据总行数
- `final_risk_level` 三个等级占比都在 20%-50%
- 每个 JSON 字段齐全，无 null

### 翻车预防
- **标签极端不均衡**（如 80% medium）：检查 Judge prompt 是否清晰，考虑加 few-shot 示例
- **Judge 评分混乱**：每 20 批重启对话，防止上下文污染
- **JSON 格式错误**：解析脚本会自动跳过，但要监控丢失率

---

## 📋 Step 4: 本地解析 + 验证

```bash
# 1. 把 responses_batch_*.jsonl 合并
python scripts/parse_batch_output.py

# 2. 合并 responses + labels
python scripts/merge_and_validate.py

# 3. 格式化为训练数据
python scripts/format_for_training.py
```

### 最终产出
- `data/labeled_train.jsonl` - 全量标注数据
- `data/train_chat.jsonl` - 训练集（Gemma chat format）
- `data/val_chat.jsonl` - 验证集
- `data/stats.json` - 分布统计

---

## ⚠️ 时间分配建议

```
08:00 - 08:15  Step 1 (种子生成)
08:15 - 10:30  Step 2 (三模型回答，并行)
10:30 - 11:30  Step 3 (Meta-Judge)
11:30 - 11:45  Step 4 (解析)
11:45 - 12:00  Buffer (修 bug / 补数据)
```

Day 1 剩下的时间可以开始熟悉 Day 2 的训练脚本。
