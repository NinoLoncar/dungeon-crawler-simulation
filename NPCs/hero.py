from NPCs.npc import Npc
from NPCs.voting_styles import VotingStyle


class Hero(Npc):
    def __init__(
        self,
        name,
        max_hp,
        speed,
        fighting_style,
        voting_style,
        icon=None,
    ):
        super().__init__(name, max_hp, speed, fighting_style, icon)
        self.voting_style = voting_style

    def vote_for_next_room(self, candidates, exit_found=False):
        if self.voting_style == VotingStyle.COWARDLY:
            return self.cowardly_voting(candidates, exit_found)
        elif self.voting_style == VotingStyle.ADVENTUROUS:
            return self.adventurous_voting(candidates, exit_found)
        elif self.voting_style == VotingStyle.CURIOUS:
            return self.curious_voting(candidates, exit_found)
        else:
            return None, False

    def cowardly_voting(self, candidates, exit_found):
        if exit_found:
            return None, True
        if candidates:
            return min(candidates, key=lambda r: len(r.enemies)), False
        return None, False

    def adventurous_voting(self, candidates, exit_found):
        if candidates:
            return max(candidates, key=lambda r: len(r.enemies)), False
        return None, exit_found

    def curious_voting(self, candidates, exit_found):
        if candidates:
            return min(candidates, key=lambda r: len(r.enemies)), False
        return None, exit_found
