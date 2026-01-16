from Abilities.damage_ability import DamageAbility
from Abilities.healing_ability import HealingAbility
from Abilities.status_abillity import StatusAbility
from Abilities.damage_status_effect import DamageStatusEffect
from Abilities.attribute_status_effect import AttributeStatusEffect
from NPCs.fighting_styles import FightingStyle
import random


class Npc:
    def __init__(
        self,
        name,
        max_hp,
        speed,
        fighting_style,
        icon=None,
    ):
        self.name = name
        self.icon = icon
        self.max_hp = max_hp
        self.hp = max_hp
        self.speed = speed
        self.fighting_style = fighting_style
        self.is_alive = True
        self.abilities = []
        self.status_effects = []
        self.is_stunned = False

    def make_action(self, game):
        if self.is_stunned:
            game.display_console_message(f"{self.name} is stunned", "stun.png")
            self.tick_status_effects(game)
            return
        ability = self.choose_ability(game)
        if not ability:
            game.display_console_message(f"{self.name} skipped their turn", "sleep.png")
            self.tick_status_effects(game)
            return
        if isinstance(ability, HealingAbility):
            targets = self.get_healing_targets(ability, game)
        elif isinstance(ability, StatusAbility):
            targets = self.get_status_effect_targets(ability, game)
        elif isinstance(ability, DamageAbility):
            targets = self.get_damage_targets(ability, game)

        message = f"{self.name} used {ability.name} on "
        if ability.aoe:
            message += "every opponent"
        else:
            message += targets[0].name

        game.display_console_message(message, ability.icon)
        game.distribute_used_ability(ability, targets)
        ability.start_cooldown()
        self.tick_status_effects(game)

    def choose_ability(self, game):
        allies = game.get_allies(self)
        opponents = game.get_opponents(self)

        heal = self.get_ability(HealingAbility)
        if heal:
            wounded_allies = [a for a in allies if a.is_alive and a.hp / a.max_hp < 0.8]
            if heal.aoe and len(wounded_allies) >= 2:
                return heal
            if not heal.aoe and wounded_allies:
                return heal

        status_ability = self.get_ability(StatusAbility)
        if status_ability:
            return status_ability

        dmg = self.get_ability(DamageAbility)
        if dmg and dmg.aoe and len(opponents) >= 2:
            return dmg
        if dmg:
            return dmg

        available_abilities = [a for a in self.abilities if not a.on_cooldown]
        return available_abilities[0] if available_abilities else None

    def get_healing_targets(self, ability, game):
        if ability.aoe:
            targets = game.get_allies(self)
        else:
            target = self.choose_most_wounded_ally(game.get_allies(self))
            targets = [target] if target else []
        return targets

    def get_damage_targets(self, ability, game):
        opponents = game.get_opponents(self)
        if ability.aoe:
            return opponents

        if self.fighting_style == FightingStyle.CHAOTIC:
            target = random.choice(opponents) if opponents else None

        elif self.fighting_style == FightingStyle.BERSERKER:
            if random.random() < 0.15:
                allies = game.get_allies(self)
                target = random.choice(allies) if allies else None
            else:
                target = random.choice(opponents) if opponents else None

        elif self.fighting_style == FightingStyle.OPPORTUNIST:
            target = self.choose_lowest_hp_target(opponents)

        elif self.fighting_style == FightingStyle.BOLD:
            target = self.choose_target_with_most_hp(opponents)

        elif self.fighting_style == FightingStyle.CHASER:
            target = self.choose_fastest_target(opponents)

        return [target] if target else []

    def get_status_effect_targets(self, ability, game):
        if ability.friendly_targets:
            if ability.aoe:
                targets = game.get_allies(self)
            else:
                target = self.choose_random_target(game.get_allies(self))
                targets = [target] if target else []
        else:
            targets = self.get_damage_targets(ability, game)
        return targets

    def recieve_used_ability(self, ability, game):
        if not self.is_alive:
            return
        if isinstance(ability, DamageAbility):
            self.apply_ability_damage(ability, game)
        if isinstance(ability, HealingAbility):
            self.apply_healing(ability, game)
        if isinstance(ability, StatusAbility):
            effect = ability.status_effect.clone(self)
            effect.on_apply(self, game)
            self.status_effects.append(effect)
            game.ui.update_npc_status_icons(self)

    def apply_ability_damage(self, ability, game):
        dmg = ability.roll_damage()
        message = f"{ability.name} did {dmg} damage to {self.name}"
        game.display_console_message(message, ability.icon)
        self.apply_damage(dmg, game)

    def apply_damage(self, dmg, game):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.icon = "skull.png"
            message = f"{self.name} died!"
            game.display_console_message(message, "skull.png")
            self.status_effects = []
            game.ui.update_npc_status_icons(self)

        game.ui.update_npc_ui(self)

    def apply_healing(self, ability, game):
        hp = ability.roll_hp()
        self.hp = min(self.max_hp, self.hp + hp)
        message = f"{ability.name} healed {self.name} for {hp} HP"
        game.display_console_message(message, ability.icon)
        game.ui.update_npc_ui(self)

    def choose_lowest_hp_target(self, possible_targets):
        alive_targets = [t for t in possible_targets if t.is_alive]
        if not alive_targets:
            return None
        return min(alive_targets, key=lambda t: t.hp)

    def get_ability(self, ability_cls):
        valid_abilities = [
            ability
            for ability in self.abilities
            if isinstance(ability, ability_cls) and not ability.on_cooldown
        ]
        if not valid_abilities:
            return None
        return max(valid_abilities, key=lambda a: a.priority)

    def choose_most_wounded_ally(self, allies):
        wounded = [a for a in allies if a.is_alive]
        if not wounded:
            return None
        return min(wounded, key=lambda a: a.hp / a.max_hp)

    def tick_status_effects(self, game):
        for effect in self.status_effects[:]:
            effect.tick(self, game)
            if effect.is_expired and effect in self.status_effects:
                self.status_effects.remove(effect)
        game.ui.update_npc_status_icons(self)

    def choose_random_target(self, possible_targets):
        alive_targets = [t for t in possible_targets if t.is_alive]
        if not alive_targets:
            return None
        return random.choice(alive_targets)

    def choose_target_with_most_hp(self, possible_targets):
        alive_targets = [t for t in possible_targets if t.is_alive]
        if not alive_targets:
            return None
        return max(alive_targets, key=lambda t: t.hp)

    def choose_fastest_target(self, possible_targets):
        alive_targets = [t for t in possible_targets if t.is_alive]
        if not alive_targets:
            return None
        return max(alive_targets, key=lambda t: t.speed)
