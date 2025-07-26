# CR3_JPG_Sorter
Sorts Canon RAW (.CR3) and JPEG files into separate folders via PowerShell


# CR3 and JPG Sorter for Canon Files

A simple PowerShell script to move `.CR3` (RAW) and `.JPG` files into their own folders.

## 🤔 Why This Exists

As a photographer and media coordinator, I regularly import hundreds of photos and RAW files from Canon DSLRs. Manually separating `.CR3` (RAW) and `.JPG` files takes time and risks errors. This script makes that workflow instant, reliable, and repeatable.

I built it to streamline sorting after events like church services, VBS, or photo shoots — and now I’m sharing it to help others save time too.

Built by [EmRamos](https://github.com/EmRamos) to serve content creators, church tech teams, and photo pros who want automation without complexity.

## Features

- Prompts for image folder
- Asks whether to create subfolders or use custom paths
- Logs failures with reasons
- Works on Windows

## How to Use

1. Download `CR3andJPGSorter.ps1`
2. Right-click > Run with PowerShell  
   *OR* open PowerShell and run:

## ⚠️ Requirements

This script is intended for users who are comfortable using PowerShell. You should be familiar with:

- Navigating directories in PowerShell
- Running scripts (e.g., `.\CR3andJPGSorter.ps1`)
- Handling execution policies (like using `Set-ExecutionPolicy RemoteSigned` if needed)

This script does **not** include a GUI — it runs entirely in a PowerShell terminal with prompts and text feedback.


```powershell
.\CR3andJPGSorter.ps1


