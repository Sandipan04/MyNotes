import os

MAIN_README_NAME = "README.md"
VAULT_ROOT = "."

def should_exclude(path):
    name = os.path.basename(path)
    return name.startswith(".") or name in {".git", "__pycache__"}

def get_folder_links():
    folder_links = []
    for root, dirs, files in os.walk(VAULT_ROOT):
        if should_exclude(root):
            continue
        if root == VAULT_ROOT:
            continue
        rel_path = os.path.relpath(root, VAULT_ROOT)
        name = os.path.basename(rel_path)
        print(f"Found folder: {rel_path}")
        folder_links.append((name, rel_path))
    return sorted(folder_links)

def generate_index_markdown(links):
    lines = ["## 📁 Vault Index\n\n"]
    for name, path in links:
        encoded_path = path.replace(" ", "%20")
        lines.append(f"- [{name}]({encoded_path})\n")
    lines.append("\n")
    return lines

def update_main_readme():
    links = get_folder_links()
    new_index = generate_index_markdown(links)

    if not os.path.exists(MAIN_README_NAME):
        print("No README.md found. Creating new one.")
        with open(MAIN_README_NAME, "w", encoding="utf-8") as f:
            f.writelines(new_index)
        return

    with open(MAIN_README_NAME, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start = None
    end = None
    for i, line in enumerate(lines):
        if "## 📁 Vault Index" in line:
            start = i
            end = i
            while end < len(lines) and (lines[end].startswith("- ") or lines[end].strip() == ""):
                end += 1
            break

    if start is not None:
        print("Replacing existing index in README.md")
        lines = lines[:start] + new_index + lines[end:]
    else:
        print("No existing index found. Appending new one.")
        lines += ["\n"] + new_index

    with open(MAIN_README_NAME, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("✅ Final README.md content preview:")
    print("".join(lines))

update_main_readme()
