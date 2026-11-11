# libro-momentum

Sitio del libro *Ojalá hubiera sabido esto antes*, de Ernesto Alvarez.
Destino: `libro.momentumhub.cloud`, servido por el Worker de Cloudflare `libro-momentum`.

## Qué hay

| Ruta | Qué es |
| --- | --- |
| `/` | Página de ventas: portada, sinopsis, contenido, Edición acompañada, autor |
| `/introduccion/` | La Introducción gratis a cambio del correo |
| `/ticket/` | Golden ticket: correo + palabra clave impresa en el libro (no se indexa) |
| `/ayuda/` | Dónde pedir ayuda. **Esta dirección se imprime en el libro: no cambiarla** |
| `/recursos/` | Bibliografía, notas y prensa (por completar) |
| `/descargas/` | Material para lectores (golden ticket). Protegido: solo con enlace firmado |
| `/descargas/intro/` | La Introducción en PDF (registro de la Introducción). Protegido |
| `/privacidad/` | Aviso de privacidad (**borrador con datos pendientes**) |
| `POST /api/registro` | Recibe los formularios y los reenvía a n8n |

- `public/`: archivos estáticos. Las páginas HTML se generan con `python3 tools/construir.py`; edita el script, no los HTML.
- `public/assets/config.js`: enlaces de Amazon y Hotmart, y la fecha de lanzamiento. Mientras estén vacíos, los botones dicen «Muy pronto».
- `src/worker.js`: el Worker. Valida, filtra robots (campo trampa) y comprueba la palabra del ticket.

## Publicar

Lo más simple es conectar el repo al Worker: Cloudflare → Workers → `libro-momentum` → Settings → Builds → Connect a GitHub repo. Cada push a `main` despliega.

También desde la terminal:

```sh
npx wrangler deploy
```

## Secretos

Se cargan en Cloudflare, nunca en el repo:

```sh
npx wrangler secret put N8N_WEBHOOK_URL     # URL del webhook de n8n
npx wrangler secret put N8N_SHARED_SECRET   # texto que n8n valida en el encabezado x-libro-secret
npx wrangler secret put TICKET_PALABRA      # la palabra impresa en el libro (sin importar mayúsculas ni acentos)
```

Sin `N8N_WEBHOOK_URL`, los formularios responden «El registro aún no está activo».

## Descargas

Al registrarse, el Worker firma un enlace (`/descargas/?t=…` o `/descargas/intro/?t=…`), lo devuelve al formulario (que redirige ahí) y lo manda a n8n en el campo `enlace` para el correo. Al abrir el enlace se guarda una cookie por un año. Sin enlace válido, `/descargas/*` redirige al formulario. La firma usa `DESCARGAS_SECRET` o, si no existe, `N8N_SHARED_SECRET`.

Para agregar un archivo: ponerlo en `public/descargas/` (o `public/descargas/intro/`), enlazarlo en `tools/construir.py` y publicar.

## Flujo de n8n

Flujo «Libro · Registro de lectores» (activo). URL de producción del webhook: `https://n8n-n8n.z3tydl.easypanel.host/webhook/libro-registro`. Guarda en la tabla de n8n `libro_lectores`. El correo al lector está desactivado hasta tener los enlaces de descarga.

QR del golden ticket (provisional, apunta a workers.dev): `docs/qr/`. Regenerarlo cuando el dominio definitivo esté activo y antes de mandar el libro a imprenta.

## Contrato con n8n

El Worker envía `POST` con encabezado `x-libro-secret` y este cuerpo:

```json
{
  "correo": "lector@ejemplo.com",
  "nombre": "Ana",
  "origen": "introduccion | ticket | ventas",
  "consentimiento": true,
  "utm_source": "youtube",
  "utm_medium": "video",
  "utm_campaign": "lanzamiento",
  "pais": "MX",
  "fecha": "2026-12-15T18:00:00.000Z"
}
```

n8n debe: (1) rechazar si el secreto no coincide, (2) hacer *upsert* en `libro_lectores` (ver `docs/supabase.sql`), (3) mandar el correo con los enlaces de descarga según `origen`, (4) responder 200.

## Dominio

Pendiente. Con el DNS en Hostinger, la ruta es un subdominio: agregar en Cloudflare el dominio personalizado `libro.momentumhub.cloud` al Worker y crear en Hostinger el registro que Cloudflare indique. Un Worker con dominio personalizado necesita que la zona esté en Cloudflare; si no se mueve la zona, la alternativa es usar la dirección `*.workers.dev` mientras tanto.

## Antes de abrir el registro

- [ ] Completar los `[PENDIENTE]` del aviso de privacidad.
- [ ] Crear el flujo de n8n y la tabla de Supabase.
- [ ] Cargar los tres secretos.
- [ ] Probar los dos formularios de punta a punta.
