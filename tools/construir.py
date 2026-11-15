"""Genera las páginas de /public con encabezado y pie comunes.
Uso: python3 tools/construir.py  (desde la raíz del repo)
Diseño: dos luces (día y luz baja), tipografías propias en /assets/fuentes, sin peticiones a terceros."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "public"
TITULO = "Ojalá hubiera sabido esto antes"
SUB = "Lo que aprendí cuando dejé de confundir aguantar con ser fuerte"
SITIO = "https://libro.momentumhub.cloud"

# Decide la luz antes de pintar, para que no parpadee: elección guardada > preferencia del sistema > hora local.
LUZ = ("(function(){var g=null;try{g=localStorage.getItem('luz')}catch(e){}var h=new Date().getHours();"
       "var b=g?g==='baja':(matchMedia('(prefers-color-scheme: dark)').matches||h>=20||h<6);"
       "if(b)document.documentElement.setAttribute('data-luz','baja')})();")

def pagina(ruta, titulo, descripcion, cuerpo, indexar=True, actual=""):
    robots = "" if indexar else '<meta name="robots" content="noindex">\n'
    url = SITIO + "/" + ruta.replace("index.html", "")
    def nav(href, texto):
        marca = ' aria-current="page"' if href == actual else ""
        return f'<a href="{href}"{marca}>{texto}</a>'
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="book">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:image" content="{SITIO}/img/elefante-toro.png">
<meta name="theme-color" content="#e7ece3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#161d18" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/img/icono.png" type="image/png">
<script>{LUZ}</script>
<link rel="preload" href="/assets/fuentes/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fuentes/literata.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/estilos.css">
</head>
<body>
<a class="salto" href="#contenido">Ir al contenido</a>
<header class="barra"><div class="ancho">
  <a class="marca" href="/">{TITULO}</a>
  <nav aria-label="Principal">{nav("/introduccion/", "Leer la Introducción")}{nav("/ayuda/", "Dónde pedir ayuda")}<button class="luz" type="button" data-luz-boton aria-pressed="false"><i aria-hidden="true"></i><span>Bajar la luz</span></button></nav>
</div></header>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie"><div class="ancho">
  <div>
    <img class="elefante" src="/img/elefante.webp" alt="" width="587" height="412" loading="lazy">
    <p>El toro embiste solo; el elefante se pinta entre dos.</p>
    <p>© 2026 Ernesto Alvarez. Publicado con Momentum Coaches.</p>
  </div>
  <nav aria-label="Pie"><a href="/ayuda/">Dónde pedir ayuda</a><a href="/recursos/">Recursos</a><a href="/privacidad/">Aviso de privacidad</a></nav>
</div></footer>
<script src="/assets/config.js"></script>
<script src="/assets/app.js"></script>
</body>
</html>
"""
    destino = RAIZ / ruta
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")

def formulario(origen, exito, con_nombre=True, con_palabra=False, boton="Enviar"):
    nombre = '<label>Tu nombre<input type="text" name="nombre" autocomplete="given-name" maxlength="120"></label>' if con_nombre else ""
    palabra = ('<label>La palabra del libro<input type="text" name="palabra" required autocomplete="off" maxlength="60">'
               '<span class="ayuda-campo">Está en la página «Una cosa más», al final del libro.</span></label>') if con_palabra else ""
    return f"""<form data-origen="{origen}" data-exito="{exito}" novalidate>
  {nombre}
  <label>Tu correo electrónico<input type="email" name="correo" required autocomplete="email" maxlength="254"></label>
  {palabra}
  <div class="oculto" aria-hidden="true"><label>Sitio web<input type="text" name="sitio_web" tabindex="-1" autocomplete="off"></label></div>
  <label class="casilla"><input type="checkbox" name="consentimiento" required> <span>Acepto recibir correos de Ernesto Alvarez sobre el libro y he leído el <a href="/privacidad/">aviso de privacidad</a>. Puedo darme de baja cuando quiera.</span></label>
  <div><button class="boton" type="submit">{boton}</button></div>
  <p class="mensaje" role="status" aria-live="polite"></p>
</form>"""

