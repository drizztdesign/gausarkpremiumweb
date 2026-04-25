#!/usr/bin/env bash
# Setup inicial — UNA SOLA VEZ por proyecto.
# Conecta GitHub ↔ Vercel para que cada `git push` haga deploy automático.

set -e
export PATH="/c/Program Files/GitHub CLI:$PATH"

REPO_NAME="$(basename "$(pwd)")"

echo "═══════════════════════════════════════════════════════"
echo "  Setup: GitHub ↔ Vercel auto-deploy"
echo "═══════════════════════════════════════════════════════"

# ---- 1. GitHub login ----
if gh auth status >/dev/null 2>&1; then
  echo "✓ GitHub autenticado: $(gh api user --jq .login)"
else
  echo ""
  echo "→ Login GitHub (UNA vez por máquina)"
  echo "  Se abrirá el navegador, pega el código de un solo uso."
  gh auth login --hostname github.com --git-protocol https --web
fi

# ---- 2. Vercel login ----
if npx -y vercel whoami >/dev/null 2>&1; then
  echo "✓ Vercel autenticado: $(npx -y vercel whoami 2>&1 | tail -1)"
else
  echo ""
  echo "→ Login Vercel"
  npx -y vercel login
fi

# ---- 3. Git init si hace falta ----
if [ ! -d .git ]; then
  echo ""
  echo "→ Inicializando git…"
  git init -b main
  git add .
  git commit -m "Initial commit"
fi

# ---- 4. Crear repo en GitHub si no existe ----
if ! git remote get-url origin >/dev/null 2>&1; then
  echo ""
  echo "→ Creando repo en GitHub: $REPO_NAME (público)…"
  gh repo create "$REPO_NAME" --public --source=. --push
else
  echo "✓ Remote 'origin' ya configurado: $(git remote get-url origin)"
fi

GH_USER="$(gh api user --jq .login)"
GH_REPO="$GH_USER/$REPO_NAME"

# ---- 5. Conectar Vercel ↔ GitHub ----
echo ""
echo "→ Conectando proyecto Vercel al repo GitHub…"
if [ ! -d .vercel ]; then
  npx -y vercel link --yes --project "$REPO_NAME" 2>&1 | tail -3
fi
npx -y vercel git connect "https://github.com/$GH_REPO" --yes 2>&1 | tail -3 || true

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✓ Setup completo"
echo "═══════════════════════════════════════════════════════"
echo "  Repo:    https://github.com/$GH_REPO"
echo "  Vercel:  https://$REPO_NAME.vercel.app"
echo ""
echo "  A partir de ahora, para desplegar:"
echo "       bash .claude/scripts/deploy.sh \"mensaje\""
echo "  o desde Claude Code:  /deploy \"mensaje\""
echo "═══════════════════════════════════════════════════════"
