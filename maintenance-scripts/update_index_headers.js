const fs = require('fs');

const base = 'c:/Users/Asfi/Desktop/MoqeetAcademy';

const indexFiles = [
  { path: `${base}/notes/class-9/physics/index.html`,          subject: 'physics' },
  { path: `${base}/notes/class-9/chemistry/index.html`,        subject: 'chemistry' },
  { path: `${base}/notes/class-9/computer-science/index.html`, subject: 'computer-science' },
];

const headerCSS = `
    /* ── Unified Site Header ── */
    .site-header{background:var(--green);color:#fff;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;box-shadow:0 2px 12px rgba(0,0,0,.15)}
    .header-container{display:flex;align-items:center;justify-content:space-between;width:100%;gap:16px}
    .header-container .logo a{font-family:'Fraunces',serif;font-size:1.4rem;font-weight:700;color:#f59e0b;text-decoration:none}
    .main-nav ul{list-style:none;display:flex;gap:20px;padding:0;margin:0}
    .main-nav ul li a{color:#cde8d8;font-size:.9rem;font-weight:500;text-decoration:none}
    .main-nav ul li a:hover,.main-nav ul li a.active{color:#fff;text-decoration:none}
    .header-cta .cta-btn-nav{background:#f59e0b;color:#fff;padding:8px 18px;border-radius:6px;font-size:.85rem;font-weight:600;white-space:nowrap;text-decoration:none;display:inline-block}
    .header-cta .cta-btn-nav:hover{background:#d97706;text-decoration:none;color:#fff}
    @media(max-width:700px){.main-nav{display:none}}`;

const navLinks = {
  physics: `
        <li><a href="/">Home</a></li>
        <li><a href="/notes/class-9/physics/" class="active">Physics Notes</a></li>
        <li><a href="/notes/class-9/chemistry/">Chemistry Notes</a></li>
        <li><a href="/notes/class-9/computer-science/">Computer Science Notes</a></li>
        <li><a href="/tutoring/">Online Tutoring</a></li>`,
  chemistry: `
        <li><a href="/">Home</a></li>
        <li><a href="/notes/class-9/physics/">Physics Notes</a></li>
        <li><a href="/notes/class-9/chemistry/" class="active">Chemistry Notes</a></li>
        <li><a href="/notes/class-9/computer-science/">Computer Science Notes</a></li>
        <li><a href="/tutoring/">Online Tutoring</a></li>`,
  'computer-science': `
        <li><a href="/">Home</a></li>
        <li><a href="/notes/class-9/physics/">Physics Notes</a></li>
        <li><a href="/notes/class-9/chemistry/">Chemistry Notes</a></li>
        <li><a href="/notes/class-9/computer-science/" class="active">Computer Science Notes</a></li>
        <li><a href="/tutoring/">Online Tutoring</a></li>`,
};

function buildHeader(subject) {
  return `<header class="site-header">
  <div class="header-container">
    <div class="logo">
      <a href="/">Moqeet Academy</a>
    </div>
    <nav class="main-nav">
      <ul>${navLinks[subject]}
      </ul>
    </nav>
    <div class="header-cta">
      <a href="https://wa.me/923315162406" target="_blank" class="cta-btn-nav">Free Trial Class</a>
    </div>
  </div>
</header>`;
}

indexFiles.forEach(({ path: filePath, subject }) => {
  if (!fs.existsSync(filePath)) {
    console.log(`SKIP (not found): ${filePath}`);
    return;
  }

  let content = fs.readFileSync(filePath, 'utf8');

  // ── 1. Inject CSS into <style> or <head> ──
  if (!content.includes('header-container')) {
    // Try injecting before </style>
    if (content.includes('</style>')) {
      // inject before FIRST </style>
      content = content.replace('</style>', headerCSS + '\n  </style>');
      console.log(`  [${subject}] CSS injected into <style>`);
    } else if (content.includes('</head>')) {
      // No style block — add one
      content = content.replace('</head>', `<style>${headerCSS}\n</style>\n</head>`);
      console.log(`  [${subject}] New <style> block added`);
    }
  } else {
    console.log(`  [${subject}] CSS already present`);
  }

  // ── 2. Replace OLD header block ──
  // These index pages use plain <header> ... </header> (no class="site-header")
  // Match both <header class="site-header"> and <header> variants
  const oldHeaderRegex = /<header(?:\s[^>]*)?>[\s\S]*?<\/header>/;

  const newHeader = buildHeader(subject);

  if (oldHeaderRegex.test(content)) {
    content = content.replace(oldHeaderRegex, newHeader);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ Updated [${subject}] index: ${filePath.replace(base + '/', '')}`);
  } else {
    console.log(`? No <header> tag found in: ${filePath}`);
  }
});

console.log('\n✅ Index pages done!');
