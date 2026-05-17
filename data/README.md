# Training Data — AI Reliability Judge

## Files
- `train_chat.jsonl` — 784 annotated samples for training
- `val_chat.jsonl` — 138 annotated samples for validation

## Format
Each line is a JSON object with a `messages` array in chat format:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "You are an AI Reliability Judge...\n\nQuestion: ...\n\nResponse A (Model1): ...\n\nResponse B (Model2): ...\n\nAssess the reliability risk level..."
    },
    {
      "role": "assistant",
      "content": "Risk Level: high\nHallucination Risk: 8\nSemantic Contradiction: 9\nUncertainty Signals: 7\nReasoning: ..."
    }
  ]
}
```

## Data Upload Instructions

Upload your `train_chat.jsonl` and `val_chat.jsonl` from AutoDL to this directory:

```bash
# From AutoDL machine:
scp /root/jinan-drone/data/train_chat.jsonl /root/jinan-drone/data/val_chat.jsonl .

# Then push to GitHub:
git add data/
git commit -m "Add training data"
git push origin feat/hackathon-plan
```

Or upload directly to Kaggle as a Dataset.
