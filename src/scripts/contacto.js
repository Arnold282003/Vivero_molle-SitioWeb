const formulario = document.getElementById('formulario-contacto');
const estado = document.getElementById('estado-formulario');
const botonEnviar = formulario.querySelector('[type="submit"]');
const campos = ['nombre', 'correo', 'telefono', 'asunto', 'mensaje', 'consentimiento'];

// Cuenta caracteres como PHP (mb_strlen), no unidades UTF-16.
const largo = (texto) => [...texto].length;

// Mismas reglas que backend/api/contacto.php, que es quien tiene la última palabra.
const reglas = {
  nombre(valor) {
    if (!valor) return 'Escribe tu nombre.';
    if (largo(valor) < 2 || largo(valor) > 80) return 'El nombre debe tener entre 2 y 80 caracteres.';
    if (!/^[\p{L}\p{M} .'’-]+$/u.test(valor)) return 'Usa solo letras, espacios, puntos o guiones.';
    return '';
  },
  correo(valor) {
    if (!valor) return 'Escribe tu correo.';
    if (valor.length > 120 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(valor)) {
      return 'Revisa el formato del correo, por ejemplo: nombre@dominio.com';
    }
    return '';
  },
  telefono(valor) {
    if (!valor) return '';
    const digitos = valor.replace(/\D/g, '').length;
    if (!/^\+?[\d ()-]{6,20}$/.test(valor) || digitos < 6 || digitos > 15) {
      return 'Escribe un teléfono válido o deja el campo vacío.';
    }
    return '';
  },
  asunto: (valor) => (valor ? '' : 'Elige un asunto.'),
  mensaje(valor) {
    if (largo(valor) < 10) return 'Cuéntanos un poco más (mínimo 10 caracteres).';
    if (largo(valor) > 1000) return 'El mensaje no puede superar los 1000 caracteres.';
    return '';
  },
  consentimiento: (_valor, control) =>
    control.checked ? '' : 'Necesitamos tu aceptación para responderte.',
};

function mostrarError(nombre, texto) {
  const control = formulario.elements[nombre];
  document.getElementById(`error-${nombre}`).textContent = texto;
  if (texto) control.setAttribute('aria-invalid', 'true');
  else control.removeAttribute('aria-invalid');
}

function validar(nombre) {
  const control = formulario.elements[nombre];
  const texto = reglas[nombre](control.value.trim(), control);
  mostrarError(nombre, texto);
  return !texto;
}

function avisar(texto, tipo = '') {
  estado.textContent = texto;
  estado.dataset.tipo = tipo;
}

// Desactiva los globos del navegador para mostrar mensajes propios.
formulario.noValidate = true;

for (const nombre of campos) {
  const control = formulario.elements[nombre];
  control.addEventListener('blur', () => {
    if (control.value.trim() || control.hasAttribute('aria-invalid')) validar(nombre);
  });
  control.addEventListener(control.type === 'checkbox' ? 'change' : 'input', () => {
    if (control.hasAttribute('aria-invalid')) validar(nombre);
  });
}

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  avisar('');

  const invalidos = campos.filter((nombre) => !validar(nombre));
  if (invalidos.length) {
    avisar('Revisa los campos marcados.', 'error');
    formulario.elements[invalidos[0]].focus();
    return;
  }

  const cuerpo = new URLSearchParams(new FormData(formulario));
  const cancelar = new AbortController();
  const limite = setTimeout(() => cancelar.abort(), 15000);
  botonEnviar.disabled = true;
  avisar('Enviando…');

  try {
    const respuesta = await fetch(formulario.action, {
      method: 'POST',
      headers: { Accept: 'application/json' },
      body: cuerpo,
      signal: cancelar.signal,
    });
    const datos = await respuesta.json();

    if (respuesta.ok && datos.ok) {
      formulario.reset();
      avisar(datos.mensaje, 'exito');
    } else if (datos.errores) {
      for (const [nombre, texto] of Object.entries(datos.errores)) {
        if (campos.includes(nombre)) mostrarError(nombre, texto);
      }
      avisar(datos.mensaje, 'error');
      formulario.querySelector('[aria-invalid="true"]')?.focus();
    } else {
      throw new Error(datos.mensaje);
    }
  } catch {
    // Sin servidor, sin conexión o respuesta inesperada.
    avisar(
      `No pudimos enviar tu mensaje. Inténtalo más tarde o escríbenos a ${formulario.dataset.correo}.`,
      'error',
    );
  } finally {
    clearTimeout(limite);
    botonEnviar.disabled = false;
  }
});

// Prellenado desde el catálogo. Solo se aceptan identificadores conocidos.
const referencias = JSON.parse(formulario.dataset.referencias);
const id = new URLSearchParams(window.location.search).get('item');
if (id && Object.hasOwn(referencias, id)) {
  const { nombre, tipo } = referencias[id];
  formulario.elements.asunto.value = tipo;
  formulario.elements.mensaje.value = `Hola, quisiera información sobre: ${nombre}.`;
}
