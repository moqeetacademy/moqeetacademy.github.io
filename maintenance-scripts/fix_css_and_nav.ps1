$paths = @(
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry\chapter-*\index.html",
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics\chapter-*\index.html"
)

$files = Get-ChildItem -Path $paths

# Extract the correct header CSS from Chemistry Chapter 1
$chem1 = [System.IO.File]::ReadAllText("c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry\chapter-1\index.html")
$headerCssRegex = '(?s)\.site-header\{.*?(?=\.header-wa\{|\.breadcrumb\{)'
$headerCssMatch = [regex]::Match($chem1, $headerCssRegex)
$correctHeaderCss = $headerCssMatch.Value

# New CTA Box CSS for better visibility
$newCtaCss = @'
.cta-box{border-radius:12px;padding:28px;margin:32px 0;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,0.06);border:2px solid transparent}
      .cta-box.pdf{background:#f0fdf4;border-color:#86efac;color:#1f2937}
      .cta-box.premium{background:#fffbeb;border-color:#fde047;color:#1f2937}
      .cta-box h3{font-family:'Fraunces',serif;font-size:1.35rem;margin-bottom:12px;color:#166534}
      .cta-box.premium h3{color:#854d0e}
      .cta-box p{font-size:1rem;color:#374151;margin-bottom:20px;line-height:1.6}
'@

foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName)
    $changed = $false

    # Fix Physics Header CSS
    if ($f.FullName -match "physics") {
        $physHeaderRegex = '(?s)\.site-header\s*\{.*?(?=\.header-wa\s*\{)'
        if ($c -match $physHeaderRegex) {
            $c = $c -replace $physHeaderRegex, $correctHeaderCss
            $changed = $true
        }
    }

    # Fix Chemistry Chapter 2 Nav link
    if ($f.FullName -match "chemistry\\chapter-2\\index.html") {
        $c = $c -replace '<a href="/notes/class-9/chemistry/" class="nav-btn">Back to Chemistry Hub.*?</a', '<a href="/notes/class-9/chemistry/chapter-3/" class="nav-btn">Chapter 3: Atomic Structure &rarr;</a'
        $changed = $true
    }

    # Fix CTA Colors
    $ctaCssRegex = '(?s)\.cta-box\{.*?\.cta-box p\{.*?\}'
    if ($c -match $ctaCssRegex) {
        $c = $c -replace $ctaCssRegex, $newCtaCss
        $changed = $true
    }

    if ($changed) {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($f.FullName, $c, $utf8NoBom)
        Write-Host "Processed $($f.FullName)"
    }
}
Write-Host "All fixes applied."
