---
name: deploy-github-vercel
description: >
  Despliega un proyecto web estático con flujo GitHub-first: cada cambio
  se commitea, pushea a GitHub, y Vercel auto-despliega vía webhook.
  Usar cuando el usuario diga "subir a GitHub", "deploy a Vercel", "publicar
  la web", "haz el deploy", "sube cambios", "actualiza producción", o
  cualquier variante. Setup one-time, después un solo comando para deploy.
---

# Deploy GitHub-first → Vercel auto-deploy

Flujo definitivo:
**editas → `/deploy` → commit + push a GitHub → Vercel detecta el push → producción actualizada en ~30s**

GitHub es la fuente de verdad. Vercel es solo el espejo desplegado.

---

## Setup inicial — UNA SOLA VEZ por proyecto

```bash
bash .claude/scripts/setup-deploy.sh
```

Este script hace, en orden:
1. **`gh auth login`** si no estás logueado en GitHub
2. **`vercel login`** si no estás logueado en Vercel
3. **`git init`** si el proyecto no es un repo
4. **`gh repo create`** crea el repo público en GitHub y hace el push inicial
5. **`vercel link`** + **`vercel git connect`** conecta el proyecto Vercel con el repo GitHub (esto es lo que activa el auto-deploy)

Tras esto, las credenciales quedan persistidas y la conexión GitHub↔Vercel está activa para siempre.

---

## Cada deploy posterior

```bash
bash .claude/scripts/deploy.sh "mensaje del commit"
```

O desde Claude Code: `/deploy "mensaje"`

El script:
1. Detecta cambios y los commitea con el mensaje (si pasas uno) o `Update YYYY-MM-DD`
2. Hace `git push origin main`
3. Vercel detecta el push automáticamente y despliega (~30 seg)

**No se llama nunca más a `vercel --prod` manualmente.** Todo va por GitHub.

---

## Cómo lo invoca Claude

Cuando el usuario pide deploy:

1. Verificar que `setup-deploy.sh` se haya ejecutado (existe `.git`, `git remote get-url origin` funciona, `.vercel/project.json` existe).
2. Si NO está configurado, ejecutar `setup-deploy.sh` (esto bloquea pidiendo OAuth — el usuario completa el login en navegador).
3. Si SÍ está configurado, ejecutar `deploy.sh` con un mensaje descriptivo del commit.
4. Reportar las URLs (las imprime el script).

**No pedir confirmación** — el usuario ya pidió el deploy.

---

## Por qué este flujo y no `vercel --prod` directo

| `vercel --prod` directo | GitHub → Vercel auto-deploy |
|---|---|
| Sin historial Git | Cada cambio en commits visibles |
| Vercel CLI necesita estar autenticado en cada máquina | Solo necesitas Git |
| Difícil revertir | `git revert` y push deshace en producción |
| No hay PRs ni preview deployments | Vercel hace preview por cada PR |
| Solo el creador puede deployar | Cualquier colaborador con acceso al repo |

---

## Verificar el estado de un deploy

```bash
npx vercel ls               # últimos deploys
npx vercel inspect <url>    # detalle de uno concreto
gh repo view --web          # abre el repo en navegador
```

---

## Errores comunes

| Síntoma | Solución |
|---|---|
| `setup-deploy.sh` cuelga en `gh auth login` | El navegador no se abrió. Copiar URL manualmente: https://github.com/login/device |
| `vercel git connect` falla | Hacerlo desde el dashboard: vercel.com/dashboard → proyecto → Settings → Git → Connect Git Repository |
| `git push` rechaza con conflictos | El repo remoto cambió. `git pull --rebase origin main` antes |
| Vercel build falla | Dashboard → proyecto → Settings → Build → Framework Preset = "Other" |
| Push pasó pero Vercel no despliega | Comprobar webhook: vercel.com → proyecto → Settings → Git → Repository (debería decir "Connected") |

---

## Archivos de la automatización

- `.claude/scripts/setup-deploy.sh` — setup one-time
- `.claude/scripts/deploy.sh` — deploy de cada cambio
- `.claude/commands/deploy.md` — slash command `/deploy`
- `.gitignore` — excluye node_modules, .vercel, screenshots, vídeo original pesado
