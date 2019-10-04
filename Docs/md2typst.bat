@echo off
setlocal enabledelayedexpansion

for %%F in (*.md) do (
    set "filename=%%~nF"
    pandoc -f markdown -t typst "%%F" -o "!filename!.typ"
)
