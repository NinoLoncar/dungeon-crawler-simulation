from NPCs.npc import Npc


class Enemy(Npc):
    def __init__(
        self,
        type,
        max_hp,
        speed,
        fighting_style,
        icon=None,
    ):
        super().__init__(type, max_hp, speed, fighting_style, icon)
        self.type = type

    def clone(self):
        enemy = Enemy(
            type=self.type,
            max_hp=self.max_hp,
            fighting_style=self.fighting_style,
            speed=self.speed,
            icon=self.icon,
        )
        enemy.abilities = [ability.clone(enemy) for ability in self.abilities]

        return enemy