# ---------- Inicio ----------
FRASES = [
    (None, "Introducción", "Aguantar no es lo mismo que ser fuerte.", "La máquina del tiempo y la grieta"),
    ("Parte I. El costo de la falsa fortaleza", "Capítulo 1", "Mi cuerpo no era una máquina que podía exprimir sin consecuencias.", "No era disciplina, era abandono"),
    (None, "Capítulo 2", "Esconder el dolor no lo hace más pequeño.", "Preferí que pensaran que todo estaba bien"),
    (None, "Capítulo 3", "Irse no es lo mismo que sanar.", "Solo lo repartía"),
    ("Parte II. El vacío y la distancia", "Capítulo 4", "Cargar la culpa no es lo mismo que hacerme responsable.", "La culpa se quedó a vivir conmigo"),
    (None, "Capítulo 5", "La presencia también se construye a distancia.", "Padre en diferido"),
    (None, "Capítulo 6", "Dejar de ser necesario no es dejar de ser importante.", "Aprendieron a no necesitarme tanto"),
    ("Parte III. El giro", "Capítulo 7", "Aceptar no es rendirse.", "Soltar la guerra"),
    (None, "Capítulo 8", "No se vuelve atrás; se construye hacia adelante.", "Esa persona ya no cabía en esta vida"),
    (None, "Capítulo 9", "Pedir ayuda es el primer acto de fuerza real.", "El primer ladrillo real"),
    ("Parte IV. La esperanza honesta", "Capítulo 10", "Al cuerpo no se le gana; se le escucha.", "Negociar con el cuerpo"),
    (None, "Capítulo 11", "No hace falta ser perfecto para seguir presente.", "Con las manos torpes"),
    (None, "Conclusión", "Siempre puedo volver a elegirme.", "Todavía puedo elegirme"),
]
filas = ""
for parte, cap, frase, tit in FRASES:
    if parte:
        filas += f'    <li class="parte">{parte}</li>\n'
    filas += f'    <li><span class="cap">{cap}</span><span class="frase">{frase}<span class="titulo">{tit}</span></span></li>\n'

