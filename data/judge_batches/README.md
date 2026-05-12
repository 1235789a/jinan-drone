# Judge Batches Directory

## 结构

```
data/judge_batches/
├── inputs/                                # 自动生成的 Judge 输入
│   ├── judge_batch_001_input.txt         # 10 组数据
│   ├── judge_batch_001_ids.json          # 该批次对应的 record ID 列表
│   └── ...
└── outputs/                               # 你手工保存的 Judge 输出
    ├── judge_batch_001_output.txt        # 10 行 JSON
    └── ...
```

## 操作流程

### 1. 生成所有 Judge 输入
```bash
python scripts/prepare_judge_batch.py --all
```

前提：`data/raw_responses.jsonl` 已经由 `parse_batch_output.py` 生成。

### 2. 循环执行（约 100 次）

对每个 judge_batch_N:

1. 打开 `inputs/judge_batch_N_input.txt`，复制内容
2. 粘贴到 **Kimi-K2.6** 对话（已提前发过系统提示词）
3. 模型输出 10 行 JSON
4. 复制 JSON 输出保存到 `outputs/judge_batch_N_output.txt`

### 3. 每 20 批重启对话

防止上下文污染标准：
- 跑完第 20 批后，新开 Kimi 对话
- 重发 `prompts/03_meta_judge.md` 的系统提示词
- 等 "JUDGE READY" 后继续

### 4. 合并生成最终数据
```bash
python scripts/merge_and_validate.py
```

输出：`data/labeled_train.jsonl` + `data/stats.json`

## 质量检查

每 10 批跑一次分布检查：
```bash
python -c "
import json, re
from pathlib import Path
from collections import Counter

levels = []
for f in sorted(Path('data/judge_batches/outputs').glob('*_output.txt')):
    text = f.read_text()
    for line in text.splitlines():
        m = re.search(r'\"final_risk_level\":\s*\"(\w+)\"', line)
        if m:
            levels.append(m.group(1))

print(Counter(levels))
total = len(levels)
if total:
    for lv in ['low', 'medium', 'high']:
        cnt = levels.count(lv)
        print(f'{lv:8s}: {cnt:4d} ({cnt/total*100:.1f}%)')
"
```

目标：每个等级 25-45%。
