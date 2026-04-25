---
name: deploy-github-vercel
description: >
  Sube un proyecto web estático a GitHub y lo despliega en Vercel en producción.
  Usar cuando el usuario diga "subir a GitHub", "deploy a Vercel", "publicar la
  web", "subir a producción", "publica esto", "haz el deploy", o cualquier
  variante. Maneja la inicialización de git, creación del repo en GitHub vía
  `gh`, primer commit, push, y deploy a Vercel vía `vercel --prod`.
---

# Deploy a GitHub + Vercel

Flujo completo de subida:
**git init → .gitignore → commit → gh repo create → push → vercel --prod**

---

## Pre-requisitos (verificar primero)

```bash
git --version          # debe estar instalado
gh --version           # GitHub CLI — instalar con: winget install GitHub.cli
npx -y vercel --version # Vercel CLI vía npx (no requiere instalación global)
```

Si `gh` o `vercel` no están autenticados:
- `gh auth login` — abre navegador para login
- `npx vercel login` — pide email, manda link al correo

---

## Paso 1 — `.gitignore`

Crear `.gitignore` en la raíz si no existe. Para proyectos web estáticos:

```gitignore
# Dependencies
node_modules/

# OS
.DS_Store
Thumbs.db

# Vercel
.vercel/

# Logs
*.log

# Build artefacts de tooling local
.claude/scripts/screenshots/
.claude/scripts/__pycache__/

# Originales pesados que ya no se sirven (opcional)
# assets/hero.mp4
```

**No excluir:**
- Carpeta `.claude/skills/` — son las skills del proyecto, sí van al repo
- `assets/` — los recursos servidos al cliente
- Archivos `*.html` raíz

---

## Paso 2 — Inicializar git y primer commit

```bash
cd /ruta/al/proyecto
git init -b main
git add .
git config --get user.email || git config user.email "tu@email.com"
git config --get user.name  || git config user.name "Tu Nombre"
git commit -m "Initial commit — primera versión web premium"
```

Verifica que no hay archivos enormes (>100MB) antes del push:
```bash
git ls-files | xargs -I {} ls -l {} 2>/dev/null | sort -k5 -rn | head -5
```

GitHub bloquea archivos > 100MB. Si hay alguno, considerar Git LFS o moverlo a hosting externo (S3, Cloudflare R2).

---

## Paso 3 — Crear repo en GitHub

```bash
gh repo create <nombre-repo> --public --source=. --push
```

- `--public` — visible (usar `--private` para privado)
- `--source=.` — el directorio actual ya tiene el código
- `--push` — hace el push del primer commit en la misma operación

Si el usuario prefiere repo privado, preguntar antes. El default debería ser **public** para que Vercel pueda desplegarlo en el plan gratis sin problemas de permisos.

---

## Paso 4 — Deploy a Vercel

```bash
npx vercel --prod --yes
```

Primera vez Vercel hace varias preguntas:
- "Set up and deploy?" → `Y`
- "Which scope?" → cuenta del usuario
- "Link to existing project?" → `N` (es nuevo)
- "Project name?" → `<nombre-repo>` (mismo que GitHub)
- "Directory?" → `./` (raíz)
- "Want to modify settings?" → `N` (defaults para HTML estático)

`--yes` automatiza estas respuestas usando defaults en runs subsecuentes.

Vercel devuelve la URL final (`https://<nombre-repo>.vercel.app`).

---

## Paso 5 — Confirmar al usuario

Mostrar:
- ✅ URL del repo en GitHub
- ✅ URL de producción en Vercel
- ✅ Push hecho a `main`
- ⚠️ Cualquier dominio personalizado pendiente de configurar

---

## Despliegues posteriores

Para cambios futuros:
```bash
git add .
git commit -m "Mensaje descriptivo"
git push
```

**Vercel auto-despliega en cada push a `main`** una vez conectado el repo. No hace falta volver a correr `vercel --prod` salvo para forzar un redeploy desde local.

---

## Errores comunes

| Síntoma | Solución |
|---|---|
| `gh: command not found` | `winget install GitHub.cli` y abrir nueva terminal |
| `vercel: command not found` | Usar `npx -y vercel` en vez de `vercel` |
| `error: failed to push some refs` | El repo en GitHub ya existe con commits — `git pull --rebase` antes del push |
| Vercel build falla | Verificar que es un sitio estático (sin `package.json` con build script) o configurar Framework Preset = "Other" |
| Archivo > 100MB rechazado por GitHub | Mover el archivo a hosting externo o usar Git LFS |
