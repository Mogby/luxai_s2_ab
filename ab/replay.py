import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional

import numpy as np
from plumbum import LocalPath


@dataclass
class Replay:
    path: Optional[LocalPath]
    player_revisions: List[str]
    seed: int
    finished: bool

    def __hash__(self) -> int:
        return hash(self.path)

    @property
    @lru_cache()
    def data(self) -> Dict:
        assert self.path is not None
        return json.load(self.path.open())

    @lru_cache()
    def get_final_board(self, board_name: str) -> np.ndarray:
        board = np.asarray(self.data["observations"][0]["board"][board_name])
        for i, obs in enumerate(self.data["observations"]):
            if i == 0:
                continue
            for loc, value in obs["board"][board_name].items():
                x, y = loc.split(",")
                x, y = int(x), int(y)
                board[x][y] = value
        return board

    @lru_cache()
    def get_final_lichen_strains(self) -> List[List[int]]:
        last_observation = self.data["observations"][-1]
        player_lichen_strains = []
        for i in range(2):
            factories_dict = last_observation["factories"][f"player_{i}"]
            lichen_strains = [f["strain_id"] for f in factories_dict.values()]
            player_lichen_strains.append(lichen_strains)
        return player_lichen_strains

    @lru_cache()
    def get_final_n_factories(self) -> List[int]:
        player_lichen_strains = self.get_final_lichen_strains()
        return [len(player_lichen_strains[0]), len(player_lichen_strains[1])]

    @lru_cache()
    def get_final_n_lichen(self) -> List[int]:
        player_lichen_strains = self.get_final_lichen_strains()
        final_lichen_board = self.get_final_board("lichen")
        final_lichen_strains_board = self.get_final_board("lichen_strains")
        player_n_lichen = []
        for i in range(2):
            mask = np.isin(final_lichen_strains_board, player_lichen_strains[i])
            n_lichen = final_lichen_board[mask].sum()
            player_n_lichen.append(n_lichen)
        return player_n_lichen

    @lru_cache()
    def get_result_by_factories_elimination(self) -> Optional[str]:
        player_n_factories = self.get_final_n_factories()
        if player_n_factories[0] == 0 and player_n_factories[1] == 0:
            return "tie"
        if player_n_factories[0] == 0:
            return "win_1"
        if player_n_factories[1] == 0:
            return "win_0"
        return None

    @lru_cache()
    def get_result_by_n_lichen(self) -> str:
        player_lichen_strains = self.get_final_lichen_strains()
        lichen_board = self.get_final_board("lichen")
        lichen_strains_board = self.get_final_board("lichen_strains")
        player_n_lichen = []
        for i in range(2):
            mask = np.isin(lichen_strains_board, player_lichen_strains[i])
            n_lichen = lichen_board[mask].sum()
            player_n_lichen.append(n_lichen)
        if player_n_lichen[0] == player_n_lichen[1]:
            return "tie"
        return "win_0" if player_n_lichen[0] > player_n_lichen[1] else "win_1"

    @lru_cache()
    def get_result(self) -> str:
        result = self.get_result_by_factories_elimination()
        if result is not None:
            return result
        return self.get_result_by_n_lichen()

    @lru_cache()
    def get_winner_hash(self) -> Optional[str]:
        result = self.get_result()
        if result == "tie":
            return None
        return self.player_revisions[0] if result == "win_0" else self.player_revisions[1]
