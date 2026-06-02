from pathlib import Path
import re

root = Path('notes')
footer_pattern = re.compile(r'<footer.*?</footer>', re.DOTALL | re.IGNORECASE)
issues = []
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    footers = footer_pattern.findall(text)
    for footer in footers:
        faq = footer.count('/faq/')
        priv = footer.count('/privacy-policy/')
        cont = footer.count('/contact/')
        if faq > 1 or priv > 1 or cont > 1:
            issues.append((path, faq, priv, cont, footer))

print('issues', len(issues))
for path, faq, priv, cont, footer in issues:
    print(path, 'faq', faq, 'priv', priv, 'cont', cont)
