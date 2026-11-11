# Construye el Cuaderno «24 horas» (HTML) para imprimir con Playwright.
import base64, io, pathlib
from PIL import Image

AQUI = pathlib.Path(__file__).parent
FUENTES = AQUI / "node_modules/@fontsource"
DIBUJO = pathlib.Path("/home/claude/libro-momentum/public/img/elefante-toro.png")
AYUDA_URL = "libro.momentumhub.cloud/ayuda"

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def png_b64(ancho):
    im = Image.open(DIBUJO)
    im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

# ---------- Contenido (sale del manuscrito; los pasos van resumidos, no copiados) ----------
CAPS = [
 (1, "No era disciplina, era abandono",
  "Ojalá hubiera sabido que mi cuerpo no era una máquina que podía exprimir sin consecuencias.",
  "¿Cuándo fue la última vez que tu cuerpo te pidió algo y le contestaste «después»?",
  [("Contesta el mensaje que dejaste en visto.", "Una sola frase verdadera, a alguien de los que permanecen."),
   ("Camina veinte minutos sin apagar nada.", "A la mitad, revisa pies, respiración y hombros. Si hoy no puedes caminar, siéntate junto a una ventana."),
   ("Haz la cita, y no le recortes nada al médico.", "Agéndala hoy. Antes de ir, anota qué te duele y desde cuándo.")],
  "Vuelve a la frase que escribiste en el margen. ¿A qué le llamas disciplina, o fortaleza, que si eres honesto es una forma de dejarte solo?", True),
 (2, "Preferí que pensaran que todo estaba bien",
  "Ojalá hubiera sabido que esconder el dolor no lo hace más pequeño.",
  "¿Cuántas veces dijiste «bien» esta semana sin que fuera cierto?",
  [("Haz la pausa de dos segundos.", "Antes de contestar «¿cómo estás?», nota cuál sería la respuesta verdadera."),
   ("Cambia un «bien» por una frase verdadera.", "Con una sola persona de confianza, sin drama."),
   ("Acuerda un porcentaje.", "Un número del 0 al 100 con alguien cercano. Estrénalo con el tuyo.")],
  "Vuelve a la frase que anotaste. ¿A quién has entrenado, sin querer, para que no te pregunte?", True),
 (3, "Solo lo repartía",
  "Ojalá hubiera sabido que irse no es lo mismo que sanar.",
  "¿De qué te alejaste creyendo que el dolor se iba a quedar ahí?",
  [("Nombra lo que terminó.", "Una línea con lo que perdiste, y también con lo que era bueno."),
   ("Deja un espacio en blanco.", "Treinta minutos sin meta, sin pantalla y sin plan."),
   ("Haz la prueba del semáforo.", "En la próxima espera, no busques el teléfono. Fíjate en qué llega.")],
  "¿Qué estás llenando de ruido para no sentir que algo terminó?", False),
 (4, "La culpa se quedó a vivir conmigo",
  "Ojalá hubiera sabido que cargar la culpa no es lo mismo que hacerme responsable.",
  "¿Qué alegría te has negado últimamente como si fuera una multa?",
  [("Haz la pregunta filtro.", "¿Se repara hoy, se corrige mañana o no hay nada que reparar?"),
   ("Si hay algo que reparar, hazlo pequeño y hoy.", "Una disculpa de una sola frase, sin «pero»."),
   ("Si no hay nada que reparar, quédate al postre.", "Un gusto pequeño, sin pagarlo después.")],
  "¿Qué estás pagando con tristeza que en realidad se paga con actos?", False),
 (5, "Padre en diferido",
  "Ojalá hubiera sabido que la presencia también se construye a distancia.",
  "¿A quién quieres que está lejos, y cuándo fue la última vez que le mandaste algo sin ningún motivo?",
  [("Manda una postal sin evento.", "Una foto y una línea: «Vi esto y me acordé de ti»."),
   ("Graba un minuto sin filtro.", "Un pedazo real de tu día, incluido lo que normalmente editarías."),
   ("Propón un ancla fija.", "Un momento a la semana que no dependa de grandes noticias.")],
  "¿Qué personaje interpretas con la gente que quieres y está lejos? ¿Qué pasaría si, la próxima vez, llegara el que eres un martes cualquiera?", False),
 (6, "Aprendieron a no necesitarme tanto",
  "Ojalá hubiera sabido que dejar de ser necesario no es dejar de ser importante.",
  "¿Quién eres cuando nadie necesita que lo rescates?",
  [("Muerde un consejo.", "Cambia «lo que tienes que hacer es…» por «¿cómo lo estás pensando tú?»."),
   ("Celebra sin «pero».", "Una frase para alguien que logró algo sin tu ayuda."),
   ("Haz algo que no sirva para nada.", "Media hora sin resolver nada. Fíjate en lo que sientes.")],
  "Si mañana nadie necesitara nada de ti, ¿qué te quedaría? ¿Y quién te seguiría eligiendo?", False),
 (7, "Soltar la guerra",
  "Ojalá hubiera sabido que aceptar no es rendirse.",
  "¿Contra qué realidad que ya no puedes cambiar sigues peleando todos los días?",
  [("Cuenta las flechas.", "La primera: lo que pasó. La segunda: lo que te sigues diciendo."),
   ("Reescribe la historia en dos columnas.", "Lo que no fue tuyo y lo que sí. Plantilla en la página {corte}."),
   ("Haz tu corte de caja.", "Diez minutos en frío; después, cierra el cuaderno. Página {corte}.")],
  "¿Qué historia te cuentas sobre lo que te pasó? ¿Cómo sonaría si la contaras desde lo que sí fue tuyo?", False),
 (8, "Esa persona ya no cabía en esta vida",
  "Ojalá hubiera sabido que no se vuelve atrás; se construye hacia adelante.",
  "¿A qué versión de ti sigues intentando volver?",
  [("Cambia la pregunta.", "Con lo que tienes hoy, ¿cómo se ve un buen día hoy?"),
   ("Deja un margen.", "Una hora sin asignar en tu agenda de mañana."),
   ("Mueve un objeto del pasado.", "No tienes que tirarlo. Solo sácalo del centro.")],
  "¿Qué del de antes te sigue sirviendo? ¿Qué ya no cabe en tu vida de hoy?", False),
 (9, "El primer ladrillo real",
  "Ojalá hubiera sabido que pedir ayuda es el primer acto de fuerza real.",
  "¿Qué llevas años intentando resolver solo?",
  [("Aplica la regla de los tres días.", "Lo que llevas tres días rumiando, cuéntaselo hoy a alguien. Página {ayuda}."),
   ("Pide ayuda específica, no salvamento.", "Termina la frase «Lo que me está ganando en esto es…». Página {ayuda}."),
   ("Revisa la casa completa.", "Cinco áreas de tu vida, del uno al diez. Página {casa}.")],
  "¿Qué ayuda dejaste de pedir porque creíste que ya debías saber resolverlo solo?", False),
 (10, "Negociar con el cuerpo",
  "Ojalá hubiera sabido que al cuerpo no se le gana; se le escucha.",
  "¿Contra qué parte de tu cuerpo llevas años peleando?",
  [("Para antes de la factura.", "Termina una actividad antes de tu límite. Página {setenta}."),
   ("Pide tregua en amarillo, no en rojo.", "Cuéntale a alguien cuál es tu amarillo. Página {amarillo}."),
   ("Deja de pelear con el ruido.", "Antes de declararle la guerra a una molestia, revisa hombros y mandíbula.")],
  "¿Contra qué parte de tu cuerpo sigues en guerra, y qué le ofrecerías si, en lugar de vencerla, tuvieras que llegar a un acuerdo con ella?", False),
 (11, "Con las manos torpes",
  "Ojalá hubiera sabido que no hace falta ser perfecto para seguir presente.",
  "¿A quién quieres cerca y no sabes cómo estar?",
  [("Cruza la puerta que está abierta hoy.", "Un gesto pequeño, sin esperar la ocasión grande."),
   ("Aparece aunque no te sientas perdonado.", "Con todo y el nudo en la garganta."),
   ("Usa el permiso del elefante verde.", "Tu vínculo como es hoy, y una sola cosa dentro de ese mapa.")],
  "¿Qué gesto pequeño has despreciado por no ser suficiente, y qué pasaría si lo hicieras de todos modos?", False),
]

