import os
import re

# --- Configuration ---
VAULT_ROOT = '.'
EXCLUDED_DIRS = {'.git', '.github', '.obsidian', '.trash', '__pycache__'}
EXCLUDED_FILES = {'generate_index.py', 'LICENSE'}
MAIN_README_NAME = 'README.md'
# --- End Configuration ---


def prettify_title(filename):
    """Convert filename to a prettier title."""
    name = os.path.splitext(filename)[0]
    name = name.replace('_', ' ').replace('-', ' ')
    return re.sub(r'\s+', ' ', name).strip().title()


def generate_folder_index(folder_path, rel_path_from_root):
    """Generate a README.md for a specific folder."""
    index_path = os.path.join(folder_path, 'README.md')
    files = sorted(os.listdir(folder_path))

    backlink = os.path.relpath(os.path.join(VAULT_ROOT, MAIN_README_NAME), folder_path)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f'# Index of `{rel_path_from_root or "."}`\n\n')
        f.write(f'[<-- Back to Home]({backlink})\n\n')

        note_files = [f for f in files if f.endswith('.md') and f != 'README.md']
        if note_files:
            f.write('## Notes\n')
            for note in note_files:
                title = prettify_title(note)
                f.write(f'- [{title}]({note.replace(" ", "%20")})\n')
            f.write('\n')


def generate_main_index(all_folders):
    """Generate the main README.md in the vault root."""
    with open(MAIN_README_NAME, 'w', encoding='utf-8') as f:
        f.write('# My Obsidian Vault\n\n')
        f.write('This is an automatically generated index of my notes.\n\n')
        f.write('## Folders\n')

        for folder in sorted(all_folders):
            folder_display = prettify_title(os.path.basename(folder))
            folder_rel = os.path.relpath(folder, VAULT_ROOT)
            f.write(f'- [{folder_display}]({folder_rel.replace(" ", "%20")}/README.md)\n')

        f.write('\n## Root Notes\n')
        for item in sorted(os.listdir(VAULT_ROOT)):
            full_path = os.path.join(VAULT_ROOT, item)
            if (
                item.endswith('.md')
                and item not in {MAIN_README_NAME}
                and item not in EXCLUDED_FILES
                and os.path.isfile(full_path)
            ):
                title = prettify_title(item)
                f.write(f'- [{title}]({item.replace(" ", "%20")})\n')


def should_exclude(path):
    parts = path.split(os.sep)
    return any(part in EXCLUDED_DIRS for part in parts)


def main():
    all_folders = []

    for root, dirs, files in os.walk(VAULT_ROOT):
        if should_exclude(root):
            continue

        if root == VAULT_ROOT:
            continue  # Skip root here; we'll handle it separately

        rel_path = os.path.relpath(root, VAULT_ROOT)
        all_folders.append(root)
        generate_folder_index(root, rel_path)

    generate_main_index(all_folders)
    print("✅ All index files generated successfully.")


if __name__ == '__main__':
    main()
