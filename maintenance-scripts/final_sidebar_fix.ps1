$basePaths = @(
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry",
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics",
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\computer-science"
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

                # 1. Bump breakpoint to 1024px and ensure sidebar is at bottom (not hidden)
                $pattern = '@media\s*\(\s*max-width\s*:\s*860px\s*\)\s*\{\s*(\.page-layout(?:,\.main-container)?)\s*\{\s*grid-template-columns\s*:\s*1fr;?\s*\}\s*\.sidebar\s*\{\s*(?:display\s*:\s*none|position\s*:\s*static;\s*margin-top\s*:\s*32px);?\s*\}\s*\}'
                $replacement = '@media(max-width:1024px){${1}{grid-template-columns:1fr} .sidebar{position:static;margin-top:32px}}'
                $content = [regex]::Replace($content, $pattern, $replacement)

                # 2. Add min-width: 0 to main-content to prevent grid blow-out
                if (-not $content.Contains(".main-content { min-width: 0; }")) {
                    $content = $content.Replace("/* Mobile responsive fixes */", "/* Mobile responsive fixes */`n    .main-content { min-width: 0; }")
                }

                if ($content -cne $originalContent) {
                    [IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
                    $updatedCount++
                }
            }
        }
    }
}

Write-Host "Updated $updatedCount files."
