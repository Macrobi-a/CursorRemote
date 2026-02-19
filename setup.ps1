# Setup script for Course-to-Agents pipeline (PowerShell)
# Run: .\setup.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# 1. Create venv if it doesn't exist
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# 2. Activate and install (run in same process so activation applies)
Write-Host "Activating venv and installing requirements..."
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. .env
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example - please edit .env and set GEMINI_API_KEY and ANTHROPIC_API_KEY"
} else {
    Write-Host ".env already exists."
}

Write-Host "Setup done. To run the pipeline: .\.venv\Scripts\Activate.ps1; python run_pipeline.py"
