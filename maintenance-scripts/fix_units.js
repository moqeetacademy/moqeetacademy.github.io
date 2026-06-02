const fs = require('fs');
const path = require('path');

const destDir = 'c:/Users/Asfi/Desktop/MoqeetAcademy/notes/class-9/computer-science';

const dirs = fs.readdirSync(destDir);
dirs.forEach(dir => {
    if (dir.startsWith('chapter-')) {
        const filePath = path.join(destDir, dir, 'index.html');
        if (fs.existsSync(filePath)) {
            let content = fs.readFileSync(filePath, 'utf8');
            
            // Replace "/unit-X/" with "/chapter-X/" in links
            content = content.replace(/\/unit-(\d+)\//g, '/chapter-$1/');
            
            // Replace "Unit X:" with "Chapter X:"
            content = content.replace(/Unit\s+(\d+):/gi, 'Chapter $1:');
            
            // Replace "Unit X Notes" with "Chapter X Notes"
            content = content.replace(/Unit\s+(\d+)\s+Notes/gi, 'Chapter $1 Notes');
            
            // Replace ">Unit X<" with ">Chapter X<"
            content = content.replace(/>\s*Unit\s+(\d+)\s*</gi, '>Chapter $1<');

            // Replace "Unit X" with "Chapter X" in meta description and schema
            content = content.replace(/Unit\s+(\d+)/gi, 'Chapter $1');
            
            fs.writeFileSync(filePath, content, 'utf8');
            console.log('Fixed ' + filePath);
        }
    }
});
