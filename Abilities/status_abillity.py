from Abilities.ability import Ability


class StatusAbility(Ability):
    def __init__(
        self,
        name,
        cooldown_duration,
        status_effect,
        aoe,
        friendly_targets,
        priority,
        source,
        icon,
    ):
        super().__init__(name, cooldown_duration, aoe, priority, source, icon)
        self.status_effect = status_effect
        self.friendly_targets = friendly_targets

    def clone(self, new_source):
        cloned_status = self.status_effect.clone(new_source)
        return StatusAbility(
            name=self.name,
            cooldown_duration=self.cooldown_duration,
            status_effect=cloned_status,
            aoe=self.aoe,
            priority=self.priority,
            source=new_source,
            icon=self.icon,
            friendly_targets=self.friendly_targets,
        )
