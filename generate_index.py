import os
import re

# --- Configuration ---
VAULT_ROOT = '.'
MAIN_README_NAME = 'README.md'
EXCLUDED_DIRS = {'.git', '.github', '.obsidian', '.trash', '__pycache__'}
EXCLUDED_FILES = {'generate_index.py', 'LICENSE'}
FOLDER_INDEX_HEADING = '## You can browse my notes here:'
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


def update_main_readme(folder_links):
    """Updates the main README.md file by preserving content above the heading."""
    existing_content = ''
    if os.path.exists(MAIN_README_NAME):
        with open(MAIN_README_NAME, 'r', encoding='utf-8') as f:
            content = f.read()
            parts = content.split(FOLDER_INDEX_HEADING)
            existing_content = parts[0].rstrip() + '\n\n' if parts else content

    with open(MAIN_README_NAME, 'w', encoding='utf-8') as f:
        f.write(existing_content)
        f.write(f'{FOLDER_INDEX_HEADING}\n\n')
        for folder_display, folder_rel in folder_links:
            f.write(f'- [{folder_display}]({folder_rel.replace(" ", "%20")}/README.md)\n')


def should_exclude(path):
    parts = path.split(os.sep)
    return any(part in EXCLUDED_DIRS for part in parts)


def main():
    all_folder_links = []

    for root, dirs, files in os.walk(VAULT_ROOT):
        if should_exclude(root):
            continue
        if root == VAULT_ROOT:
            continue

        rel_path = os.path.relpath(root, VAULT_ROOT)
        generate_folder_index(root, rel_path)
        folder_display = prettify_title(os.path.basename(root))
        all_folder_links.append((folder_display, rel_path))

    update_main_readme(sorted(all_folder_links))
    print("✅ All index files generated successfully.")


if __name__ == '__main__':
    main()
