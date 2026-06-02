const fs = require('fs');
const path = require('path');

const ch5Path = 'c:/Users/Asfi/Desktop/MoqeetAcademy/notes/class-9/computer-science/chapter-5/index.html';
const ch5Content = fs.readFileSync(ch5Path, 'utf8');

// Extract the header (from <!DOCTYPE html> up to <main class="main-content"> inclusive)
let headerTemplate = ch5Content.substring(0, ch5Content.indexOf('<h1') );
// Replace specific strings for generic templating
headerTemplate = headerTemplate.replace(/Chapter 5/g, 'Chapter {{NUM}}');
headerTemplate = headerTemplate.replace(/Applications of Computer Science/g, '{{TITLE}}');
headerTemplate = headerTemplate.replace('class="active"', ''); // remove active class from sidebar in template? No, the sidebar is in the footer template!

// Extract the footer (from <nav class="chapter-nav" to the end)
let footerTemplate = ch5Content.substring(ch5Content.indexOf('<nav class="chapter-nav"'));
// We need to dynamically update the previous/next links and the active sidebar link
// We'll do that inside the loop

const processChapter = (num, title, nextTitle, prevTitle) => {
    const chapPath = `c:/Users/Asfi/Desktop/MoqeetAcademy/notes/class-9/computer-science/chapter-${num}/index.html`;
    const content = fs.readFileSync(chapPath, 'utf8');
    
    // Extract the main content from the current file
    // The current file has <body> ... </body>
    // we want everything from <h1> down to just before <div class="cta-box pdf"> or <footer
    let mainBody = '';
    const h1Index = content.indexOf('<h1');
    const ctaIndex = content.indexOf('<div class="cta-box pdf">');
    const footerIndex = content.indexOf('<footer');
    
    const endIndex = ctaIndex !== -1 ? ctaIndex : (footerIndex !== -1 ? footerIndex : content.indexOf('</body>'));
    
    if (h1Index !== -1 && endIndex !== -1) {
        mainBody = content.substring(h1Index, endIndex).trim();
    }
    
    // Now construct the new file
    let newHeader = headerTemplate.replace(/\{\{NUM\}\}/g, num).replace(/\{\{TITLE\}\}/g, title);
    
    // Construct new chapter-nav
    let prevLink = num > 1 ? `<a href="/notes/class-9/computer-science/chapter-${num-1}/" class="nav-btn">← Chapter ${num-1}: ${prevTitle}</a>` : '';
    let nextLink = num < 7 ? `<a href="/notes/class-9/computer-science/chapter-${num+1}/" class="nav-btn">Chapter ${num+1}: ${nextTitle} →</a>` : '';
    
    let customNav = `
    <nav class="chapter-nav" aria-label="Chapter navigation">
      ${prevLink}
      ${nextLink}
    </nav>
  </main>`;
    
    // Build the footer part (sidebar + actual footer)
    // take the sidebar from footerTemplate, but we need to set the active class correctly
    let newFooter = footerTemplate.replace(/<nav class="chapter-nav"[\s\S]*?<\/main>/, customNav);
    
    // Fix active class in sidebar
    newFooter = newFooter.replace('class="active"', ''); // clear existing
    newFooter = newFooter.replace(`href="/notes/class-9/computer-science/chapter-${num}/"`, `href="/notes/class-9/computer-science/chapter-${num}/" class="active"`);
    
    // We also need the CTA PDF box at the end of the main content before customNav
    const pdfBox = `
    <div class="cta-box pdf">
      <h3>📥 Get Chapter ${num} Solved PDF Bundle</h3>
      <p>Download comprehensive print-ready study reference sheets containing SLO testing guidelines, complete unit summaries, and mock question verification sheets directly via WhatsApp.</p>
      <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 20px; color: #166534;">Price: Rs 70</p>
      <a href="https://wa.me/923315162406?text=Assalam%20o%20Alaikum!%20I%20want%20to%20download%20Class%209%20Computer%20Science%20Chapter%20${num}%20Notes%20PDF." class="cta-btn" target="_blank">💬 Connect via WhatsApp</a>
    </div>
    `;

    const finalHtml = newHeader + mainBody + '\n' + pdfBox + '\n' + newFooter;
    
    fs.writeFileSync(chapPath, finalHtml, 'utf8');
    console.log(`Updated Chapter ${num}`);
};

// Process Chapter 6
processChapter(6, 'Impacts of Computing', 'Entrepreneurship', 'Applications of Computer Science');
// Process Chapter 7
processChapter(7, 'Entrepreneurship', '', 'Impacts of Computing');
