from Abilities.ability import Ability
import random

class HealingAbility(Ability):
    def __init__(self, name, cooldown_duration, min_hp, max_hp,aoe, priority, source,icon ):
        super().__init__(name, cooldown_duration, aoe,priority, source,icon)
        self.min_hp = min_hp
        self.max_hp= max_hp
    
    def roll_hp(self):
        return random.randint(self.min_hp, self.max_hp)
    
    def clone(self, new_source):
        return HealingAbility(
            name=self.name,
            cooldown_duration=self.cooldown_duration,
            min_hp=self.min_hp,
            max_hp=self.max_hp,
            aoe=self.aoe,
            priority=self.priority,
            icon=self.icon,
            source=new_source
        )