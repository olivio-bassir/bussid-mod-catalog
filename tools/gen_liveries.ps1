Add-Type -AssemblyName System.Drawing
$OUT = 'd:\AGENTOVA\SAMY\bussid-mod-catalog\liveries'
New-Item -ItemType Directory -Force $OUT | Out-Null
$SZ = 2048

function C([int]$r, [int]$gr, [int]$b) { [System.Drawing.Color]::FromArgb(255, $r, $gr, $b) }

function Fill-Gradient($g, $c1, $c2, [single]$angle) {
    $rect = [System.Drawing.Rectangle]::new(0, 0, $SZ, $SZ)
    $br = [System.Drawing.Drawing2D.LinearGradientBrush]::new($rect, $c1, $c2, $angle)
    $g.FillRectangle($br, $rect)
    $br.Dispose()
}

function Diagonal-Bands($g, $c, [int]$count, [int]$width, [int]$alpha) {
    $b = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb($alpha, $c.R, $c.G, $c.B))
    for ($i = -1; $i -lt $count; $i++) {
        $x = $i * ($SZ / $count) * 1.6
        $pts = @(
            [System.Drawing.Point]::new([int]$x, $SZ),
            [System.Drawing.Point]::new([int]($x + $SZ * 0.9), 0),
            [System.Drawing.Point]::new([int]($x + $SZ * 0.9 + $width), 0),
            [System.Drawing.Point]::new([int]($x + $width), $SZ)
        )
        $g.FillPolygon($b, $pts)
    }
    $b.Dispose()
}

$schemes = @(
    @('sunset',   (C 255 61 87),  (C 255 154 0),   (C 255 255 255)),
    @('ocean',    (C 0 96 170),   (C 0 212 255),   (C 255 255 255)),
    @('jungle',   (C 12 92 40),   (C 170 220 50),  (C 255 255 255)),
    @('grape',    (C 74 20 140),  (C 224 64 251),  (C 255 255 255)),
    @('inferno',  (C 30 30 30),   (C 229 57 53),   (C 255 179 0)),
    @('ice',      (C 40 60 90),   (C 130 200 255), (C 255 255 255)),
    @('gold',     (C 20 20 20),   (C 197 160 60),  (C 255 224 130)),
    @('flamingo', (C 233 30 99),  (C 255 138 101), (C 255 255 255)),
    @('emerald',  (C 0 77 64),    (C 0 200 150),   (C 224 255 240)),
    @('midnight', (C 15 15 40),   (C 63 81 181),   (C 130 177 255)),
    @('lava',     (C 60 10 10),   (C 255 87 34),   (C 255 193 7)),
    @('mint',     (C 0 121 107),  (C 128 255 219), (C 255 255 255)),
    @('royal',    (C 26 35 126),  (C 92 107 192),  (C 255 214 0)),
    @('coral',    (C 255 82 82),  (C 255 171 145), (C 255 255 255)),
    @('steel',    (C 55 71 79),   (C 144 164 174), (C 236 239 241)),
    @('neon',     (C 10 10 20),   (C 0 230 118),   (C 0 176 255)),
    @('cherry',   (C 136 14 79),  (C 244 67 54),   (C 255 235 238)),
    @('sky',      (C 2 119 189),  (C 129 212 250), (C 255 255 255)),
    @('sand',     (C 121 85 72),  (C 215 204 200), (C 255 235 205)),
    @('violet',   (C 49 27 146),  (C 171 71 188),  (C 234 128 252))
)

foreach ($s in $schemes) {
    $name = $s[0]; $a = $s[1]; $b = $s[2]; $acc = $s[3]

    # Style 1 : dégradé + bandes diagonales
    $bmp = [System.Drawing.Bitmap]::new($SZ, $SZ)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    Fill-Gradient $g $a $b 40
    Diagonal-Bands $g $acc 5 90 70
    $g.Dispose()
    $bmp.Save((Join-Path $OUT "livery_${name}_bandes.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()

    # Style 2 : dégradé + grande vague
    $bmp = [System.Drawing.Bitmap]::new($SZ, $SZ)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    Fill-Gradient $g $b $a 90
    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $path.AddBezier(0, [int]($SZ * 0.55), [int]($SZ * 0.35), [int]($SZ * 0.35), [int]($SZ * 0.65), [int]($SZ * 0.75), $SZ, [int]($SZ * 0.5))
    $path.AddLine($SZ, $SZ)
    $path.AddLine(0, $SZ)
    $path.CloseFigure()
    $wave = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(230, $acc.R, $acc.G, $acc.B))
    $g.FillPath($wave, $path)
    $wave.Dispose()
    $g.Dispose()
    $bmp.Save((Join-Path $OUT "livery_${name}_vague.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
}

(Get-ChildItem $OUT -Filter 'livery_*.png' | Measure-Object).Count