# Números de página (la portada no lleva número)
P = {"usar": 1, "intro": 2}
p = 3
for c in CAPS:
    P[f"cap{c[0]}"] = p; p += 2
for k in ["corte", "ayuda", "casa", "setenta", "amarillo"]:
    P[k] = p; p += 1
P["carta"] = p; P["noche"] = p + 1; P["hoysé"] = p + 2; P["recursos"] = p + 3

AYUDA_LINEA = f"Si lo que escribes pesa más de lo que puedes cargar solo, no lo cargues solo. Página {P['recursos']} y {AYUDA_URL}."

def renglones(n=None, clase=""):
    if n is None:
        return f'<div class="renglones llena {clase}"></div>'
    return f'<div class="renglones {clase}" style="height:{n * 0.29:.2f}in"></div>'

def pagina(cuerpo, clase=""):
    return f'<section class="pagina {clase}">{cuerpo}</section>'

def casilla():
    return '<span class="casilla"></span>'

paginas = []

# 1 · Cómo usarlo
paginas.append(pagina(f"""
<p class="etiqueta">Antes de empezar</p>
<h1>Cómo usar este cuaderno</h1>
<p>Este cuaderno acompaña al libro <em>Ojalá hubiera sabido esto antes</em>. No lo resume: cada página te manda a un capítulo, y funciona mejor con el libro al lado.</p>
<p>La regla es una sola. Cuando termines un capítulo, abre su página, elige uno de los tres pasos y hazlo en las siguientes veinticuatro horas. Después anota la fecha y qué notaste.</p>
<p>No hace falta hacer los tres pasos, ni ir en orden, ni llenar todas las líneas. Puedes volver a un capítulo meses después; la segunda vez casi nunca se escribe lo mismo.</p>
<p>Las plantillas están en la página {P['corte']}, en hojas sueltas para imprimir las veces que haga falta. El cierre del libro, en la página {P['carta']}.</p>
<p>Lo que escribas aquí es tuyo. No tienes que enseñárselo a nadie.</p>
<div class="aviso">Este cuaderno acompaña; no sustituye la atención de un médico ni de un profesional de la salud mental. Si algo de lo que escribes pesa más de lo que puedes cargar solo, no lo cargues solo: en la página {P['recursos']} y en <strong>{AYUDA_URL}</strong> hay a dónde llamar.</div>
"""))

