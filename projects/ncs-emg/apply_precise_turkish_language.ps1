$ErrorActionPreference = "Stop"

$workspaceRoot = (Get-Location).Path
$replacementSource = Join-Path $workspaceRoot "apply_precise_turkish_language.mjs"
$targetRoots = @(
    (Join-Path $workspaceRoot "animations"),
    "C:\Users\uugur\OneDrive\Desktop\EMG_NCS_Nonfizyolojik_Faktorler_Sunumu_FIXED_2026-07-31"
)

$pairs = @()
foreach ($line in Get-Content -LiteralPath $replacementSource -Encoding UTF8) {
    if ($line -match '^\s+\[".*", ".*"\],?\s*$') {
        $json = $line.Trim()
        if ($json.EndsWith(",")) {
            $json = $json.Substring(0, $json.Length - 1)
        }
        $pair = $json | ConvertFrom-Json
        $pairs += ,@([string]$pair[0], [string]$pair[1])
    }
}

$counts = @{}
foreach ($pair in $pairs) {
    $counts[$pair[0]] = 0
}

$changedFiles = @()
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

foreach ($targetRoot in $targetRoots) {
    if (-not (Test-Path -LiteralPath $targetRoot -PathType Container)) {
        continue
    }

    foreach ($file in Get-ChildItem -LiteralPath $targetRoot -Recurse -File -Filter "*.html") {
        $original = [System.IO.File]::ReadAllText($file.FullName)
        $updated = $original
        $fileCount = 0

        foreach ($pair in $pairs) {
            $from = $pair[0]
            $to = $pair[1]
            $hits = ([regex]::Matches($updated, [regex]::Escape($from))).Count
            if ($hits -eq 0) {
                continue
            }
            $updated = $updated.Replace($from, $to)
            $counts[$from] += $hits
            $fileCount += $hits
        }

        if ($updated -ne $original) {
            [System.IO.File]::WriteAllText($file.FullName, $updated, $utf8NoBom)
            $changedFiles += [pscustomobject]@{
                File = $file.FullName
                Replacements = $fileCount
            }
        }
    }
}

$unmatched = @($pairs | ForEach-Object { $_[0] } | Where-Object { $counts[$_] -eq 0 })
$totalReplacements = ($counts.Values | Measure-Object -Sum).Sum

[pscustomobject]@{
    TargetRoots = $targetRoots
    ChangedFileCount = $changedFiles.Count
    TotalReplacements = $totalReplacements
    ChangedFiles = $changedFiles
    Unmatched = $unmatched
} | ConvertTo-Json -Depth 6