inicio = f"""
<div class="entrada"><div class="ancho">
  <h1>Aguantar no es lo mismo que ser fuerte.</h1>
  <p class="bajada"><em>{TITULO}</em>. Memorias y manual de vida de Ernesto Alvarez.</p>
  <div class="repisa">
    <img class="elefante" src="/img/elefante.webp" alt="Un elefante verde, pintado a mano" width="587" height="412">
    <img class="toro" src="/img/toro.webp" alt="Un toro negro, de ónix, con la cabeza baja" width="602" height="412">
  </div>
  <div class="bajo-repisa">
    <div>
      <p>Un hombre pasó años confundiendo las dos cosas, hasta que el cuerpo dejó de obedecer. Once capítulos, once cicatrices y, al final de cada uno, tres pasos para las próximas veinticuatro horas.</p>
      <div class="acciones">
        <a class="boton" href="/introduccion/">Leer la Introducción gratis</a>
        <a class="enlace" data-enlace="amazonUrl" data-pronto="En Amazon, muy pronto" href="#">Comprar en Amazon</a>
      </div>
    </div>
    <p class="ficha">Sale el <span data-fecha>15 de diciembre de 2026</span><br>Ebook e impreso</p>
  </div>
</div></div>

<section class="bloque"><div class="ancho dos">
  <h2>A las 11:47 de una noche de noviembre</h2>
  <div>
    <p>Frente a una pantalla, su cuerpo empezó a decir lo que él llevaba años sin escuchar.</p>
    <p>Había hecho todo «bien»: dormía cuatro horas, resolvía las crisis de todos, corría maratones y enseñaba a otros a cuidarse. Debajo de esa armadura se estaba quedando sin aire.</p>
    <p>Este libro no es una autobiografía. Es un mapa de cicatrices. Cada capítulo nace de un momento concreto (un hospital, un divorcio, la salida de la empresa después de media vida, la distancia con quienes más quiere, un cuerpo que hoy convive con la migraña y el tinitus) y de la lección que llegó tarde.</p>
    <blockquote class="promesa">Este no es un libro sobre cómo volví a ser el de antes. Es sobre cómo aprendí a ser el de ahora.</blockquote>
    <p class="breve">Es un libro breve. Se lee en un fin de semana y se trabaja con calma: un capítulo, tres pasos, veinticuatro horas.</p>
  </div>
</div></section>

<section class="bloque"><div class="ancho dos">
  <div>
    <h2>Trece cosas que ojalá hubiera sabido antes</h2>
    <p class="nota columna">Cada frase es un capítulo. Todos empiezan en un momento concreto y terminan con tres pasos pequeños. Puedes leerlo en orden o saltar al que te duela.</p>
  </div>
  <ol class="frases">
{filas}  </ol>
</div></section>

<section class="bloque"><div class="ancho dos">
  <h2>Para quién es</h2>
  <ul class="para">
    <li>Para quien vive en piloto automático, <span>cansado y empujando.</span></li>
    <li>Para quien carga una distancia <span>que no sabe cómo cruzar.</span></li>
    <li>Para quien convive con el dolor <span>y está harto de que le prometan curas.</span></li>
    <li>Y para quien todavía no se ha roto, <span>pero ya escucha el crujido.</span></li>
  </ul>
</div></section>

<section class="bloque" id="edicion"><div class="ancho">
  <h2>Tres formas de acercarte</h2>
  <div class="caminos">
    <div>
      <h3>El libro</h3>
      <p>Ebook e impreso, en Amazon.</p>
      <p><a class="enlace" data-enlace="amazonUrl" data-pronto="Muy pronto" href="#">Ver en Amazon</a></p>
    </div>
    <div>
      <h3>Edición acompañada</h3>
      <p>Para quien quiere hacer el trabajo, no solo leerlo: el audiolibro narrado por el autor (se entrega en enero) y las plantillas editables de las herramientas. El libro se compra aparte, en Amazon.</p>
      <p><a class="enlace" data-enlace="hotmartUrl" data-pronto="Muy pronto" href="#">Quiero la Edición acompañada</a></p>
    </div>
    <div>
      <h3>Si ya lo leíste</h3>
      <p>Al final del libro hay una palabra. Con ella recibes el Cuaderno 24 horas y un texto que no entró, «Cómo escribí este libro».</p>
      <p><a class="enlace" href="/ticket/">Tengo la palabra</a></p>
    </div>
  </div>
</div></section>

<section class="bloque"><div class="ancho autor">
  <img src="/img/autor.jpg" alt="Ernesto Alvarez" width="800" height="800" loading="lazy">
  <div>
    <h2>Sobre el autor</h2>
    <p><strong>Ernesto Alvarez</strong> ha pasado unos treinta años diseñando sistemas que no deben caerse y liderando equipos de ingenieros en distintos países. Se formó en psicología y en coaching, fundó Momentum Coaches y acompaña a adolescentes, profesionistas y emprendedores en sus momentos de cambio.</p>
    <p>Durante mucho tiempo supo cuidar todo menos a sí mismo. Este libro es lo que aprendió cuando dejó de aguantar.</p>
    <p class="nota">Este libro acompaña; no sustituye la atención de un médico ni de un profesional de la salud mental. Si lo necesitas, aquí está <a href="/ayuda/">dónde pedir ayuda</a>.</p>
  </div>
</div></section>
"""
pagina("index.html", f"{TITULO} · Ernesto Alvarez",
       "Memorias y manual de vida: lo que aprendí cuando dejé de confundir aguantar con ser fuerte. Lee la Introducción gratis.", inicio)

# ---------- Introducción ----------
intro = f"""
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>Lee la Introducción, gratis</h1>
  <p class="entradilla">Déjame tu correo y te mando la Introducción completa, «La máquina del tiempo y la grieta». Empieza así:</p>
  <blockquote class="fragmento">
    <p>Son las tres de la mañana del 13 de diciembre, y acabo de recordar que mi hermana cumplió años ayer.</p>
    <p>No le llamé. No le escribí. Ni siquiera lo pensé.</p>
    <p>Estoy tirado en la cama, con los ojos abiertos, mirando el techo del departamento. No puedo dormir. En los oídos tengo un zumbido que no se detiene, un ruido fino que aturde cada pensamiento antes de que termine de formarse…</p>
  </blockquote>
  {formulario("introduccion", "Listo. Revisa tu correo en unos minutos (y la carpeta de promociones, por si acaso).", boton="Envíame la Introducción")}
</div></div></div>
"""
pagina("introduccion/index.html", f"Lee la Introducción · {TITULO}",
       "Recibe gratis la Introducción de «Ojalá hubiera sabido esto antes», de Ernesto Alvarez.", intro, actual="/introduccion/")

