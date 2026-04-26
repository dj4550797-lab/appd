import os
import re

# Configuration
REPLACEMENTS = {
    "dreamxbotz": "Flixora",
    "dreamx": "Flixora",
    "Dreamx": "Flixora",
    "DREAMX": "FLIXORA",
    "dreamcinezone": "Flixora",
    "Dreamcinezone": "Flixora",
    "DREAMCINEZONE": "FLIXORA",
    "Techno Krrish": "Flixora",
    "Flixoar": "Flixora",
    "t.me/dreamxbotz": "t.me/flixoraoffiacial",
    "t.me/dreamx": "t.me/flixoraoffiacial",
    "t.me/dream": "t.me/flixoraoffiacial",
}

# File extensions to process
TEXT_EXTENSIONS = {'.py', '.md', '.txt', '.html', '.json', '.yml', '.yaml', '.conf', '.sh', '.css', '.js', '.xml'}
FILE_NAMES = {'Dockerfile', 'Procfile', 'app.json', 'heroku.yml', 'docker-compose.yml'}

def is_text_file(filename):
    if filename in FILE_NAMES:
        return True
    _, ext = os.path.splitext(filename)
    return ext in TEXT_EXTENSIONS

def replace_in_content(content):
    # Sort keys by length descending to avoid partial replacements
    sorted_keys = sorted(REPLACEMENTS.keys(), key=len, reverse=True)
    
    for old in sorted_keys:
        new = REPLACEMENTS[old]
        content = content.replace(old, new)
    
    # Final cleanup for any missed case variations
    content = re.sub(r'dreamxbotz', 'Flixora', content, flags=re.IGNORECASE)
    content = re.sub(r'dreamx', 'Flixora', content, flags=re.IGNORECASE)
    content = re.sub(r'dreamcinezone', 'Flixora', content, flags=re.IGNORECASE)
    content = re.sub(r'Techno Krrish', 'Flixora', content, flags=re.IGNORECASE)
    content = re.sub(r'Flixoar', 'Flixora', content, flags=re.IGNORECASE)
    
    return content

def rebrand(root_dir):
    print(f"Starting thorough rebranding in {root_dir}...")
    
    # 1. Process file contents
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for file in files:
            if file == 'rebrand.py':
                continue
                
            file_path = os.path.join(root, file)
            
            if is_text_file(file):
                try:
                    content = None
                    for encoding in ['utf-8', 'latin-1']:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                content = f.read()
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if content is None:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    
                    new_content = replace_in_content(content)
                    
                    if content != new_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated content: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        # 2. Rename files and directories
        for name in files + dirs:
            if name == 'rebrand.py': continue
            
            old_path = os.path.join(root, name)
            new_name = name
            
            # Specific renames
            if "dreamxbotz" in name.lower():
                new_name = name.lower().replace("dreamxbotz", "Flixora")
            elif "dreamx" in name.lower():
                new_name = name.lower().replace("dreamx", "Flixora")
            elif "dreamcinezone" in name.lower():
                new_name = name.lower().replace("dreamcinezone", "Flixora")
            
            if new_name != name:
                new_path = os.path.join(root, new_name)
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    workspace = os.getcwd()
    rebrand(workspace)
    print("Rebranding complete!")
