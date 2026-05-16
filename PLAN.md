# AI Reliability Judge - 3天黑客马拉松执行计划

## 项目总目标精确定义

**一句话**：训练一个 2B 参数的轻量模型，使其能感知多 LLM 回答之间的语义分歧模式，输出结构化的可靠性风险等级（low / medium / high）。

**不是什么**：
- 不是真理裁判（不判断谁对谁错）
- 不是简单的文本相似度比较器
- 不是通用事实核查工具

**是什么**：
- 一个 **Reliability Risk Layer**（可靠性风险感知层）
- 输入：一个问题 + 多个 LLM 的回答
- 输出：风险等级 + 结构化风险维度评分
- 核心能力：检测 hallucination risk（幻觉风险）、semantic contradiction（语义矛盾）、uncertainty signals（不确定信号）

**技术栈约束**：
- 模型：Gemma 3 1B（QLoRA 微调，4-bit）
- 算力：Kaggle 免费 T4/P100（每周 30h GPU）
- 推理：单卡 T4 可运行
- 数据：从零构建，API 调用生成

---

## Day 1：数据工厂（Data Factory Day）

### 目标
从零构建 1000+ 条高质量结构化训练数据，覆盖 3 个风险等级的均衡分布。

### 按小时拆分

| 时间段 | 任务 | 产出 |
|--------|------|------|
| 0-1h | 设计种子问题分类体系 + 高风险领域选择 | `seeds/taxonomy.json` |
| 1-2h | 编写种子问题生成脚本（5大高风险领域 × 40题 = 200 种子） | `scripts/generate_seeds.py` |
| 2-4h | 编写多模型调用流水线（GPT-4o / Claude 3.5 / Gemini 1.5） | `scripts/call_models.py` |
| 4-6h | 并发调用 API，收集 200 组三模型回答 | `data/raw_responses.jsonl` |
| 6-8h | 编写结构化标注脚本（用 GPT-4o 做 judge） | `scripts/label_judge.py` |
| 8-10h | 运行标注流水线 + 人工抽检 50 条 | `data/labeled_train.jsonl` |
| 10-11h | 数据质量统计 + 分布验证 + 修复不均衡 | `data/stats.json` |
| 11-12h | 编写数据转换为训练格式的脚本 | `scripts/format_for_training.py` |

### 核心设计决策

#### 1. 种子问题的 5 大高风险领域
```
1. 医疗健康（药物交互、症状诊断）
2. 法律法规（管辖权差异、条文解读）
3. 历史事实（有争议的事件、具体数字）
4. 科学前沿（最新研究、未定论的理论）
5. 技术细节（API 版本、配置参数）
```

#### 2. 标签生成逻辑（不是字符串匹配！）

用 GPT-4o 作为 Meta-Judge，对每组回答执行结构化评估：

```json
{
  "question": "...",
  "responses": {"gpt4": "...", "claude": "...", "gemini": "..."},
  "judgment": {
    "hallucination_risk": 0-10,
    "semantic_contradiction": 0-10,
    "uncertainty_signals": 0-10,
    "confidence_calibration": 0-10,
    "final_risk_level": "low|medium|high",
    "reasoning": "..."
  }
}
```

判定规则：
- **Low**：三模型语义一致 + 无不确定表达 + 无事实性冲突
- **Medium**：存在部分细节分歧 / 某模型表达不确定 / 有轻微矛盾但核心一致
- **High**：核心观点冲突 / 至少一个模型可能产生幻觉 / 存在明显事实性矛盾

#### 3. 分布控制目标
- Low : Medium : High = 30% : 40% : 30%
- 如果自然分布偏斜，通过追加特定领域种子来平衡

### Day 1 交付物
- [ ] `seeds/taxonomy.json` - 领域分类 + 200 种子问题
- [ ] `data/raw_responses.jsonl` - 200 组三模型回答
- [ ] `data/labeled_train.jsonl` - 1000+ 条带标签训练数据
- [ ] `data/stats.json` - 数据分布统计
- [ ] `scripts/` 目录下所有流水线脚本