# ---------- Golden ticket ----------
ticket = f"""
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>Una cosa más</h1>
  <p class="entradilla">Si llegaste hasta aquí, te guardé algo que no cabe en el libro: las hojas de trabajo de las herramientas y un texto que no entró, «Cómo escribí este libro».</p>
  <p>Escribe tu correo y la palabra que te pido al final del libro. Te llega todo por correo.</p>
  {formulario("ticket", "Listo. Revisa tu correo: ahí están tus descargas.", con_palabra=True, boton="Quiero mi regalo")}
</div></div></div>
"""
pagina("ticket/index.html", f"Una cosa más · {TITULO}",
       "Material adicional para lectores del libro.", ticket, indexar=False)

# ---------- Ayuda ----------
ayuda = """
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>Dónde pedir ayuda</h1>
  <p class="urgente"><strong>Si estás en peligro inmediato, o alguien cerca de ti lo está, llama al número de emergencias de tu país:</strong> <a href="tel:911">911</a> en México, Estados Unidos y buena parte de América Latina; <a href="tel:112">112</a> en España.</p>
  <p>Si lo que cargas pesa más de lo que puedes sostener solo, estas líneas son gratuitas y confidenciales:</p>
  <ul class="lineas">
    <li><span><span class="pais">México</span><span class="servicio">Línea de la Vida. Atención las 24 horas.</span></span><a href="tel:8009112000">800 911 2000</a></li>
    <li><span><span class="pais">España</span><span class="servicio">Línea de atención a la conducta suicida. Atención las 24 horas.</span></span><a href="tel:024">024</a></li>
    <li><span><span class="pais">Argentina</span><span class="servicio">Línea de salud mental del Ministerio de Salud de la Nación. Atención las 24 horas.</span></span><a href="tel:08009990091">0800 999 0091</a></li>
    <li><span><span class="pais">Colombia</span><span class="servicio">Línea Nacional de Teleorientación en Salud Mental. Atención las 24 horas.</span></span><a href="tel:106">106</a></li>
    <li><span><span class="pais">Chile</span><span class="servicio">Línea de prevención del suicidio.</span></span><a href="tel:*4141">*4141</a></li>
    <li><span><span class="pais">Perú</span><span class="servicio">Línea 113, opción 5 (salud mental).</span></span><a href="tel:113">113</a></li>
    <li><span><span class="pais">Estados Unidos, en español</span><span class="servicio">Línea de Prevención del Suicidio y Crisis: marca 988 y elige la opción 2.</span></span><a href="tel:988">988</a></li>
  </ul>
  <p>Si tu país no aparece aquí, el directorio internacional <a href="https://findahelpline.com" rel="noopener">Find A Helpline</a> reúne líneas gratuitas de muchos países.</p>
  <p>Y si el dolor es del cuerpo, la primera llamada es a tu médico. No esperes a que se vuelva insoportable.</p>
  <p class="nota">Números verificados el 9 de noviembre de 2026.</p>
</div></div></div>
"""
pagina("ayuda/index.html", f"Dónde pedir ayuda · {TITULO}",
       "Líneas gratuitas y confidenciales de apoyo emocional y prevención del suicidio en México, España, América Latina y Estados Unidos.", ayuda, actual="/ayuda/")

# ---------- Recursos ----------
recursos = """
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>Recursos</h1>
  <p>Las ideas que no son del autor tienen nombre y fuente en las notas de cada capítulo y en la bibliografía del libro. Aquí irán la bibliografía con enlaces, las notas por capítulo y la ficha de prensa.</p>
  <h2>Prensa y entrevistas</h2>
  <p>Ficha de prensa, portada en alta resolución y foto del autor: <em>disponibles a partir del lanzamiento.</em></p>
  <h2>Dónde pedir ayuda</h2>
  <p>La lista actualizada está en <a href="/ayuda/">Dónde pedir ayuda</a>.</p>
</div></div></div>
"""
pagina("recursos/index.html", f"Recursos · {TITULO}",
       "Bibliografía, notas y ficha de prensa del libro.", recursos)

