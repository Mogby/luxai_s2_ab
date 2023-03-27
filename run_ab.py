import argparse
import logging
from typing import Optional

from plumbum import LocalPath

from ab.agent import AgentRevision
from ab.run import run_ab


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-a", type=LocalPath, help="path to main.py of agent A")
    parser.add_argument("--agent-b", type=LocalPath, help="path to main.py of agent B")
    parser.add_argument(
        "--workdir",
        type=LocalPath,
        help="replay data and A/B results will be written to this directory",
    )
    parser.add_argument(
        "--n-seeds",
        type=int,
        default=10,
        help="number of seeds to run, for each seed two games will be played: one with "
        "agent A as player 0 and another with agent B as player 0",
    )
    parser.add_argument(
        "--n-jobs",
        type=int,
        required=False,
        help="number of games to run simultaniously, is equal to the number of CPU "
        "cores by default",
    )
    parser.add_argument(
        "--disable-mirroring",
        action="store_true",
        help="if set, only one game will be played for each seed: agent A will always "
        "go first and agent B will always go second",
    )
    parser.add_argument(
        "--reuse-existing-replays",
        action="store_true",
        help="if set, existing replay files will be reused instead of being generated "
        "again",
    )
    return parser.parse_args()


def main(
    agent_a: LocalPath,
    agent_b: LocalPath,
    workdir: LocalPath,
    n_seeds: int,
    n_jobs: Optional[int],
    enable_mirroring: bool,
    reuse_existing_replays: bool,
) -> None:
    rev_a = AgentRevision(script_path=agent_a, revision="A")
    rev_b = AgentRevision(script_path=agent_b, revision="B")
    result = run_ab(
        rev_a,
        rev_b,
        range(n_seeds),
        workdir / "replays",
        n_jobs=n_jobs,
        enable_mirroring=enable_mirroring,
        reuse_existing_replays=reuse_existing_replays,
    )
    result.get_result_df().to_csv(workdir / "result.csv", index=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    main(
        args.agent_a,
        args.agent_b,
        args.workdir,
        args.n_seeds,
        args.n_jobs,
        not args.disable_mirroring,
        args.reuse_existing_replays,
    )
