// Worker del sitio del libro «Ojalá hubiera sabido esto antes».
// Sirve las páginas estáticas de /public y atiende POST /api/registro.
//
// Secretos (Cloudflare → Workers → libro-momentum → Settings → Variables and Secrets):
//   N8N_WEBHOOK_URL    URL del webhook de n8n que guarda en Supabase y envía el correo
//   N8N_SHARED_SECRET  Texto compartido que n8n valida en el encabezado X-Libro-Secret
//   TICKET_PALABRA     Palabra clave impresa en el libro para el golden ticket

const ORIGENES = new Set(["introduccion", "ticket", "ventas"]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/registro") {
      if (request.method !== "POST") {
        return json({ ok: false, error: "Método no permitido" }, 405);
      }
      return registrar(request, env);
    }

    return env.ASSETS.fetch(request);
  },
};

async function registrar(request, env) {
  let datos;
  try {
    datos = await request.json();
  } catch {
    return json({ ok: false, error: "Solicitud inválida" }, 400);
  }

  // Campo trampa: los humanos no lo ven; si llega lleno, es un robot.
  if (datos.sitio_web) return json({ ok: true });

  const correo = String(datos.correo || "").trim().toLowerCase();
  const nombre = String(datos.nombre || "").trim().slice(0, 120);
  const origen = String(datos.origen || "");
  const consentimiento = datos.consentimiento === true;

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(correo) || correo.length > 254) {
    return json({ ok: false, error: "Revisa tu correo electrónico." }, 400);
  }
  if (!ORIGENES.has(origen)) {
    return json({ ok: false, error: "Origen no válido." }, 400);
  }
  if (!consentimiento) {
    return json({ ok: false, error: "Necesitamos tu consentimiento para escribirte." }, 400);
  }

  if (origen === "ticket") {
    const esperada = normalizar(env.TICKET_PALABRA || "");
    const recibida = normalizar(datos.palabra || "");
    if (!esperada || recibida !== esperada) {
      return json({ ok: false, error: "Esa no es la palabra. Búscala de nuevo en la página «Una cosa más», al final del libro." }, 400);
    }
  }

  if (!env.N8N_WEBHOOK_URL) {
    return json({ ok: false, error: "El registro aún no está activo. Inténtalo más tarde." }, 503);
  }

  const registro = {
    correo,
    nombre,
    origen,
    consentimiento,
    utm_source: String(datos.utm_source || "").slice(0, 80),
    utm_medium: String(datos.utm_medium || "").slice(0, 80),
    utm_campaign: String(datos.utm_campaign || "").slice(0, 80),
    pais: request.cf?.country || null,
    fecha: new Date().toISOString(),
  };

  const respuesta = await fetch(env.N8N_WEBHOOK_URL, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-libro-secret": env.N8N_SHARED_SECRET || "",
    },
    body: JSON.stringify(registro),
  });

  if (!respuesta.ok) {
    return json({ ok: false, error: "No pudimos registrarte. Inténtalo en unos minutos." }, 502);
  }
  return json({ ok: true });
}

function normalizar(texto) {
  return String(texto)
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-zA-Z0-9]/g, "")
    .toLowerCase();
}

function json(cuerpo, estado = 200) {
  return new Response(JSON.stringify(cuerpo), {
    status: estado,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}
