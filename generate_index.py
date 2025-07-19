import os

README_PATH = "README.md"

EXCLUDED_FOLDERS = {".git", ".github", "__pycache__"}

def is_valid_folder(folder):
    return (
        os.path.isdir(folder)
        and not folder.startswith(".")  # skip hidden folders
        and folder not in EXCLUDED_FOLDERS
    )

folders = [f for f in os.listdir() if is_valid_folder(f)]

lines = [
    "# MyNotes\n",
    "\nThis repository contains my personal notes, thoughts, and ideas.\n",
    "\nI use this space for note-taking, organizing information, and keeping track of things that interest me.\n",
    "\nFeel free to browse, but please remember these notes are primarily for my personal use and may not always be perfectly organized or complete.\n",
    "\n## You can browse my notes here:",
    "## 📁 Vault Index\n"
]

for folder in sorted(folders):
    folder_link = folder.replace(" ", "%20")
    lines.append(f"- [{folder}]({folder_link})\n")

with open(README_PATH, "w") as f:
    f.writelines(lines)

print(f"✅ Updated README.md with {len(folders)} folders.")
