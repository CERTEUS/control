Param(
  [Parameter(ValueFromRemainingArguments=$true)] [string[]] $Args
)
$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$target = Join-Path $root 'certeus\tools\windows\setup-git-safety.ps1'
if (-not (Test-Path $target)) {
  Write-Error "Nie znaleziono $target"
  exit 2
}
& $target @Args
