import os
from datetime import datetime

BASE_URL = "https://moqeet.com/"
ROOT_DIR = "." 
SITEMAP_PATH = "sitemap.xml"

def get_url_settings(rel_path):
    if rel_path == "":
        return "1.0", "weekly"
    elif "notes/class-9/" in rel_path and "chapter-" in rel_path:
        return "0.8", "monthly"
    elif "notes/class-9/" in rel_path:
        return "0.9", "weekly"
    elif rel_path in ["notes/", "blog/"]:
        return "0.9", "weekly"
    elif rel_path in ["premium-notes/", "tutoring/"]:
        return "0.8", "monthly"
    elif rel_path in ["contact/", "about/", "faq/"]:
        return "0.6", "monthly"
    elif rel_path == "privacy-policy/":
        return "0.3", "yearly"
    return "0.5", "monthly"

urls = []
current_date = datetime.today().strftime('%Y-%m-%d')

for root, dirs, files in os.walk(ROOT_DIR):
    # Ignore system, hidden, and script folders
    if any(x in root for x in ["maintenance-scripts", ".git", ".claude", "assets"]):
        continue
        
    if "index.html" in files:
        rel_path = os.path.relpath(root, ROOT_DIR)
        if rel_path == ".":
            rel_path = ""
        else:
            rel_path = rel_path.replace("\\", "/") + "/"
        
        priority, changefreq = get_url_settings(rel_path)
        urls.append({
            "loc": f"{BASE_URL}{rel_path}",
            "lastmod": current_date,
            "changefreq": changefreq,
            "priority": priority
        })

# Sort pages logically by priority
urls.sort(key=lambda x: (-float(x["priority"]), x["loc"]))

# Build the XML string
xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in urls:
    xml_content += '  <url>\n'
    xml_content += f'    <loc>{url["loc"]}</loc>\n'
    xml_content += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
    xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
    xml_content += f'    <priority>{url["priority"]}</priority>\n'
    xml_content += '  </url>\n'

xml_content += '</urlset>\n'

with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
    f.write(xml_content)

print(f"Success! Generated sitemap.xml with {len(urls)} total pages detected.")