### Day 1 风险点

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| API 限流导致数据不够 | 高 | 致命 | 预备方案：用 Gemini 免费层做 2/3 的调用；准备 prompt 变体复用同一问题 |
| 标签分布极度不均衡 | 中 | 高 | 第一批 50 条后立即检查分布，不均衡则调整种子领域比例 |
| GPT-4o judge 标注质量不稳定 | 中 | 高 | 用 few-shot 示例固定评分标准 + 设置 temperature=0 |
| 数据格式错误导致 Day 2 无法训练 | 低 | 致命 | 最后 1h 强制做端到端验证：加载数据 → tokenize → 检查长度 |

### Day 1 验收标准
1. `labeled_train.jsonl` 行数 ≥ 800
2. 三个风险等级占比均在 20%-50% 区间
3. 随机抽 10 条人工审核，标签合理率 ≥ 80%
4. 数据可被 tokenizer 正常处理，最长样本 < 2048 tokens

---

## Day 2：训练 + 推理（Model Day）

### 目标
在 Kaggle T4 上完成 Gemma 3 1B 的 QLoRA 微调，并验证推理效果。

### 按小时拆分

| 时间段 | 任务 | 产出 |
|--------|------|------|
| 0-1h | 上传数据到 Kaggle Dataset + 环境配置 | Kaggle notebook ready |
| 1-2h | 编写训练脚本（QLoRA config + data loading） | `train/train_qlora.py` |
| 2-3h | 小规模验证（50 条数据，1 epoch）确认流程跑通 | 无 loss 异常 |
| 3-6h | 正式训练（全量数据，3-5 epochs） | `checkpoints/` |
| 6-7h | 编写推理脚本 + 加载 adapter | `inference/predict.py` |
| 7-9h | 在 held-out 测试集上评估（accuracy, F1, confusion matrix） | `eval/results.json` |
| 9-10h | 错误分析：哪些 case 预测错了？为什么？ | `eval/error_analysis.md` |
| 10-11h | 如果效果差：调整 prompt template / 增加 epoch / 调 lr | 改进版 checkpoint |
| 11-12h | 导出最终模型 + 写推理示例 | `model/` + `demo/example.py` |

### 训练配置

```python
# QLoRA Config
qlora_config = {
    "model": "google/gemma-3-1b-it",
    "quantization": "4bit",  # NF4
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"],
    "learning_rate": 2e-4,
    "batch_size": 4,
    "gradient_accumulation": 4,
    "epochs": 3,
    "max_seq_length": 1024,
    "warmup_ratio": 0.03,
}
```

### Prompt Template 设计

```
<start_of_turn>user
You are a Reliability Risk Judge. Analyze the following multi-LLM responses and assess the reliability risk level.

Question: {question}

Response A (GPT-4): {response_a}
Response B (Claude): {response_b}  
Response C (Gemini): {response_c}

Evaluate along these dimensions:
1. Hallucination Risk (0-10)
2. Semantic Contradiction (0-10)
3. Uncertainty Signals (0-10)

Output your assessment in this format:
Risk Level: [low/medium/high]
Hallucination Risk: [score]
Semantic Contradiction: [score]
Uncertainty Signals: [score]
Reasoning: [brief explanation]
<end_of_turn>
<start_of_turn>model
Risk Level: {label}
...
<end_of_turn>
```

### Day 2 交付物
- [ ] `train/train_qlora.py` - 完整训练脚本
- [ ] `train/kaggle_notebook.ipynb` - Kaggle 可运行的 notebook
- [ ] `checkpoints/final/` - 训练好的 adapter weights
- [ ] `inference/predict.py` - 推理脚本
- [ ] `eval/results.json` - 评估指标
- [ ] `eval/error_analysis.md` - 错误分析

### Day 2 风险点

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| Kaggle GPU 配额不够 | 中 | 致命 | 用两个 Kaggle 账号轮换；训练脚本支持 checkpoint resume |
| OOM（显存爆了） | 高 | 高 | 降 batch_size 到 2 + gradient checkpointing；缩 max_seq_length 到 768 |
| 训练 loss 不降 | 中 | 高 | 检查 data format → lr 过大则降到 1e-4 → 检查 label 是否在 vocab 中 |
| 模型只输出一个类别 | 中 | 高 | 增加 class weight / 用 focal loss / 检查数据分布 |
| Gemma 模型加载失败 | 低 | 中 | 预备 Qwen2.5-1.5B 作为 fallback |

