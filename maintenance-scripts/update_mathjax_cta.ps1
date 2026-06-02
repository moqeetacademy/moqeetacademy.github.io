$paths = @(
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry\chapter-*\index.html",
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics\chapter-*\index.html"
)

$files = Get-ChildItem -Path $paths

$mathJaxScript = @'
  <script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']]
    }
  };
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
'@

foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName)
    $changed = $false

    # 1. Add MathJax if not present
    if ($c -notmatch "MathJax-script") {
        $c = $c -replace "</head>", $mathJaxScript
        $changed = $true
    }

    # 2. Move Premium CTA before Long Questions
    $premRegex = '(?s)\s*<div class="cta-box premium">.*?</div>'
    if ($c -match $premRegex) {
        $premContent = $matches[0].Trim()
        
        # Remove all instances of Premium CTA
        $c = $c -replace $premRegex, ""
        
        # Insert it before Long Questions heading
        if ($c -match '(<h2 class="section-heading">Long)') {
            $c = $c -replace '(<h2 class="section-heading">Long)', ("`n`n    " + $premContent + "`n`n    `$1")
            $changed = $true
        } else {
            # Fallback to before short or chapter-nav
            if ($c -match '(<h2 class="section-heading">Short)') {
                $c = $c -replace '(<h2 class="section-heading">Short)', ("`n`n    " + $premContent + "`n`n    `$1")
            } else {
                $c = $c -replace '(<nav class="chapter-nav")', ("`n`n    " + $premContent + "`n`n    `$1")
            }
            $changed = $true
        }
    }

    if ($changed) {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($f.FullName, $c, $utf8NoBom)
        Write-Host "Processed $($f.FullName)"
    }
}
Write-Host "Update completed."
