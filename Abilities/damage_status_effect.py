from Abilities.status_effect import StatusEffect
import random


class DamageStatusEffect(StatusEffect):
    def __init__(self, name, duration, min_dmg, max_dmg, source, icon):
        super().__init__(name, duration, source, icon)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def on_apply(self, target, game):
        game.display_console_message(
            f"{target.name} received {self.name} ({self.min_dmg} - {self.max_dmg} dmg/turn for {self.duration} turns)",
            self.icon,
        )

    def on_expire(self, target, game):
        game.display_console_message(f"{self.name} expired on {target.name}", self.icon)

    def on_action_start(self, target, game):
        dmg = random.randint(self.min_dmg, self.max_dmg)
        game.display_console_message(
            f"{self.name} status did {dmg} dmg to {target.name}", self.icon
        )
        target.apply_damage(dmg, game)

    def clone(self, new_source):
        return DamageStatusEffect(
            name=self.name,
            duration=self.duration,
            min_dmg=self.min_dmg,
            max_dmg=self.max_dmg,
            source=new_source,
            icon=self.icon,
        )
