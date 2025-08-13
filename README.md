# 🔥 FireDex — Pokémon FireRed Info App

A Python Tkinter desktop application that displays **FireRed Pokédex** Pokémon data from **PokéAPI**,  
including **sprites**, **type icons**, and **evolution details** — all in a clean and responsive UI.

---

## ✨ Features

- 🔍 Search any **FireRed Pokédex** Pokémon by name  
- 🧩 Type icons with text labels (from local PNG assets)  
- 🧬 Evolution chain with level or trigger details  
- 🖼️ Graceful image handling (fallback to text if icons are missing)  
- 🎨 Clean light-gray UI background for smooth performance  

---

## 🛠️ Technologies Used

- Python 3.x  
- `tkinter` (built-in)  
- `requests` (HTTP requests to PokéAPI)  
- `Pillow` (image handling)  

---

## 📂 Project Structure

FireDex/
├─ main.py
├─ requirements.txt
├─ icons/
│ ├─ normal.png
│ ├─ fire.png
│ ├─ water.png
│ ├─ ... (all types)
├─ pokemon_firered_logo.png (optional)
├─ pokeball.png (optional)
└─ screenshots/
├─ charizard_info.png
├─ name_error.png
└─ empty_search.png


> Type icon filenames must match the lowercase type names:  
`normal, fire, water, grass, electric, ice, fighting, poison, ground, flying, psychic, bug, rock, ghost, dragon, dark, steel`

---

## ⚙️ Installation

1️⃣ Clone this repository:

git clone https://github.com/username/FireDex.git
cd FireDex

2️⃣ Install dependencies:
pip install -r requirements.txt

3️⃣ (Optional) Add logo and type icon PNGs to the project directory.

🚀 Usage
Run the app:
python main.py

1. Enter a Pokémon name (e.g., charmander)
2. Press Enter or click Get Info
3. View sprite, types, and evolution details

🖼️ Screenshots
✅ Pokémon Info Example (Charizard)

<img width="496" height="528" alt="image" src="https://github.com/user-attachments/assets/2583b8d3-15f3-463f-8503-53b17bc25cfb" />

❌ Not in FireRed Pokédex Example

<img width="497" height="530" alt="image" src="https://github.com/user-attachments/assets/0912ff37-7937-4104-9638-67d56037cfc0" />

⬜ Empty Search

<img width="497" height="529" alt="image" src="https://github.com/user-attachments/assets/47c0f97b-beac-4631-a794-a44efea85e2e" />

📚 Notes
Pokémon must exist in the FireRed Pokédex; otherwise, an error message appears.

Missing icons are replaced with plain text type labels.

Internet connection is required for PokéAPI requests and sprite loading.

📄 License
This project is for educational purposes.
Feel free to modify or expand — just give proper credit.

📦 requirements.txt
requests>=2.32.0
Pillow>=10.3.0



