# YouTube Video Script — AI Reliability Judge
**Duration Target: 2:30-3:00 minutes**

---

## [0:00 - 0:20] Opening Hook

**[Screen: Title card with project name]**

> "What happens when two AI models give you completely opposite medical advice? One says call 911, the other says just wait it out. How do you know which one to trust?"
>
> "I built the AI Reliability Judge — a fine-tuned Gemma 4 model that automatically detects when AI responses are unreliable or dangerous."

---

## [0:20 - 0:50] Problem Statement

**[Screen: Split screen showing two contradicting LLM responses]**

> "As AI becomes part of daily life, people ask different models for advice on health, money, legal issues. But these models can hallucinate — confidently giving wrong, even dangerous information."
>
> "The problem gets worse when different models disagree. A regular user has no way to tell which response is reliable."

---

## [0:50 - 1:30] Solution & How It Works

**[Screen: Architecture diagram — Question + Two Responses → Judge → Risk Assessment]**

> "The AI Reliability Judge takes a question and two AI responses, then outputs a structured risk assessment: risk level (low/medium/high), numerical scores for hallucination, semantic contradiction, and uncertainty, plus reasoning."
>
> "I fine-tuned Gemma 4 E2B — Google's efficient 2-billion parameter model — on 922 expert-annotated examples across medical, legal, financial, scientific, and technical domains."

**[Screen: Training config code snippet]**

> "Full-parameter fine-tuning on a single T4 GPU. No adapters needed — Gemma 4 E2B is small enough to train directly in bfloat16."

---

## [1:30 - 2:20] Live Demo

**[Screen: Kaggle notebook running]**

> "Let me show you the judge in action."

**[Run Medical case]**

> "Medical case: GPT-4 correctly describes heart attack symptoms. The other model dangerously says 'just wait 24 hours.' The judge flags HIGH risk — hallucination 9/10, contradiction 9/10."

**[Run Science case]**

> "Science case: Both models correctly explain Earth's seasons. Judge says LOW risk — responses agree and are accurate."

**[Run Financial case]**

> "Financial case: One model gives balanced advice, the other claims crypto guarantees 50% returns. Judge: HIGH risk — catches the hallucinated claim."

---

## [2:20 - 2:50] Impact

**[Screen: Deployment diagram]**

> "In production, this judge acts as a safety layer between AI and users, flagging dangerous outputs in real-time. At 2B parameters, it runs in 3 seconds per judgment."
>
> "This is how we build trustworthy AI — not one perfect model, but a lightweight verification layer that catches failures."

---

## [2:50 - 3:00] Outro

**[Screen: Links to code and demo]**

> "Links to code and demo in the description. Thanks for watching!"

---

## Recording Notes
- **Tool:** OBS Studio or Loom
- **Visuals:** Title card → Problem slides → Architecture → Notebook cells running → Summary
- **Tone:** Clear, confident, slightly urgent