### Day 2 验收标准
1. 训练完成无报错，final loss < 初始 loss 的 40%
2. 三分类 accuracy ≥ 55%（随机基线 33%）
3. 每个类别 recall ≥ 40%（不能全预测同一类）
4. 推理脚本可在 T4 上 < 3 秒/条 运行
5. 至少有 5 个 compelling example 可用于 Demo

---

## Day 3：Demo + 叙事 + 提交（Polish Day）

### 目标
打磨 Demo 叙事、撰写 write-up、录制/截图演示、完成提交。

### 按小时拆分

| 时间段 | 任务 | 产出 |
|--------|------|------|
| 0-1h | 筛选 10 个最有说服力的 case（覆盖 low/med/high） | `demo/showcase_cases.json` |
| 1-3h | 搭建极简 Gradio/Streamlit Demo（可本地运行） | `demo/app.py` |
| 3-5h | 撰写 write-up（结构见下方） | `WRITEUP.md` |
| 5-6h | 制作架构图 + 数据流程图 | `assets/architecture.png` |
| 6-7h | 录制 Demo 视频 / 截图序列 | `assets/demo_video.mp4` |
| 7-8h | 完善 README + 复现说明 | `README.md` |
| 8-9h | 代码清理 + 注释 + requirements.txt | 干净的代码库 |
| 9-10h | 最终检查 + 提交 | Done! |

### Day 3 交付物
- [ ] `demo/app.py` - 可运行的 Demo
- [ ] `demo/showcase_cases.json` - 10 个展示案例
- [ ] `WRITEUP.md` - 完整项目文档
- [ ] `README.md` - 项目说明 + 复现指南
- [ ] `assets/` - 架构图 + 演示素材
- [ ] 最终提交物（按比赛要求格式）

### Day 3 风险点

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| Demo 环境装不好 | 中 | 中 | 用 Gradio 最简方案（单文件）；备选：纯 CLI demo |
| 模型效果不够惊艳 | 中 | 高 | 精选 case + 叙事包装："这是 2B 模型做到的" |
| 时间不够写文档 | 高 | 中 | 用下方模板直接填空，不从零写 |
| 视频录制出问题 | 低 | 低 | 用截图序列 + GIF 代替 |

### Day 3 验收标准
1. Demo 可在 30 秒内启动并展示一个完整 case
2. Write-up 完整覆盖所有要求的 section
3. README 包含一键复现命令
4. 代码库无敏感信息（API key 等）

---

## 最终 Demo 叙事

### 开场（30秒）
> "当你问 3 个 AI 同一个问题，它们给出不同答案时——你应该相信谁？答案是：你不需要判断谁对，你需要知道这个答案**有多大风险**。"

### 问题定义（1分钟）
> "我们构建了一个 **Reliability Risk Layer**——一个只有 1B 参数的小模型，它学会了感知大模型之间的分歧模式。它不判断真假，它告诉你：这个问题的回答存在多大的不确定性风险。"

### 技术展示（2分钟）
1. 展示一个 **High Risk** case：三个模型对同一医学问题给出矛盾答案
2. 展示一个 **Low Risk** case：三个模型一致回答的常识问题
3. 展示 Judge 模型的输出：风险等级 + 维度评分 + 推理解释

### 技术亮点（1分钟）
> "这个 1B 模型是用 QLoRA 在免费 GPU 上 3 小时训练出来的。数据是我们通过结构化分歧检测从零构建的。它可以部署在边缘设备上，为任何 AI 系统提供实时的可靠性保障层。"

### 愿景（30秒）
> "未来每个 AI 系统都需要一个 reliability layer。不是更大的模型，而是更聪明的风险感知。这就是我们的方向。"

---

## Write-up 结构

