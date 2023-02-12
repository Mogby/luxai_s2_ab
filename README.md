# luxai_s2_ab

An A/B testing framework for the Lux AI Season 2 competition.

# Run

You can run A/B tests either from the `run_ab.ipynb` notebook or by running the `run_ab.py` script.

# Script Usage

## Example

```
python ./run_ab.py --agent-a ./sub_a/main.py --agent-b ./sub_b/main.py --workdir ./workdir --n-seeds 10
```

## Help

```
usage: run_ab.py [-h] [--agent-a AGENT_A] [--agent-b AGENT_B]
                 [--workdir WORKDIR] [--n-seeds N_SEEDS] [--n-jobs N_JOBS]

optional arguments:
  -h, --help         show this help message and exit
  --agent-a AGENT_A  Path to main.py of Agent A
  --agent-b AGENT_B  Path to main.py of Agent B
  --workdir WORKDIR  Replay data and A/B results will be written to this
                     directory
  --n-seeds N_SEEDS  Number of seeds to run. For each seed two games will be
                     played: one with Agent A as player 0 and another with
                     Agent B as player 0.
  --n-jobs N_JOBS    Number of games to run simultaniously. Is equal to the
                     number of CPU cores by default.
```
