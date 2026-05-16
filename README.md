# 🛡️ AI Reliability Judge

> **A Lightweight Risk Perception Layer for LLM Outputs**

让小模型（Gemma 3 1B）学习多个大模型之间的分歧模式，输出结构化的可靠性风险等级。不判断谁对谁错，只告诉你：这个回答有多大风险。

---

## 核心理念

当你问 3 个 AI 同一个问题，它们给出不同答案时——你不需要判断谁对，你需要知道**风险有多大**。

| 维度 | 检测目标 |
|------|----------|
| 🧠 Hallucination Risk | 回答是否可能是编造的 |
| ⚔️ Semantic Contradiction | 模型间是否存在核心观点冲突 |
| ❓ Uncertainty Signals | 置信度是否校准合理 |

**输出**：`low` / `medium` / `high` 风险等级 + 三维评分 + 推理解释

---

## 项目结构

```
├── PLAN.md                      # 3天详细执行计划
├── seeds/taxonomy.json          # 领域分类 + 种子问题
├── scripts/
│   ├── generate_seeds.py        # 种子生成
│   ├── call_models.py           # 多模型调用
│   ├── label_judge.py           # 结构化标注（GPT-4o Meta-Judge）
│   └── format_for_training.py   # 数据格式转换
├── train/train_qlora.py         # QLoRA 训练脚本
├── inference/predict.py         # 推理引擎
├── demo/app.py                  # Gradio Demo
├── eval/                        # 评估结果
└── model/adapter/               # LoRA weights
```

---

## 技术栈

- **模型**：Gemma 3 1B + QLoRA（4-bit NF4）
- **训练**：Kaggle T4/P100，约 3 小时
- **数据**：结构化分歧检测，GPT-4o 作为 Meta-Judge 标注
- **推理**：单卡 T4，< 3 秒/条
- **Demo**：Gradio 单文件应用

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置 API Keys（数据生成阶段需要）
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"

# 3. Day 1: 数据生成
python scripts/generate_seeds.py
python scripts/call_models.py
python scripts/label_judge.py
python scripts/format_for_training.py

# 4. Day 2: 训练（在 Kaggle 上运行）
python train/train_qlora.py

# 5. Day 3: 运行 Demo
python demo/app.py
```

---

## 执行计划

详见 [PLAN.md](./PLAN.md) — 包含：
- 3 天按小时拆分的完整任务表
- 每天的交付物和验收标准
- 风险点和应对方案
- Demo 叙事脚本
- Write-up 结构模板

---

## 设计哲学

1. **不是真理裁判** — 不判断对错，只感知风险
2. **结构化语义判断** — 标签由多维语义分析产生，不是字符串匹配
3. **高风险领域优先** — 医疗、法律、历史、科学前沿、技术细节
4. **极致轻量** — 1B 模型可部署到边缘设备
5. **可复现** — 数据流水线完全脚本化

---

## License

MIT
