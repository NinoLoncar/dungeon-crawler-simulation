import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from NPCs.hero import Hero
from NPCs.enemy import Enemy

HEADING1_FONT_SIZE = 20
TEXT_FONT_SIZE = 16
CONSOLE_FONT_SIZE = 12
CONSOLE_IMAGE_SIZE = 45
FONT = "Verdana"

MAP_TILE_SIZE = 40
ICON_SIZE = 75

WINDOW_BG_COLOR = "#bdbbb7"
CONSOLE_BG_COLOR = "#c8c985"
NPC_GROUP_BG_COLOR = "#ffffff"

SMALL_PADDING = 5
MEDIUM_PADDING = 20

import tkinter as tk
from PIL import Image, ImageTk


class GameUi:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Game")
        self.root.config(bg=WINDOW_BG_COLOR)

        self.hero_ui = {}
        self.enemy_ui = {}
        self.console_icons = []

        self.create_ui()
        if game.state == "exploration":
            self.show_exploration_ui()
        elif game.state == "combat":
            self.show_combat_ui()

    def create_ui(self):
        self.create_heroes_ui()
        self.create_enemies_ui()
        self.create_console()
        self.draw_dungeon_map()
        self.create_buttons()

    def create_buttons(self):
        self.buttons_frame = tk.Frame(self.root, bg=WINDOW_BG_COLOR)
        self.buttons_frame.pack(side=tk.BOTTOM, pady=SMALL_PADDING)

        self.execute_turn_button = tk.Button(
            self.buttons_frame, text="Execute turn", command=self.game.execute_turn
        )
        self.execute_turn_button.pack(side=tk.LEFT, pady=SMALL_PADDING)

        self.execute_next_action_button = tk.Button(
            self.buttons_frame,
            text="Execute next action",
            command=self.game.execute_next_action,
        )
        self.execute_next_action_button.pack(side=tk.LEFT, pady=SMALL_PADDING)

        self.change_room_button = tk.Button(
            self.buttons_frame,
            text="Choose next room",
            command=self.game.move_to_next_room,
        )
        self.change_room_button.pack(side=tk.LEFT, pady=SMALL_PADDING)

        self.clear_console_button = tk.Button(
            self.buttons_frame,
            text="Clear console",
            command=self.clear_console,
        )
        self.clear_console_button.pack(side=tk.LEFT, pady=SMALL_PADDING)

        self.exit_button = tk.Button(
            self.buttons_frame,
            text="Exit",
            command=self.root.destroy,
        )
        self.exit_button.pack(side=tk.LEFT, pady=SMALL_PADDING)

    def create_heroes_ui(self):
        frame = tk.Frame(self.root, bg=NPC_GROUP_BG_COLOR)
        frame.pack(side=tk.LEFT, padx=MEDIUM_PADDING, pady=MEDIUM_PADDING)

        tk.Label(
            frame, text="Heroes", font=(FONT, HEADING1_FONT_SIZE), bg=NPC_GROUP_BG_COLOR
        ).pack()

        for hero in self.game.heroes:
            self.create_npc_ui(frame, hero, self.hero_ui, side=tk.LEFT)

    def create_enemies_ui(self):
        self.enemy_frame = tk.Frame(self.root, bg=NPC_GROUP_BG_COLOR)
        self.enemy_frame.pack(side=tk.RIGHT, padx=MEDIUM_PADDING, pady=MEDIUM_PADDING)

        tk.Label(
            self.enemy_frame,
            text="Enemies",
            font=(FONT, HEADING1_FONT_SIZE),
            bg=NPC_GROUP_BG_COLOR,
        ).pack()

        for enemy in self.game.enemies:
            self.create_npc_ui(self.enemy_frame, enemy, self.enemy_ui, side=tk.RIGHT)

    def create_npc_ui(self, parent, npc, storage, side):
        npc_frame = tk.Frame(parent, bg=NPC_GROUP_BG_COLOR)
        npc_frame.pack(anchor="w", pady=SMALL_PADDING)

        icon_image = self._load_icon(npc.icon, ICON_SIZE)
        icon_label = tk.Label(npc_frame, image=icon_image, bg=NPC_GROUP_BG_COLOR)
        icon_label.image = icon_image
        icon_label.pack(side=side)

        info_frame = tk.Frame(npc_frame, bg=NPC_GROUP_BG_COLOR)
        info_frame.pack(side=side, padx=SMALL_PADDING)

        hp_label = tk.Label(
            info_frame,
            text=self._format_hp(npc),
            font=(FONT, TEXT_FONT_SIZE),
            bg=NPC_GROUP_BG_COLOR,
        )
        hp_label.pack(anchor="w")

        status_frame = tk.Frame(info_frame, bg=NPC_GROUP_BG_COLOR)
        status_frame.pack(anchor="w", pady=SMALL_PADDING)

        storage[npc] = {
            "frame": npc_frame,
            "icon": icon_label,
            "hp": hp_label,
            "icon_image": icon_image,
            "status_frame": status_frame,
            "status_icons": [],
        }

    def update_npc_ui(self, npc):
        ui = self.hero_ui.get(npc) or self.enemy_ui.get(npc)
        if not ui:
            return
        ui["hp"].config(text=self._format_hp(npc))

        if not npc.is_alive:
            self._set_dead_icon(ui)

    def update_npcs_ui(self):
        for npc in self.game.heroes + self.game.enemies:
            self.update_npc_ui(npc)

    def _load_icon(self, icon_name, size):
        try:
            img = Image.open(f"Images/{icon_name}")
            img = img.resize((size, size))
            return ImageTk.PhotoImage(img)
        except Exception:
            return ImageTk.PhotoImage(Image.new("RGBA", (size, size)))

    def _set_dead_icon(self, ui):
        dead_icon = self._load_icon("skull.png", ICON_SIZE)
        ui["icon"].config(image=dead_icon)
        ui["icon"].image = dead_icon

    def clear_console(self):
        self.console_text.delete("1.0", tk.END)
        self.console_icons.clear()

    def _format_hp(self, npc):
        hp = max(0, npc.hp)
        return f"{npc.name}\n{hp}/{npc.max_hp} HP"

    def create_console(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.BOTTOM, padx=MEDIUM_PADDING, pady=MEDIUM_PADDING)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.console_text = tk.Text(
            frame,
            height=10,
            width=60,
            font=(FONT, CONSOLE_FONT_SIZE),
            bg=CONSOLE_BG_COLOR,
        )
        self.console_text.pack()

        self.console_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.console_text.yview)

    def update_console(self, text, icon=None):
        if icon:
            icon_image = self._load_icon(icon, CONSOLE_IMAGE_SIZE)
            self.console_icons.append(icon_image)

            label = tk.Label(self.console_text, image=icon_image)
            label.image = icon_image
            self.console_text.window_create(tk.END, window=label)

        self.console_text.insert(tk.END, text + "\n")
        self.console_text.see(tk.END)

    def update_npc_status_icons(self, npc):
        ui = self.hero_ui.get(npc) or self.enemy_ui.get(npc)
        if not ui:
            return
        for lbl in ui["status_icons"]:
            lbl.destroy()
        ui["status_icons"].clear()

        for status in npc.status_effects:
            img = self._load_icon(status.icon, 24)
            lbl = tk.Label(ui["status_frame"], image=img, bg=NPC_GROUP_BG_COLOR)
            lbl.image = img
            lbl.pack(side=tk.LEFT, padx=1)
            ui["status_icons"].append(lbl)

    def draw_dungeon_map(self):
        if not self.game.dungeon:
            return

        max_x = max(room.x for room in self.game.dungeon.values())
        max_y = max(room.y for room in self.game.dungeon.values())
        min_x = min(room.x for room in self.game.dungeon.values())
        min_y = min(room.y for room in self.game.dungeon.values())

        width = (max_x - min_x + 1) * MAP_TILE_SIZE
        height = (max_y - min_y + 1) * MAP_TILE_SIZE

        if hasattr(self, "map_canvas"):
            self.map_canvas.destroy()

        self.map_canvas = tk.Canvas(self.root, width=width, height=height, bg="black")
        self.map_canvas.pack(padx=MEDIUM_PADDING, pady=MEDIUM_PADDING)

        self.map_icons = {}
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                room = self.game.dungeon.get((x, y), None)
                if room:
                    icon_name = room.get_icon()
                else:
                    icon_name = "undiscovered.png"

                img = self._load_icon(icon_name, MAP_TILE_SIZE)
                self.map_icons[(x, y)] = img

                canvas_x = (x - min_x) * MAP_TILE_SIZE
                canvas_y = (y - min_y) * MAP_TILE_SIZE

                self.map_canvas.create_image(
                    canvas_x + MAP_TILE_SIZE // 2,
                    canvas_y + MAP_TILE_SIZE // 2,
                    image=img,
                )

    def show_exploration_ui(self):
        for enemy, ui in self.enemy_ui.items():
            ui["frame"].pack_forget()
        self.execute_turn_button.config(state=tk.DISABLED)
        self.execute_next_action_button.config(state=tk.DISABLED)
        self.change_room_button.config(state=tk.NORMAL)
        self.draw_dungeon_map()

    def show_combat_ui(self):
        for enemy in self.game.enemies:
            if enemy not in self.enemy_ui:
                self.create_npc_ui(
                    self.enemy_frame, enemy, self.enemy_ui, side=tk.RIGHT
                )
            else:
                self.update_npc_ui(enemy)

        self.execute_turn_button.config(state=tk.NORMAL)
        self.execute_next_action_button.config(state=tk.NORMAL)

        self.change_room_button.config(state=tk.DISABLED)
        self.draw_dungeon_map()

    def show_game_over_ui(self):
        self.execute_turn_button.config(state=tk.DISABLED)
        self.execute_next_action_button.config(state=tk.DISABLED)
        self.change_room_button.config(state=tk.DISABLED)
