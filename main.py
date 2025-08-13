import requests
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

# ---- SIZE SETTINGS ----
ICON_SIZE = (28, 28)   # Type icon size (width, height)
LOGO_SIZE = (150, 90)  # Logo size (width, height)
SPRITE_SIZE = (96, 96) # Pokémon sprite size
# -----------------------

# ---- UI COLORS ----
BG_COLOR = "#f2f2f2"   # light gray background
FG_COLOR = "#111111"   # dark text
# -------------------

# Type icon mapping for all FireRed types
type_icons = {
    "normal": "normal.png",
    "fire": "fire.png",
    "water": "water.png",
    "grass": "grass.png",
    "electric": "electric.png",
    "ice": "ice.png",
    "fighting": "fighting.png",
    "poison": "poison.png",
    "ground": "ground.png",
    "flying": "flying.png",
    "psychic": "psychic.png",
    "bug": "bug.png",
    "rock": "rock.png",
    "ghost": "ghost.png",
    "dragon": "dragon.png",
    "dark": "dark.png",
    "steel": "steel.png",
}

# Load and resize image (return None if file is missing)
def load_image(path, size):
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

# Get FireRed Pokémon list
def get_firered_pokemon():
    version_url = "https://pokeapi.co/api/v2/version/firered"
    version_data = requests.get(version_url, timeout=10).json()
    version_group = version_data["version_group"]["name"]

    vg_url = f"https://pokeapi.co/api/v2/version-group/{version_group}"
    vg_data = requests.get(vg_url, timeout=10).json()

    pokemon_list = []
    for dex in vg_data["pokedexes"]:
        dex_data = requests.get(dex["url"], timeout=10).json()
        for entry in dex_data["pokemon_entries"]:
            pokemon_list.append(entry["pokemon_species"]["name"])
    return pokemon_list

firered_pokemon = get_firered_pokemon()

# Get Pokémon info and display
def get_pokemon_info():
    pokemon_name = entry.get().strip().lower()
    info_label.config(text="", image="", compound="none", fg=FG_COLOR, bg=BG_COLOR)
    for widget in types_frame.winfo_children():
        widget.destroy()

    try:
        if pokemon_name not in firered_pokemon:
            raise ValueError("Not in FireRed Pokédex — check the name please.")

        details_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        details_data = requests.get(details_url, timeout=10).json()

        # Load Pokémon sprite
        sprite_url = details_data["sprites"]["front_default"]
        sprite_img = None
        if sprite_url:
            resp = requests.get(sprite_url, timeout=10, stream=True)
            img = Image.open(resp.raw).resize(SPRITE_SIZE, Image.LANCZOS)
            sprite_img = ImageTk.PhotoImage(img)
            info_label.sprite_img = sprite_img  # GC protection

        # Get types and display icons
        for t in details_data["types"]:
            type_name = t["type"]["name"]
            icon_path = type_icons.get(type_name)
            if icon_path:
                icon_img = load_image(icon_path, ICON_SIZE)
                if icon_img:
                    lbl = tk.Label(
                        types_frame,
                        image=icon_img,
                        text=f" {type_name.capitalize()}",
                        compound="left",
                        bg=BG_COLOR,
                        fg=FG_COLOR
                    )
                    lbl.image = icon_img  # keep a reference to avoid GC
                else:
                    lbl = tk.Label(types_frame, text=type_name.capitalize(), bg=BG_COLOR, fg=FG_COLOR)
            else:
                lbl = tk.Label(types_frame, text=type_name.capitalize(), bg=BG_COLOR, fg=FG_COLOR)
            lbl.pack(anchor="w")

        # Get evolution info
        species_url = details_data["species"]["url"]
        species_data = requests.get(species_url, timeout=10).json()
        evo_chain_url = species_data["evolution_chain"]["url"]
        evo_chain_data = requests.get(evo_chain_url, timeout=10).json()

        def find_evolution(chain, target):
            if chain["species"]["name"] == target:
                return chain.get("evolves_to", [])
            for evo in chain["evolves_to"]:
                result = find_evolution(evo, target)
                if result is not None:
                    return result
            return None

        evolutions = find_evolution(evo_chain_data["chain"], pokemon_name)
        evo_text = ""
        if evolutions:
            for evo in evolutions:
                evo_name = evo["species"]["name"]
                evo_details = evo["evolution_details"][0] if evo["evolution_details"] else {}
                min_level = evo_details.get("min_level")
                trigger = (evo_details.get("trigger") or {}).get("name", "unknown")
                if min_level:
                    evo_text += f"\n→ Evolves into {evo_name.capitalize()} at level {min_level} ({trigger})"
                else:
                    evo_text += f"\n→ Evolves into {evo_name.capitalize()} via {trigger}"
        else:
            evo_text = "\n→ This Pokémon does not evolve further."

        # Show sprite and evolution info
        result_text = f"{pokemon_name.capitalize()}{evo_text}"
        info_label.config(text=result_text, image=sprite_img, compound="top", bg=BG_COLOR, fg=FG_COLOR)

    except ValueError as ve:
        info_label.config(text=f"❌ {ve}", bg=BG_COLOR, fg=FG_COLOR)
    except Exception as e:
        info_label.config(text=f"⚠️ Error: {e}", bg=BG_COLOR, fg=FG_COLOR)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Pokémon FireRed Info")