# 2 · Introducción
paginas.append(pagina(f"""
<p class="etiqueta">Introducción</p>
<h1>La máquina del tiempo y la grieta</h1>
<p class="ojala">Ojalá hubiera sabido que aguantar no es lo mismo que ser fuerte.</p>
<p class="pregunta">Si pudieras volver a un solo día de tu vida, ¿cuál sería, y qué te dirías?</p>
<p class="campo">El día</p>{renglones(3)}
<p class="campo">Lo que te dirías</p>{renglones()}
<p class="nota">Al final del cuaderno vas a volver a esta página.</p>
"""))

# Capítulos
for num, titulo, ojala, apertura, pasos, diario, margen in CAPS:
    filas = ""
    for i, (nombre, linea) in enumerate(pasos, 1):
        linea = linea.format(**P)
        filas += f"""
<div class="paso">
  <p class="paso-nombre">{casilla()}<span><strong>{nombre}</strong> {linea}</span></p>
  <p class="paso-datos"><span>Fecha</span><span class="raya"></span><span>Qué noté</span></p>
  {renglones(None, "paso-renglones")}
</div>"""
    extra = '<p class="nota">Aquí puedes anotar también la frase del margen.</p>' if margen else ""
    paginas.append(pagina(f"""
<p class="etiqueta">Capítulo {num}</p>
<h1>{titulo}</h1>
<p class="ojala">{ojala}</p>
<p class="pregunta">{apertura}</p>{extra}
{renglones(2)}
<h2>Tres pasos para las próximas 24 horas</h2>
<p class="nota">Elige uno. Si te animas, los tres.</p>
{filas}
""", "capitulo"))
    paginas.append(pagina(f"""
<p class="etiqueta">Capítulo {num} · Para el diario</p>
<p class="pregunta grande">{diario}</p>
{renglones()}
<p class="pie-ayuda">{AYUDA_LINEA}</p>
"""))

# Plantillas
def encabezado_plantilla(cap, titulo, bajada):
    return f"""<p class="etiqueta">Plantilla · {cap}</p><h1>{titulo}</h1><p class="bajada">{bajada}</p>
<p class="paso-datos solo"><span>Fecha</span><span class="raya"></span></p>"""

PIE_PLANTILLA = '<p class="pie-plantilla">Imprime esta hoja las veces que haga falta.</p>'

