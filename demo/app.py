"""
Day 3: Gradio Demo 应用
极简单文件 Demo，展示 AI Reliability Judge 的核心功能。
"""

import json
import gradio as gr
from pathlib import Path

# --- Load showcase cases for quick demo ---
SHOWCASE_PATH = Path(__file__).parent / "showcase_cases.json"


def load_showcase_cases():
    """加载预设展示案例"""
    if SHOWCASE_PATH.exists():
        with open(SHOWCASE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def judge_reliability(question: str, response_a: str, response_b: str, response_c: str) -> str:
    """
    主推理函数 - 调用 Reliability Judge 模型
    在正式部署时替换为真实模型推理
    """
    # TODO: 替换为真实模型推理
    # from inference.predict import ReliabilityJudge
    # judge = ReliabilityJudge()
    # result = judge.predict(question, response_a, response_b, response_c)

    # Placeholder output for demo structure
    result = {
        "risk_level": "medium",
        "hallucination_risk": 5,
        "semantic_contradiction": 6,
        "uncertainty_signals": 4,
        "reasoning": "Models show partial disagreement on specific details while agreeing on general principles.",
    }

    # Format output
    risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(result["risk_level"], "⚪")
    
    output = f"""## {risk_emoji} Risk Level: {result['risk_level'].upper()}

### Dimension Scores

| Dimension | Score | Level |
|-----------|-------|-------|
| Hallucination Risk | {result['hallucination_risk']}/10 | {'🔴' if result['hallucination_risk'] > 6 else '🟡' if result['hallucination_risk'] > 3 else '🟢'} |
| Semantic Contradiction | {result['semantic_contradiction']}/10 | {'🔴' if result['semantic_contradiction'] > 6 else '🟡' if result['semantic_contradiction'] > 3 else '🟢'} |
| Uncertainty Signals | {result['uncertainty_signals']}/10 | {'🔴' if result['uncertainty_signals'] > 6 else '🟡' if result['uncertainty_signals'] > 3 else '🟢'} |

### Reasoning
{result['reasoning']}

---
*Assessed by AI Reliability Judge (Gemma 3 1B + QLoRA)*
"""
    return output


def load_example(case_idx: int):
    """加载预设案例到输入框"""
    cases = load_showcase_cases()
    if 0 <= case_idx < len(cases):
        case = cases[case_idx]
        return (
            case["question"],
            case["responses"]["gpt4o"],
            case["responses"]["claude"],
            case["responses"]["gemini"],
        )
    return ("", "", "", "")


# === Build Gradio Interface ===
with gr.Blocks(
    title="AI Reliability Judge",
    theme=gr.themes.Soft(),
) as demo:
    gr.Markdown("""
    # 🛡️ AI Reliability Judge
    ### A Lightweight Risk Perception Layer for LLM Outputs
    
    This tool analyzes responses from multiple LLMs and assesses the **reliability risk level** — 
    not who is right, but how much you should trust the answers.
    
    **Risk Dimensions:**
    - 🧠 **Hallucination Risk** — Are responses potentially fabricated?
    - ⚔️ **Semantic Contradiction** — Do models fundamentally disagree?
    - ❓ **Uncertainty Signals** — Is there appropriate confidence calibration?
    """)

    with gr.Row():
        with gr.Column(scale=1):
            question_input = gr.Textbox(
                label="📝 Question",
                placeholder="Enter the question asked to multiple LLMs...",
                lines=3,
            )
            response_a = gr.Textbox(
                label="🤖 Response A (GPT-4)",
                placeholder="GPT-4's response...",
                lines=5,
            )
            response_b = gr.Textbox(
                label="🤖 Response B (Claude)",
                placeholder="Claude's response...",
                lines=5,
            )
            response_c = gr.Textbox(
                label="🤖 Response C (Gemini)",
                placeholder="Gemini's response...",
                lines=5,
            )
            judge_btn = gr.Button("🔍 Assess Reliability Risk", variant="primary", size="lg")

        with gr.Column(scale=1):
            output = gr.Markdown(label="Assessment Result")

    judge_btn.click(
        fn=judge_reliability,
        inputs=[question_input, response_a, response_b, response_c],
        outputs=output,
    )

    # Example cases
    gr.Markdown("### 📚 Example Cases")
    gr.Examples(
        examples=[
            [
                "What is the maximum safe daily dose of acetaminophen for an adult with mild liver disease?",
                "The maximum safe dose is 3000mg per day for adults with liver disease.",
                "Adults with liver disease should not exceed 2000mg per day.",
                "The standard maximum is 4000mg per day. For liver disease, 3000-4000mg is generally acceptable.",
            ],
            [
                "What is the capital of France?",
                "The capital of France is Paris.",
                "Paris is the capital city of France.",
                "France's capital is Paris, located in the north-central part of the country.",
            ],
        ],
        inputs=[question_input, response_a, response_b, response_c],
        label="Click to load example",
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
