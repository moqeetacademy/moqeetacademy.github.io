import os
import re

base_paths = [
    r"c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry",
    r"c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics"
]

files_updated = 0

for base_path in base_paths:
    if not os.path.exists(base_path):
        continue
    for folder in os.listdir(base_path):
        if folder.startswith("chapter-"):
            file_path = os.path.join(base_path, folder, "index.html")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                original_content = content
                
                # Replace HTML class
                content = re.sub(
                    r'(<div class="header-cta">\s*<a[^>]+class=")cta-btn(")',
                    r'\1cta-btn-nav\2',
                    content
                )
                
                # Replace CSS if media query is missing
                if "@media(max-width:700px){.main-nav{display:none}}" not in content:
                    pattern = r"\.header-cta \.cta-btn\{[^}]+\}"
                    replacement = (
                        ".header-cta .cta-btn-nav{background:var(--gold);color:#fff;padding:8px 18px;border-radius:6px;font-size:.85rem;font-weight:600;white-space:nowrap;text-decoration:none;display:inline-block}\n"
                        "    .header-cta .cta-btn-nav:hover{background:#b8860b;text-decoration:none;color:#fff}\n"
                        "    @media(max-width:700px){.main-nav{display:none}}"
                    )
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    files_updated += 1

print(f"Updated {files_updated} files.")
