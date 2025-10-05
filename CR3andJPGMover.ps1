# CR3andJPGMover.ps1
param(
  [Parameter(Mandatory=$true)]
  [string]$Path
)

# Validate path
$root = (Resolve-Path -Path $Path -ErrorAction Stop).Path
if (-not (Test-Path -LiteralPath $root -PathType Container)) {
  throw "Path not found or not a directory: $root"
}

# Dest folders
$cr3Dir = Join-Path $root "CR3"
$jpgDir = Join-Path $root "JPG"
foreach ($d in @($cr3Dir, $jpgDir)) {
  if (-not (Test-Path -LiteralPath $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
}

# Helper to avoid overwriting
function Get-UniquePath([string]$destPath) {
  if (-not (Test-Path -LiteralPath $destPath)) { return $destPath }
  $dir  = Split-Path -Parent $destPath
  $base = [IO.Path]::GetFileNameWithoutExtension($destPath)
  $ext  = [IO.Path]::GetExtension($destPath)
  $i = 1
  do {
    $candidate = Join-Path $dir "$base ($i)$ext"
    $i++
  } while (Test-Path -LiteralPath $candidate)
  return $candidate
}

# Move CR3 -> CR3\
Get-ChildItem -Path $root -File -Filter *.CR3 -ErrorAction SilentlyContinue | ForEach-Object {
  $dest = Get-UniquePath (Join-Path $cr3Dir $_.Name)
  if ($_.FullName -ieq $dest) { return }
  Move-Item -LiteralPath $_.FullName -Destination $dest
}

# Move JPG/JPEG -> JPG\   (FIX: don't use -Include; filter by extension instead)
Get-ChildItem -Path $root -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Extension -match '^\.jpe?g$' } |
  ForEach-Object {
    $dest = Get-UniquePath (Join-Path $jpgDir $_.Name)
    if ($_.FullName -ieq $dest) { return }
    Move-Item -LiteralPath $_.FullName -Destination $dest
  }

Write-Host "Done. CR3 files in '$cr3Dir', JPG/JPEG files in '$jpgDir'."
