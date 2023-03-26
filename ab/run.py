import logging
import sys
from typing import Iterable, Optional, Tuple

from joblib import Parallel, delayed
from plumbum import BG, LocalPath, ProcessExecutionError, local
from plumbum.commands.modifiers import Future
from tqdm.auto import tqdm

from ab.agent import AgentRevision
from ab.replay import Replay
from ab.result import ABResult


def get_replay_file_name(rev_a: AgentRevision, rev_b: AgentRevision, seed: int) -> str:
    return f"{seed}_{rev_a.revision}_{rev_b.revision}.json"


def run_game(
    script_a: LocalPath, script_b: LocalPath, seed: int, out_file: LocalPath
) -> Tuple[int, str, str]:
    cmd = local["luxai-s2"][script_a][script_b]["-v", 1]["-s", seed]["-o", out_file]
    retcode, stdout, stderr = cmd.run(retcode=None)
    return retcode, stdout, stderr


def run_game_and_get_replay(
    rev_a: AgentRevision, rev_b: AgentRevision, seed: int, replay_file: LocalPath
) -> Replay:
    replay_file = replay_file
    retcode, stdout, stderr = run_game(rev_a.script_path, rev_b.script_path, seed, replay_file)

    if retcode != 0:
        logging.error(f"game finished with non-zero code: {retcode}")
        logging.error(f"seed: {seed}")
        logging.error(f"rev_a: {rev_a.revision}")
        logging.error(f"rev_b: {rev_b.revision}")
        logging.error(f"stdout:\n\u001b[36m{stdout.strip()}\u001b[0m")
        logging.error(f"stderr:\n\u001b[31m{stderr.strip()}\u001b[0m")

    return Replay(
        path=replay_file,
        player_revisions=[rev_a.revision, rev_b.revision],
        seed=seed,
    )


def run_ab(
    rev_a: AgentRevision,
    rev_b: AgentRevision,
    seeds: Iterable[int],
    replays_dir: LocalPath,
    n_jobs: Optional[int] = None,
) -> ABResult:
    if n_jobs is None:
        n_jobs = -1

    assert rev_a.revision != rev_b.revision

    replays_dir.mkdir()
    jobs = []
    for seed in seeds:
        jobs.append(
            delayed(run_game_and_get_replay)(
                rev_a,
                rev_b,
                seed,
                replays_dir / get_replay_file_name(rev_a, rev_b, seed),
            )
        )
        # swap rev_a and rev_b
        jobs.append(
            delayed(run_game_and_get_replay)(
                rev_b,
                rev_a,
                seed,
                replays_dir / get_replay_file_name(rev_b, rev_a, seed),
            )
        )
    replays = Parallel(n_jobs=n_jobs, backend="threading")(tqdm(jobs))
    return ABResult(rev_a, rev_b, replays)
