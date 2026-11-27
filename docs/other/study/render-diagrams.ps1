param([string]$ChromePath = 'C:\Program Files\Google\Chrome\Application\chrome.exe')
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$toolRoot = Join-Path $repoRoot '.venv/diagram-tools'
$cli = Join-Path $toolRoot 'node_modules/.bin/mmdc.cmd'
if (-not (Test-Path -LiteralPath $ChromePath)) { throw 'Set -ChromePath to an installed Chrome or Edge executable.' }
if (-not (Test-Path -LiteralPath $cli)) {
    & npm.cmd install --prefix $toolRoot '@mermaid-js/mermaid-cli@12.0.0' --ignore-scripts --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw 'Mermaid CLI installation failed' }
}
$config = Join-Path $toolRoot 'puppeteer.json'
@{ executablePath = $ChromePath; headless = $true } | ConvertTo-Json | Set-Content -LiteralPath $config -Encoding ASCII
foreach ($diagram in @('database', 'question_crud', 'search')) {
    foreach ($format in @('svg', 'png')) {
        & $cli -i (Join-Path $PSScriptRoot "$diagram.mmd") -o (Join-Path $PSScriptRoot "$diagram.$format") -p $config -b white --size 2200 -s 2 --no-font-embed
        if ($LASTEXITCODE -ne 0) { throw "Could not render $diagram.$format" }
    }
}