# ---------- Privacidad (borrador) ----------
privacidad = """
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>Aviso de privacidad</h1>
  <p class="nota">Borrador pendiente de revisión. No abrir el registro hasta completar los datos marcados.</p>
  <h2>Responsable</h2>
  <p>[PENDIENTE: nombre completo o razón social del responsable], con domicilio en [PENDIENTE: domicilio], es responsable del tratamiento de tus datos personales conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.</p>
  <h2>Qué datos recabamos</h2>
  <p>Nombre (opcional), correo electrónico, el país aproximado desde el que te conectas y la etiqueta del canal por el que llegaste (por ejemplo, un video o el código del libro).</p>
  <h2>Para qué los usamos</h2>
  <ul>
    <li>Enviarte lo que pediste: la Introducción o el material adicional del libro.</li>
    <li>Escribirte sobre el libro y sobre nuevos materiales del autor, si aceptaste recibir correos.</li>
    <li>Saber qué canales traen lectores, de forma agregada.</li>
  </ul>
  <p>No vendemos ni rentamos tus datos. Los servicios que usamos para guardarlos y enviar correos [PENDIENTE: listar proveedores, p. ej. Cloudflare, Supabase y el servicio de correo] solo los tratan por nuestra cuenta.</p>
  <h2>Tus derechos</h2>
  <p>Puedes darte de baja desde cualquier correo que te enviemos. Para acceder, rectificar, cancelar u oponerte al uso de tus datos (derechos ARCO), o revocar tu consentimiento, escribe a [PENDIENTE: correo de contacto de privacidad].</p>
  <h2>Cambios a este aviso</h2>
  <p>Cualquier cambio se publicará en esta página. Última actualización: [PENDIENTE: fecha].</p>
</div></div></div>
"""
pagina("privacidad/index.html", f"Aviso de privacidad · {TITULO}",
       "Aviso de privacidad del sitio del libro.", privacidad, indexar=False)

# ---------- 404 ----------
no_encontrada = """
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>Esta página no existe</h1>
  <p>Puede que el enlace esté mal escrito. Empieza por <a href="/">la página del libro</a>.</p>
  <p class="nota">¿Llegaste desde el código del libro? Ve a <a href="/ticket/">Una cosa más</a>.</p>
</div></div></div>
"""
pagina("404.html", f"Página no encontrada · {TITULO}", "Página no encontrada.", no_encontrada, indexar=False)

# ---------- Descargas (protegidas por el Worker) ----------
desc_intro = """
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>La Introducción</h1>
  <p class="entradilla">Gracias por registrarte. Aquí está la Introducción completa de <em>Ojalá hubiera sabido esto antes</em>, lista para leer o guardar.</p>
  <p><a class="boton" href="/descargas/intro/introduccion.pdf" download>Descargar la Introducción (PDF)</a></p>
  <p class="nota">Puedes volver a esta página desde el enlace que te llegó por correo.</p>
  <h2>¿Quieres seguir?</h2>
  <p>El libro completo sale el <span data-fecha>15 de diciembre de 2026</span>.</p>
  <p><a class="enlace" data-enlace="amazonUrl" data-pronto="En Amazon, muy pronto" href="#">Comprar en Amazon</a></p>
</div></div></div>
"""
pagina("descargas/intro/index.html", f"Tu Introducción · {TITULO}", "Descarga de la Introducción.", desc_intro, indexar=False)

desc_completo = """
<div class="pagina"><div class="ancho"><div class="columna">
  <h1>Tus descargas</h1>
  <p class="entradilla">Esto es lo que te guardé por llegar hasta el final del libro. Es gratis y es tuyo.</p>
  <ul class="descargas">
    <li><strong>La Introducción</strong> (PDF), para compartirla con alguien a quien le pueda servir.<br><a href="/descargas/intro/introduccion.pdf" download>Descargar</a></li>
    <li><strong>Cuaderno «24 horas»</strong>: las herramientas de los once capítulos, con espacio para escribir.<br><span class="nota">Disponible el día que sale el libro.</span></li>
    <li><strong>«Cómo escribí este libro»</strong>: el texto que no entró en el libro.<br><span class="nota">Disponible el día que sale el libro.</span></li>
  </ul>
  <p class="nota">Puedes volver a esta página desde el enlace que te llegó por correo. Si algo no abre, responde ese correo.</p>
  <p class="nota">Si estás pasando por un momento difícil, aquí está <a href="/ayuda/">dónde pedir ayuda</a>.</p>
</div></div></div>
"""
pagina("descargas/index.html", f"Tus descargas · {TITULO}", "Material para lectores del libro.", desc_completo, indexar=False)

print("Páginas generadas en", RAIZ)
