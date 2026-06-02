const fs = require('fs');
const path = require('path');

const destDir = 'c:/Users/Asfi/Desktop/MoqeetAcademy/notes/class-9/computer-science';

const newCss = `
    .cta-box{border-radius:12px;padding:28px;margin:32px 0;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,0.06);border:2px solid transparent}
    .cta-box.pdf{background:#f0fdf4;border-color:#86efac;color:#1f2937}
    .cta-box.premium{background:#fffbeb;border-color:#fde047;color:#1f2937}
    .cta-box h3{font-family:'Fraunces',serif;font-size:1.35rem;margin-bottom:12px;color:#166534}
    .cta-box.premium h3{color:#854d0e}
    .cta-box p{font-size:1rem;color:#374151 !important;margin-bottom:20px;line-height:1.6}
    .cta-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#f59e0b;color:#fff;padding:14px 32px;border-radius:8px;font-weight:700;font-size:1.05rem;transition:transform 0.2s, background 0.2s;text-decoration:none;border:none;cursor:pointer}
    .cta-btn:hover{transform:translateY(-2px);background:#d97706;color:#fff;text-decoration:none}
`;

const dirs = fs.readdirSync(destDir);
dirs.forEach(dir => {
    if (dir.startsWith('chapter-')) {
        const filePath = path.join(destDir, dir, 'index.html');
        if (fs.existsSync(filePath)) {
            let content = fs.readFileSync(filePath, 'utf8');
            
            const regex = /\.cta-box\s*\{[\s\S]*?\.cta-box\.premium \.cta-btn\s*\{[\s\S]*?\}/;
            if (regex.test(content)) {
                content = content.replace(regex, newCss.trim());
                fs.writeFileSync(filePath, content, 'utf8');
                console.log('Fixed CSS in ' + filePath);
            } else {
                console.log('CSS block not found in ' + filePath);
            }
        }
    }
});
