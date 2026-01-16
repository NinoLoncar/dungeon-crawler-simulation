from Abilities.status_effect import StatusEffect
import random


class StunnedStatusEffect(StatusEffect):
    def __init__(self, name, duration, source, icon):
        super().__init__(name, duration, source, icon)

    def on_apply(self, target, game):
        game.display_console_message(
            f"{target.name} received {self.name} (stun for {self.duration} turns)",
            self.icon,
        )
        target.is_stunned = True

    def on_expire(self, target, game):
        game.display_console_message(f"{self.name} expired on {target.name}", self.icon)
        target.is_stunned = False

    def on_action_start(self, target, game):
        target.is_stunned = True

    def clone(self, new_source):
        return StunnedStatusEffect(
            name=self.name,
            duration=self.duration,
            source=new_source,
            icon=self.icon,
        )
