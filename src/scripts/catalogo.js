const lista = document.getElementById('lista-catalogo');
const busqueda = document.getElementById('busqueda');
const chips = [...document.querySelectorAll('.chip')];
const conteo = document.getElementById('conteo');
const vacio = document.getElementById('sin-resultados');

// Compara sin mayúsculas ni tildes: "arbol" encuentra "Árbol".
const normalizar = (texto) =>
  texto.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().trim();

const elementos = [...lista.children].map((nodo) => ({
  nodo,
  categoria: nodo.dataset.categoria,
  texto: normalizar(nodo.dataset.texto),
}));

let categoria = '';

function filtrar() {
  const palabras = normalizar(busqueda.value).split(/\s+/).filter(Boolean);
  let visibles = 0;

  for (const elemento of elementos) {
    const coincide =
      (!categoria || elemento.categoria === categoria) &&
      palabras.every((palabra) => elemento.texto.includes(palabra));
    elemento.nodo.hidden = !coincide;
    if (coincide) visibles += 1;
  }

  conteo.textContent = visibles === 1 ? '1 resultado' : `${visibles} resultados`;
  vacio.hidden = visibles > 0;
  guardarEnUrl();
}

function elegirCategoria(valor) {
  categoria = valor;
  for (const chip of chips) {
    chip.setAttribute('aria-pressed', String(chip.dataset.categoria === valor));
  }
}

// La URL refleja el filtro para poder compartirlo.
function guardarEnUrl() {
  const url = new URL(window.location.href);
  const valores = { categoria, q: busqueda.value.trim() };
  for (const [clave, valor] of Object.entries(valores)) {
    if (valor) url.searchParams.set(clave, valor);
    else url.searchParams.delete(clave);
  }
  window.history.replaceState(null, '', url);
}

for (const chip of chips) {
  chip.addEventListener('click', () => {
    elegirCategoria(chip.dataset.categoria);
    filtrar();
  });
}

busqueda.addEventListener('input', filtrar);

document.getElementById('limpiar').addEventListener('click', () => {
  busqueda.value = '';
  elegirCategoria('');
  filtrar();
  busqueda.focus();
});

const parametros = new URLSearchParams(window.location.search);
const inicial = parametros.get('categoria') ?? '';
busqueda.value = parametros.get('q') ?? '';
elegirCategoria(chips.some((c) => c.dataset.categoria === inicial) ? inicial : '');
filtrar();
