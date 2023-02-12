from dataclasses import dataclass

from plumbum import LocalPath


@dataclass
class AgentRevision:
    script_path: LocalPath
    revision: str
