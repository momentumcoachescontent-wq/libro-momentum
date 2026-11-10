"""Genera las páginas de /public con encabezado y pie comunes.
Uso: python3 tools/construir.py  (desde la raíz del repo)"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent / "public"
TITULO = "Ojalá hubiera sabido esto antes"
SUB = "Lo que aprendí cuando dejé de confundir aguantar con ser fuerte"

def pagina(ruta, titulo, descripcion, cuerpo, indexar=True):
    robots = "" if indexar else '<meta name="robots" content="noindex">\n'
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
{robots}<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descripcion}">
<meta property="og:image" content="https://libro.momentumhub.cloud/img/elefante-toro.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/estilos.css">
</head>
<body>
<header class="barra"><div class="contenedor">
  <a class="marca" href="/">{TITULO}</a>
  <nav aria-label="Principal"><a href="/introduccion/">Lee la Introducción</a><a href="/#edicion">Edición acompañada</a><a href="/ayuda/">Dónde pedir ayuda</a></nav>
</div></header>
<main>
{cuerpo}
</main>
<footer><div class="contenedor">
  <p>© 2026 Ernesto Alvarez · Momentum Coaches</p>
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
               '<span class="nota">La encuentras en la página «Una cosa más», al final del libro.</span></label>') if con_palabra else ""
    return f"""<form data-origen="{origen}" data-exito="{exito}" novalidate>
  {nombre}
  <label>Tu correo electrónico<input type="email" name="correo" required autocomplete="email" maxlength="254"></label>
  {palabra}
  <div class="oculto" aria-hidden="true"><label>Sitio web<input type="text" name="sitio_web" tabindex="-1" autocomplete="off"></label></div>
  <label class="casilla"><input type="checkbox" name="consentimiento" required> <span>Acepto recibir correos de Ernesto Alvarez sobre el libro y he leído el <a href="/privacidad/">aviso de privacidad</a>. Puedo darme de baja cuando quiera.</span></label>
  <div><button class="boton primario" type="submit">{boton}</button></div>
  <p class="mensaje" role="status" aria-live="polite"></p>
</form>"""

# ---------- Inicio ----------
inicio = f"""
<div class="hero"><div class="contenedor">
  <div class="libro" role="img" aria-label="Portada del libro: un elefante verde frente a un toro negro">
    <div>
      <p class="libro-titulo">Ojalá hubiera sabido esto antes</p>
      <p class="libro-subtitulo">{SUB}</p>
    </div>
    <div class="libro-ilustracion"><img src="/img/elefante-toro.png" alt="" width="1161" height="412"></div>
    <p class="libro-autor">Ernesto Alvarez</p>
  </div>
  <div>
    <span class="fecha">Sale el <span data-fecha>15 de diciembre de 2026</span></span>
    <h1 class="titular">Aguantar no es lo mismo que ser fuerte.</h1>
    <p class="entradilla">Memorias y manual de vida de un hombre que pasó años confundiendo las dos cosas, hasta que el cuerpo dejó de obedecer. Once capítulos, once cicatrices y, al final de cada uno, tres pasos para las próximas veinticuatro horas.</p>
    <div class="acciones">
      <a class="boton primario" href="/introduccion/">Lee la Introducción gratis</a>
      <a class="boton" data-enlace="amazonUrl" data-pronto="En Amazon, muy pronto" href="#">Comprar en Amazon</a>
    </div>
  </div>
</div></div>

<section><div class="estrecho">
  <h2>De qué trata</h2>
  <p>A las 11:47 de una noche de noviembre, frente a una pantalla, su cuerpo empezó a decir lo que él llevaba años sin escuchar.</p>
  <p>Había hecho todo «bien»: dormía cuatro horas, resolvía las crisis de todos, corría maratones y enseñaba a otros a cuidarse. Debajo de esa armadura se estaba quedando sin aire.</p>
  <p>Este libro no es una autobiografía. Es un mapa de cicatrices. Cada capítulo nace de un momento concreto (un hospital, un divorcio, la salida de la empresa después de media vida, la distancia con quienes más quiere, un cuerpo que hoy convive con la migraña y el tinitus) y de la lección que llegó tarde.</p>
  <blockquote class="cita">Este no es un libro sobre cómo volví a ser el de antes. Es sobre cómo aprendí a ser el de ahora.</blockquote>
