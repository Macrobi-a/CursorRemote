# PowerShell version: Quick deploy for remote access
# Usage: .\deploy_remote.ps1

Write-Host "🚀 Deploying recruitment workflow for remote access..." -ForegroundColor Cyan
Write-Host ""

# Check if git repo exists
if (-not (Test-Path .git)) {
    Write-Host "⚠️  Not a git repo. Initializing..." -ForegroundColor Yellow
    git init
    Write-Host "📝 Add your GitHub remote: git remote add origin <your-repo-url>" -ForegroundColor Yellow
    Write-Host "Then run this script again."
    exit 1
}

# Check if Railway CLI is installed
if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# Push to GitHub (if remote exists)
try {
    $remote = git remote get-url origin 2>$null
    if ($remote) {
        Write-Host "📤 Pushing to GitHub..." -ForegroundColor Green
        git add .
        git commit -m "Deploy for remote access" 2>$null
        git push origin main 2>$null
        if ($LASTEXITCODE -ne 0) {
            git push origin master 2>$null
        }
    }
} catch {
    Write-Host "⚠️  No GitHub remote found. Add one:" -ForegroundColor Yellow
    Write-Host "   git remote add origin <your-repo-url>"
    Write-Host "   Then push manually: git push -u origin main"
}

# Deploy to Railway
Write-Host ""
Write-Host "🚂 Deploying to Railway..." -ForegroundColor Cyan
try {
    railway status 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Railway project linked. Deploying..." -ForegroundColor Green
        railway up
    } else {
        throw "Not linked"
    }
} catch {
    Write-Host "🔗 Linking Railway project..." -ForegroundColor Yellow
    railway login
    railway init
    Write-Host "📝 Set environment variables in Railway dashboard:" -ForegroundColor Yellow
    Write-Host "   - GEMINI_API_KEY"
    Write-Host "   - ANTHROPIC_API_KEY"
    Write-Host "   - INSTANTLY_API_KEY (optional)"
    Write-Host "   - HEYGEN_API_KEY (optional)"
    Write-Host "   - STRIPE_SECRET_KEY (optional)"
    Write-Host ""
    Write-Host "Then run: railway up" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Done! Your Chainlit UI will be available at: https://your-app.up.railway.app" -ForegroundColor Green
Write-Host "   Access it from any computer — just open the URL in a browser." -ForegroundColor Green
