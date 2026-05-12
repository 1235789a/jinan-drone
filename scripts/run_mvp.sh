#!/bin/bash
# MVP 快速验证 —— 跑 60 条，端到端 5-10 分钟

set -euo pipefail
cd "$(dirname "$0")/.."

echo "=========================================="
echo "AI Reliability Judge - MVP Pipeline Test"
echo "=========================================="

echo ""
echo "[0/4] Checking providers..."
python scripts/providers.py

echo ""
echo "[1/4] Generating 60 seed questions..."
python scripts/generate_seeds.py --mvp

echo ""
echo "[2/4] Calling 3 models for each seed..."
python scripts/call_models.py --mvp

echo ""
echo "[3/4] Running Meta-Judge on responses..."
python scripts/label_judge.py --mvp

echo ""
echo "[4/4] Formatting for training..."
python scripts/format_for_training.py

echo ""
echo "=========================================="
echo "MVP pipeline complete."
echo "Check data/stats.json for label distribution."
echo "=========================================="