</div></section>

<section><div class="contenedor">
  <h2>Es para ti si…</h2>
  <div class="rejilla">
    <div><h3>Vives en piloto automático</h3><p>Cansado, empujando, y orgulloso de aguantar más que nadie.</p></div>
    <div><h3>Cargas una distancia</h3><p>Con alguien que quieres, y no sabes cómo cruzarla.</p></div>
    <div><h3>Convives con el dolor</h3><p>Y estás harto de que te prometan curas.</p></div>
    <div><h3>Todavía no te has roto</h3><p>Pero ya escuchas el crujido.</p></div>
  </div>
</div></section>

<section><div class="contenedor">
  <h2>Contenido</h2>
  <ul class="indice">
    <li><strong>Introducción</strong>La máquina del tiempo y la grieta</li>
    <li><strong>Parte I · El costo de la falsa fortaleza</strong>1. No era disciplina, era abandono<br>2. Preferí que pensaran que todo estaba bien<br>3. Solo lo repartía</li>
    <li><strong>Parte II · El vacío y la distancia</strong>4. La culpa se quedó a vivir conmigo<br>5. Padre en diferido<br>6. Aprendieron a no necesitarme tanto</li>
    <li><strong>Parte III · El giro</strong>7. Soltar la guerra<br>8. Esa persona ya no cabía en esta vida<br>9. El primer ladrillo real</li>
    <li><strong>Parte IV · La esperanza honesta</strong>10. Negociar con el cuerpo<br>11. Con las manos torpes</li>
    <li><strong>Conclusión</strong>Todavía puedo elegirme</li>
  </ul>
</div></section>

<section id="edicion"><div class="contenedor">
  <h2>Edición acompañada</h2>
  <div class="rejilla">
    <div class="recuadro">
      <h3>El libro</h3>
      <p>Ebook e impreso, en Amazon.</p>
      <p style="margin-top:16px"><a class="boton" data-enlace="amazonUrl" data-pronto="Muy pronto" href="#">Ver en Amazon</a></p>
    </div>
    <div class="recuadro">
      <h3>Edición acompañada</h3>
      <p>Para quien quiere hacer el trabajo, no solo leerlo: el cuaderno «24 horas» con las herramientas de cada capítulo, plantillas descargables, un capítulo inédito y el audiolibro narrado por el autor (se entrega en enero). El libro se compra aparte, en Amazon.</p>
      <p style="margin-top:16px"><a class="boton primario" data-enlace="hotmartUrl" data-pronto="Muy pronto" href="#">Quiero la Edición acompañada</a></p>
    </div>
  </div>
</div></section>

<section><div class="contenedor autor">
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
<div class="texto"><div class="estrecho">
  <span class="fecha">Gratis</span>
  <h1>Lee la Introducción</h1>
  <p class="entradilla">Déjame tu correo y te mando la Introducción completa, «La máquina del tiempo y la grieta». Empieza así:</p>
  <blockquote class="cita" style="font-size:22px">Son las tres de la mañana del 13 de diciembre, y acabo de recordar que mi hermana cumplió años ayer.<br><br>No le llamé. No le escribí. Ni siquiera lo pensé.</blockquote>
  <p style="margin-top:28px">Estoy tirado en la cama, con los ojos abiertos, mirando el techo del departamento. No puedo dormir. En los oídos tengo un zumbido que no se detiene, un ruido fino que aturde cada pensamiento antes de que termine de formarse…</p>
  {formulario("introduccion", "Listo. Revisa tu correo en unos minutos (y la carpeta de promociones, por si acaso).", boton="Envíame la Introducción")}
</div></div>
"""
pagina("introduccion/index.html", f"Lee la Introducción · {TITULO}",
       "Recibe gratis la Introducción de «Ojalá hubiera sabido esto antes», de Ernesto Alvarez.", intro)

# ---------- Golden ticket ----------
ticket = f"""
<div class="texto"><div class="estrecho">
  <span class="fecha">Para quien llegó hasta el final</span>
  <h1>Una cosa más</h1>
  <p class="entradilla">Si llegaste hasta aquí, te guardé algo que no cabe en el libro: las hojas de trabajo de las herramientas y un texto que no entró, «Cómo escribí este libro».</p>
  <p>Escribe tu correo y la palabra que te pido al final del libro. Te llega todo por correo.</p>
  {formulario("ticket", "Listo. Revisa tu correo: ahí están tus descargas.", con_palabra=True, boton="Quiero mi regalo")}
