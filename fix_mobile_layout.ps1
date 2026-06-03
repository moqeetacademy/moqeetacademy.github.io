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

                # Fix sidebar on mobile
                $pattern = '@media\s*\(\s*max-width\s*:\s*860px\s*\)\s*\{\s*\.page-layout\s*\{\s*grid-template-columns\s*:\s*1fr;?\s*\}\s*\.sidebar\s*\{\s*display\s*:\s*none;?\s*\}\s*\}'
                $replacement = '@media(max-width:860px){.page-layout{grid-template-columns:1fr}.sidebar{position:static;margin-top:32px}}'
                $content = [regex]::Replace($content, $pattern, $replacement)

                # Add responsive fixes before </style>
                if (-not $content.Contains("/* Mobile responsive fixes */")) {
                    $responsiveFixes = "`n    /* Mobile responsive fixes */`n    body { word-wrap: break-word; }`n    img, video { max-width: 100%; height: auto; }`n    .notes-table { display: block; overflow-x: auto; white-space: nowrap; }`n    .solution, pre { overflow-x: auto; }`n    mjx-container { max-width: 100%; overflow-x: auto; overflow-y: hidden; }`n    @media(max-width:480px){`n      .site-header{padding:12px 14px}`n      .header-container{gap:8px}`n      .header-container .logo a{font-size:1.15rem}`n      .header-cta .cta-btn-nav{padding:6px 12px;font-size:0.8rem}`n      .page-layout{padding:20px 14px}`n    }`n  </style>"
                    $content = $content.Replace("</style>", $responsiveFixes)
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
