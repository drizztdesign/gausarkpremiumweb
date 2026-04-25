---
description: Deploy completo automatizado — git → GitHub → Vercel
---

Ejecuta el deploy completo del proyecto sin pedir confirmaciones.

Pasos a hacer:

1. Verificar estado: `cd a:/gausarkpremiumweb && bash .claude/scripts/deploy.sh "$ARGUMENTS"`

2. Si el script falla por falta de autenticación, ejecutar primero:
   `bash .claude/scripts/setup-deploy.sh`
   y luego volver a intentar el deploy.

3. Al terminar, mostrar al usuario:
   - URL del repo en GitHub
   - URL de producción en Vercel
   - Cualquier paso pendiente (dominio personalizado, etc.)

El argumento `$ARGUMENTS` (opcional) se usa como mensaje del commit. Si no se pasa, usa por defecto "Update web YYYY-MM-DD".

NO pedir confirmación al usuario antes de ejecutar — el comando es explícito.
