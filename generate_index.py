import os

# Config
VAULT_ROOT = '.'
MAIN_README_NAME = 'README.md'
EXCLUDED_DIRS = {'.git', '.github', '.obsidian', '.trash', '__pycache__'}
FOLDER_INDEX_HEADING = '## You can browse my notes here:'


def should_exclude(path):
    parts = path.split(os.sep)
    return any(part in EXCLUDED_DIRS for part in parts)


def get_folder_links():
    folder_links = []
    for root, dirs, files in os.walk(VAULT_ROOT):
        if should_exclude(root):
            continue
        if root == VAULT_ROOT:
            continue  # skip root itself

        rel_path = os.path.relpath(root, VAULT_ROOT)
        name = os.path.basename(rel_path)
        folder_links.append((name, rel_path))
    return sorted(folder_links)


def update_main_readme(folder_links):
    existing_lines = []

    if os.path.exists(MAIN_README_NAME):
        with open(MAIN_README_NAME, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            found = False
            for line in lines:
                if line.strip() == FOLDER_INDEX_HEADING.strip():
                    found = True
                    break
                existing_lines.append(line)
            if not found:
                existing_lines.append('\n' + FOLDER_INDEX_HEADING + '\n')

    else:
        existing_lines = ['# MyNotes\n\n', FOLDER_INDEX_HEADING + '\n']

    # Now add the folder links
    existing_lines.append('\n')
    for name, rel in folder_links:
        existing_lines.append(f'- [{name}]({rel.replace(" ", "%20")}/README.md)\n')

    with open(MAIN_README_NAME, 'w', encoding='utf-8') as f:
        f.writelines(existing_lines)


if __name__ == '__main__':
    folder_links = get_folder_links()
    update_main_readme(folder_links)
    print(f"✅ Updated README.md with {len(folder_links)} folders.")
