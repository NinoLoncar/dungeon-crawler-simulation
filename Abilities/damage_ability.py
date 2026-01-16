from Abilities.ability import Ability
import random

class DamageAbility(Ability):
    def __init__(self, name, cooldown_duration, min_dmg, max_dmg, aoe,priority, source,icon ):
        super().__init__(name, cooldown_duration,  aoe,priority, source,icon)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
    
    def roll_damage(self):
        return random.randint(self.min_dmg, self.max_dmg)
    
    def clone(self, new_source):
        return DamageAbility(
            name=self.name,
            cooldown_duration=self.cooldown_duration,
            min_dmg=self.min_dmg,
            max_dmg=self.max_dmg,
            aoe=self.aoe,
            priority=self.priority,
            icon=self.icon,
            source=new_source
        )