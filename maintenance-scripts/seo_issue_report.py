import json
from pathlib import Path
import re

root = Path('c:/Users/Asfi/Desktop/MoqeetAcademy')

class HTMLChecker:
    def __init__(self, path):
        self.path = path
        self.text = path.read_text(encoding='utf-8', errors='replace')
        self.lower_text = self.text.lower()
        self.h1 = self.extract_tag('h1')
        self.meta = self.extract_meta_description()
        self.word_count = self.count_words()
        self.definition_box = 'class="definition-box"' in self.text or "class='definition-box'" in self.text
        self.faq_schema = 'faqpage' in self.lower_text and 'application/ld+json' in self.lower_text

    def extract_tag(self, tag):
        m = re.search(fr'<{tag}[^>]*>(.*?)</{tag}>', self.text, re.IGNORECASE|re.DOTALL)
        return m.group(1).strip() if m else ''

    def extract_meta_description(self):
        m = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', self.text, re.IGNORECASE)
        return m.group(1).strip() if m else ''

    def count_words(self):
        body = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', self.text, flags=re.IGNORECASE|re.DOTALL)
        return len(re.findall(r"[A-Za-z0-9']+", body))

    def has_definition_term(self):
        return bool(re.search(r'\bdefinition\b', self.text, re.IGNORECASE))

    def h1_format_ok(self):
        pattern = r'^Class 9 [A-Za-z ]+ Chapter \d+ Notes \u2014 .+ NBF Syllabus$'
        return bool(re.match(pattern, self.h1))

    def meta_len_ok(self):
        return 140 <= len(self.meta) <= 160

    def is_chapter_page(self):
        return re.search(r'notes/class-9/(chemistry|computer-science|physics)/chapter-\d+/index\.html$', self.path.as_posix())


reports = []
for path in sorted(root.rglob('*.html')):
    checker = HTMLChecker(path)
    reports.append({'path': path.relative_to(root).as_posix(), 'checker': checker})

issues = {
    'chapter_h1_mismatch': [],
    'chapter_word_count_low': [],
    'chapter_meta_invalid': [],
    'chapter_meta_missing': [],
    'faq_schema_missing': [],
    'definition_wrapper_issues': [],
    'meta_not_unique': []
}

meta_map = {}
for rep in reports:
    c = rep['checker']
    if c.meta:
        meta_map.setdefault(c.meta, []).append(rep['path'])

for rep in reports:
    path = rep['path']
    c = rep['checker']
    if c.is_chapter_page():
        if not c.h1_format_ok():
            issues['chapter_h1_mismatch'].append({'path': path, 'h1': c.h1})
        if c.word_count < 400:
            issues['chapter_word_count_low'].append({'path': path, 'word_count': c.word_count})
        if not c.meta:
            issues['chapter_meta_missing'].append(path)
        elif not c.meta_len_ok():
            issues['chapter_meta_invalid'].append({'path': path, 'meta_len': len(c.meta), 'meta': c.meta})
    if path == 'faq/index.html':
        if not c.faq_schema:
            issues['faq_schema_missing'].append(path)
    if c.has_definition_term() and not c.definition_box:
        issues['definition_wrapper_issues'].append(path)

for meta, paths in meta_map.items():
    if len(paths) > 1:
        issues['meta_not_unique'].append({'meta': meta, 'paths': paths})

print(json.dumps(issues, indent=2))
