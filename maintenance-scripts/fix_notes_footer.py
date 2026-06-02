from pathlib import Path
import re

paths = []
for base in [Path('notes/class-9/physics'), Path('notes/class-9/computer-science')]:
    if base.exists():
        paths.extend(sorted(base.rglob('*.html')))

footer_re = re.compile(r'<footer(?P<attrs>[^>]*)>.*?</footer>', re.S | re.I)
site_footer_color_re = re.compile(r'(\.site-footer\s*\{[^}]*?)color\s*:\s*#[0-9A-Fa-f]{3,6};', re.S | re.I)

expected_footer = "<footer{attrs}>\n  <p>© 2026 Moqeet Academy. All rights reserved. | <a href='/faq/'>FAQ</a> | <a href='/privacy-policy/'>Privacy Policy</a> | <a href='/contact/'>Contact</a></p>\n</footer>"
updated_files = []
for path in paths:
    text = path.read_text(encoding='utf-8')
    new_text = text
    new_text = site_footer_color_re.sub(lambda m: m.group(1) + 'color: #ffffff;', new_text)

    def replace_footer(match):
        attrs = match.group('attrs')
        return expected_footer.format(attrs=attrs)

    new_text = footer_re.sub(replace_footer, new_text)

    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        updated_files.append(str(path))

print('updated', len(updated_files), 'files')
for f in updated_files:
    print(f)
