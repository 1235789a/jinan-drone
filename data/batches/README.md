# Batches Directory

## 结构

```
data/batches/
├── inputs/                          # 自动生成的输入（30 题/批）
│   ├── batch_01_input.txt
│   ├── batch_02_input.txt
│   └── ...
└── outputs/                         # 你手工保存的三模型回答
    ├── batch_01_deepseek.txt        # 从 Trae DeepSeek-V4-Pro 对话复制
    ├── batch_01_glm.txt             # 从 Trae GLM-5.1 对话复制
    ├── batch_01_qwen.txt            # 从 Trae Qwen3.6-Plus 对话复制
    ├── batch_02_deepseek.txt
    └── ...
```

## 操作流程

### 1. 生成所有输入
```bash
python scripts/prepare_batch.py --all
```

这会在 `inputs/` 下生成 34 个文件，每个包含 30 个问题。

### 2. 循环执行（34 次）

对每个 batch_N:

1. 打开 `inputs/batch_N_input.txt`，全选复制内容
2. 粘贴到 **3 个 Trae 对话**（DeepSeek / GLM / Qwen）
3. 等三个模型都回复完
4. 复制三份回答，分别保存到：
   - `outputs/batch_N_deepseek.txt`
   - `outputs/batch_N_glm.txt`
   - `outputs/batch_N_qwen.txt`

### 3. 解析合并
```bash
python scripts/parse_batch_output.py
```

输出：`data/raw_responses.jsonl`

## 命名规则（必须严格遵守）

- 批次号补零两位：`batch_01`、`batch_34`
- 模型名小写：`deepseek`、`glm`、`qwen`
- 扩展名统一 `.txt`
- 模型回答直接粘贴，不要修改或加标题
