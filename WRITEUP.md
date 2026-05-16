# AI Reliability Judge: A Lightweight Risk Perception Layer for LLM Outputs

## Track: Safety & Trust

### Subtitle
Teaching Gemma 4 2B to detect hallucination risk and semantic contradictions across multi-LLM outputs — a deployable safety layer for any AI system.

---

## The Problem

When multiple AI models answer the same question differently, users face a critical trust dilemma: which answer should they believe? Current solutions require either expensive ground-truth verification or human expert review — neither scales.

The gap is especially dangerous in high-stakes domains (medical advice, legal guidance, scientific claims) where a confidently-wrong AI answer can cause real harm. We need an automated, lightweight "reliability thermometer" that flags risky outputs before they reach users.

## Our Solution: AI Reliability Judge

We built a **Reliability Risk Layer** powered by Gemma 4 2B that:

1. **Ingests** responses from multiple LLMs to the same question
2. **Detects** three risk dimensions: hallucination risk, semantic contradiction, and uncertainty signals
3. **Outputs** a structured risk assessment (low / medium / high) with dimensional scores and reasoning

This is NOT a truth-arbiter — it's a **risk sensor**. It tells you "how much should you trust this answer?" rather than "who is right?"

## How We Used Gemma 4

**Model**: `google/gemma-4-2b-it` with QLoRA (4-bit NF4 quantization)

**Why Gemma 4 2B?**
- Small enough for edge deployment (phones, embedded devices, offline clinics)
- Native instruction-following capability enables structured output
- QLoRA reduces trainable parameters to ~0.5% while preserving performance
- Runs inference in <3 seconds on a single T4 GPU

**Training Configuration**:
- LoRA rank: 16, alpha: 32, targeting q/k/v/o projections
- 3 epochs, batch size 4 with gradient accumulation 4
- Learning rate: 2e-4 with cosine decay
- Total training time: ~2-3 hours on Kaggle T4

## Data Pipeline (Built from Scratch)

We generated 1000+ labeled training samples through a structured pipeline:

1. **Seed Generation**: 1000 high-risk questions across 5 domains (medical, legal, science, tech, history) designed to trigger model disagreement
2. **Multi-Model Collection**: Each question answered by DeepSeek-V3 and Qwen2.5-7B — models from different training paradigms to maximize disagreement signal
3. **Structured Labeling**: Claude Sonnet 4.6 as independent Meta-Judge, producing 3-dimensional risk scores + final risk level using calibrated rubrics (not string similarity)

**Key Design Choice**: The Judge (Claude) is completely independent from the data sources (DeepSeek/Qwen), eliminating self-preference bias documented in recent evaluation literature.

## Results

- **Training samples**: [FILL] labeled examples
- **Risk distribution**: low [FILL]% / medium [FILL]% / high [FILL]%
- **Test accuracy**: [FILL]% (vs. 33% random baseline)
- **Per-class recall**: low=[FILL]%, medium=[FILL]%, high=[FILL]%
- **Inference speed**: <3s per assessment on T4

## Real-World Impact (Safety & Trust Track)

This tool directly addresses AI safety by providing:

1. **Transparency**: Users see WHY an AI answer might be unreliable, not just a binary safe/unsafe flag
2. **Deployability**: At 2B parameters, it runs on edge devices — critical for offline medical clinics, rural education, disaster response
3. **Universality**: Works as a wrapper around ANY multi-LLM system, regardless of the underlying models
4. **Cost-efficiency**: One small model replaces expensive ensemble-based verification pipelines

**Use Cases**:
- Hospital AI systems flagging potentially hallucinated drug interactions
- Educational platforms warning students about uncertain AI-generated explanations
- Legal research tools highlighting contradictory interpretations across AI assistants

## Challenges Overcome

1. **Data from scratch**: No existing "reliability risk" dataset existed; we built the entire pipeline including seed design, multi-model collection, and structured labeling
2. **Free-tier constraints**: Operated entirely within SiliconFlow 16 CNY credit + Kaggle free GPU
3. **Label balance**: Iteratively tuned judge prompts with calibration anchors to achieve balanced risk distribution

## Architecture

```
User Query → [LLM A] → Response A ─┐
           → [LLM B] → Response B ─┼→ Gemma 4 2B Judge → Risk Level + Scores + Reasoning
           → [LLM C] → Response C ─┘
```

## Links

- **Code**: https://github.com/1235789a/jinan-drone
- **Live Demo**: [FILL - HuggingFace Spaces URL]
- **Video**: [FILL - YouTube URL]
