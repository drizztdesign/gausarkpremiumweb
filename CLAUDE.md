# CLAUDE.md — Gausark S.L.P.

> **⚠ Proyecto en paralelo con Drizzt Design (`a:\drizzt-design\`)**
>
> Cualquier mejora **genérica** (form, deploy, scroll-video, SEO, accesibilidad,
> performance, fix de bug) **DEBE aplicarse a ambos proyectos** sin esperar a que
> el usuario lo pida explícitamente.
>
> Solo el contenido específico (copy, colores de marca, fotos, datos de cliente)
> queda en este proyecto.

## Cliente

**Gausark S.L.P.** — Estudio de arquitectura y diseño en Donostia (Gipuzkoa).
Más de 40 años de experiencia. Web rebuild del WordPress original.

## Stack y convenciones

- HTML + CSS + JS puro (sin frameworks)
- Tipografías: Cormorant Garamond + Nunito
- Paleta: charcoal/blanco + naranja `#ff9901` (extraído del logo)
- 4 páginas: index, servicios, nosotros, contacto
- Hero con scroll-driven video
- SEO completo (Schema.org ProfessionalService)

## Producción

- 🌐 https://gausarkpremiumweb.vercel.app/
- 📦 https://github.com/drizztdesign/gausarkpremiumweb
- Auto-deploy: cada `git push origin main` despliega solo

## Para desplegar cambios

```bash
bash .claude/scripts/deploy.sh "mensaje commit"
# o desde Claude Code:
/deploy "mensaje commit"
```

## Aplicar cambio en ambos proyectos (workflow obligatorio)

Cuando hagas un cambio genérico aquí, repítelo en `a:\drizzt-design\`:

```bash
# 1. Aplicar cambio en este proyecto
# 2. Aplicar cambio equivalente en Drizzt
# 3. /deploy en ambos
# 4. Confirmar al usuario: "Aplicado en Gausark y Drizzt"
```

Si el patrón también amerita actualizar el kit (`a:\CLAUDESKILLS\.claude\skills\`),
hacerlo y sincronizar al plugin global.

## Datos del cliente reales

- Email: gausarksl@gausark.es
- Teléfono: 943 44 07 52
- Dirección: Txapillo Kalea, 3, bajo izq · 20009 Donostia, Gipuzkoa
- Instagram: @gausarksl
