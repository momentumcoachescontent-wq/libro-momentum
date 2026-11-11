// Worker del sitio del libro «Ojalá hubiera sabido esto antes».
// Sirve las páginas estáticas de /public y atiende POST /api/registro.
//
// Secretos (Cloudflare → Workers → libro-momentum → Settings → Variables and Secrets):
//   N8N_WEBHOOK_URL    URL del webhook de n8n que guarda en Supabase y envía el correo
//   N8N_SHARED_SECRET  Texto compartido que n8n valida en el encabezado X-Libro-Secret
//   TICKET_PALABRA     Palabra clave impresa en el libro para el golden ticket
//   DESCARGAS_SECRET   (opcional) firma los enlaces de /descargas; si falta, usa N8N_SHARED_SECRET
//
// Zona de descargas: /descargas/ (todo) y /descargas/intro/ (solo la Introducción).
// Solo se entra con un enlace firmado (?t=...) que se entrega al registrarse y va en el correo.
// Al abrirlo se guarda una cookie por un año para volver sin el enlace.

const ORIGENES = new Set(["introduccion", "ticket", "ventas"]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname.startsWith("/descargas")) {
      return descargas(request, env, url);
    }

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

  const nivel = origen === "ticket" ? "completo" : "intro";
  const token = await firmarToken(env, nivel);
  const enlace = `${url_base(request)}/descargas/${nivel === "intro" ? "intro/" : ""}?t=${token}`;

  const registro = {
    enlace,
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
  return json({ ok: true, enlace });
}

// ---------- Descargas ----------

const COOKIE = "libro_acceso";

async function descargas(request, env, url) {
  const desdeEnlace = url.searchParams.get("t");
  const desdeCookie = leerCookie(request, COOKIE);
  const token = desdeEnlace || desdeCookie;
  const nivel = token ? await verificarToken(env, token) : null;

  const pideIntro = url.pathname.startsWith("/descargas/intro");
  const permitido = nivel === "completo" || (nivel === "intro" && pideIntro);
  if (!permitido) {
    return Response.redirect(`${url.origin}${pideIntro ? "/introduccion/" : "/ticket/"}`, 302);
  }

  if (desdeEnlace) {
    // Guarda el acceso y limpia el enlace de la barra de direcciones.
    url.searchParams.delete("t");
    return new Response(null, {
      status: 302,
      headers: {
        location: url.pathname + (url.search || ""),
        "set-cookie": `${COOKIE}=${token}; Path=/descargas; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax`,
        "cache-control": "no-store",
      },
    });
  }

  const respuesta = await env.ASSETS.fetch(request);
  const r = new Response(respuesta.body, respuesta);
  r.headers.set("cache-control", "private, no-store");
  r.headers.set("x-robots-tag", "noindex");
  return r;
}

function secreto(env) {
  return env.DESCARGAS_SECRET || env.N8N_SHARED_SECRET || "";
}

async function hmac(env, texto) {
  const clave = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(secreto(env)), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const firma = await crypto.subtle.sign("HMAC", clave, new TextEncoder().encode(texto));
  return b64url(new Uint8Array(firma)).slice(0, 32);
}

async function firmarToken(env, nivel) {
  const id = b64url(crypto.getRandomValues(new Uint8Array(9)));
  return `${nivel}.${id}.${await hmac(env, nivel + "." + id)}`;
}

async function verificarToken(env, token) {
  if (!secreto(env)) return null;
  const partes = String(token).split(".");
  if (partes.length !== 3) return null;
  const [nivel, id, firma] = partes;
  if (nivel !== "intro" && nivel !== "completo") return null;
  const esperada = await hmac(env, nivel + "." + id);
  return esperada === firma ? nivel : null;
}

function b64url(bytes) {
  let s = "";
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function leerCookie(request, nombre) {
  const c = request.headers.get("cookie") || "";
  const m = c.match(new RegExp("(?:^|; )" + nombre + "=([^;]+)"));
  return m ? m[1] : null;
}

function url_base(request) {
  return new URL(request.url).origin;
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
