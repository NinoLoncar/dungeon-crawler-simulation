import csv
from NPCs.hero import Hero
from NPCs.enemy import Enemy
from Abilities.damage_ability import DamageAbility
from Abilities.healing_ability import HealingAbility
from Abilities.status_abillity import StatusAbility
from Abilities.damage_status_effect import DamageStatusEffect
from Abilities.attribute_status_effect import AttributeStatusEffect
from Abilities.stunned_status_effect import StunnedStatusEffect
from NPCs.fighting_styles import FightingStyle
from NPCs.voting_styles import VotingStyle
from Dungeon.dungeon_room import DungeonRoom

DUNGEON_ROOMS_FILE = "./Data/dungeon_rooms.csv"

HEROES_FILE = "./Data/heroes.csv"
ENEMIES_FILE = "./Data/enemies.csv"
ENEMY_GROUPS_FILE = "./Data/enemy_groups.csv"

ATTRIBUTE_STATUS_EFFECTS_FILE = "./Data/attribute_status_effects.csv"
DAMAGE_STATUS_EFFECTS_FILE = "./Data/damage_status_effects.csv"
STUNNED_STATUS_EFFECTS_FILE = "./Data/stunned_status_effects.csv"

HERO_DAMAGE_ABILITIES_FILE = "./Data/hero_damage_abilities.csv"
HERO_HEALING_ABILITIES_FILE = "./Data/hero_healing_abilities.csv"
HERO_STATUS_ABILITIES_FILE = "./Data/hero_status_abilities.csv"

ENEMY_HEALING_ABILITIES_FILE = "./Data/enemy_healing_abilities.csv"
ENEMY_DAMAGE_ABILITIES_FILE = "./Data/enemy_damage_abilities.csv"
ENEMY_STATUS_ABILITIES_FILE = "./Data/enemy_status_abilities.csv"


