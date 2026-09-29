param([switch]$RunTests)
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$pythonExe = Join-Path $repoRoot '.venv/Scripts/python.exe'
$demoEnv = Join-Path $repoRoot '.env.study'

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program failed with exit code $LASTEXITCODE" }
}

if (-not (Test-Path -LiteralPath $pythonExe)) {
    Invoke-Checked 'python' @('-m', 'venv', (Join-Path $repoRoot '.venv'))
}
Invoke-Checked $pythonExe @('-m', 'pip', 'install', '-r', (Join-Path $PSScriptRoot 'requirements.txt'))

if (-not (Test-Path -LiteralPath $demoEnv)) {
    # This file is covered by the existing .env.* Git ignore rule.
    $secret = & $pythonExe -c 'import secrets; print(secrets.token_urlsafe(48))'
    if ($LASTEXITCODE -ne 0) { throw 'Could not generate local secret' }
    $password = & $pythonExe -c 'import secrets; print(secrets.token_urlsafe(32))'
    if ($LASTEXITCODE -ne 0) { throw 'Could not generate database password' }
    @(
        'STACK_UNDERFLOW_ENV_ID=local'
        "STACK_UNDERFLOW_SECRET_KEY=$secret"
        'DB_NAME=stack_underflow_study'
        'DB_USER=study'
        "DB_PASSWORD=$password"
        'DB_HOST=127.0.0.1'
        'DB_PORT=55432'
        'USE_REDIS=False'
    ) | Set-Content -LiteralPath $demoEnv -Encoding ASCII
}

Invoke-Checked 'docker' @('compose', '--env-file', $demoEnv, '-f', (Join-Path $PSScriptRoot 'compose.yml'), 'up', '-d', '--wait', 'db')
$demoArguments = @((Join-Path $PSScriptRoot 'verify_demo.py'))
if ($RunTests) { $demoArguments += '--tests' }
Invoke-Checked $pythonExe $demoArguments
Get-Content -Raw -Encoding UTF8 (Join-Path $PSScriptRoot 'check_tables.sql') |
    & docker compose --env-file $demoEnv -f (Join-Path $PSScriptRoot 'compose.yml') exec -T db psql -X -U study -d stack_underflow_study -v ON_ERROR_STOP=1 -P pager=off |
    Set-Content -LiteralPath (Join-Path $PSScriptRoot 'psql_results.txt') -Encoding UTF8
if ($LASTEXITCODE -ne 0) { throw 'Direct psql verification failed' }
Write-Host "Results: $PSScriptRoot/sql_results.md"