paginas.append(pagina(encabezado_plantilla("Cap. 7", "El corte de caja",
    "Para una guerra que sigues peleando contra algo que ya pasó.") + f"""
<p class="campo">La primera flecha: lo que pasó y no elegiste</p>{renglones(2)}
<p class="campo">La segunda flecha: lo que te sigues diciendo desde entonces</p>{renglones(2)}
<div class="columnas llena-col"><div><p class="campo">No fue mío</p>{renglones()}</div><div><p class="campo">Sí fue mío</p>{renglones()}</div></div>
<p class="campo">El corte: qué parte dependió de mí</p>{renglones(2)}
<p class="campo">El siguiente paso práctico</p>{renglones(2)}
<p class="nota">Si la guerra es reciente, date hasta mañana para estar enojado. Después haz el corte y cierra el cuaderno. El impuesto se paga una vez.</p>
{PIE_PLANTILLA}""", "plantilla"))

paginas.append(pagina(encabezado_plantilla("Cap. 9", "Ayuda específica",
    "La regla de los tres días, y una petición con nombre.") + f"""
<p class="campo">Llevo <span class="raya corta"></span> días dándole vueltas a</p>{renglones(2)}
<p class="campo">Lo que me está ganando en esto es…</p>
<p class="opciones">{casilla()} el miedo {casilla()} la duda {casilla()} la prisa {casilla()} el orgullo {casilla()} otro</p>{renglones(2)}
<p class="campo">Se lo voy a contar a</p>{renglones(1)}
<p class="campo">Lo que le voy a pedir, en una frase</p>{renglones(2)}
<p class="campo">Cómo lo ve desde afuera</p>{renglones()}
{PIE_PLANTILLA}""", "plantilla"))

AREAS = ["Salud", "Pareja o vínculos cercanos", "Trabajo", "Dinero", "Tiempo para ti"]
filas_casa = "".join(f"<tr><th>{a}</th><td></td><td></td><td></td></tr>" for a in AREAS)
paginas.append(pagina(encabezado_plantilla("Cap. 9", "La casa completa",
    "Cinco áreas de tu vida, del uno al diez. Puedes repetirla cada cierto tiempo y comparar.").replace(
    '<p class="paso-datos solo"><span>Fecha</span><span class="raya"></span></p>', "") + f"""
<table class="tabla casa"><thead><tr><th>Área</th><th>Fecha:<br>&nbsp;</th><th>Fecha:<br>&nbsp;</th><th>Fecha:<br>&nbsp;</th></tr></thead><tbody>{filas_casa}</tbody></table>
<p class="campo">Si una va muy por encima de las otras, ¿qué te está cobrando?</p>{renglones(4)}
<p class="campo">Si alguna está muy abajo, ¿a quién podrías pedirle ayuda con esa?</p>{renglones()}
{PIE_PLANTILLA}""", "plantilla"))

filas_70 = "".join("<tr><td></td><td></td><td></td><td></td><td></td></tr>" for _ in range(11))
paginas.append(pagina(encabezado_plantilla("Cap. 10", "La regla del 70 %",
    "Termina antes de tu límite, aunque sientas que todavía te queda cuerda.").replace(
    '<p class="paso-datos solo"><span>Fecha</span><span class="raya"></span></p>', "") + f"""
<table class="tabla setenta"><thead><tr><th>Fecha</th><th>Actividad</th><th>Mi límite y mi 70 %</th><th>Hasta dónde llegué</th><th>Cómo amanecí al día siguiente</th></tr></thead><tbody>{filas_70}</tbody></table>
<p class="nota">El setenta por ciento es una regla de tanteo del autor, sin pretensión científica. Si vives con una condición de salud, acuerda con tu médico cuánto y cómo moverte.</p>
{PIE_PLANTILLA}""", "plantilla"))

paginas.append(pagina(encabezado_plantilla("Cap. 10", "El aviso en amarillo",
    "Pide tregua cuando empieza, no cuando ya no tiene remedio.") + f"""
<p class="campo">Mi amarillo se siente así (las primeras señales)</p>{renglones(2)}
<p class="campo">Mi rojo se siente así</p>{renglones(2)}
<p class="campo">Cuando aparece el amarillo, necesito</p>{renglones()}
<p class="campo">Cómo lo voy a decir, en una frase</p>{renglones(2)}
<p class="campo">En el trabajo, lo digo así</p>{renglones(2)}
<p class="paso-datos solo"><span>Se lo conté a</span><span class="raya"></span></p>
{PIE_PLANTILLA}""", "plantilla"))

