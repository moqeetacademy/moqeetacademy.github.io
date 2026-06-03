$files = @{
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry\chapter-10\index.html" = @(
        @{
            old = '<p><strong>Definition:</strong> <div class="definition-box"></div><div class="definition-box">An Arrhenius acid is a substance that ionizes when dissolved in water to increase the concentration of hydrogen ions ($H^+$).</div></p>'
            new = '<div class="definition-box"><strong>Definition:</strong> An Arrhenius acid is a substance that ionizes when dissolved in water to increase the concentration of hydrogen ions ($H^+$).</div>'
        }
    )
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry\chapter-15\index.html" = @(
        @{
            old = '<p><strong>Definition:</strong> <div class="definition-box"></div><div class="definition-box">Lipids comprise a diverse group of naturally occurring organic macromolecules that share a distinctive physical property: they are completely insoluble in polar solvents like water, but readily dissolve in non-polar organic solvents such as chloroform, benzene, and ether. Chemically, they include esters of long-chain fatty acids joined with glycerol, presenting commonly as solid fats, liquid oils, and structural waxes.</div></p>'
            new = '<div class="definition-box"><strong>Definition:</strong> Lipids comprise a diverse group of naturally occurring organic macromolecules that share a distinctive physical property: they are completely insoluble in polar solvents like water, but readily dissolve in non-polar organic solvents such as chloroform, benzene, and ether. Chemically, they include esters of long-chain fatty acids joined with glycerol, presenting commonly as solid fats, liquid oils, and structural waxes.</div>'
        }
    )
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics\chapter-3\index.html" = @(
        @{
            old = '<p><strong>Definition:</strong> <div class="definition-box"></div><div class="definition-box">Momentum is a measurement of the quantity of motion possessed by a moving object. It is the product of the mass of the body and its velocity.</div></p>'
            new = '<div class="definition-box"><strong>Definition:</strong> Momentum is a measurement of the quantity of motion possessed by a moving object. It is the product of the mass of the body and its velocity.</div>'
        }
    )
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\physics\chapter-5\index.html" = @(
        @{
            old = '<li><strong>Definition:</strong> <div class="definition-box"></div><div class="definition-box">The stiffness of a spring — the magnitude of force required to produce a unit extension or compression.</li>'
            new = '<li><div class="definition-box"><strong>Definition:</strong> The stiffness of a spring — the magnitude of force required to produce a unit extension or compression.</div></li>'
        },
        @{
            old = '<p class="question">Q3. Draw and explain the force-extension graph for elastic solids.</div></p>'
            new = '<p class="question">Q3. Draw and explain the force-extension graph for elastic solids.</p>'
        }
    )
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\chemistry\chapter-3\index.html" = @(
        @{
            old = '<td><strong>Definition</strong><div class="definition-box"></div><div class="definition-box"></td>'
            new = '<td><strong>Definition</strong></td>'
        },
        @{
            old = '<p class="question">Q(iii): An atom has 2 electrons in K shell, 8 electrons in L shell, and 3 electrons in M shell. Write down its electronic configuration.</div></p>'
            new = '<p class="question">Q(iii): An atom has 2 electrons in K shell, 8 electrons in L shell, and 3 electrons in M shell. Write down its electronic configuration.</p>'
        }
    )
    "c:\Users\Asfi\Desktop\MoqeetAcademy\notes\class-9\computer-science\chapter-3\index.html" = @(
        @{
            old = '<td><strong>Definition</strong><div class="definition-box"></div><div class="definition-box"></td>'
            new = '<td><strong>Definition</strong></td>'
        },
        @{
            old = '<p>The <code>href</code> attribute in HTML stands for <strong>"Hypertext Reference"</strong> and is used to specify the destination URL of a hyperlink.</div></p>'
            new = '<p>The <code>href</code> attribute in HTML stands for <strong>"Hypertext Reference"</strong> and is used to specify the destination URL of a hyperlink.</p>'
        }
    )
}

$updatedCount = 0

foreach ($file in $files.Keys) {
    if (Test-Path $file) {
        $content = [IO.File]::ReadAllText($file)
        $original = $content
        foreach ($replacement in $files[$file]) {
            $content = $content.Replace($replacement.old, $replacement.new)
        }
        if ($content -cne $original) {
            [IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
            $updatedCount++
        }
    }
}

Write-Host "Updated $updatedCount files."
