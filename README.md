# luxai_s2_ab

An A/B testing framework for the Lux AI Season 2 competition.

# Requirements

`python >= 3.7`, `pip` are required.

Run `pip install -r ./requirements.txt` to install required python packages.

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
                 [--disable-mirroring] [--reuse-existing-replays]

optional arguments:
  -h, --help            show this help message and exit
  --agent-a AGENT_A     path to main.py of agent A
  --agent-b AGENT_B     path to main.py of agent B
  --workdir WORKDIR     replay data and A/B results will be written to this
                        directory
  --n-seeds N_SEEDS     number of seeds to run, for each seed two games will
                        be played: one with agent A as player 0 and another
                        with agent B as player 0
  --n-jobs N_JOBS       number of games to run simultaniously, is equal to the
                        number of CPU cores by default
  --disable-mirroring   if set, only one game will be played for each seed:
                        agent A will always go first and agent B will always
                        go second
  --reuse-existing-replays
                        if set, existing replay files will be reused instead
                        of being generated again
```
