from NPCs.hero import Hero
from NPCs.enemy import Enemy
from Abilities.damage_ability import DamageAbility
from Abilities.healing_ability import HealingAbility
from game_data_loader import GameDataLoader
from collections import Counter
import random


class Game:
    def __init__(self):
        loader = GameDataLoader()
        self.heroes = loader.load_heroes()
        self.dungeon = loader.load_dungeon_rooms()
        self.npcs_in_room = []
        self.npc_turn_order = []
        self.current_turn_index = 0
        self.turn_counter = 0
        self.turn_active = False
        self.current_room = self.choose_start_room()
        self.current_room.visited = True
        self.current_room.is_current = True
        self.current_room.visible = True
        self.current_room.reveal_neighbors()
        self.enemies = self.current_room.enemies.copy()
        if self.current_room.enemies:
            self.state = "combat"
        else:
            self.state = "exploration"
        self.exit_found = self.current_room.is_exit

    def execute_turn(self):
        if not self.turn_active:
            self.start_new_turn()
        while not self.is_turn_finished():
            npc = self.get_current_npc()
            if npc is None:
                break
            npc.make_action(self)
            self.end_current_npc_action()
            self.check_game_state()
            if self.state != "combat":
                return
        self.end_turn()

    def start_new_turn(self):
        self.turn_counter += 1
        self.npcs_in_room = []
        self.npcs_in_room.extend(self.heroes)
        self.npcs_in_room.extend(self.enemies)
        self.npc_turn_order = []
        self.npc_turn_order = sorted(
            [npc for npc in self.npcs_in_room if npc.is_alive],
            key=lambda npc: npc.speed,
            reverse=True,
        )
        self.current_turn_index = 0
        self.ui.update_console(f"--- Turn {self.turn_counter} ---", "hourglass.png")
        self.turn_active = True

    def execute_next_action(self):
        if not self.turn_active:
            self.start_new_turn()

        if self.is_turn_finished():
            self.end_turn()
            self.start_new_turn()

        npc = self.get_current_npc()

        if npc is None:
            self.end_turn()
            return
        npc.make_action(self)
        self.end_current_npc_action()
        self.check_game_state()

    def get_current_npc(self):
        while self.current_turn_index < len(self.npc_turn_order):
            npc = self.npc_turn_order[self.current_turn_index]
            if npc.is_alive:
                return npc
            self.current_turn_index += 1
        return None

    def end_current_npc_action(self):
        self.current_turn_index += 1

    def is_turn_finished(self):
        return self.current_turn_index >= len(self.npc_turn_order)

    def distribute_used_ability(self, ability, targets):
        for target in targets:
            target.recieve_used_ability(ability, self)

    def display_console_message(self, message, icon):
        self.ui.update_console(message, icon)

    def get_opponents(self, npc):
        if isinstance(npc, Hero):
            return [e for e in self.enemies if e.is_alive]
        else:
            return [h for h in self.heroes if h.is_alive]

    def get_allies(self, npc):
        if isinstance(npc, Hero):
            return [e for e in self.heroes if e.is_alive]
        else:
            return [h for h in self.enemies if h.is_alive]

    def tick_cooldowns(self):
        for npc in self.npcs_in_room:
            for ability in npc.abilities:
                ability.tick_cooldown()

    def reset_hero_cooldowns(self):
        for hero in self.heroes:
            for ability in hero.abilities:
                ability.reset_cooldown()

    def end_turn(self):
        self.tick_cooldowns()
        self.turn_active = False

    def choose_start_room(self):
        start_rooms = [room for room in self.dungeon.values() if room.is_start]
        if start_rooms:
            return random.choice(start_rooms)
        else:
            return random.choice(self.dungeon.values())

    def get_rooms_for_voting(self):
        available_rooms = []
        for room in self.dungeon.values():
            if room.visited:
                continue
            if any(neighbor.visited for neighbor in room.neighbors.values()):
                available_rooms.append(room)
        return available_rooms

    def move_to_next_room(self):
        possible_rooms = self.get_rooms_for_voting()

        if not possible_rooms:
            self.ui.update_console(
                "No available unvisited rooms to move to! Dungeon cleared.",
                "victory.png",
            )
            self.ui.show_game_over_ui()
            return

        next_room, chosen_exit = self.vote_for_next_room(possible_rooms)

        if chosen_exit:
            self.ui.update_console(
                "The heroes leave the dungeon.",
                "victory.png",
            )
            self.ui.show_game_over_ui()
            return

        self.current_room.is_current = False
        self.current_room = next_room
        self.current_room.is_current = True
        self.enemies = next_room.enemies
        next_room.visited = True
        next_room.reveal_neighbors()
        self.ui.update_console(
            f"Heroes moved to the next room ({next_room.x}, {next_room.y})",
            "footsteps.png",
        )
        if next_room.is_exit:
            self.ui.update_console(
                f"Heroes found an exit out of the dungeon!",
                "stairs.png",
            )
            self.exit_found = True
        self.check_game_state()

    def vote_for_next_room(self, candidate_rooms):
        exit_found = any(r.is_exit and r.visited for r in self.dungeon.values())
        if not candidate_rooms:
            return None, exit_found
        room_votes = []
        exit_votes = 0
        for hero in self.heroes:
            voted_room, voted_exit = hero.vote_for_next_room(
                candidate_rooms, exit_found
            )
            if voted_exit:
                self.ui.update_console(
                    f"{hero.name} voted for exit",
                    "vote.png",
                )
            elif voted_room:
                self.ui.update_console(
                    f"{hero.name} voted for room ({voted_room.x},{voted_room.y})",
                    "vote.png",
                )
            if voted_exit:
                exit_votes += 1
            elif voted_room:
                room_votes.append(voted_room)

        if room_votes:
            room_vote_counts = Counter(room_votes)
            max_votes = max(room_vote_counts.values())
            top_rooms = [
                room for room, count in room_vote_counts.items() if count == max_votes
            ]
            most_voted_room = random.choice(top_rooms)

        else:
            max_votes = 0
            most_voted_room = None

        if exit_votes > max_votes:
            self.ui.update_console(
                f"The voting has ended. The exit has been chosen!",
                "scales.png",
            )
            return None, True
        elif exit_votes < max_votes:
            self.ui.update_console(
                f"The voting has ended. Room ({most_voted_room.x},{most_voted_room.y}) has been chosen!",
                "scales.png",
            )
            return most_voted_room, False
        else:
            self.ui.update_console(
                f"The voting ended in a tie. The winner will be chosen randomly.",
                "coinflip.png",
            )
            return (
                (None, True)
                if random.choice([True, False])
                else (most_voted_room, False)
            )

    def check_game_state(self):
        if self.state == "exploration":
            if self.current_room.enemies:
                self.ui.update_console(
                    f"Battle started!",
                    "crossed_swords.png",
                )
                self.reset_hero_cooldowns()
                self.ui.show_combat_ui()
                self.state = "combat"
            else:
                self.ui.show_exploration_ui()
        elif self.state == "combat":
            if all(not e.is_alive for e in self.heroes):
                self.ui.update_console(
                    f"All heroes died... Game over!",
                    "reaper.png",
                )
                self.state = "over"
                self.ui.show_game_over_ui()
            if all(not e.is_alive for e in self.enemies):
                self.ui.update_console(
                    f"The heroes won the battle!",
                    "victory.png",
                )
                for hero in self.heroes:
                    hero.status_effects.clear()
                    hero.is_stunned = False
                    self.ui.update_npc_status_icons(hero)
                self.ui.show_exploration_ui()
                self.state = "exploration"
                self.turn_active = False
                self.turn_counter = 0
                self.current_turn_index = 0
