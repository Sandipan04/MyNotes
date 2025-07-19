name: Generate Vault Index

# This action runs on every push to the main/master branch
on:
  push:
    branches:
      - main # Or 'master', depending on your repo's default branch

jobs:
  build-and-commit:
    runs-on: ubuntu-latest
    steps:
      # 1. Check out the repository code
      - name: Checkout Repo
        uses: actions/checkout@v4

      # 2. Set up Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # 3. Run the index generation script
      - name: Generate Index Files
        run: python generate_index.py

      # 4. Commit the new/updated README files back to the repo
      - name: Commit Files
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: auto-generate vault index"
          # The pattern of files to look for changes in
          file_pattern: "**/*.md"
          commit_user_name: "GitHub Actions Bot"
          commit_user_email: "actions@github.com"
          commit_author: "GitHub Actions Bot <actions@github.com>"
          