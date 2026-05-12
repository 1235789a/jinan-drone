# Day 1 执行 Checklist（打勾版）

> 打印出来或开一个实时窗口跟着做

---

## 🟢 准备阶段（10 分钟）

- [ ] Trae 客户端打开，确认可以用 DeepSeek-V4-Pro / GLM-5.1 / Qwen3.6-Plus / Kimi-K2.6
- [ ] 仓库 clone 到本地，能跑 `python --version`（3.10+）
- [ ] 阅读完 `WORKFLOW.md`（5 分钟）

---

## 🟡 Step 1: 种子问题生成（10-15 分钟）

- [ ] Trae 新开对话，选 DeepSeek-V4-Pro
- [ ] 复制 `prompts/01_seed_generation.md` 的完整 prompt，粘贴
- [ ] 等待生成完成（可能需要 continue 几次）
- [ ] 所有 JSONL 拼接保存为 `data/seeds.jsonl`
- [ ] 验证：`wc -l data/seeds.jsonl` 结果 ≈ 1000
- [ ] 验证：JSON 合法性检查（见 WORKFLOW.md）
- [ ] 验证：5 个 domain 每个约 200 条

---

## 🟡 Step 2: 三模型回答收集（1.5-2 小时）

### 准备

- [ ] 跑 `python scripts/prepare_batch.py --all`，确认生成 34 个 input 文件
- [ ] 打开 3 个 Trae 窗口：DeepSeek-V4-Pro / GLM-5.1 / Qwen3.6-Plus
- [ ] 三个窗口都粘贴 `prompts/02_response_collection.md` 的系统提示词
- [ ] 三个窗口都回复 "READY"

### 批次循环（34 次）

**每跑一批勾一次**，建议三路并行：

- [ ] Batch 01  [ ] Batch 02  [ ] Batch 03  [ ] Batch 04  [ ] Batch 05
- [ ] Batch 06  [ ] Batch 07  [ ] Batch 08  [ ] Batch 09  [ ] Batch 10
- [ ] Batch 11  [ ] Batch 12  [ ] Batch 13  [ ] Batch 14  [ ] Batch 15
- [ ] Batch 16  [ ] Batch 17  [ ] Batch 18  [ ] Batch 19  [ ] Batch 20
- [ ] Batch 21  [ ] Batch 22  [ ] Batch 23  [ ] Batch 24  [ ] Batch 25
- [ ] Batch 26  [ ] Batch 27  [ ] Batch 28  [ ] Batch 29  [ ] Batch 30
- [ ] Batch 31  [ ] Batch 32  [ ] Batch 33  [ ] Batch 34

**每批操作**：
1. 打开 `data/batches/inputs/batch_NN_input.txt`
2. 全选复制 → 粘到 3 个 Trae 对话
3. 等全部回复完
4. 复制回答 → 保存 `data/batches/outputs/batch_NN_{deepseek|glm|qwen}.txt`

**每 5 批自检**：
- [ ] 回答长度正常（80-160 字）
- [ ] 没有大量 [UNANSWERABLE]
- [ ] 编号完整无缺失
- [ ] 发现问题时新开对话

### 解析

- [ ] 跑 `python scripts/parse_batch_output.py`
- [ ] 验证：`wc -l data/raw_responses.jsonl` ≈ 900-1000（允许 10% 丢失）

---

## 🟡 Step 3: Meta-Judge 标注（1 小时）

### 准备

- [ ] 跑 `python scripts/prepare_judge_batch.py --all`，确认生成 ~100 个 judge 输入
- [ ] Trae 新开对话，选 **Kimi-K2.6**
- [ ] 粘贴 `prompts/03_meta_judge.md` 的系统提示词
- [ ] 等回复 "JUDGE READY"

### 批次循环（~100 次）

**每 10 批打一组勾**：

- [ ] Judge 001-010  [ ] Judge 011-020
- [ ] Judge 021-030  [ ] Judge 031-040
- [ ] Judge 041-050  [ ] Judge 051-060
- [ ] Judge 061-070  [ ] Judge 071-080
- [ ] Judge 081-090  [ ] Judge 091-100

**每批操作**：
1. 打开 `data/judge_batches/inputs/judge_batch_NNN_input.txt`
2. 复制 → 粘到 Kimi 对话
3. 复制 JSON 输出 → 保存到 `data/judge_batches/outputs/judge_batch_NNN_output.txt`

**每 20 批强制重启 Kimi 对话**：
- [ ] 重启 1 (第 20 批后)  [ ] 重启 2 (第 40 批后)
- [ ] 重启 3 (第 60 批后)  [ ] 重启 4 (第 80 批后)

### 合并

- [ ] 跑 `python scripts/merge_and_validate.py`
- [ ] 验证 `data/stats.json`：
    - [ ] total_samples ≥ 800
    - [ ] balanced == true（每类 20-50%）
    - [ ] 5 个 domain 都有样本

---

## 🟢 Step 4: 转换训练数据（5 分钟）

- [ ] 跑 `python scripts/format_for_training.py`
- [ ] 验证：`data/train_chat.jsonl` 行数合理（~85% 总量）
- [ ] 验证：`data/val_chat.jsonl` 行数合理（~15% 总量）
- [ ] 用 tokenizer 试一条，确认 < 2048 tokens

---

## 🎯 Day 1 完成标准

全部满足才进 Day 2：

- [ ] `data/labeled_train.jsonl` ≥ 800 行
- [ ] `data/train_chat.jsonl` + `data/val_chat.jsonl` 生成成功
- [ ] `data/stats.json` 显示 balanced=true
- [ ] 5 个 domain 每个至少 100 条
- [ ] 3 个 risk level 每个至少 20%
- [ ] 随机抽检 20 条，标签合理率 ≥ 85%

---

## 🚨 紧急情况应对

| 情况 | 处理 |
|------|------|
| Trae 某模型额度用完 | 换同家族模型（DS-Flash 代替 DS-Pro 等） |
| 某一批回答大面积缺失 | 重跑该批次 |
| Meta-Judge 输出格式坏了 | 解析脚本会跳过，缺多了重新判 |
| 时间不够 1000 条 | 保底 500 条也能训，调 Day 2 策略 |
| 数据严重偏斜 | 针对性补种子题目重跑 |