# Cierre
paginas.append(pagina(f"""
<p class="etiqueta">Conclusión</p>
<h1>Todavía puedo elegirme</h1>
<p class="ojala">Ojalá hubiera sabido que siempre puedo volver a elegirme.</p>
<p class="pregunta">¿A quién le escribirías una carta, si pudieras mandarla hacia atrás?</p>
<p class="nota">Vuelve a la página {P['intro']}. Escríbele a quien eras ese día.</p>
{renglones()}
"""))

paginas.append(pagina(f"""
<p class="etiqueta">Conclusión · Una pregunta y un gesto</p>
<h2 class="primero">Esta noche</h2>
<p class="pregunta">Antes de apagar la luz: ¿en qué rincón de tu vida estás llamando «disciplina», «lealtad» o «fortaleza» a lo que en realidad es abandono?</p>
{renglones()}
<h2>Mañana, a primera hora</h2>
<p class="nota">Un solo gesto físico. Cancelar una carga que no te toca, agendar la consulta que llevas meses posponiendo, apagar la pantalla a tiempo, marcar un teléfono para pedir ayuda.</p>
<p class="paso-nombre">{casilla()}<span><strong>Mi gesto:</strong></span></p>{renglones(2)}
<p class="paso-datos solo"><span>Fecha</span><span class="raya"></span></p>
<p class="pie-ayuda">{AYUDA_LINEA}</p>
"""))

hoy = "".join('<p class="hoyse">Hoy sé que</p>' for _ in range(11))
paginas.append(pagina(f"""
<p class="etiqueta">Conclusión · Hoy sé</p>
<h1>Las tuyas</h1>
<p>Cada capítulo del libro empezó con «Ojalá hubiera sabido…». Al final, esas frases se volvieron «Hoy sé». Escribe las tuyas.</p>
{hoy}
"""))

paginas.append(pagina(f"""
<p class="etiqueta">Recursos</p>
<h1>Dónde pedir ayuda</h1>
<p><strong>Si estás en peligro inmediato, o alguien cerca de ti lo está, llama al número de emergencias de tu país:</strong> 911 en México, Estados Unidos y buena parte de América Latina; 112 en España.</p>
<p>Si lo que cargas pesa más de lo que puedes sostener solo, estas líneas son gratuitas y confidenciales:</p>
<ul class="recursos">
<li><strong>México.</strong> Línea de la Vida: 800 911 2000. Las 24 horas.</li>
<li><strong>España.</strong> Línea 024 de atención a la conducta suicida. Las 24 horas.</li>
<li><strong>Argentina.</strong> Línea de salud mental del Ministerio de Salud: 0800 999 0091. Las 24 horas.</li>
<li><strong>Colombia.</strong> Línea Nacional de Teleorientación en Salud Mental: 106. Las 24 horas.</li>
<li><strong>Chile.</strong> Línea de prevención del suicidio: *4141.</li>
<li><strong>Perú.</strong> Línea 113, opción 5 (salud mental).</li>
<li><strong>Estados Unidos, en español.</strong> Línea 988: marca 988 y elige la opción 2.</li>
</ul>
<p>Si tu país no aparece aquí, findahelpline.com reúne líneas gratuitas de muchos países. Y si el dolor es del cuerpo, la primera llamada es a tu médico.</p>
<p class="nota">Lista verificada el 9 de noviembre de 2026. La versión actualizada está en <strong>{AYUDA_URL}</strong>.</p>
<p class="creditos">Cuaderno 24 horas · © 2026 Ernesto Alvarez. Para uso personal de los lectores de <em>Ojalá hubiera sabido esto antes</em>. Puedes imprimirlo las veces que quieras; por favor, no lo vendas ni lo compartas fuera de tu uso personal.</p>
"""))

assert len(paginas) == P["recursos"], (len(paginas), P)

