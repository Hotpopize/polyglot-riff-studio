@echo off
title Polyglot Sales & Riff Studio — Full-Stack Launcher
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_polyglot_stack.ps1"
if errorlevel 1 (
  start "" "%~dp0index.html"
)
