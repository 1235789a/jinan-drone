# MVP 快速验证 (10 分钟跑通全流程)

> 先用 60 条跑通整个 Day 1 流水线，验证 API 和脚本都正常，再跑 1000 条。

---

## 1. 装依赖

```bash
pip install -r requirements.txt
```

## 2. 配置 API key

```bash
cp .env.example .env
# 编辑 .env，至少填 DEEPSEEK_API_KEY
# 推荐方案: 注册 SiliconFlow 一个 key 解决所有问题
```

### 拿 key 的最快路径

| provider | 页面 | 拿 key 耗时 |
|----------|------|-------------|
| **SiliconFlow** (推荐) | https://siliconflow.cn | 3 min，注册送 14 元 |
| DeepSeek | https://platform.deepseek.com | 你已经有 |
| 智谱 AI (GLM) | https://open.bigmodel.cn | 5 min，送 2000 万 tokens |
| DashScope (Qwen) | https://dashscope.aliyun.com | 5 min，免费额度 |
| Moonshot (Kimi) | https://platform.moonshot.cn | 5 min，送 15 元 |

**最省事**：只注册 SiliconFlow，填 `SILICONFLOW_API_KEY` 即可，其他留空会自动 fallback 到 SiliconFlow。

## 3. 检查配置

```bash
python scripts/providers.py
```

期望输出像这样（显示你配置好的 4 个 provider）：

```
Configured providers (4):
  deepseek   -> model=deepseek-chat, key=sk-abc...xyz1, url=https://api.deepseek.com/v1
  glm        -> model=glm-4.5, key=sk-abc...xyz2, url=...
  qwen       -> model=qwen-plus, key=sk-abc...xyz3, url=...
  kimi       -> model=moonshot-v1-32k, key=sk-abc...xyz4, url=...
```

## 4. 跑 MVP（60 条，约 5-10 分钟）

```bash
bash scripts/run_mvp.sh
```

这会依次执行：
1. `generate_seeds.py --mvp` — 生成 60 条种子问题（每个 domain 12 条）
2. `call_models.py --mvp` — 三模型并发调用，收集回答
3. `label_judge.py --mvp` — Kimi 做 Meta-Judge 标注
4. `format_for_training.py` — 转 Gemma 训练格式

## 5. 验收

跑完检查 `data/stats.json`：

```json
{
  "total_samples": 55,
  "level_pct": { "low": 27.3, "medium": 45.5, "high": 27.3 },
  "balanced": true
}
```

**验收标准**：
- `total_samples` >= 50（允许约 15% API 失败）
- 3 个 level 都有样本，每个占比 15%-55%
- `balanced == true`

---

## MVP 通过 → 跑全量 1000 条

```bash
python scripts/generate_seeds.py            # 生成 1000 条种子
python scripts/call_models.py               # 调模型 (约 15-30 分钟)
python scripts/label_judge.py               # Meta-Judge (约 10-20 分钟)
python scripts/format_for_training.py       # 格式化
```

全量大约 **30-60 分钟**就能跑完，你去喝杯咖啡回来就行。

---

## 出问题了怎么办

| 报错 | 原因 | 解决 |
|------|------|------|
| `No providers configured` | .env 没填或找不到 | 检查 `.env` 路径，运行 `python scripts/providers.py` 确认 |
| `401 Unauthorized` | API key 错误 | 检查 key 有没有复制对 |
| `model not found` | 模型名在你的 provider 下不叫这个 | 去对应平台的文档查正确 model 名，更新 .env |
| 大量 `Timeout` | 并发过高或网络慢 | .env 里降低 `MAX_CONCURRENT=3` |
| 某个 provider 全部失败 | 额度用完 / 节流 | 暂时跳过，或换 SiliconFlow |
| `level_pct` 严重不均衡 | Meta-Judge 偏见 | 检查 judge prompt，考虑换 provider |

---

## 断点续传

所有脚本都支持**中断后重启**，已处理的 id 不会重复调用：

```bash
# 如果 call_models 跑到一半挂了
python scripts/call_models.py   # 直接重跑，从断点继续

# 如果想全部重新跑
python scripts/call_models.py --no-resume
```