CSS = f"""
@font-face {{ font-family: Archivo; font-weight: 400; src: url(data:font/woff2;base64,{b64(FUENTES/'archivo/files/archivo-latin-400-normal.woff2')}) format('woff2'); }}
@font-face {{ font-family: Archivo; font-weight: 600; src: url(data:font/woff2;base64,{b64(FUENTES/'archivo/files/archivo-latin-600-normal.woff2')}) format('woff2'); }}
@font-face {{ font-family: Archivo; font-weight: 800; src: url(data:font/woff2;base64,{b64(FUENTES/'archivo/files/archivo-latin-800-normal.woff2')}) format('woff2'); }}
@font-face {{ font-family: Instrument; font-style: normal; src: url(data:font/woff2;base64,{b64(FUENTES/'instrument-serif/files/instrument-serif-latin-400-normal.woff2')}) format('woff2'); }}
@font-face {{ font-family: Instrument; font-style: italic; src: url(data:font/woff2;base64,{b64(FUENTES/'instrument-serif/files/instrument-serif-latin-400-italic.woff2')}) format('woff2'); }}
:root {{ --tinta:#1b1a17; --tinta2:#3a3832; --tinta3:#5f5b52; --verde:#3d7650; --verde-o:#2f5e3c; --linea:#cfc6b6; --papel:#efe9de; }}
@page {{ size: 5.5in 8.5in; margin: 0.55in 0.55in 0.7in; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; }}
body {{ font-family: Archivo, sans-serif; font-size: 9.5pt; line-height: 1.45; color: var(--tinta); }}
.pagina {{ height: 7.2in; display: flex; flex-direction: column; break-after: page; overflow: hidden; }}
.pagina:last-child {{ break-after: auto; }}
p {{ margin: 0 0 6pt; }}
h1 {{ font-family: Instrument, serif; font-weight: 400; font-size: 24pt; line-height: 1.05; margin: 0 0 6pt; }}
h2 {{ font-family: Archivo; font-weight: 800; font-size: 8pt; letter-spacing: .09em; text-transform: uppercase; color: var(--verde-o); margin: 10pt 0 2pt; }}
h2.primero {{ margin-top: 4pt; }}
.etiqueta {{ font-weight: 600; font-size: 7.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--verde-o); margin: 0 0 4pt; }}
.ojala {{ font-family: Instrument, serif; font-style: italic; font-size: 12.5pt; line-height: 1.25; color: var(--tinta2); margin-bottom: 8pt; }}
.pregunta {{ font-weight: 600; font-size: 10pt; line-height: 1.35; padding-left: 8pt; border-left: 2.5pt solid var(--verde); margin: 2pt 0 4pt; }}
.pregunta.grande {{ font-family: Instrument, serif; font-weight: 400; font-size: 15pt; line-height: 1.25; margin: 4pt 0 10pt; }}
.nota {{ font-size: 8pt; color: var(--tinta3); margin: 0 0 4pt; }}
.bajada {{ color: var(--tinta2); margin-bottom: 6pt; }}
.campo {{ font-weight: 600; font-size: 8.5pt; margin: 11pt 0 0; color: var(--tinta2); }}
.renglones {{ background-image: repeating-linear-gradient(to bottom, transparent 0, transparent calc(0.29in - 0.6pt), var(--linea) calc(0.29in - 0.6pt), var(--linea) 0.29in); flex-shrink: 0; }}
.renglones.llena {{ flex: 1 1 auto; min-height: 1in; }}
.paso {{ margin-top: 7pt; flex: 1 1 0; display: flex; flex-direction: column; min-height: 0; }}
.paso .renglones.llena {{ min-height: .58in; }}
.paso-nombre {{ display: flex; gap: 6pt; align-items: flex-start; margin: 0; line-height: 1.35; }}
.paso-nombre strong {{ font-weight: 800; }}
.casilla {{ display: inline-block; width: 9pt; height: 9pt; border: 1.2pt solid var(--tinta); border-radius: 1.5pt; flex-shrink: 0; margin-top: 1.5pt; vertical-align: -1pt; }}
.opciones .casilla {{ margin: 0 2pt 0 8pt; }}
.opciones .casilla:first-child {{ margin-left: 0; }}
.paso-datos {{ display: flex; align-items: flex-end; gap: 5pt; font-size: 7.5pt; letter-spacing: .06em; text-transform: uppercase; color: var(--tinta3); margin: 5pt 0 0 15pt; }}
.paso-datos.solo {{ margin-left: 0; margin-top: 8pt; }}
.paso-datos .raya {{ border-bottom: .6pt solid var(--linea); width: 1.1in; height: 9pt; margin-right: 10pt; }}
.paso-datos.solo .raya {{ flex: 1; }}
.raya.corta {{ display: inline-block; border-bottom: .6pt solid var(--linea); width: .5in; }}
.paso-renglones {{ margin-left: 15pt; }}
.pie-ayuda {{ font-size: 7pt; color: var(--tinta3); margin: 6pt 0 0; padding-top: 4pt; border-top: .6pt solid var(--linea); }}
.pie-plantilla {{ margin-top: auto; font-size: 7pt; color: var(--tinta3); text-align: right; }}
.columnas {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14pt; }}
.pagina > * {{ flex-shrink: 0; }}
.pagina > .renglones.llena {{ flex: 1 1 auto; }}
.columnas.llena-col {{ flex: 1 1 auto; }}
.llena-col > div {{ display: flex; flex-direction: column; }}
.llena-col .renglones.llena {{ flex: 1 1 auto; }}
.aviso {{ margin-top: auto; background: var(--papel); padding: 10pt 12pt; border-radius: 4pt; font-size: 8.5pt; line-height: 1.4; }}
.tabla {{ width: 100%; border-collapse: collapse; margin: 8pt 0 6pt; font-size: 8pt; }}
.tabla th {{ text-align: left; font-weight: 600; color: var(--tinta2); padding: 4pt; border-bottom: 1pt solid var(--tinta); vertical-align: bottom; }}
.tabla td, .tabla tbody th {{ border-bottom: .6pt solid var(--linea); padding: 4pt; }}
.casa tbody th {{ font-weight: 600; height: .42in; width: 40%; }}
.casa td {{ border-left: .6pt solid var(--linea); }}
.setenta td {{ height: .42in; border-left: .6pt solid var(--linea); }}
.setenta td:first-child {{ border-left: 0; }}
.setenta th {{ font-size: 7pt; }}
.hoyse {{ font-family: Instrument, serif; font-style: italic; font-size: 12pt; color: var(--tinta2); border-bottom: .6pt solid var(--linea); padding: 12pt 0 3pt; margin: 0; }}
ul.recursos {{ padding-left: 12pt; margin: 0 0 6pt; }}
ul.recursos li {{ margin-bottom: 3pt; }}
.creditos {{ margin-top: auto; font-size: 7pt; color: var(--tinta3); border-top: .6pt solid var(--linea); padding-top: 6pt; }}
"""