root.geometry("500x500")

# ---- BACKGROUND: PLAIN LIGHT GRAY ----
root.configure(bg=BG_COLOR)

# ----- TTK THEME & STYLE -----
style = ttk.Style()
try:
    style.theme_use("clam")
except tk.TclError:
    pass

# Make general ttk backgrounds light gray as well
for element in ("TFrame", "TLabel", "TButton", "TLabelframe"):
    style.configure(element, background=BG_COLOR)

style.configure(
    "Pokeball.TButton",
    font=("Verdana", 11, "bold"),
    padding=(14, 8),
    foreground="white",
    background="#E3350D",   # FireRed red
    borderwidth=0
)
style.map(
    "Pokeball.TButton",
    background=[("active", "#FF5A3C"), ("disabled", "#B9B9B9")],
    relief=[("pressed", "sunken"), ("!pressed", "flat")]
)

# Logo (show if available; otherwise use text fallback)
logo_img = load_image("pokemon_firered_logo.png", LOGO_SIZE)
if logo_img:
    logo_label = tk.Label(root, image=logo_img, bg=BG_COLOR)
    logo_label.pack(pady=10)
else:
    logo_label = tk.Label(
        root,
        text="Pokémon FireRed",
        font=("Verdana", 14, "bold"),
        bg=BG_COLOR,
        fg=FG_COLOR
    )
    logo_label.pack(pady=10)

# Input row (Entry + Button side by side)
search_row = ttk.Frame(root)
search_row.pack(pady=6)

entry = tk.Entry(search_row, width=28, font=("Verdana", 11))
entry.pack(side="left", ipady=6, padx=(0, 8))

# Pokeball icon (if available)
pokeball_img = load_image("pokeball.png", (20, 20))

btn = ttk.Button(
    search_row,
    text=(" Get Info" if pokeball_img else "🔎 Get Info"),
    image=(pokeball_img if pokeball_img else None),
    compound="left",
    style="Pokeball.TButton",
    command=get_pokemon_info
)
btn.image = pokeball_img  # keep a reference to avoid GC
btn.pack(side="left")

# Trigger search on Enter key
entry.bind("<Return>", lambda e: get_pokemon_info())

# Info label
info_label = tk.Label(root, text="", wraplength=480, justify="center", bg=BG_COLOR, fg=FG_COLOR)
info_label.pack(pady=10)

# Types section
types_frame = tk.Frame(root, bg=BG_COLOR)
types_frame.pack(pady=5)

root.mainloop()
