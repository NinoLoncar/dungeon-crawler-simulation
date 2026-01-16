class Ability:
        def __init__(self, name, cooldown_duration,aoe, priority, source,icon):
            self.name=name
            self.cooldown_duration = cooldown_duration
            self.icon=icon
            self.aoe=aoe
            self.source=source
            self.on_cooldown = False
            self.cooldown_left = 0
            self.priority = priority
        
        def start_cooldown(self):
            if self.cooldown_duration > 0:
                self.on_cooldown = True
                self.cooldown_left = self.cooldown_duration
        
        def tick_cooldown(self):
            if not self.on_cooldown:
                return
            self.cooldown_left -= 1
            if self.cooldown_left <= 0:
                self.cooldown_left = 0
                self.on_cooldown = False
        
        def is_ready(self):
            return not self.on_cooldown
        
        def reset_cooldown(self):
            self.cooldown_left=0
            self.on_cooldown=False