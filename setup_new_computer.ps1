# Quick setup script for running this project on a new computer
# Usage: .\setup_new_computer.ps1

param(
    [string]$RepoUrl = ""
)

Write-Host "🚀 Setting up recruitment workflow on new computer..." -ForegroundColor Cyan
Write-Host ""

# Check if repo URL provided
if ([string]::IsNullOrWhiteSpace($RepoUrl)) {
    Write-Host "⚠️  No repo URL provided. Usage:" -ForegroundColor Yellow
    Write-Host "   .\setup_new_computer.ps1 -RepoUrl 'https://github.com/yourusername/your-repo.git'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or clone manually:" -ForegroundColor Yellow
    Write-Host "   git clone <your-repo-url>" -ForegroundColor Yellow
    exit 1
}

# Clone repo
if (-not (Test-Path "money-curs-proj")) {
    Write-Host "📥 Cloning repository..." -ForegroundColor Green
    git clone $RepoUrl money-curs-proj
    Set-Location money-curs-proj
} else {
    Write-Host "📁 Repository exists. Updating..." -ForegroundColor Green
    Set-Location money-curs-proj
    git pull
}

# Check Python
Write-Host ""
Write-Host "🐍 Checking Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Install Python 3.11+ from python.org" -ForegroundColor Red
    exit 1
}

# Create venv
Write-Host ""
Write-Host "📦 Creating virtual environment..." -ForegroundColor Cyan
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "   ✅ Created .venv" -ForegroundColor Green
} else {
    Write-Host "   ✅ .venv already exists" -ForegroundColor Green
}

# Activate venv
Write-Host ""
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host ""
Write-Host "📚 Installing dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

# Setup .env
Write-Host ""
if (-not (Test-Path ".env")) {
    Write-Host "⚙️  Setting up .env file..." -ForegroundColor Cyan
    if (Test-Path ".env.example") {
        Copy-Item .env.example .env
        Write-Host "   ✅ Created .env from .env.example" -ForegroundColor Green
        Write-Host "   ⚠️  IMPORTANT: Edit .env and add your API keys!" -ForegroundColor Yellow
    } else {
        Write-Host "   ⚠️  No .env.example found. Create .env manually." -ForegroundColor Yellow
    }
} else {
    Write-Host "   ✅ .env already exists" -ForegroundColor Green
}

# Check if output/agents exist (generated code)
Write-Host ""
if (-not (Test-Path "output\agents")) {
    Write-Host "⚠️  No generated agents found. Run the pipeline first:" -ForegroundColor Yellow
    Write-Host "   python run_pipeline.py" -ForegroundColor Yellow
    Write-Host "   (This generates output/agents/ and output/master_graph.py)" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Generated agents found" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env and add your API keys (GEMINI_API_KEY, ANTHROPIC_API_KEY)" -ForegroundColor White
Write-Host "2. If needed, run: python run_pipeline.py (generates agents)" -ForegroundColor White
Write-Host "3. Run Chainlit: chainlit run app.py -w" -ForegroundColor White
Write-Host "4. Or use Railway URL (if deployed): https://your-app.up.railway.app" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: Deploy to Railway once, then access from any browser!" -ForegroundColor Yellow
Write-Host "   See QUICK_START_REMOTE.md for details." -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
