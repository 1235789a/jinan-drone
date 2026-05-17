# YouTube Video Script — AI Reliability Judge
**Duration Target: 2:30-3:00 minutes**

---

## [0:00 - 0:20] Opening Hook

**[Screen: Title card with project name + Gemma 4 logo]**

> "What happens when two AI models give you completely opposite medical advice? One says call 911, the other says just wait it out. How do you know which one to trust?"
>
> "I'm [Your Name], and I built the AI Reliability Judge — a fine-tuned Gemma 4 model that automatically detects when AI responses are unreliable or dangerous."

---

## [0:20 - 0:50] Problem Statement

**[Screen: Split screen showing two contradicting LLM responses]**

> "As AI becomes part of daily life, people ask ChatGPT, Claude, Gemini — all these models — for advice on health, money, legal issues. But these models can hallucinate. They can confidently give you wrong, even dangerous information."
>
> "The problem gets worse when different models disagree. A regular user has no way to tell which response is reliable. That's the trust gap in AI."

---

## [0:50 - 1:30] Solution & How It Works

**[Screen: Architecture diagram showing Question → Two LLM Responses → Judge → Risk Assessment]**

> "The AI Reliability Judge solves this. It takes a question and two AI responses, then outputs a structured risk assessment: a risk level — low, medium, or high — along with numerical scores for hallucination risk, semantic contradiction, and uncertainty signals, plus a reasoning explanation."
>
> "I fine-tuned Gemma 4 E2B — Google's efficient 2-billion parameter model — on 922 expert-annotated examples across medical, legal, financial, scientific, and technical domains."

**[Screen: Code snippet of training config]**

> "The model runs on a single T4 GPU. Full-parameter fine-tuning with bfloat16 precision and gradient checkpointing. No adapters needed — Gemma 4 E2B is small enough to train directly."

---

## [1:30 - 2:20] Live Demo

**[Screen: Kaggle notebook running]**

> "Let me show you the judge in action."

**[Run Case 1: Medical]**

> "Here's a medical case. GPT-4 correctly describes heart attack symptoms and says call 911. The other model says 'just wait 24 hours.' The judge correctly flags this as HIGH risk — hallucination score 9 out of 10, semantic contradiction 9 out of 10."

**[Run Case 3: Science]**

> "Now two models both correctly explain Earth's seasons. The judge gives this LOW risk — both responses agree and are accurate."

**[Run Case 4: Financial]**

> "And here — one model gives balanced investment advice, the other claims crypto guarantees 50% returns. The judge: HIGH risk. It catches the hallucinated financial claim."

---

## [2:20 - 2:50] Impact & Conclusion

**[Screen: Deployment diagram]**

> "In production, this judge acts as a safety layer — sitting between AI models and users, flagging dangerous outputs in real-time. At only 2 billion parameters, it runs in 3 seconds per judgment."
>
> "For the Safety & Trust track: this is how we build AI systems people can actually rely on. Not by making one perfect model, but by adding a lightweight verification layer that catches the failures."

**[Screen: Summary card]**

> "AI Reliability Judge. Gemma 4 E2B. Making AI safer, one judgment at a time."

---

## [2:50 - 3:00] Outro

**[Screen: Links to code, notebook, writeup]**

> "Links to the code and demo notebook are in the description. Thanks for watching!"

---

## Production Notes

- **Recording tool:** OBS Studio or Loom (screen recording + voiceover)
- **Key visuals needed:**
  - Title card
  - Architecture diagram (Question → Models → Judge → Risk)
  - Kaggle notebook running cells
  - Results summary table
- **Tone:** Confident, clear, slightly urgent (safety matters)
- **Pace:** Medium-fast, ~150 words/minute
