$basePaths = @(
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry",
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics"
)

$updatedCount = 0

foreach ($basePath in $basePaths) {
    if (Test-Path $basePath) {
        $folders = Get-ChildItem -Path $basePath -Directory | Where-Object { $_.Name -like "chapter-*" }
        foreach ($folder in $folders) {
            $filePath = Join-Path $folder.FullName "index.html"
            if (Test-Path $filePath) {
                $content = [IO.File]::ReadAllText($filePath)
                $originalContent = $content

                # Replace HTML class
                $content = [regex]::Replace($content, '(<div class="header-cta">\s*<a[^>]+class=")cta-btn(")', '${1}cta-btn-nav${2}')

                # Replace CSS if media query is missing
                if (-not $content.Contains("@media(max-width:700px){.main-nav{display:none}}")) {
                    $pattern = '\.header-cta \.cta-btn\{[^}]+\}'
                    $replacement = ".header-cta .cta-btn-nav{background:var(--gold);color:#fff;padding:8px 18px;border-radius:6px;font-size:.85rem;font-weight:600;white-space:nowrap;text-decoration:none;display:inline-block}`n    .header-cta .cta-btn-nav:hover{background:#b8860b;text-decoration:none;color:#fff}`n    @media(max-width:700px){.main-nav{display:none}}"
                    $content = [regex]::Replace($content, $pattern, $replacement)
                }

                if ($content -cne $originalContent) {
                    [IO.File]::WriteAllText($filePath, $content)
                    $updatedCount++
                }
            }
        }
    }
}

Write-Host "Updated $updatedCount files."
