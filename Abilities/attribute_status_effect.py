from Abilities.status_effect import StatusEffect


class AttributeStatusEffect(StatusEffect):
    def __init__(self, name, duration, attribute, amount, source, icon):
        super().__init__(name, duration, source, icon)
        self.amount = amount
        self.attribute = attribute

    def on_apply(self, target, game):
        sign = ""
        if self.amount > 0:
            sign = "+"
        if self.attribute == "speed":
            target.speed += self.amount
            game.display_console_message(
                f"{target.name} received {self.name} ({sign}{self.amount} speed)",
                self.icon,
            )

    def on_expire(self, target, game):
        sign = ""
        if self.amount > 0:
            sign = "+"
        if self.attribute == "speed":
            target.speed -= self.amount
            game.display_console_message(
                f"{self.name} expired on {target.name} ({sign}{self.amount} speed)",
                self.icon,
            )

    def clone(self, new_source):
        return AttributeStatusEffect(
            name=self.name,
            duration=self.duration,
            amount=self.amount,
            attribute=self.attribute,
            source=new_source,
            icon=self.icon,
        )
