const fs = require('fs');
const path = require('path');

const dir = 'c:/Users/Asfi/Desktop/MoqeetAcademy/computernotes';

if (fs.existsSync(dir)) {
  const files = fs.readdirSync(dir);
  files.forEach(f => {
    if (f.endsWith('.html')) {
      const content = fs.readFileSync(path.join(dir, f), 'utf8');
      const matches = [...content.matchAll(/<h2 class="section-heading">([\s\S]*?)<\/h2>/g)];
      console.log(`${f}:`);
      matches.forEach(m => {
        console.log(`  - ${m[1].trim()}`);
      });
    }
  });
}
