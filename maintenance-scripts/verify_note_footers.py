from pathlib import Path
import re

paths = []
for base in [Path('notes/class-9/physics'), Path('notes/class-9/computer-science')]:
    if base.exists():
        paths.extend(sorted(base.rglob('*.html')))

footer_re = re.compile(r'<footer.*?>.*?</footer>', re.S | re.I)
p_re = re.compile(r'<p\b', re.I)
color_re = re.compile(r'\.site-footer\s*\{[^}]*color\s*:\s*#[0-9A-Fa-f]{3,6};', re.S | re.I)

bad = []
for path in paths:
    text = path.read_text(encoding='utf-8')
    m = footer_re.search(text)
    if not m:
        bad.append((str(path), 'no footer'))
        continue
    footer = m.group(0)
    ps = len(p_re.findall(footer))
    if ps != 1:
        bad.append((str(path), f'footer p count={ps}'))
    if color_re.search(text):
        bad.append((str(path), 'old color'))

print('checked', len(paths), 'files')
print('bad', len(bad))
for item in bad:
    print(item)
