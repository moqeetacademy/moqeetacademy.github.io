import re
from pathlib import Path

root = Path('c:/Users/Asfi/Desktop/MoqeetAcademy')

# Maps of subject folder to subject name and chapter info
h1_fixes = {
    'notes/class-9/chemistry/chapter-13/index.html': {
        'subject': 'Chemistry',
        'chapter': '13',
        'title': 'Hydrocarbons and Functional Groups'
    },
    'notes/class-9/chemistry/chapter-14/index.html': {
        'subject': 'Chemistry',
        'chapter': '14',
        'title': 'Hydrocarbons Reactions and Properties'
    },
    'notes/class-9/chemistry/chapter-15/index.html': {
        'subject': 'Chemistry',
        'chapter': '15',
        'title': 'Biochemistry'
    },
    'notes/class-9/chemistry/chapter-16/index.html': {
        'subject': 'Chemistry',
        'chapter': '16',
        'title': 'Empirical Data Collection and Analysis'
    },
    'notes/class-9/chemistry/chapter-17/index.html': {
        'subject': 'Chemistry',
        'chapter': '17',
        'title': 'Separation of Mixtures'
    },
    'notes/class-9/chemistry/chapter-18/index.html': {
        'subject': 'Chemistry',
        'chapter': '18',
        'title': 'Introduction to Analytical Chemistry'
    },
    'notes/class-9/chemistry/chapter-19/index.html': {
        'subject': 'Chemistry',
        'chapter': '19',
        'title': 'Chromatography'
    },
    'notes/class-9/computer-science/chapter-1/index.html': {
        'subject': 'Computer Science',
        'chapter': '1',
        'title': 'Fundamentals of Computer'
    },
    'notes/class-9/computer-science/chapter-2/index.html': {
        'subject': 'Computer Science',
        'chapter': '2',
        'title': 'Computational Thinking and Algorithms'
    },
    'notes/class-9/computer-science/chapter-3/index.html': {
        'subject': 'Computer Science',
        'chapter': '3',
        'title': 'Programming Fundamentals'
    },
    'notes/class-9/computer-science/chapter-4/index.html': {
        'subject': 'Computer Science',
        'chapter': '4',
        'title': 'Data and Analysis'
    },
    'notes/class-9/computer-science/chapter-5/index.html': {
        'subject': 'Computer Science',
        'chapter': '5',
        'title': 'Applications of Computer Science'
    },
    'notes/class-9/computer-science/chapter-6/index.html': {
        'subject': 'Computer Science',
        'chapter': '6',
        'title': 'Impacts of Computing'
    },
    'notes/class-9/computer-science/chapter-7/index.html': {
        'subject': 'Computer Science',
        'chapter': '7',
        'title': 'Entrepreneurship'
    },
}

for rel, info in h1_fixes.items():
    path = root / rel
    text = path.read_text(encoding='utf-8', errors='replace')
    new_h1 = f"Class 9 {info['subject']} Chapter {info['chapter']} Notes — {info['title']} NBF Syllabus"
    old_h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I|re.S)
    if old_h1_match:
        old_h1_full = old_h1_match.group(0)
        new_h1_full = f'<h1>{new_h1}</h1>'
        print(f"{rel}")
        print(f"  OLD: {old_h1_match.group(1).strip()[:70]}")
        print(f"  NEW: {new_h1}")
        print()
