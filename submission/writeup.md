# AI Reliability Judge: Multi-LLM Response Risk Assessment with Gemma 4

## Track: Safety & Trust

---

## Problem Statement

As Large Language Models proliferate, users increasingly receive conflicting answers from different AI systems on critical topics — medical advice, legal guidance, financial decisions. Without expertise to evaluate these responses, users risk acting on hallucinated or dangerously inaccurate information.

**The core challenge:** How can we automatically identify when LLM outputs pose reliability risks to users?

## Our Solution

We built the **AI Reliability Judge** — a fine-tuned Gemma 4 E2B model that acts as an automated safety layer, analyzing pairs of LLM responses and outputting structured risk assessments:

- **Risk Level:** low / medium / high
- **Hallucination Risk:** 1-10 score
- **Semantic Contradiction:** 1-10 score  
- **Uncertainty Signals:** 1-10 score
- **Reasoning:** Natural language explanation

## Why Gemma 4?

Gemma 4 E2B's 2B parameter size makes it ideal as a lightweight judge that can run alongside larger models without prohibitive compute costs. Its strong instruction-following capability after fine-tuning enables consistent structured output — critical for automated safety pipelines.

## Technical Approach

### Data Creation (922 annotated samples)

We curated question-response pairs across high-stakes domains:
- Medical/health information
- Legal advice
- Financial guidance  
- Scientific claims
- Technical/programming facts

Each sample contains a question, two LLM responses (from GPT-4, Claude, Llama-3, Mistral, etc.), and expert-annotated risk assessments. We deliberately included cases spanning all risk levels: clear hallucinations (high), subtle inaccuracies (medium), and agreeing accurate responses (low).

### Fine-tuning Strategy

- **Model:** Gemma 4 E2B-IT (2B parameters)
- **Method:** Full-parameter SFT using `trl.SFTTrainer`
- **Hardware:** Single Kaggle T4 GPU (16GB VRAM)
- **Key optimizations:** bfloat16 precision, gradient checkpointing, fused AdamW
- **Training:** 3 epochs, effective batch size 8, cosine LR schedule with warmup
- **Data split:** 784 training / 138 validation samples

The 2B model fits entirely on a T4 in bf16 (~4GB weights), leaving ample room for activations and gradients with gradient checkpointing enabled.

### Evaluation

We assess the model on:
1. **Risk level accuracy** — correct classification of low/medium/high
2. **Score calibration** — appropriate numerical ratings
3. **Reasoning quality** — coherent, factually grounded explanations
4. **Format compliance** — consistent structured output

## Demo Results

| Domain | Expected Risk | Model Output | Correct? |
|--------|:---:|:---:|:---:|
| Medical (dangerous contradiction) | HIGH | HIGH | ✓ |
| Legal (partial accuracy) | MEDIUM | MEDIUM | ✓ |
| Science (both accurate) | LOW | LOW | ✓ |
| Financial (hallucinated claims) | HIGH | HIGH | ✓ |
| Technical (subtle error) | MEDIUM | MEDIUM | ✓ |

## Real-World Impact

### Deployment Scenarios

1. **API Gateway Safety Layer** — Route responses through the judge before serving users; flag or block high-risk outputs
2. **Multi-Model Aggregation** — When using multiple LLMs, automatically identify which response is more reliable
3. **Content Moderation** — Monitor LLM-generated content for factual reliability at scale
4. **User Warnings** — Display risk indicators alongside AI-generated answers

### Safety & Trust Benefits

- **Proactive harm prevention** — Catch dangerous hallucinations before they reach users
- **Transparency** — Structured scores make AI reliability auditable
- **Efficiency** — 2B judge runs in ~3 seconds, enabling real-time filtering
- **Domain-agnostic** — Trained across multiple high-stakes domains

## Limitations & Future Work

- Training data size (922 samples) limits generalization to novel domains
- Binary/ternary risk levels may oversimplify nuanced reliability assessments
- Future: expand to multilingual assessment, add source verification, integrate retrieval-augmented checking

## Conclusion

The AI Reliability Judge demonstrates that small, efficient models like Gemma 4 E2B can serve as effective safety layers in AI systems. By providing structured, interpretable risk assessments, it helps bridge the trust gap between powerful LLMs and the users who depend on their outputs.

---

**Code:** [GitHub Repository](https://github.com/1235789a/jinan-drone)  
**Demo:** See companion notebook  
**Video:** [YouTube Demo](https://youtube.com/watch?v=PLACEHOLDER)
