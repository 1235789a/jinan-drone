# Step 2: 三模型回答收集 Prompt

> 三个 Trae 对话并行使用
> 对话 A: DeepSeek-V4-Pro
> 对话 B: GLM-5.1
> 对话 C: Qwen3.6-Plus

---

## 2.1 系统提示词（每个对话开头粘这一份）

```
You are now acting as a DETERMINISTIC ANSWER API. I will send batches of 30 questions. You must answer each one strictly.

## Answer Rules
1. Answer from your internal parameter knowledge. DO NOT add "I need to search" or "please consult an expert".
2. Each answer must be 80-160 words. No shorter, no longer.
3. Plain text only. No markdown, no bullets, no headers, no bold.
4. Do NOT add disclaimers like "consult a doctor/lawyer". Answer the actual question.
5. Maintain your natural reasoning style - if you are confident, be confident. If uncertain, express it. Do not artificially hedge or over-commit.
6. Reply in the SAME LANGUAGE as each question (English question → English answer, 中文问题 → 中文回答).
7. Do NOT show reasoning steps. Just the answer.

## Input Format
I will send:
```
Q1: <question text>
Q2: <question text>
...
Q30: <question text>
```

## Output Format (STRICT)
You reply with exactly 30 answers, each on ONE line (use \n for internal line breaks if absolutely needed, but prefer one line):

A1: <answer for Q1>
A2: <answer for Q2>
...
A30: <answer for Q30>

Nothing else. No preamble. No closing remarks. No meta-commentary.

If a question is unanswerable, reply: `A<N>: [UNANSWERABLE]`

When ready, reply exactly: `READY`
```

---

## 2.2 批次输入模板

每次粘贴到三个对话的格式：

```
Q1: What is the maximum daily acetaminophen dose for an adult with child-pugh class B cirrhosis?
Q2: Can a California employer require a positive marijuana test as grounds for termination under AB 2188 if the employee works in federally regulated construction?
Q3: How many Bengali civilians died in the 1943 famine, and what did the Woodhead Commission conclude about its causes?
...（共 30 条）...
Q30: ...
```

**操作方法**：
1. 打开 `data/seeds.jsonl`
2. 用脚本 `scripts/prepare_batch.py N` 生成第 N 批的 30 个问题模板
3. 三个对话同时粘贴
4. 三份回答分别存到 `data/batches/batch_N_deepseek.txt`、`..._glm.txt`、`..._qwen.txt`

---

## 2.3 质量检查点

每跑完 5 批，检查：

| 问题 | 信号 | 应对 |
|------|------|------|
| 回答开始变短 | 平均 < 80 字 | 新开对话，重发系统提示词 |
| 大量 [UNANSWERABLE] | > 10% | 检查种子质量，去掉太刁钻的问题 |
| 编号乱了 | A5 缺失 | 解析脚本会标记，补跑该条 |
| 中英文错位 | 中文问英文答 | 提醒模型"reply in same language" |
| 疑似复制粘贴 | 多条答案高度相似 | 新开对话 |

---

## 2.4 并行操作技巧

```
流程优化版（30 条/批 × 3 模型并行）:

00:00  打开 3 个 Trae 窗口，分别选模型 A/B/C
00:02  三个窗口都粘系统提示词，等 READY
00:03  准备第 1 批 30 题（用 prepare_batch.py）
00:04  Ctrl+V × 3 → 三个窗口同时发
00:05  等待... (三个模型并行生成)
00:08  最先完成的开始复制答案
00:09  第二个完成
00:10  第三个完成 → 保存三个 txt
00:11  准备第 2 批...
```

**关键**：复制答案时保持窗口顺序 A→B→C，文件命名也按这个顺序，方便后面对齐。

---

## 2.5 批次状态追踪表

在 `data/batches/progress.md` 里维护：

```markdown
| Batch | DeepSeek | GLM | Qwen | Notes |
|-------|----------|-----|------|-------|
| 1     | ✅       | ✅  | ✅   | -     |
| 2     | ✅       | ✅  | ⚠️   | Q17 缺失，已补 |
| 3     | ✅       | ✅  | ✅   | -     |
| ...   |          |     |      |       |
| 34    |          |     |      |       |
```
