import os

# --- Configuration ---
VAULT_ROOT = '.'  # Use '.' for the current directory
MAIN_README_NAME = 'README.md'
EXCLUDED_DIRS = ['.obsidian', '.git', '.github']
EXCLUDED_FILES = ['generate_index.py', 'LICENSE']
# --- End Configuration ---

def generate_folder_index(folder_path, folder_name):
    """Generates a README.md for a specific folder."""
    index_path = os.path.join(folder_path, 'README.md')
    files_and_dirs = sorted(os.listdir(folder_path))
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f'# Index of {folder_name}\n\n')
        f.write('[<-- Back to Home](../README.md)\n\n')
        
        f.write('## Notes\n')
        # List markdown files
        for item in files_and_dirs:
            if item.endswith('.md') and item != 'README.md':
                # Create a link with the .md extension removed for cleaner text
                note_name = os.path.splitext(item)[0]
                f.write(f'- [{note_name}]({item.replace(" ", "%20")})\n')
                
        f.write('\n')

def generate_main_index():
    """Generates the main README.md for the vault root."""
    all_items = sorted(os.listdir(VAULT_ROOT))
    
    with open(MAIN_README_NAME, 'w', encoding='utf-8') as f:
        f.write('# My Obsidian Vault\n\n')
        f.write('This is an automatically generated index of my notes.\n\n')
        
        f.write('## Folders\n')
        # List directories
        for item in all_items:
            path = os.path.join(VAULT_ROOT, item)
            if os.path.isdir(path) and item not in EXCLUDED_DIRS:
                f.write(f'- [{item}](./{item.replace(" ", "%20")}/README.md)\n')
                generate_folder_index(path, item) # Generate index for the subfolder
                
        f.write('\n## Root Notes\n')
        # List markdown files in the root
        for item in all_items:
            if item.endswith('.md') and item != MAIN_README_NAME and item not in EXCLUDED_FILES:
                note_name = os.path.splitext(item)[0]
                f.write(f'- [{note_name}]({item.replace(" ", "%20")})\n')

if __name__ == '__main__':
    generate_main_index()
    print("✅ All index files generated successfully.")

