import argparse
from typing import Optional

from plumbum import LocalPath

from ab.git import make_agent_revision_from_repo_path
from ab.run import run_ab


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-a", type=LocalPath)
    parser.add_argument("--repo-b", type=LocalPath)
    parser.add_argument("--workdir", type=LocalPath)
    parser.add_argument("--n-seeds", type=int, default=10)
    parser.add_argument("--n-jobs", type=int, required=False)
    return parser.parse_args()


def main(
    repo_a: LocalPath,
    repo_b: LocalPath,
    workdir: LocalPath,
    n_seeds: int,
    n_jobs: Optional[int],
) -> None:
    rev_a = make_agent_revision_from_repo_path(repo_a)
    rev_b = make_agent_revision_from_repo_path(repo_b)
    result = run_ab(rev_a, rev_b, range(10), workdir / "replays")
    result.get_result_df().to_csv(workdir / "result.csv", index=False)


if __name__ == "__main__":
    args = parse_args()
    main(args.repo_a, args.repo_b, args.workdir, args.n_seeds, args.n_jobs)
