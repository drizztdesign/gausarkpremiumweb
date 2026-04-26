# Configuración del formulario de contacto

Hola,

Para que el formulario de la nueva web envíe los mensajes directamente a vuestro email **gausarksl@gausark.es**, necesito que ejecutéis un pequeño paso desde vuestra cuenta de Google. Es de **3 minutos** y solo se hace una vez.

---

## Paso 1 — Iniciar sesión en Google

Importante: tenéis que estar en la cuenta de Google que tenga acceso al email **gausarksl@gausark.es** (la cuenta corporativa).

Si no estáis seguros: abrid Gmail con esa cuenta primero. Comprobad que arriba a la derecha aparece el avatar correcto.

---

## Paso 2 — Abrir Google Apps Script

Abrid este enlace en el navegador: **https://script.google.com**

Click en **"Nuevo proyecto"** (botón azul arriba a la izquierda).

---

## Paso 3 — Pegar el código

Borrad todo el código que aparece por defecto en el editor (la línea `function myFunction() {…}` y demás).

Pegad en su lugar el siguiente código (lo tenéis adjunto en el archivo `setup-google-form.gs`):

> [Pega aquí el contenido completo de a:\gausarkpremiumweb\setup-google-form.gs]

---

## Paso 4 — Ejecutar

1. Arriba del editor hay un botón con un **▶ triángulo** ("Ejecutar"). A su derecha hay un desplegable.
2. Aseguraos de que en el desplegable está seleccionado **`setupForm`**.
3. Click en **▶ Ejecutar**.

---

## Paso 5 — Aceptar permisos

Google os preguntará si autorizáis al script a:
- Crear formularios en vuestro Drive
- Enviar emails desde vuestra cuenta

Aparecerá una pantalla diciendo **"Google no ha verificado esta aplicación"**. Es normal — el código lo escribió tu desarrollador, no es de un tercero. Para continuar:

1. Abajo a la izquierda click en **"Configuración avanzada"**
2. Aparece un texto en azul al final: **"Ir a Untitled project (no seguro)"** — click ahí
3. Click en **"Permitir"** en la siguiente pantalla

(Estos avisos solo aparecen la primera vez. No vuelven a salir.)

---

## Paso 6 — Copiar el resultado

Tras unos segundos, en el panel inferior **"Registro de ejecución"** aparecerá un texto largo entre llaves `{ }`. Algo así:

```
══════════════════════════════════════════════════════════
  COPIA ESTE JSON Y PÉGALO EN CLAUDE CODE:
══════════════════════════════════════════════════════════
{
  "form_id": "1abc...",
  "edit_url": "...",
  "published_url": "...",
  "notify_email": "gausarksl@gausark.es",
  "entries": {
    "NOMBRE": "...",
    "TELEFONO": "...",
    "EMAIL": "...",
    "SERVICIO": "...",
    "MENSAJE": "..."
  }
}
══════════════════════════════════════════════════════════
```

**Copiad ese bloque entero (desde la `{` inicial hasta la `}` final)** y enviádmelo por email/WhatsApp.

---

## Comprobación: ¿llegó el email de bienvenida?

A los pocos segundos de ejecutar el script, debéis recibir un email a **gausarksl@gausark.es** con el asunto **"✓ Form de Gausark configurado — listo para recibir contactos"**.

Si no aparece en la bandeja de entrada en 1-2 minutos, **revisad la carpeta de Spam** (Google a veces marca como spam los emails que vienen de scripts propios la primera vez).

Si está en spam: marcadlo como "No es spam" para que los siguientes lleguen al inbox.

---

## ¿Y luego?

Cuando me enviéis el JSON, lo conecto al formulario de la web (5 minutos) y desde ese momento cada mensaje que envíe alguien desde el formulario de contacto os llegará automáticamente al email **gausarksl@gausark.es**.

El formulario en Google que se ha creado se puede ver en vuestro **Google Drive** (carpeta "Mi unidad" → archivo "Gausark S.L.P. — Contacto"). Ahí podéis ver también todas las respuestas históricas en formato hoja de cálculo si queréis.

Cualquier duda, escribidme.

Un saludo
