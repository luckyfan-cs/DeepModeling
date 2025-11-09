#!/bin/bash
# Monitor DeepModeling RL training progress

echo "======================================"
echo "DeepModeling RL Training Monitor"
echo "======================================"
echo ""

# Find training processes
echo "[1] Training Processes:"
ps aux | grep "train_deepmodeling.py" | grep -v grep | awk '{printf "  PID: %s, Runtime: %s, CMD: ", $2, $10; for(i=11;i<=NF;i++) printf "%s ", $i; printf "\n"}'

if [ -z "$(ps aux | grep train_deepmodeling.py | grep -v grep)" ]; then
    echo "  ❌ No training process found"
else
    echo ""
fi

# GPU status
echo "[2] GPU Status:"
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits | \
    awk -F',' '{printf "  GPU %s: %s%% util, %s/%s MB memory\n", $1, $3, $4, $5}'
echo ""

# Check workspace activity
echo "[3] Workspace Activity:"
if [ -d "./workspace_rl" ]; then
    TASK_DIRS=$(find ./workspace_rl -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    echo "  Workspace task directories: $TASK_DIRS"
    if [ $TASK_DIRS -gt 0 ]; then
        echo "  Recent tasks:"
        ls -lth ./workspace_rl | head -6 | tail -5 | awk '{printf "    %s %s %s\n", $6, $7, $9}'
    fi
else
    echo "  ❌ Workspace directory not created yet"
fi
echo ""

# Check Ray status
echo "[4] Ray Status:"
RAY_PROCS=$(ps aux | grep "ray::" | grep -v grep | wc -l)
echo "  Ray worker processes: $RAY_PROCS"
if [ $RAY_PROCS -gt 0 ]; then
    echo "  ✓ Ray is running"
else
    echo "  ⚠️  No Ray processes detected"
fi
echo ""

# Check recent logs
echo "[5] Recent Activity (last 20 lines from agentops.log):"
if [ -f "./agentops.log" ]; then
    tail -20 ./agentops.log | sed 's/^/  /'
else
    echo "  ℹ️  No agentops.log found"
fi
echo ""

# Look for ROLLOUT logs in Ray session
echo "[6] Training Progress (searching Ray logs for ROLLOUT markers):"
RAY_SESSION=$(ls -dt /tmp/ray/session_* 2>/dev/null | head -1)
if [ -n "$RAY_SESSION" ]; then
    echo "  Ray session: $RAY_SESSION"
    ROLLOUT_COUNT=$(grep -r "\[ROLLOUT START\]" "$RAY_SESSION/logs/" 2>/dev/null | wc -l)
    echo "  Total rollouts started: $ROLLOUT_COUNT"

    if [ $ROLLOUT_COUNT -gt 0 ]; then
        echo "  Most recent rollout activity:"
        grep -h "\[ROLLOUT" "$RAY_SESSION/logs/"python-core-worker*.log 2>/dev/null | tail -5 | sed 's/^/    /'
    fi
else
    echo "  ⚠️  No Ray session found"
fi
echo ""

echo "======================================"
echo "Monitoring Tips:"
echo "  - Run: watch -n 5 ./monitor_training.sh"
echo "  - GPU util should spike during training"
echo "  - workspace_rl should have task directories"
echo "  - Look for [ROLLOUT START/COMPLETE] logs"
echo "======================================"
