(function () {
  var cfg = window.LIBRO || {};

  // Botones de venta: se activan solo cuando hay enlace.
  document.querySelectorAll("[data-enlace]").forEach(function (a) {
    var url = cfg[a.getAttribute("data-enlace")];
    if (url) {
      a.href = url + (url.indexOf("?") > -1 ? "&" : "?") + "utm_source=libro.momentumhub.cloud";
      a.removeAttribute("aria-disabled");
    } else {
      a.setAttribute("aria-disabled", "true");
      a.removeAttribute("href");
      var etiqueta = a.getAttribute("data-pronto");
      if (etiqueta) a.textContent = etiqueta;
    }
  });
  document.querySelectorAll("[data-fecha]").forEach(function (el) {
    if (cfg.fechaLanzamiento) el.textContent = cfg.fechaLanzamiento;
  });

  // Luz: de día o luz baja. La elección se guarda en este navegador.
  var raiz = document.documentElement;
  document.querySelectorAll("[data-luz-boton]").forEach(function (b) {
    function pinta() {
      var baja = raiz.getAttribute("data-luz") === "baja";
      b.setAttribute("aria-pressed", baja ? "true" : "false");
      b.querySelector("span").textContent = baja ? "Subir la luz" : "Bajar la luz";
    }
    b.addEventListener("click", function () {
      var baja = raiz.getAttribute("data-luz") !== "baja";
      if (baja) raiz.setAttribute("data-luz", "baja"); else raiz.removeAttribute("data-luz");
      try { localStorage.setItem("luz", baja ? "baja" : "dia"); } catch (e) {}
      pinta();
    });
    pinta();
  });

  // Formularios de registro.
  var params = new URLSearchParams(location.search);
  document.querySelectorAll("form[data-origen]").forEach(function (form) {
    var mensaje = form.querySelector(".mensaje");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var boton = form.querySelector("button[type=submit]");
      var datos = {
        origen: form.getAttribute("data-origen"),
        nombre: (form.nombre && form.nombre.value) || "",
        correo: form.correo.value,
        palabra: (form.palabra && form.palabra.value) || "",
        consentimiento: form.consentimiento.checked,
        sitio_web: form.sitio_web.value,
        utm_source: params.get("utm_source") || "",
        utm_medium: params.get("utm_medium") || "",
        utm_campaign: params.get("utm_campaign") || "",
      };
      mensaje.className = "mensaje";
      mensaje.textContent = "Enviando…";
      boton.disabled = true;
      fetch("/api/registro", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(datos),
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            mensaje.className = "mensaje ok";
            mensaje.textContent = form.getAttribute("data-exito");
            if (res.enlace) {
              var a = document.createElement("a");
              a.href = res.enlace;
              a.className = "boton";
              a.textContent = "Ir a mis descargas";
              mensaje.appendChild(document.createElement("br"));
              mensaje.appendChild(a);
              setTimeout(function () { location.href = res.enlace; }, 2500);
            }
          } else {
            mensaje.className = "mensaje error";
            mensaje.textContent = res.error || "Algo salió mal. Inténtalo de nuevo.";
          }
        })
        .catch(function () {
          mensaje.className = "mensaje error";
          mensaje.textContent = "No hay conexión. Inténtalo de nuevo.";
        })
        .finally(function () { boton.disabled = false; });
    });
  });
})();
