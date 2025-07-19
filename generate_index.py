import os
import urllib.parse

VAULT_ROOT = os.getcwd()
EXCLUDED_DIRS = ['.git', '.obsidian', '.trash', '.github']

def generate_readme(path, is_root=False):
    items = os.listdir(path)
    folders = []
    files = []

    for item in items:
        full_path = os.path.join(path, item)
        if any(excl in full_path for excl in EXCLUDED_DIRS):
            continue
            
        if os.path.isdir(full_path):
            folders.append(item)
            generate_readme(full_path)
        elif item.endswith('.md') and item != 'README.md':
            files.append(item)

    with open(os.path.join(path, 'README.md'), 'w', encoding='utf-8') as f:
        if is_root:
            f.write("# My Obsidian Vault\n\n")
            f.write("Click folders to view notes\n\n## Folders\n")
            folders.sort()
            for folder in folders:
                encoded = urllib.parse.quote(folder)
                f.write(f"- [{folder}]({encoded}/README.md)\n")
        else:
            folder_name = os.path.basename(path)
            f.write(f"# {folder_name}\n\n")
            f.write(f"Go to: [Home]({get_home_link(path)})\n\n## Files\n")
            files.sort()
            for file in files:
                display_name = file.replace('.md', '')
                encoded = urllib.parse.quote(file)
                f.write(f"- [{display_name}]({encoded})\n")

def get_home_link(current_path):
    rel_path = os.path.relpath(VAULT_ROOT, current_path)
    return urllib.parse.quote(os.path.join(rel_path, 'README.md').replace('\\', '/'))

if __name__ == '__main__':
    generate_readme(VAULT_ROOT, is_root=True)
