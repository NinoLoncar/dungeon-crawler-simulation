class StatusEffect:
    def __init__(self, name, duration, source, icon=None):
        self.name = name
        self.duration = duration
        self.remaining = duration
        self.source = source
        self.icon = icon
        self.is_expired = False

    def on_apply(self, target, game):
        pass

    def on_action_start(self, target, game):
        pass

    def on_expire(self, target, game):
        pass

    def tick(self, target, game):
        self.on_action_start(target, game)
        self.remaining -= 1
        if self.remaining <= 0:
            self.on_expire(target, game)
            self.is_expired = True
