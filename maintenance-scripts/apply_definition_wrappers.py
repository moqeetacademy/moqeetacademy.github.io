import re
from pathlib import Path

root = Path('c:/Users/Asfi/Desktop/MoqeetAcademy')

# Pages that need definition wrapping
definition_pages = [
    'notes/class-9/chemistry/chapter-3/index.html',
    'notes/class-9/chemistry/chapter-7/index.html',
    'notes/class-9/chemistry/chapter-10/index.html',
    'notes/class-9/chemistry/chapter-14/index.html',
    'notes/class-9/chemistry/chapter-15/index.html',
    'notes/class-9/chemistry/chapter-16/index.html',
    'notes/class-9/chemistry/chapter-17/index.html',
    'notes/class-9/chemistry/chapter-18/index.html',
    'notes/class-9/chemistry/chapter-19/index.html',
    'notes/class-9/computer-science/chapter-2/index.html',
    'notes/class-9/computer-science/chapter-3/index.html',
    'notes/class-9/computer-science/chapter-4/index.html',
    'notes/class-9/physics/chapter-1/index.html',
    'notes/class-9/physics/chapter-2/index.html',
    'notes/class-9/physics/chapter-3/index.html',
    'notes/class-9/physics/chapter-4/index.html',
    'notes/class-9/physics/chapter-5/index.html',
]

def wrap_definitions(html_text):
    """Find definition content and wrap in definition-box div"""
    
    # Pattern 1: Look for explicit "Definition:" headings or paragraphs
    # Find <strong>Definition</strong> or <strong>Definition:</strong> patterns
    pattern1 = r'(<strong>Definition[:\s]*</strong>\s*)(.*?)(?=<(?:h\d|strong|p|div))'
    
    # Pattern 2: Look for <strong>Definition</strong> in middle of paragraph
    pattern2 = r'(<p[^>]*>.*?<strong>Definition[:\s]*</strong>\s*)(.*?)(</p>)'
    
    wrapped = html_text
    match_count = 0
    
    # Handle inline definition patterns within paragraphs
    def replace_inline(match):
        nonlocal match_count
        pre = match.group(1)
        content = match.group(2)
        post = match.group(3)
        
        # Only wrap if not already wrapped
        if 'definition-box' not in pre:
            match_count += 1
            return f'{pre}<div class="definition-box">{content}</div>{post}'
        return match.group(0)
    
    wrapped = re.sub(
        r'(<p[^>]*>.*?<strong>Definition[:\s]*</strong>\s*)(.*?)(</p>)',
        replace_inline,
        wrapped,
        flags=re.DOTALL|re.IGNORECASE
    )
    
    # Pattern: <strong>Definition:</strong> followed by text until next element
    # This handles single-line definitions
    def replace_block(match):
        nonlocal match_count
        if 'definition-box' not in match.group(0):
            match_count += 1
            label = match.group(1)
            content = match.group(2).strip()
            return f'{label}<div class="definition-box">{content}</div>'
        return match.group(0)
    
    wrapped = re.sub(
        r'(<strong>Definition[:\s]*</strong>\s*)(.*?)(?=(?:<(?:strong|h\d|div|/div))|$)',
        replace_block,
        wrapped,
        flags=re.DOTALL|re.IGNORECASE
    )
    
    return wrapped, match_count

fixed_count = 0
total_defs_wrapped = 0

for rel in definition_pages:
    path = root / rel
    if not path.exists():
        print(f"Skipped (not found): {rel}")
        continue
    
    text = path.read_text(encoding='utf-8', errors='replace')
    original_text = text
    
    wrapped_text, defs_wrapped = wrap_definitions(text)
    
    if wrapped_text != original_text:
        path.write_text(wrapped_text, encoding='utf-8')
        fixed_count += 1
        total_defs_wrapped += defs_wrapped
        print(f"Fixed: {rel} ({defs_wrapped} definitions wrapped)")
    else:
        print(f"No changes needed: {rel}")

print(f"\nTotal files modified: {fixed_count}")
print(f"Total definitions wrapped: {total_defs_wrapped}")
