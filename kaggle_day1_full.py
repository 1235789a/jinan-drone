# === AI Reliability Judge - Day 1 Full Pipeline (Kaggle) ===
# Copy-paste this ENTIRE file into a single Kaggle Code cell.
# It handles everything: clone, env, seeds, models, judge, format.
# Safe to re-run after Kaggle session reload (idempotent).
#
# Prerequisites (Kaggle right sidebar):
#   Internet: ON
#   Secrets:  SILICONFLOW_API_KEY [ON], ANTHROPIC_API_KEY [ON]
# ================================================================

import os, json, shutil, subprocess

WORK = "/kaggle/working"
REPO = WORK + "/jinan-drone"

# ---- STEP 0: Environment setup (idempotent) ----
os.chdir(WORK)
if not os.path.exists(REPO + "/scripts/providers.py"):
    if os.path.exists(REPO):
        shutil.rmtree(REPO)
    subprocess.run(["git", "clone", "-b", "feat/hackathon-plan", "--depth", "1",
                    "https://github.com/1235789a/jinan-drone.git", REPO], check=True)
os.chdir(REPO)
subprocess.run(["pip", "install", "-q", "openai", "python-dotenv", "tenacity", "tqdm"], check=True)

# ---- STEP 1: Generate .env from Kaggle Secrets ----
from kaggle_secrets import UserSecretsClient
s = UserSecretsClient()
env_lines = [
    "SILICONFLOW_API_KEY=" + s.get_secret("SILICONFLOW_API_KEY"),
    "GOOGLE_API_KEY=",
    "ANTHROPIC_API_KEY=" + s.get_secret("ANTHROPIC_API_KEY"),
    "ANTHROPIC_BASE_URL=https://api123.top/v1",
    "ANTHROPIC_MODEL=claude-sonnet-4-6",
    "MAX_CONCURRENT=2",
    "REQUEST_TIMEOUT=180",
]
with open(".env", "w") as f:
    f.write("\n".join(env_lines) + "\n")
print("[OK] .env created")

# ---- STEP 2: Verify providers ----
result = subprocess.run(["python", "scripts/providers.py"], capture_output=True, text=True)
print(result.stdout)
if "deepseek" not in result.stdout or "qwen" not in result.stdout:
    print("[FAIL] Missing data-source providers. Check SILICONFLOW_API_KEY secret.")
    raise SystemExit(1)
if "claude" not in result.stdout:
    print("[FAIL] Missing judge provider. Check ANTHROPIC_API_KEY secret.")
    raise SystemExit(1)
print("[OK] All providers ready")

# ---- STEP 3: Generate 1000 seeds (batched, timeout-safe) ----
SEEDS_FILE = "data/seeds.jsonl"
if os.path.exists(SEEDS_FILE):
    with open(SEEDS_FILE) as f:
        existing = sum(1 for l in f if l.strip())
    if existing >= 900:
        print("[SKIP] Seeds already exist: " + str(existing) + " lines")
    else:
        os.remove(SEEDS_FILE)
        existing = 0
else:
    existing = 0

if existing < 900:
    print("[RUN] Generating 1000 seeds in 10 batches...")
    all_seeds = []
    for batch in range(10):
        print("  Batch " + str(batch+1) + "/10")
        subprocess.run(["python", "scripts/generate_seeds.py", "--target", "100"], check=True)
        with open(SEEDS_FILE) as f:
            batch_seeds = [json.loads(l) for l in f if l.strip()]
        all_seeds.extend(batch_seeds)
    # Re-number and write final
    for i, seed in enumerate(all_seeds, 1):
        seed["id"] = i
    with open(SEEDS_FILE, "w") as f:
        for seed in all_seeds:
            f.write(json.dumps(seed, ensure_ascii=False) + "\n")
    print("[OK] Total seeds: " + str(len(all_seeds)))

# ---- STEP 4: Call 2 data sources ----
RAW_FILE = "data/raw_responses.jsonl"
if os.path.exists(RAW_FILE):
    with open(RAW_FILE) as f:
        existing_raw = sum(1 for l in f if l.strip())
    if existing_raw >= 900:
        print("[SKIP] Responses already exist: " + str(existing_raw) + " lines")
    else:
        print("[RUN] Calling models (resume from " + str(existing_raw) + ")...")
        subprocess.run(["python", "scripts/call_models.py"], check=True)
else:
    print("[RUN] Calling 2 models for each seed...")
    subprocess.run(["python", "scripts/call_models.py"], check=True)

# ---- STEP 5: Claude Meta-Judge ----
LABELED_FILE = "data/labeled_train.jsonl"
if os.path.exists(LABELED_FILE):
    with open(LABELED_FILE) as f:
        existing_labeled = sum(1 for l in f if l.strip())
    if existing_labeled >= 900:
        print("[SKIP] Labels already exist: " + str(existing_labeled) + " lines")
    else:
        print("[RUN] Judging (resume from " + str(existing_labeled) + ")...")
        subprocess.run(["python", "scripts/label_judge.py"], check=True)
else:
    print("[RUN] Claude Meta-Judge labeling...")
    subprocess.run(["python", "scripts/label_judge.py"], check=True)

# ---- STEP 6: Format for training ----
print("[RUN] Formatting for training...")
subprocess.run(["python", "scripts/format_for_training.py"], check=True)

# ---- STEP 7: Report ----
if os.path.exists("data/stats.json"):
    with open("data/stats.json") as f:
        stats = json.load(f)
    print("\n" + "=" * 50)
    print("DAY 1 RESULTS")
    print("=" * 50)
    print("Total labeled: " + str(stats.get("total_samples", 0)))
    print("Risk distribution: " + json.dumps(stats.get("level_pct", {})))
    print("Balanced: " + str(stats.get("balanced", False)))
    if os.path.exists("data/train_chat.jsonl"):
        with open("data/train_chat.jsonl") as f:
            train_count = sum(1 for l in f if l.strip())
        with open("data/val_chat.jsonl") as f:
            val_count = sum(1 for l in f if l.strip())
        print("Train: " + str(train_count) + " / Val: " + str(val_count))
    print("=" * 50)

# ---- STEP 8: Save to /kaggle/working for persistence ----
os.makedirs(WORK + "/reliability_judge_data", exist_ok=True)
for fname in ["train_chat.jsonl", "val_chat.jsonl", "labeled_train.jsonl", "stats.json", "seeds.jsonl"]:
    src = "data/" + fname
    if os.path.exists(src):
        shutil.copy(src, WORK + "/reliability_judge_data/" + fname)
print("\n[OK] Data saved to /kaggle/working/reliability_judge_data/")
print("Save this notebook version to persist for Day 2.")
