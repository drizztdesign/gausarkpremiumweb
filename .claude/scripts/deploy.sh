#!/usr/bin/env bash
# Deploy: commit cambios → push a GitHub → Vercel auto-despliega vía webhook.
# Pre-requisito: ejecutar setup-deploy.sh UNA vez antes.
# Uso: bash .claude/scripts/deploy.sh ["mensaje del commit"]

set -e
export PATH="/c/Program Files/GitHub CLI:$PATH"

REPO_NAME="$(basename "$(pwd)")"
COMMIT_MSG="${1:-Update $(date +%Y-%m-%d)}"

echo "═══════════════════════════════════════════════════════"
echo "  Deploy: $REPO_NAME"
echo "═══════════════════════════════════════════════════════"

# ---- Pre-flight ----
if ! gh auth status >/dev/null 2>&1; then
  echo "✗ Setup no completado. Ejecuta primero:"
  echo "    bash .claude/scripts/setup-deploy.sh"
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "✗ Repo no enlazado a GitHub. Ejecuta primero:"
  echo "    bash .claude/scripts/setup-deploy.sh"
  exit 1
fi

# ---- Commit cambios pendientes ----
if [ -n "$(git status --porcelain)" ]; then
  echo ""
  echo "→ Commit: \"$COMMIT_MSG\""
  git add .
  git commit -m "$COMMIT_MSG"
else
  echo "✓ Nada que commitear (working tree limpio)"
fi

# ---- Push a GitHub ----
echo ""
echo "→ Push a GitHub (origin/main)…"
git push origin main 2>&1 | tail -3

GH_USER="$(gh api user --jq .login)"
echo "✓ GitHub: https://github.com/$GH_USER/$REPO_NAME"

# ---- Vercel auto-despliega ----
echo ""
echo "→ Vercel detectará el push y desplegará automáticamente."
echo "  Tarda ~30 seg. Comprobar estado:"
echo "    npx vercel ls"
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✓ Push completado"
echo "  Producción:  https://$REPO_NAME.vercel.app"
echo "═══════════════════════════════════════════════════════"
