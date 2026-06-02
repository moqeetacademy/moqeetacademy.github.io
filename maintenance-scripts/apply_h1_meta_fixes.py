import re
from pathlib import Path

root = Path('c:/Users/Asfi/Desktop/MoqeetAcademy')

# H1 fixes
h1_fixes = {
    'notes/class-9/chemistry/chapter-13/index.html': 'Class 9 Chemistry Chapter 13 Notes — Hydrocarbons and Functional Groups NBF Syllabus',
    'notes/class-9/chemistry/chapter-14/index.html': 'Class 9 Chemistry Chapter 14 Notes — Hydrocarbons Reactions and Properties NBF Syllabus',
    'notes/class-9/chemistry/chapter-15/index.html': 'Class 9 Chemistry Chapter 15 Notes — Biochemistry NBF Syllabus',
    'notes/class-9/chemistry/chapter-16/index.html': 'Class 9 Chemistry Chapter 16 Notes — Empirical Data Collection and Analysis NBF Syllabus',
    'notes/class-9/chemistry/chapter-17/index.html': 'Class 9 Chemistry Chapter 17 Notes — Separation of Mixtures NBF Syllabus',
    'notes/class-9/chemistry/chapter-18/index.html': 'Class 9 Chemistry Chapter 18 Notes — Introduction to Analytical Chemistry NBF Syllabus',
    'notes/class-9/chemistry/chapter-19/index.html': 'Class 9 Chemistry Chapter 19 Notes — Chromatography NBF Syllabus',
    'notes/class-9/computer-science/chapter-1/index.html': 'Class 9 Computer Science Chapter 1 Notes — Fundamentals of Computer NBF Syllabus',
    'notes/class-9/computer-science/chapter-2/index.html': 'Class 9 Computer Science Chapter 2 Notes — Computational Thinking and Algorithms NBF Syllabus',
    'notes/class-9/computer-science/chapter-3/index.html': 'Class 9 Computer Science Chapter 3 Notes — Programming Fundamentals NBF Syllabus',
    'notes/class-9/computer-science/chapter-4/index.html': 'Class 9 Computer Science Chapter 4 Notes — Data and Analysis NBF Syllabus',
    'notes/class-9/computer-science/chapter-5/index.html': 'Class 9 Computer Science Chapter 5 Notes — Applications of Computer Science NBF Syllabus',
    'notes/class-9/computer-science/chapter-6/index.html': 'Class 9 Computer Science Chapter 6 Notes — Impacts of Computing NBF Syllabus',
    'notes/class-9/computer-science/chapter-7/index.html': 'Class 9 Computer Science Chapter 7 Notes — Entrepreneurship NBF Syllabus',
}

