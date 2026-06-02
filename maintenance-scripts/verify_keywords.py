import re
from pathlib import Path
from html.parser import HTMLParser

root = Path('c:/Users/Asfi/Desktop/MoqeetAcademy')

# All chapter pages to verify
chapter_pages = [
    ('notes/class-9/chemistry/chapter-1/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-2/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-3/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-4/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-5/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-6/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-7/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-8/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-9/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-10/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-11/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-12/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-13/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-14/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-15/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-16/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-17/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-18/index.html', 'Chemistry'),
    ('notes/class-9/chemistry/chapter-19/index.html', 'Chemistry'),
    ('notes/class-9/computer-science/chapter-1/index.html', 'Computer Science'),
    ('notes/class-9/computer-science/chapter-2/index.html', 'Computer Science'),
    ('notes/class-9/computer-science/chapter-3/index.html', 'Computer Science'),
    ('notes/class-9/computer-science/chapter-4/index.html', 'Computer Science'),
    ('notes/class-9/computer-science/chapter-5/index.html', 'Computer Science'),
    ('notes/class-9/computer-science/chapter-6/index.html', 'Computer Science'),
    ('notes/class-9/computer-science/chapter-7/index.html', 'Computer Science'),
    ('notes/class-9/physics/chapter-1/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-2/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-3/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-4/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-5/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-6/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-7/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-8/index.html', 'Physics'),
    ('notes/class-9/physics/chapter-9/index.html', 'Physics'),
]

class IntroExtractor(HTMLParser):
    """Extract first 300 characters of body text, skipping nav/header"""
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.intro_text = ""
        self.capture_text = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['article', 'main']:
            self.in_article = True
            self.capture_text = True
        elif tag in ['nav', 'header', 'script', 'style']:
            self.capture_text = False
            
    def handle_endtag(self, tag):
        if tag in ['nav', 'header', 'script', 'style']:
            if self.in_article:
                self.capture_text = True
        
    def handle_data(self, data):
        if self.capture_text and self.in_article and len(self.intro_text) < 500:
            text = data.strip()
            if text:
                self.intro_text += " " + text

print("Verifying keywords in intro paragraphs...")
print("=" * 80)

missing_keywords = []

for rel, subject in chapter_pages:
    path = root / rel
    if not path.exists():
        continue
    
    html_text = path.read_text(encoding='utf-8', errors='replace')
    
    # Extract intro text
    parser = IntroExtractor()
    parser.feed(html_text)
    intro = parser.intro_text[:500].lower()
    
    # Check for keywords
    has_class_notes = bool(re.search(r'class\s+9.*?notes|9th\s+class|class\s+9', intro, re.I))
    has_subject = subject.lower() in intro
    has_fbise = 'fbise' in intro or 'free notes' in intro
    
    status = "✓" if (has_class_notes and has_subject) else "✗"
    
    if not (has_class_notes and has_subject):
        missing_keywords.append((rel, subject, not has_class_notes, not has_subject, not has_fbise))
        print(f"{status} {rel}")
        if not has_class_notes:
            print(f"   Missing: 'Class 9 Notes' keyword")
        if not has_subject:
            print(f"   Missing: '{subject}' keyword")
        if not has_fbise:
            print(f"   Optional: FBISE/Free Notes keyword")

print("\n" + "=" * 80)
print(f"Summary: {len(chapter_pages) - len(missing_keywords)}/{len(chapter_pages)} pages have proper keywords")

if missing_keywords:
    print(f"\nPages requiring intro keyword updates: {len(missing_keywords)}")
    for rel, subject, missing_class, missing_subj, missing_fbise in missing_keywords:
        print(f"  - {rel.split('/')[-2]}: {subject}")
else:
    print("\n✓ All pages have proper SEO keywords in intro!")
