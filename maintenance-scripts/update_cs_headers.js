const fs = require('fs');

const chapters = [1, 2, 3, 4, 5, 6, 7];
const baseDir = 'c:/Users/Asfi/Desktop/MoqeetAcademy/notes/class-9/computer-science';

// The new header CSS to ADD (inject into existing <style> block)
const newHeaderCSS = `
    .header-container{display:flex;align-items:center;justify-content:space-between;width:100%;gap:16px}
    .header-container .logo a{font-family:'Fraunces',serif;font-size:1.4rem;font-weight:700;color:var(--gold);text-decoration:none}
    .main-nav ul{list-style:none;display:flex;gap:20px;padding:0;margin:0}
    .main-nav ul li a{color:#cde8d8;font-size:.9rem;font-weight:500}
    .main-nav ul li a:hover,.main-nav ul li a.active{color:#fff;text-decoration:none}
    .header-cta .cta-btn-header{background:var(--gold);color:#fff;padding:8px 18px;border-radius:6px;font-size:.85rem;font-weight:600;white-space:nowrap;text-decoration:none;display:inline-block}
    .header-cta .cta-btn-header:hover{background:#b8860b;text-decoration:none;color:#fff}
    @media(max-width:700px){.main-nav{display:none}}
`;

// The new header HTML to REPLACE the old simple header
const newHeaderHTML = `<header class="site-header">
  <div class="header-container">
    <div class="logo">
      <a href="/">Moqeet Academy</a>
    </div>
    <nav class="main-nav">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/notes/class-9/physics/">Physics Notes</a></li>
        <li><a href="/notes/class-9/chemistry/">Chemistry Notes</a></li>
        <li><a href="/notes/class-9/computer-science/" class="active">Computer Science Notes</a></li>
        <li><a href="/tutoring/">Online Tutoring</a></li>
      </ul>
    </nav>
    <div class="header-cta">
      <a href="https://wa.me/923315162406" target="_blank" class="cta-btn-header">Free Trial Class</a>
    </div>
  </div>
</header>`;

let totalUpdated = 0;

chapters.forEach(num => {
  const filePath = `${baseDir}/chapter-${num}/index.html`;
  
  if (!fs.existsSync(filePath)) {
    console.log(`SKIP: chapter-${num} not found`);
    return;
  }
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  // ── 1. Inject new CSS before the closing </style> tag ──
  // Only inject if not already injected
  if (!content.includes('header-container')) {
    content = content.replace('</style>', newHeaderCSS + '\n  </style>');
    console.log(`chapter-${num}: injected CSS`);
  } else {
    console.log(`chapter-${num}: CSS already present, skipping CSS inject`);
  }
  
  // ── 2. Replace the old simple header ──
  // Old pattern: <header class="site-header"> ... </header>
  // We'll use a regex to capture and replace the entire header block
  const oldHeaderRegex = /<header class="site-header">[\s\S]*?<\/header>/;
  
  if (oldHeaderRegex.test(content)) {
    content = content.replace(oldHeaderRegex, newHeaderHTML);
    console.log(`chapter-${num}: replaced header`);
    totalUpdated++;
  } else {
    console.log(`chapter-${num}: WARNING - old header pattern not found`);
  }
  
  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`chapter-${num}: DONE ✓`);
});

console.log(`\nTotal chapters updated: ${totalUpdated}`);
