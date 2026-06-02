from pathlib import Path
import re

paths = []
for base in [Path('notes/class-9/physics'), Path('notes/class-9/computer-science')]:
    if base.exists():
        paths.extend(sorted(base.rglob('*.html')))

color_re = re.compile(r'color\s*:\s*#f5f5f5;?', re.I)
updated_files = []
for path in paths:
    text = path.read_text(encoding='utf-8')
    new_text = color_re.sub('color: #ffffff;', text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        updated_files.append(str(path))

print('updated', len(updated_files), 'files')
for f in updated_files:
    print(f)