```markdown
# AI Reliability Judge: A Lightweight Risk Perception Layer for LLM Outputs

## 1. Problem Statement (200字)
- LLM hallucination 的现状
- 现有方案的局限（需要 ground truth / 计算开销大）
- 我们的切入点：多模型分歧 → 风险信号

## 2. Approach (400字)
- 核心思想：分歧模式 = 风险信号
- 三个风险维度的定义
- 为什么用小模型（可部署性、实时性、成本）

## 3. Data Pipeline (300字)
- 种子设计策略
- 多模型调用方案
- 结构化标注方法（GPT-4o as Meta-Judge）
- 数据分布控制

## 4. Model Training (300字)
- Gemma 3 1B + QLoRA 配置
- Prompt template 设计
- 训练细节 + 超参数选择

## 5. Results (300字)
- 定量指标（accuracy, F1, per-class metrics）
- 定性分析（case study × 3）
- 错误分析 + 局限性

## 6. Discussion (200字)
- 为什么这种方法可行
- 局限性和改进方向
- 部署场景想象

## 7. Conclusion (100字)
```

---

## 简洁版执行 Checklist

### Day 1 Checklist ✅

```
□ 1.1 定义 5 大高风险领域 + 每领域 8 个子话题
□ 1.2 编写种子问题生成脚本，产出 200 种子问题
□ 1.3 编写多模型 API 调用脚本（GPT/Claude/Gemini）
□ 1.4 调用 API 收集 200 组回答（注意限流和错误处理）
□ 1.5 编写 GPT-4o 结构化标注 prompt + 脚本
□ 1.6 运行标注，产出带标签数据
□ 1.7 检查分布：low/med/high 占比各 20-50%
□ 1.8 随机抽检 10 条，人工确认标签质量
□ 1.9 转换为训练格式（chat template）
□ 1.10 端到端验证：tokenize 不报错 + 长度 < 2048
```

### Day 2 Checklist ✅

```
□ 2.1 上传数据到 Kaggle Dataset
□ 2.2 配置训练环境（transformers, peft, bitsandbytes）
□ 2.3 编写训练脚本 + QLoRA config
□ 2.4 小规模验证（50条，1 epoch，loss 正常下降）
□ 2.5 全量训练（3 epochs，约 2-3 小时）
□ 2.6 编写推理脚本 + 加载 adapter
□ 2.7 测试集评估：accuracy ≥ 55%, 每类 recall ≥ 40%
□ 2.8 精选 5 个 compelling cases
□ 2.9 错误分析：找出典型错误模式
□ 2.10 导出 adapter weights + 推理 demo
```

### Day 3 Checklist ✅

```
□ 3.1 筛选 10 个展示 case
□ 3.2 搭建 Gradio Demo（单文件，< 100 行）
□ 3.3 撰写 write-up（用上方模板）
□ 3.4 画架构图（可用 mermaid / draw.io）
□ 3.5 录制 Demo / 截图
□ 3.6 完善 README（含复现命令）
□ 3.7 清理代码 + requirements.txt
□ 3.8 删除所有 API key / 敏感信息
□ 3.9 最终提交
```

---

## 关键文件结构

```
jinan-drone/
├── README.md                    # 项目说明
├── PLAN.md                      # 本执行计划
├── WRITEUP.md                   # 最终文档
├── requirements.txt             # 依赖
├── seeds/
│   └── taxonomy.json            # 领域分类 + 种子问题
├── scripts/
│   ├── generate_seeds.py        # 种子生成
│   ├── call_models.py           # 多模型调用
│   ├── label_judge.py           # 结构化标注
│   └── format_for_training.py   # 数据格式转换
├── data/
│   ├── raw_responses.jsonl      # 原始回答
│   ├── labeled_train.jsonl      # 标注数据
│   └── stats.json               # 分布统计
├── train/
│   ├── train_qlora.py           # 训练脚本
│   └── kaggle_notebook.ipynb    # Kaggle notebook
├── inference/
│   └── predict.py               # 推理脚本
├── eval/
│   ├── results.json             # 评估结果
│   └── error_analysis.md        # 错误分析
├── demo/
│   ├── app.py                   # Gradio Demo
│   └── showcase_cases.json      # 展示案例
├── assets/
│   └── architecture.png         # 架构图
└── model/
    └── adapter/                 # LoRA adapter weights
```
