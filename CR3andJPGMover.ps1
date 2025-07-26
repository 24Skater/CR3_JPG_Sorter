# Sort-RawAndJpeg.ps1
# Author: EmRamos
# Function: Move .CR3 (RAW) and .JPG/.JPEG files to destination folders, interactively

Clear-Host
Write-Host "🔁 Canon Image Sorter Script - by EmRamos" -ForegroundColor Cyan
Write-Host ""

# Prompt: Source path
$sourcePath = Read-Host "📁 Enter the path where all the images are located"
if (-not (Test-Path $sourcePath)) {
    Write-Host "❌ The source path '$sourcePath' does not exist. Exiting." -ForegroundColor Red
    exit
}

# Ask: Do you want to create RAW/JPG folders under the source path?
$useAutoFolders = Read-Host "🗂️  Do you want to create RAW and JPG subfolders under the source path? (Y/N)"

if ($useAutoFolders -match "^(Y|y)") {
    $rawPath = Join-Path $sourcePath "RAW"
    $jpgPath = Join-Path $sourcePath "JPG"

    if (-not (Test-Path $rawPath)) {
        New-Item -Path $rawPath -ItemType Directory | Out-Null
        Write-Host "✅ Created RAW folder at $rawPath"
    }

    if (-not (Test-Path $jpgPath)) {
        New-Item -Path $jpgPath -ItemType Directory | Out-Null
        Write-Host "✅ Created JPG folder at $jpgPath"
    }
}
else {
    # Prompt: Ask for RAW and JPG paths manually
    $rawPath = Read-Host "📂 Enter the full path where you want to store RAW (.CR3) files"
    $jpgPath = Read-Host "📂 Enter the full path where you want to store JPG (.JPG/.JPEG) files"

    foreach ($path in @($rawPath, $jpgPath)) {
        if (-not (Test-Path $path)) {
            Write-Host "❌ Path '$path' does not exist. Please create it manually and re-run." -ForegroundColor Red
            exit
        }
    }
}

# Prepare log file
$logFile = Join-Path $sourcePath "move_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
Write-Host "`n📄 Logging failures to: $logFile"

# Move files
$rawExtensions = @("*.CR3")
$jpgExtensions = @("*.JPG", "*.JPEG")

$filesMoved = 0
$errors = 0

function Move-Files {
    param (
        [string]$filter,
        [string]$destination
    )

    Get-ChildItem -Path $sourcePath -Filter $filter -File -ErrorAction SilentlyContinue | ForEach-Object {
        $file = $_
        try {
            $destFile = Join-Path $destination $file.Name
            Move-Item -Path $file.FullName -Destination $destFile -ErrorAction Stop
            Write-Host "✅ Moved: $($file.Name)" -ForegroundColor Green
            $script:filesMoved++
        }
        catch {
            $errorMessage = "❌ FAILED: $($file.Name) → $($_.Exception.Message)"
            Add-Content -Path $logFile -Value $errorMessage
            Write-Host $errorMessage -ForegroundColor Red
            $script:errors++
        }
    }
}

Write-Host "`n📂 Moving RAW files (.CR3)..."
foreach ($ext in $rawExtensions) { Move-Files -filter $ext -destination $rawPath }

Write-Host "`n📂 Moving JPG files (.JPG/.JPEG)..."
foreach ($ext in $jpgExtensions) { Move-Files -filter $ext -destination $jpgPath }

# Summary
Write-Host "`n✅ Done! Files moved: $filesMoved"
if ($errors -gt 0) {
    Write-Host "⚠️  Failures: $errors (see log file for details)"
} else {
    Write-Host "🎉 No errors encountered." -ForegroundColor Green
}