class GameDataLoader:
    def __init__(self):
        self.status_effects = {}
        self.load_attribute_status_effects()
        self.load_damage_status_effects()
        self.load_stunned_status_effects()
        self.enemy_types = self.load_enemy_types()
        self.enemy_groups = self.load_enemy_groups()

    def load_heroes(self):
        heroes = {}
        with open(HEROES_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                figthing_style_str = row.get("fighting_style", "CHAOTIC").upper()
                try:
                    figthing_style = FightingStyle[figthing_style_str]
                except KeyError:
                    figthing_style = FightingStyle.CHAOTIC

                voting_style_str = row.get("voting_style", "CURIOUS").upper()
                try:
                    voting_sytle = VotingStyle[voting_style_str]
                except KeyError:
                    voting_sytle = VotingStyle.CURIOUS

                hero_id = row["id"]
                hero = Hero(
                    name=row["name"],
                    max_hp=int(row["max_hp"]),
                    speed=int(row["speed"]),
                    icon=row["icon"],
                    fighting_style=figthing_style,
                    voting_style=voting_sytle,
                )
                heroes[hero_id] = hero
        self.load_damage_abilities(heroes, HERO_DAMAGE_ABILITIES_FILE)
        self.load_healing_abilities(heroes, HERO_HEALING_ABILITIES_FILE)
        self.load_status_abilities(heroes, HERO_STATUS_ABILITIES_FILE)
        return list(heroes.values())

    def load_damage_abilities(self, npcs, file_name):
        with open(file_name, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                npc_id = row["npc"]
                if npc_id in npcs:
                    ability = DamageAbility(
                        name=row["name"],
                        cooldown_duration=int(row["cooldown_duration"]),
                        min_dmg=int(row["min_dmg"]),
                        max_dmg=int(row["max_dmg"]),
                        aoe=row["aoe"].lower() == "true",
                        priority=int(row["priority"]),
                        icon=row["icon"],
                        source=npcs[npc_id],
                    )
                    npcs[npc_id].abilities.append(ability)

    def load_healing_abilities(self, npcs, file):
        with open(file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                npc_id = row["npc"]
                if npc_id in npcs:
                    ability = HealingAbility(
                        name=row["name"],
                        cooldown_duration=int(row["cooldown_duration"]),
                        min_hp=int(row["min_hp"]),
                        max_hp=int(row["max_hp"]),
                        aoe=row["aoe"].lower() == "true",
                        priority=int(row["priority"]),
                        icon=row["icon"],
                        source=npcs[npc_id],
                    )
                    npcs[npc_id].abilities.append(ability)

    def load_attribute_status_effects(self):
        with open(ATTRIBUTE_STATUS_EFFECTS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = AttributeStatusEffect(
                    name=row["name"],
                    duration=int(row["duration"]),
                    amount=int(row["amount"]),
                    attribute=row["attribute"],
                    source=None,
                    icon=row.get("icon"),
                )
                self.status_effects[status.name] = status

    def load_damage_status_effects(self):
        with open(DAMAGE_STATUS_EFFECTS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = DamageStatusEffect(
                    name=row["name"],
                    duration=int(row["duration"]),
                    min_dmg=int(row["min_dmg"]),
                    max_dmg=int(row["max_dmg"]),
                    source=None,
                    icon=row.get("icon"),
                )
                self.status_effects[status.name] = status

    def load_stunned_status_effects(self):
        with open(STUNNED_STATUS_EFFECTS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = StunnedStatusEffect(
                    name=row["name"],
                    duration=int(row["duration"]),
                    source=None,
                    icon=row.get("icon"),
                )
                self.status_effects[status.name] = status

    def load_status_abilities(self, npcs, file):
        with open(file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                npc_id = row["npc"]
                if npc_id not in npcs:
                    continue
                npc = npcs[npc_id]
                status_name = row["status_effect"]
                if status_name not in self.status_effects:
                    continue
                status_effect = self.status_effects[status_name].clone(npc)

                ability = StatusAbility(
                    name=row["name"],
                    cooldown_duration=int(row["cooldown_duration"]),
                    status_effect=status_effect,
                    aoe=row["aoe"].lower() == "true",
                    friendly_targets=row["friendly_targets"].lower() == "true",
                    priority=int(row["priority"]),
                    source=npc,
                    icon=row.get("icon"),
                )
                npc.abilities.append(ability)

    def load_enemy_types(self):
        enemies = {}
        with open(ENEMIES_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                figthing_style_str = row.get("fighting_style", "CHAOTIC").upper()
                try:
                    figthing_style = FightingStyle[figthing_style_str]
                except KeyError:
                    figthing_style = FightingStyle.CHAOTIC
                enemy = Enemy(
                    type=row["type"],
                    max_hp=int(row["max_hp"]),
                    speed=int(row["speed"]),
                    icon=row["icon"],
                    fighting_style=figthing_style,
                )
                enemies[enemy.type] = enemy
        self.load_damage_abilities(enemies, ENEMY_DAMAGE_ABILITIES_FILE)
        self.load_status_abilities(enemies, ENEMY_STATUS_ABILITIES_FILE)
        return enemies

    def load_enemy_groups(self):
        groups = {}
        with open(ENEMY_GROUPS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                group_id = row["group_id"]
                enemy_type = row["enemy_type"]
                count = int(row["count"])

                if group_id not in groups:
                    groups[group_id] = []

                groups[group_id].append({"enemy_type": enemy_type, "count": count})
        return groups

    def create_enemy_group(self, group_id, groups, enemy_templates):
        enemies = []
        if group_id not in groups or not groups[group_id]:
            return []
        for entry in groups[group_id]:
            enemy_type = entry["enemy_type"]
            count = entry["count"]
            template = enemy_templates[enemy_type]
            for i in range(1, count + 1):
                enemy = template.clone()
                if count > 1:
                    enemy.name = f"{enemy_type} {i}"
                enemies.append(enemy)
        return enemies

    def load_dungeon_rooms(self):
        rooms = {}

        with open(DUNGEON_ROOMS_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                x = int(row["x"])
                y = int(row["y"])
                rooms[(x, y)] = DungeonRoom(
                    x=x,
                    y=y,
                    is_start=row["is_start"].lower() == "true",
                    is_exit=row["is_exit"].lower() == "true",
                )
                enemy_group_name = row.get("enemy_group", "").strip()
                if enemy_group_name:
                    room = rooms[(x, y)]
                    room.enemies = self.create_enemy_group(
                        enemy_group_name, self.enemy_groups, self.enemy_types
                    )
        direction_offsets = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
        }
        with open(DUNGEON_ROOMS_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                x = int(row["x"])
                y = int(row["y"])
                connections = row["connections"].strip().upper()
                room = rooms[(x, y)]
                for direction in connections:
                    dx, dy = direction_offsets[direction]
                    neighbor_coords = (x + dx, y + dy)
                    if neighbor_coords in rooms:
                        neighbor = rooms[neighbor_coords]
                        room.connect(neighbor, direction)
        return rooms
