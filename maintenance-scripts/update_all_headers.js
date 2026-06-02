const fs = require('fs');
const path = require('path');

const base = 'c:/Users/Asfi/Desktop/MoqeetAcademy';

// ── Collect ALL html files under notes/ ──
function getAllHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllHtmlFiles(fullPath));
    } else if (file.endsWith('.html')) {
      results.push(fullPath);
    }
  });
  return results;
}

const notesDir = path.join(base, 'notes');
const allFiles = getAllHtmlFiles(notesDir);
console.log(`Found ${allFiles.length} HTML files total.\n`);

// ── The FULL correct header for each subject ──
// We use a function so the correct nav link gets "active" class per subject

function makeHeader(activeSubject) {
  const navItems = [
    { label: 'Home', href: '/' },
    { label: 'Physics Notes', href: '/notes/class-9/physics/' },
    { label: 'Chemistry Notes', href: '/notes/class-9/chemistry/' },
    { label: 'Computer Science Notes', href: '/notes/class-9/computer-science/' },
    { label: 'Online Tutoring', href: '/tutoring/' },
  ];
  
  const navLinks = navItems.map(item => {
    const isActive = item.label.toLowerCase().includes(activeSubject.toLowerCase());
    return `        <li><a href="${item.href}"${isActive ? ' class="active"' : ''}>${item.label}</a></li>`;
  }).join('\n');
  
  return `<header class="site-header">
  <div class="header-container">
    <div class="logo">
      <a href="/">Moqeet Academy</a>
    </div>
    <nav class="main-nav">
      <ul>
        <li><a href="/">Home</a></li>
${navLinks.replace('        <li><a href="/">Home</a></li>\n', '')}      </ul>
    </nav>
    <div class="header-cta">
      <a href="https://wa.me/923315162406" target="_blank" class="cta-btn">Free Trial Class</a>
    </div>
  </div>
</header>`;
}

// Simpler, cleaner approach - build header directly per subject
function buildHeader(subject) {
  const links = {
    physics:  `        <li><a href="/">Home</a></li>
        <li><a href="/notes/class-9/physics/" class="active">Physics Notes</a></li>
        <li><a href="/notes/class-9/chemistry/">Chemistry Notes</a></li>
        <li><a href="/notes/class-9/computer-science/">Computer Science Notes</a></li>
        <li><a href="/tutoring/">Online Tutoring</a></li>`,
    chemistry: `        <li><a href="/">Home</a></li>
        <li><a href="/notes/class-9/physics/">Physics Notes</a></li>
        <li><a href="/notes/class-9/chemistry/" class="active">Chemistry Notes</a></li>
        <li><a href="/notes/class-9/computer-science/">Computer Science Notes</a></li>
        <li><a href="/tutoring/">Online Tutoring</a></li>`,
    'computer-science': `        <li><a href="/">Home</a></li>
        <li><a href="/notes/class-9/physics/">Physics Notes</a></li>
        <li><a href="/notes/class-9/chemistry/">Chemistry Notes</a></li>
        <li><a href="/notes/class-9/computer-science/" class="active">Computer Science Notes</a></li>
        <li><a href="/tutoring/">Online Tutoring</a></li>`,
  };
  
  // CSS to ensure header-container styles are present (injected once)
  const headerCSS = `    .header-container{display:flex;align-items:center;justify-content:space-between;width:100%;gap:16px}
    .header-container .logo a{font-family:'Fraunces',serif;font-size:1.4rem;font-weight:700;color:var(--gold);text-decoration:none}
    .main-nav ul{list-style:none;display:flex;gap:20px;padding:0;margin:0}
    .main-nav ul li a{color:#cde8d8;font-size:.9rem;font-weight:500}
    .main-nav ul li a:hover,.main-nav ul li a.active{color:#fff;text-decoration:none}
    .header-cta .cta-btn{background:var(--gold);color:#fff;padding:8px 18px;border-radius:6px;font-size:.85rem;font-weight:600;white-space:nowrap;text-decoration:none;display:inline-block}
    .header-cta .cta-btn:hover{background:#b8860b;text-decoration:none;color:#fff}
    @media(max-width:700px){.main-nav{display:none}}`;

  const html = `<header class="site-header">
  <div class="header-container">
    <div class="logo">
      <a href="/">Moqeet Academy</a>
    </div>
    <nav class="main-nav">
      <ul>
${links[subject]}
      </ul>
    </nav>
    <div class="header-cta">
      <a href="https://wa.me/923315162406" target="_blank" class="cta-btn">Free Trial Class</a>
    </div>
  </div>
</header>`;

  return { html, css: headerCSS };
}

// Detect which subject the file belongs to
function getSubject(filePath) {
  const normalized = filePath.replace(/\\/g, '/');
  if (normalized.includes('/physics/')) return 'physics';
  if (normalized.includes('/chemistry/')) return 'chemistry';
  if (normalized.includes('/computer-science/')) return 'computer-science';
  return null;
}

let updated = 0;
let skipped = 0;

allFiles.forEach(filePath => {
  const subject = getSubject(filePath);
  if (!subject) {
    console.log(`SKIP (no subject): ${filePath}`);
    skipped++;
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  const { html: newHeader, css: headerCSS } = buildHeader(subject);
  
  // ── Step 1: Ensure CSS is present ──
  // Replace ALL variations of nav-less header CSS with the full version
  // Only inject if header-container block is missing
  if (!content.includes('header-container{display:flex') && !content.includes('header-container {display')) {
    // Inject before </style>
    if (content.includes('</style>')) {
      content = content.replace('</style>', headerCSS + '\n  </style>');
    }
  }
  
  // ── Step 2: Replace the entire <header>...</header> block ──
  const headerRegex = /<header class="site-header">[\s\S]*?<\/header>/;
  if (headerRegex.test(content)) {
    content = content.replace(headerRegex, newHeader);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ Updated [${subject}]: ${path.relative(base, filePath)}`);
    updated++;
  } else {
    console.log(`? No header found: ${path.relative(base, filePath)}`);
    skipped++;
  }
});

console.log(`\n✅ Done! Updated: ${updated} files | Skipped: ${skipped} files`);
