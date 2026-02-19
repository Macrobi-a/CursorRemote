#!/bin/bash
# Quick deploy script: push to GitHub and deploy to Railway
# Usage: ./deploy_remote.sh

set -e

echo "🚀 Deploying recruitment workflow for remote access..."
echo ""

# Check if git repo exists
if [ ! -d .git ]; then
    echo "⚠️  Not a git repo. Initializing..."
    git init
    echo "📝 Add your GitHub remote: git remote add origin <your-repo-url>"
    echo "Then run this script again."
    exit 1
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Push to GitHub (if remote exists)
if git remote get-url origin &> /dev/null; then
    echo "📤 Pushing to GitHub..."
    git add .
    git commit -m "Deploy for remote access" || echo "No changes to commit"
    git push origin main || git push origin master || echo "Push failed (check your remote)"
else
    echo "⚠️  No GitHub remote found. Add one:"
    echo "   git remote add origin <your-repo-url>"
    echo "   Then push manually: git push -u origin main"
fi

# Deploy to Railway
echo ""
echo "🚂 Deploying to Railway..."
if railway status &> /dev/null; then
    echo "✅ Railway project linked. Deploying..."
    railway up
else
    echo "🔗 Linking Railway project..."
    railway login
    railway init
    echo "📝 Set environment variables in Railway dashboard:"
    echo "   - GEMINI_API_KEY"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - INSTANTLY_API_KEY (optional)"
    echo "   - HEYGEN_API_KEY (optional)"
    echo "   - STRIPE_SECRET_KEY (optional)"
    echo ""
    echo "Then run: railway up"
fi

echo ""
echo "✅ Done! Your Chainlit UI will be available at: https://your-app.up.railway.app"
echo "   Access it from any computer — just open the URL in a browser."
