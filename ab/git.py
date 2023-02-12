from plumbum import BG, LocalPath, local

from ab.agent import AgentRevision


def get_repo_hash(repo_path: LocalPath) -> str:
    job = local["git"]["show"]["--format=%H"]["-s"].with_cwd(repo_path) & BG
    job.wait()
    return job.stdout.strip()


def make_agent_revision_from_repo_path(repo_path: LocalPath) -> LocalPath:
    return AgentRevision(
        script_path=repo_path / "main.py",
        revision=get_repo_hash(repo_path),
    )
