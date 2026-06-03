# fix_html_pages.py - Moqeet Academy HTML Cleaner
# This script removes stray characters (like > or >>) that appear
# before <!DOCTYPE html> in your HTML files.
#
# HOW TO USE:
# 1. Place this file in your main MoqeetAcademy folder
# 2. Open Command Prompt
# 3. Run: python fix_html_pages.py

import os
import re

WEBSITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_FOLDERS = {'.git', 'node_modules', '__pycache__'}

def find_all_html_files(root_folder):
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        dirnames[:] = [d for d in dirnames if d not in SKIP_FOLDERS]
        for filename in filenames:
            if filename.lower().endswith('.html'):
                html_files.append(os.path.join(dirpath, filename))
    return html_files

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original_content = f.read()

    doctype_match = re.search(r'<!DOCTYPE', original_content, re.IGNORECASE)

    if doctype_match is None:
        return 'no_doctype'

    start_index = doctype_match.start()

    if start_index == 0:
        return 'clean'

    junk = original_content[:start_index]
    junk_display = repr(junk.strip())

    fixed_content = original_content[start_index:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    return junk_display

def main():
    print("============================================================")
    print("  Moqeet Academy - HTML Page Cleaner")
    print("============================================================")
    print("")
    print("Scanning folder: " + WEBSITE_ROOT)
    print("")

    html_files = find_all_html_files(WEBSITE_ROOT)

    if not html_files:
        print("No HTML files found.")
        print("Make sure this script is inside your MoqeetAcademy folder.")
        return

    print("Found " + str(len(html_files)) + " HTML file(s). Checking each one...")
    print("")

    fixed_count   = 0
    clean_count   = 0
    skipped_count = 0

    for filepath in sorted(html_files):
        short_path = os.path.relpath(filepath, WEBSITE_ROOT)
        result = fix_html_file(filepath)

        if result == 'clean':
            clean_count += 1

        elif result == 'no_doctype':
            skipped_count += 1
            print("  SKIPPED  " + short_path + "  (no <!DOCTYPE found)")

        else:
            fixed_count += 1
            print("  FIXED    " + short_path)
            print("           Removed: " + result)

    print("")
    print("============================================================")
    print("  Done!")
    print("  Fixed        : " + str(fixed_count) + " file(s)")
    print("  Already clean: " + str(clean_count) + " file(s)")
    print("  Skipped      : " + str(skipped_count) + " file(s)")
    print("============================================================")
    print("")

    if fixed_count > 0:
        print(str(fixed_count) + " file(s) were fixed.")
        print("Upload the changed files back to GitHub to see the fix live.")
    else:
        print("All files were already clean. No changes were made.")

if __name__ == '__main__':
    main()