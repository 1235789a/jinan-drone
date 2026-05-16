# Step 1: 种子问题生成 Prompt

> 用法：打开 Trae，选 **DeepSeek-V4-Pro**，把下面整段 prompt 粘过去即可。

---

```
You are a dataset architect building a RELIABILITY RISK detection benchmark. Your job: generate 1000 high-quality seed questions that are likely to produce DISAGREEMENT among different frontier LLMs.

## Core Design Principles

Questions must be designed to trigger reliability risk signals:
1. **Hallucination-prone**: specific numbers, dates, citations, technical parameters
2. **Contradiction-prone**: contested interpretations, jurisdiction-specific, version-specific
3. **Uncertainty-prone**: edge cases, recent developments, expert-level nuance

AVOID:
- Trivia with clear single answers ("capital of France")
- Opinion questions with no factual anchor ("what's your favorite color")
- Questions requiring real-time info ("what's today's weather")

## Distribution Plan (1000 total)

### Domain 1: Medical (200 questions, ENGLISH)
Subtopics (25 questions each):
- Drug interactions & dosage edge cases
- Differential diagnosis of atypical presentations
- Post-op risk assessments
- Pediatric vs adult dosing conflicts
- Alternative therapy efficacy claims
- Rare disease diagnostic criteria
- Lab result interpretation edge cases
- Emergency triage decision points

### Domain 2: Legal (200 questions, ENGLISH)
Subtopics (25 questions each):
- Cross-jurisdictional conflicts (US state vs federal, EU vs US)
- Contract clause interpretation disputes
- IP boundary cases (AI-generated content, fair use)
- Labor law gray zones
- Data privacy compliance (GDPR/CCPA/PIPL conflicts)
- Criminal liability thresholds
- Administrative penalty standards
- Arbitration vs litigation strategic choices

### Domain 3: Science (200 questions, ENGLISH)
Subtopics (25 questions each):
- Dark matter / dark energy interpretations
- Quantum computing practical limits
- CRISPR ethics and boundary cases
- Climate model divergences
- Neuroscience of consciousness debates
- Nutrition controversies with conflicting studies
- Evolutionary biology edge cases
- Cosmological hypotheses under contention

### Domain 4: Tech (200 questions, ENGLISH)
Subtopics (25 questions each):
- API version compatibility traps
- Framework best-practice disputes
- Performance optimization tradeoffs
- Security vulnerability mitigation choices
- System architecture pattern selection
- Config parameter tuning for specific workloads
- Deprecation migration paths
- Concurrency model selection

### Domain 5: History & Society (200 questions, 50% ENGLISH 50% 中文)
Subtopics (25 questions each, alternating EN/ZH):
- 有争议历史事件的归因 / Contested historical attributions
- 具体数字考证（伤亡、经济数据）/ Specific figure verification
- 历史人物评价分歧 / Contested historical figure evaluations
- 文明起源理论 / Civilization origin theories
- 战争决策动机 / Wartime decision motivations
- 文化遗产归属争议 / Cultural heritage ownership disputes
- 历史分期与定性 / Periodization disputes
- 社会政策效果评估 / Social policy impact assessments

## Output Format (STRICT)

Output exactly 1000 lines of JSONL. No preamble, no commentary, no markdown fences. Just pure JSONL starting from line 1.

Each line format:
{"id": <int>, "domain": "<medical|legal|science|tech|history>", "subtopic": "<subtopic name>", "question": "<the question>", "lang": "<en|zh>"}

## Quality Bar

Each question must:
- Be answerable in 80-200 words
- Mention specific entities (drugs, laws, APIs, historical events, etc.)
- Not be Googleable with a single canonical answer
- Trigger at least one of: hallucination / contradiction / uncertainty

## Start Generation

Begin with id=1 and continue through id=1000. Maintain strict distribution:
- ids 1-200: medical
- ids 201-400: legal  
- ids 401-600: science
- ids 601-800: tech
- ids 801-1000: history

If the response would exceed your output limit, stop at a clean point and end with a single line: `<CONTINUE_FROM_ID=N>` where N is the next id to resume. Do not add any other text.
```

---

## 如果被截断了

直接回复：

```
Continue from id=<N>, same format, no preamble. End with <CONTINUE_FROM_ID=M> again if you hit the limit.
```

把所有分段的输出拼到 `data/seeds.jsonl` 里。

---

## 验证

```bash
# 检查行数
wc -l data/seeds.jsonl

# 检查 JSON 合法性
python -c "
import json
errs = 0
with open('data/seeds.jsonl') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except:
            errs += 1
            print(f'Line {i} invalid')
print(f'Total errors: {errs}')
"

# 检查分布
python -c "
import json
from collections import Counter
domains = []
with open('data/seeds.jsonl') as f:
    for line in f:
        domains.append(json.loads(line)['domain'])
print(Counter(domains))
"
```

预期：
```
medical: 200, legal: 200, science: 200, tech: 200, history: 200
```
