# 🛡️ AI Reliability Judge

**Gemma 4 Good Hackathon — Safety & Trust Track**

Fine-tuned Gemma 4 E2B to judge multi-LLM response reliability risk levels.

## What It Does

Given a question and two LLM responses, the AI Reliability Judge outputs:
- **Risk Level:** low / medium / high
- **Hallucination Risk:** 1-10
- **Semantic Contradiction:** 1-10
- **Uncertainty Signals:** 1-10
- **Reasoning:** Detailed explanation

## Project Structure

```
├── notebooks/
│   ├── train_gemma4_reliability_judge.ipynb  # Fine-tuning notebook (Kaggle)
│   └── demo_reliability_judge.ipynb          # Live demo notebook
├── data/
│   ├── train_chat.jsonl                      # 784 training samples
│   └── val_chat.jsonl                        # 138 validation samples
├── scripts/
│   └── upload_data_to_kaggle.py              # Data upload helper
├── submission/
│   ├── writeup.md                            # Kaggle writeup (≤1500 words)
│   ├── video_script.md                       # YouTube video script (≤3 min)
│   └── cover_image.md                        # Cover image design brief
└── README.md
```

## Technical Details

| Component | Detail |
|-----------|--------|
| Model | Gemma 4 E2B-IT (2B params) |
| Method | Full-parameter SFT via trl.SFTTrainer |
| Hardware | Kaggle T4 GPU (16GB) |
| Precision | bfloat16 + gradient checkpointing |
| Data | 922 samples (784 train / 138 val) |
| Domains | Medical, Legal, Financial, Scientific, Technical |

## Quick Start

1. **Training:** Open `notebooks/train_gemma4_reliability_judge.ipynb` in Kaggle with GPU enabled
2. **Demo:** Open `notebooks/demo_reliability_judge.ipynb` to see the judge in action
3. **Data:** Training data is in `data/` directory

## Submission Checklist

- [x] Training data prepared (922 samples)
- [ ] Training notebook runs successfully on Kaggle T4
- [ ] Demo notebook shows real-world cases
- [ ] Writeup posted on Kaggle (≤1500 words)
- [ ] YouTube video uploaded (≤3 minutes)
- [ ] Cover image created
- [ ] Code made public on Kaggle

## License

MIT