# Meta descriptions (140-160 chars)
meta_fixes = {
    'notes/class-9/chemistry/chapter-10/index.html': 'Free Class 9 Chemistry Chapter 10 notes on Acids, Bases and Salts. Fully solved MCQs, short answers, and long questions for NBF.',
    'notes/class-9/chemistry/chapter-11/index.html': 'Free Class 9 Chemistry Chapter 11 notes on Atmosphere and Environmental Chemistry. Solved MCQs, short and long answers for NBF.',
    'notes/class-9/chemistry/chapter-12/index.html': 'Free Class 9 Chemistry Chapter 12 notes on Water. Complete solutions for MCQs, short answers, and treatment processes for NBF syllabus.',
    'notes/class-9/chemistry/chapter-13/index.html': 'Class 9 Chemistry Chapter 13 notes on Hydrocarbons and Functional Groups. Fully solved MCQs, structural formulas, and practice exercises.',
    'notes/class-9/chemistry/chapter-14/index.html': 'Class 9 Chemistry Chapter 14 notes on Hydrocarbons Reactions and Properties. Complete solutions for MCQs and long answer questions.',
    'notes/class-9/chemistry/chapter-15/index.html': 'Free Class 9 Chemistry Chapter 15 notes on Biochemistry. MCQs, short and long questions fully solved for FBISE and Punjab Board.',
    'notes/class-9/chemistry/chapter-16/index.html': 'Free Class 9 Chemistry Chapter 16 notes on Data Collection and Analysis. Complete MCQs, short questions, and long answers for NBF.',
    'notes/class-9/chemistry/chapter-18/index.html': 'Free Class 9 Chemistry Chapter 18 notes on Analytical Chemistry. Complete MCQs, chemical gas tests, and flame test solutions for NBF.',
    'notes/class-9/chemistry/chapter-19/index.html': 'Free Class 9 Chemistry Chapter 19 notes on Chromatography. Detailed explanations of Paper Chromatography, Rf values, and phase changes.',
    'notes/class-9/chemistry/chapter-2/index.html': 'Free Class 9 Chemistry Chapter 2 notes on Matter. Fully solved MCQs, short and long questions for NBF FBISE Punjab Board Pakistan.',
    'notes/class-9/chemistry/chapter-6/index.html': 'Free Class 9 Chemistry Chapter 6 notes on Stoichiometry. Solved numerical equations, formula mass, and mole calculations for NBF.',
    'notes/class-9/chemistry/chapter-8/index.html': 'Free Class 9 Chemistry Chapter 8 notes on Energetics. Solved MCQs, short questions, and bond energy calculations for NBF syllabus.',
    'notes/class-9/chemistry/chapter-9/index.html': 'Free Class 9 Chemistry Chapter 9 notes on Chemical Equilibrium. Complete solutions for MCQs, short, and long exercise answers for NBF.',
    'notes/class-9/computer-science/chapter-2/index.html': 'Free Class 9 Computer Science Chapter 2 notes on Computational Thinking and Algorithms. Solved MCQs and comprehensive exercise solutions.',
    'notes/class-9/computer-science/chapter-3/index.html': 'Free Class 9 Computer Science Chapter 3 notes on Programming Fundamentals, HTML, CSS, and JavaScript with fully solved MCQs and exercises.',
    'notes/class-9/computer-science/chapter-4/index.html': 'Free Class 9 Computer Science Chapter 4 notes on Data and Analysis, Big Data, and Machine Learning with solved MCQs and exercises.',
    'notes/class-9/computer-science/chapter-5/index.html': 'Free Class 9 Computer Science Chapter 5 notes on Applications of CS, AI, Machine Learning, and Cloud Computing with solved exercises.',
    'notes/class-9/computer-science/chapter-6/index.html': 'Free Class 9 Computer Science Chapter 6 notes on Computing Impacts covering ethics, privacy, and economic effects with solved questions.',
    'notes/class-9/computer-science/chapter-7/index.html': 'Free Class 9 Computer Science Chapter 7 notes on Entrepreneurship. Solved MCQs, short questions, and complete exercise solutions.',
    'notes/class-9/physics/chapter-2/index.html': 'Free Class 9 Physics Chapter 2 notes on Kinematics. MCQs, short and long questions with numericals on motion, velocity, and acceleration.',
    'notes/class-9/physics/chapter-3/index.html': 'Free Class 9 Physics Chapter 3 notes on Dynamics. MCQs, short and long questions with numericals on Newton\'s laws, momentum, and inertia.',
    'notes/class-9/physics/chapter-4/index.html': 'Free Class 9 Physics Chapter 4 notes on Turning Effect of Forces. MCQs, short and long questions with numericals on torque and equilibrium.',
    'notes/class-9/physics/chapter-5/index.html': 'Free Class 9 Physics Chapter 5 notes on Elasticity and Pressure. MCQs, short and long questions with numericals on Hooke\'s law.',
}

print("Applying all fixes...")
fixed_count = 0

for rel in list(h1_fixes.keys()) + list(meta_fixes.keys()):
    path = root / rel
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8', errors='replace')
    original_text = text
    
    # Fix H1
    if rel in h1_fixes:
        h1_pattern = r'<h1[^>]*>(.*?)</h1>'
        new_h1 = f'<h1>{h1_fixes[rel]}</h1>'
        text = re.sub(h1_pattern, new_h1, text, count=1, flags=re.I|re.S)
    
    # Fix meta description
    if rel in meta_fixes:
        new_meta = meta_fixes[rel]
        meta_pattern = r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']'
        old_meta_match = re.search(meta_pattern, text, re.I)
        if old_meta_match:
            old_meta_full = old_meta_match.group(0)
            new_meta_full = f'<meta name="description" content="{new_meta}">'
            text = text.replace(old_meta_full, new_meta_full, 1)
    
    if text != original_text:
        path.write_text(text, encoding='utf-8')
        fixed_count += 1
        print(f"Fixed: {rel}")

print(f"\nTotal files fixed: {fixed_count}")
