#!/bin/bash
# Real-time log monitoring for DeepModeling RL training

echo "Monitoring training logs in real-time..."
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

# Find the most recent Ray session
RAY_SESSION=$(ls -dt /tmp/ray/session_* 2>/dev/null | head -1)

if [ -z "$RAY_SESSION" ]; then
    echo "ERROR: No Ray session found"
    exit 1
fi

echo "Ray session: $RAY_SESSION"
echo ""

# Monitor multiple log sources
echo "Watching for training activity (ROLLOUT, ERROR, LitDeepModeling)..."
echo "========================================"

# Use tail -F to follow logs even if files rotate
tail -F \
    "$RAY_SESSION"/logs/python-core-worker*.log \
    "$RAY_SESSION"/logs/worker*.log \
    2>/dev/null | \
    grep --line-buffered -E "\[ROLLOUT|\[EPISODE|\[NODE:|ERROR|Exception|Traceback|dequeue_rollout|Starting training|trainer.fit|LitDeepModeling" | \
    while IFS= read -r line; do
        # Add timestamp and color
        echo "[$(date '+%H:%M:%S')] $line"
    done
