from pathlib import Path
import re
root = Path('c:/Users/Asfi/Desktop/MoqeetAcademy')
chapter_paths = sorted(root.rglob('notes/class-9/*/chapter-*/index.html'))

results = []
for path in chapter_paths:
    text = path.read_text(encoding='utf-8', errors='replace')
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I|re.S)
    h1_text = h1_match.group(1).strip() if h1_match else ''
    desc_index = text.find('name="description"')
    meta_text = ''
    if desc_index != -1:
        content_index = text.find('content="', desc_index)
        if content_index != -1:
            start = content_index + len('content="')
            end = text.find('"', start)
            meta_text = text[start:end].strip()
    body = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', text, flags=re.I|re.S)
    word_count = len(re.findall(r"[A-Za-z0-9']+", body))
    definition = bool(re.search(r'\bdefinition\b', text, re.I))
    def_box = 'class="definition-box"' in text or "class='definition-box'" in text
    results.append({
        'path': str(path.relative_to(root)),
        'h1': h1_text,
        'meta_len': len(meta_text),
        'word_count': word_count,
        'definition_term': definition,
        'has_definition_box': def_box,
    })

bad_h1 = [r for r in results if not re.match(r'^Class 9 [A-Za-z ]+ Chapter \d+ Notes — .+ NBF Syllabus$', r['h1'])]
meta_bad = [r for r in results if r['meta_len'] < 140 or r['meta_len'] > 160]
word_bad = [r for r in results if r['word_count'] < 400]
definition_bad = [r for r in results if r['definition_term'] and not r['has_definition_box']]
print('BAD_H1', len(bad_h1))
for r in bad_h1:
    print(r['path'], r['h1'])
print('META_BAD', len(meta_bad))
for r in meta_bad:
    print(r['path'], r['meta_len'])
print('WORD_BAD', len(word_bad))
for r in word_bad:
    print(r['path'], r['word_count'])
print('DEFINITION_BAD', len(definition_bad))
for r in definition_bad:
    print(r['path'])