</div></div>
"""
pagina("ticket/index.html", f"Una cosa más · {TITULO}",
       "Material adicional para lectores del libro.", ticket, indexar=False)

# ---------- Ayuda ----------
ayuda = """
<div class="texto"><div class="estrecho">
  <h1>Dónde pedir ayuda</h1>
  <p><strong>Si estás en peligro inmediato, o alguien cerca de ti lo está, llama al número de emergencias de tu país:</strong> 911 en México, Estados Unidos y buena parte de América Latina; 112 en España.</p>
  <p>Si lo que cargas pesa más de lo que puedes sostener solo, estas líneas son gratuitas y confidenciales:</p>
  <ul>
    <li><strong>México.</strong> Línea de la Vida: <a href="tel:8009112000">800 911 2000</a>. Atención las 24 horas.</li>
    <li><strong>España.</strong> Línea <a href="tel:024">024</a> de atención a la conducta suicida. Atención las 24 horas.</li>
    <li><strong>Argentina.</strong> Línea de salud mental del Ministerio de Salud de la Nación: <a href="tel:08009990091">0800 999 0091</a>. Atención las 24 horas.</li>
    <li><strong>Colombia.</strong> Línea Nacional de Teleorientación en Salud Mental: <a href="tel:106">106</a>. Atención las 24 horas.</li>
    <li><strong>Chile.</strong> Línea de prevención del suicidio: <a href="tel:*4141">*4141</a>.</li>
    <li><strong>Perú.</strong> Línea <a href="tel:113">113</a>, opción 5 (salud mental).</li>
    <li><strong>Estados Unidos, en español.</strong> Línea 988 de Prevención del Suicidio y Crisis: marca <a href="tel:988">988</a> y elige la opción 2.</li>
  </ul>
  <p>Si tu país no aparece aquí, el directorio internacional <a href="https://findahelpline.com" rel="noopener">Find A Helpline</a> reúne líneas gratuitas de muchos países.</p>
  <p>Y si el dolor es del cuerpo, la primera llamada es a tu médico. No esperes a que se vuelva insoportable.</p>
  <p class="nota">Números verificados el 9 de noviembre de 2026.</p>
</div></div>
"""
pagina("ayuda/index.html", f"Dónde pedir ayuda · {TITULO}",
       "Líneas gratuitas y confidenciales de apoyo emocional y prevención del suicidio en México, España, América Latina y Estados Unidos.", ayuda)

# ---------- Recursos ----------
recursos = """
<div class="texto"><div class="estrecho">
  <h1>Recursos</h1>
  <p>Las ideas que no son del autor tienen nombre y fuente en las notas de cada capítulo y en la bibliografía del libro. Aquí irán la bibliografía con enlaces, las notas por capítulo y la ficha de prensa.</p>
  <h2>Prensa y entrevistas</h2>
  <p>Ficha de prensa, portada en alta resolución y foto del autor: <em>disponibles a partir del lanzamiento.</em></p>
  <h2>Dónde pedir ayuda</h2>
  <p>La lista actualizada está en <a href="/ayuda/">Dónde pedir ayuda</a>.</p>
</div></div>
"""
pagina("recursos/index.html", f"Recursos · {TITULO}",
       "Bibliografía, notas y ficha de prensa del libro.", recursos)

# ---------- Privacidad (borrador) ----------
privacidad = """
<div class="texto"><div class="estrecho">
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
</div></div>
"""
pagina("privacidad/index.html", f"Aviso de privacidad · {TITULO}",
       "Aviso de privacidad del sitio del libro.", privacidad, indexar=False)

# ---------- 404 ----------
no_encontrada = """
<div class="texto"><div class="estrecho">
  <h1>Esta página no existe</h1>
  <p>Puede que el enlace esté mal escrito. Empieza por <a href="/">la página del libro</a>.</p>
  <p class="nota">¿Llegaste desde el código del libro? Ve a <a href="/ticket/">Una cosa más</a>.</p>
</div></div>
"""
pagina("404.html", f"Página no encontrada · {TITULO}", "Página no encontrada.", no_encontrada, indexar=False)
print("Páginas generadas en", RAIZ)
