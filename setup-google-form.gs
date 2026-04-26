/**
 * Auto-setup de Google Form para "Gausark S.L.P. — Contacto"
 *
 * Cómo usar:
 *   1. Pega TODO este archivo en https://script.google.com (New project)
 *   2. Click en "Run" (selecciona setupForm)
 *   3. Autoriza los permisos cuando Google los pida (Forms + Gmail)
 *   4. En el "Execution log" verás un JSON. Cópialo entero.
 *   5. Pégalo de vuelta en Claude Code.
 */

function setupForm() {
  const FORM_TITLE       = "Gausark S.L.P. — Contacto";
  const FORM_DESCRIPTION = "Formulario de contacto desde gausarkpremiumweb.vercel.app";
  const NOTIFY_EMAIL     = "gausarksl@gausark.es";

  const FIELDS = [
    { key: "NOMBRE",   title: "Nombre",            type: "text",      required: true  },
    { key: "TELEFONO", title: "Teléfono",          type: "text",      required: false },
    { key: "EMAIL",    title: "Email",             type: "text",      required: true  },
    { key: "SERVICIO", title: "Tipo de proyecto",  type: "list",      required: false,
      choices: ["Obra nueva", "Reforma", "Rehabilitación", "Consulta general"] },
    { key: "MENSAJE",  title: "Mensaje",           type: "paragraph", required: true  }
  ];

  // ---- Crear el form ----
  const form = FormApp.create(FORM_TITLE);
  form.setDescription(FORM_DESCRIPTION);
  form.setCollectEmail(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage("¡Gracias! Le respondemos en menos de 24 horas.");

  // ---- Añadir los campos en orden ----
  const items = [];
  FIELDS.forEach(function (field) {
    let item;
    switch (field.type) {
      case "text":
        item = form.addTextItem();
        break;
      case "paragraph":
        item = form.addParagraphTextItem();
        break;
      case "list":
        item = form.addListItem();
        item.setChoices(field.choices.map(function (c) { return item.createChoice(c); }));
        break;
      default:
        throw new Error("Tipo de campo no soportado: " + field.type);
    }
    item.setTitle(field.title);
    if (field.required) item.setRequired(true);
    items.push({ key: field.key, item: item });
  });

  // ---- Trigger automático para enviar email cuando alguien responde ----
  ScriptApp.newTrigger("onFormSubmitNotify")
    .forForm(form)
    .onFormSubmit()
    .create();
  PropertiesService.getScriptProperties().setProperty("NOTIFY_EMAIL", NOTIFY_EMAIL);

  // ---- Forzar autorización MailApp enviando un email de bienvenida ----
  // Esto evita el bug donde el trigger se crea sin permiso de Gmail.
  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: "✓ Form de Gausark configurado — listo para recibir contactos",
    body: "El formulario de gausarkpremiumweb.vercel.app ya está conectado.\n\n" +
          "A partir de ahora, cada mensaje enviado desde la web te llegará\n" +
          "automáticamente a esta dirección.\n\n" +
          "Form en Drive: " + form.getEditUrl() + "\n" +
          "Respuestas: " + form.getEditUrl().replace("/edit", "/responses")
  });

  // ---- Sacar entry IDs vía URL pre-rellenada ----
  const fakeResponse = form.createResponse();
  items.forEach(function (entry) {
    const item = entry.item;
    let itemResponse;
    if (item.getType() === FormApp.ItemType.TEXT || item.getType() === FormApp.ItemType.PARAGRAPH_TEXT) {
      itemResponse = item.createResponse("ENTRY_" + entry.key);
    } else if (item.getType() === FormApp.ItemType.LIST) {
      const choices = item.getChoices();
      itemResponse = item.createResponse(choices[0].getValue());
    }
    fakeResponse.withItemResponse(itemResponse);
  });
  const prefilledUrl = fakeResponse.toPrefilledUrl();

  // Extraer TODOS los entry.NUMBER de la URL en orden
  const entryMap = {};
  const entryPattern = /entry\.(\d+)=/g;
  const allEntryIds = [];
  let m;
  while ((m = entryPattern.exec(prefilledUrl)) !== null) {
    allEntryIds.push(m[1]);
  }
  items.forEach(function (entry, i) {
    if (allEntryIds[i]) entryMap[entry.key] = allEntryIds[i];
  });

  // ---- Salida ----
  const result = {
    form_id:        form.getId(),
    edit_url:       form.getEditUrl(),
    published_url:  form.getPublishedUrl(),
    notify_email:   NOTIFY_EMAIL,
    entries:        entryMap
  };

  console.log("");
  console.log("══════════════════════════════════════════════════════════");
  console.log("  COPIA ESTE JSON Y PÉGALO EN CLAUDE CODE:");
  console.log("══════════════════════════════════════════════════════════");
  console.log(JSON.stringify(result, null, 2));
  console.log("══════════════════════════════════════════════════════════");

  return result;
}

/**
 * Trigger: envía email al recibir respuesta del form. NO BORRAR.
 */
function onFormSubmitNotify(e) {
  const notifyEmail = PropertiesService.getScriptProperties().getProperty("NOTIFY_EMAIL");
  if (!notifyEmail) return;

  const items = e.response.getItemResponses();
  let body = "Nuevo mensaje desde el formulario de gausarkpremiumweb.vercel.app:\n\n";
  items.forEach(function (it) {
    body += "• " + it.getItem().getTitle() + ":\n  " + it.getResponse() + "\n\n";
  });
  body += "—\nVer todas las respuestas: " + e.source.getEditUrl().replace("/edit", "/responses");

  const remitente = items[0] ? items[0].getResponse() : "Anónimo";
  MailApp.sendEmail({
    to: notifyEmail,
    subject: "📩 Nuevo mensaje en Gausark — " + remitente,
    body: body
  });
}