html = f'<!doctype html><html lang="es"><meta charset="utf-8"><title>Cuaderno 24 horas</title><style>{CSS}</style><body>{"".join(paginas)}</body></html>'
(AQUI / "cuaderno.html").write_text(html, encoding="utf-8")

# Portada (sin pie de página)
portada = f"""<!doctype html><html lang="es"><meta charset="utf-8"><style>{CSS}
@page {{ size: 5.5in 8.5in; margin: 0; }}
.portada {{ width: 5.5in; height: 8.5in; background: var(--papel); padding: .75in .6in .6in; display: flex; flex-direction: column; justify-content: space-between; }}
.p-titulo {{ font-family: Archivo; font-weight: 800; text-transform: uppercase; font-size: 46pt; line-height: .9; letter-spacing: -.035em; margin: 0; }}
.p-sub {{ font-family: Instrument, serif; font-style: italic; font-size: 15pt; line-height: 1.2; color: var(--tinta2); margin: 12pt 0 0; }}
.p-dibujo {{ border-bottom: 2pt solid var(--tinta); }}
.p-dibujo img {{ width: 100%; display: block; }}
.p-autor {{ font-size: 10pt; letter-spacing: .12em; text-transform: uppercase; font-weight: 600; margin: 0; }}
</style><body><div class="portada">
<div><p class="p-titulo">Cuaderno<br>24 horas</p>
<p class="p-sub">Las herramientas de <span style="font-style:normal">Ojalá hubiera sabido esto antes</span>, con espacio para escribir</p></div>
<div class="p-dibujo"><img src="data:image/png;base64,{png_b64(900)}" alt=""></div>
<p class="p-autor">Ernesto Alvarez</p></div></body></html>"""
(AQUI / "portada.html").write_text(portada, encoding="utf-8")

pie = f"""<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7.5pt;color:#5f5b52;display:flex;justify-content:center;align-items:center;gap:6px;padding-bottom:0.28in;-webkit-print-color-adjust:exact;">
<img src="data:image/png;base64,{png_b64(120)}" style="height:13px;width:auto;"><span class="pageNumber"></span></div>"""
(AQUI / "pie.html").write_text(pie, encoding="utf-8")
print(len(paginas), "páginas numeradas;", P)
