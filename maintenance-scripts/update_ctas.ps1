$chemistryPaths = Get-ChildItem -Path "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry\chapter-*\index.html"
$physicsPaths = Get-ChildItem -Path "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics\chapter-*\index.html"

function ProcessFile($f, $subject, $chapter) {
    $c = [System.IO.File]::ReadAllText($f)
    
    # Extract hrefs
    $pdfHref = "https://wa.me/923315162406"
    if ($c -match '(?s)<div class="cta-box pdf">.*?<a href="(.*?)".*?</a>\s*</div>') {
        $pdfHref = $matches[1]
    }
    $premHref = "https://wa.me/923315162406"
    if ($c -match '(?s)<div class="cta-box premium">.*?<a href="(.*?)".*?</a>\s*</div>') {
        $premHref = $matches[1]
    }
    
    # Remove old CTAs completely
    $c = $c -replace '(?s)\s*<div class="cta-box pdf">.*?</div>', ""
    $c = $c -replace '(?s)\s*<div class="cta-box premium">.*?</div>', ""
    
    # Construct new CTAs
    if ($subject -eq "chemistry") {
        $pdfText = "Get the complete Class 9 Chemistry Chapter $chapter notes detailing every textbook exercise answer in high-quality PDF format. Secure your copy for a small student verification fee of Rs 30, or buy the full book file package for Rs 500."
        $pdfBtn = "Get PDF on WhatsApp - Rs 30"
    } else {
        $pdfText = "Get the complete Class 9 Physics Chapter $chapter notes detailing every textbook exercise answer in high-quality PDF format. Secure your copy for a small student verification fee of Rs 50, or buy the full book file package for Rs 350."
        $pdfBtn = "Get PDF on WhatsApp - Rs 50"
    }
    
    $pdfCta = @"
    <div class="cta-box pdf">
      <h3>Download Chapter $chapter Notes as PDF</h3>
      <p>$pdfText</p>
      <a href="$pdfHref" class="cta-btn" target="_blank">$pdfBtn</a>
    </div>
"@

    $premCta = @"
    <div class="cta-box premium">
      <h3>Access Premium SLO-Based Prep Materials</h3>
      <p>Elevate your scores with our comprehensive premium study guides. Includes extended Student Learning Outcomes (SLO) insights, hidden conceptual questions, worked model solutions, and common exam traps to avoid. <strong>Get your free sample chapter right now!</strong></p>
      <a href="$premHref" class="cta-btn" target="_blank">Request Sample Chapter on WhatsApp</a>
    </div>
"@

    # Insert Premium CTA before Short Questions or Long Questions
    if ($c -match '(<h2 class="section-heading">Short)') {
        $c = $c -replace '(<h2 class="section-heading">Short)', ($premCta + "`n`n    `$1")
    } elseif ($c -match '(<h2 class="section-heading">Long)') {
        $c = $c -replace '(<h2 class="section-heading">Long)', ($premCta + "`n`n    `$1")
    } else {
        # Fallback: place before chapter-nav
        if ($c -match '(<nav class="chapter-nav")') {
            $c = $c -replace '(<nav class="chapter-nav")', ($premCta + "`n`n    `$1")
        }
    }
    
    # Insert PDF CTA at the bottom before chapter-nav
    $c = $c -replace '(<nav class="chapter-nav")', ($pdfCta + "`n`n    `$1")
    
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($f, $c, $utf8NoBom)
}

foreach ($file in $chemistryPaths) {
    if ($file.Directory.Name -match 'chapter-(\d+)') {
        $ch = $matches[1]
        ProcessFile $file.FullName "chemistry" $ch
    }
}

foreach ($file in $physicsPaths) {
    if ($file.Directory.Name -match 'chapter-(\d+)') {
        $ch = $matches[1]
        ProcessFile $file.FullName "physics" $ch
    }
}
Write-Host "Update completed."
