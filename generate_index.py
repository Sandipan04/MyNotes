import os
import urllib.parse
from pathlib import Path

EXCLUDED_DIRS = ['.git', '.obsidian', '.trash', '.github']
EXCLUDED_FILES = ['README.md', '.DS_Store']

def generate_readme(path, root_path):
    path = Path(path)
    items = os.listdir(path)
    folders = []
    files = []
    
    # Collect items
    for item in items:
        item_path = path / item
        if any(excl in str(item_path) for excl in EXCLUDED_DIRS):
            continue
            
        if item in EXCLUDED_FILES:
            continue
            
        if item_path.is_dir():
            folders.append(item)
            generate_readme(item_path, root_path)  # Recurse into subfolder
        elif item_path.suffix == '.md':
            files.append(item)

    # Sort alphabetically
    folders.sort()
    files.sort()
    
    # Calculate relative path to root
    rel_to_root = os.path.relpath(root_path, path)
    
    # Generate README content
    content = []
    
    # Header
    if path == root_path:
        content.append("# MyNotes\n\nThis repository contains my personal notes, thoughts, and ideas.\n\nI use this space for note-taking, organizing information, and keeping track of things that interest me.\n\nFeel free to browse, but please remember these notes are primarily for my personal use and may not always be perfectly organized or complete.")
        content.append("Click folders to explore notes\n\n")

    else:
        content.append(f"# {path.name}\n\n")
        content.append(f"Go to: [Home]({rel_to_root}/README.md)\n\n")
    
    # Parent folder link (if not root and not top-level)
    if path != root_path and path.parent != root_path:
        parent_rel = os.path.relpath(root_path, path.parent) if path.parent != root_path else "."
        content.append(f"Go back: [{path.parent.name}]({parent_rel}/README.md)\n\n")
    
    # Subfolders section
    if folders:
        content.append("## Folders\n")
        for folder in folders:
            folder_enc = urllib.parse.quote(folder)
            content.append(f"- [{folder}]({folder_enc}/README.md)\n")
        content.append("\n")
    
    # Files section
    if files:
        content.append("## Files\n")
        for file in files:
            file_name = os.path.splitext(file)[0]
            file_enc = urllib.parse.quote(file)
            content.append(f"- [{file_name}]({file_enc})\n")
        content.append("\n")
    
    # Subfolder listings
    # if folders:
    #     content.append("## Subfolder Contents\n")
    #     for folder in folders:
    #         folder_path = path / folder
    #         if any(os.scandir(folder_path)):
    #             content.append(f"### {folder}\n")
    #             content.append(f"[View all notes in {folder}]({urllib.parse.quote(folder)}/README.md)\n\n")
    
    # Write to file
    with open(path / "README.md", "w", encoding="utf-8") as f:
        f.write("".join(content))

if __name__ == "__main__":
    root_path = Path(os.getcwd())
    generate_readme(root_path, root_path)
