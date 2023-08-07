import glob
import os
import shutil
import frontmatter

for file in glob.glob("*.md"):
    parts = file[:-3].split("-")
    year, month, day = parts[:3]
    slug = '-'.join(parts[3:])

    data = frontmatter.load(file)
    title = data['title'].replace(":", " ").replace("?", " ")
    title = title.strip()

    folder = os.path.join("..", f"{year}{month}{day}_{title}")
    os.makedirs(folder, exist_ok=True)
    os.makedirs(os.path.join(folder, "images"), exist_ok=True)
    os.replace(file, os.path.join(folder, "index.md"))