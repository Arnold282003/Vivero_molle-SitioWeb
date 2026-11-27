const boton = document.querySelector('.menu-boton');
const menu = document.getElementById('menu-principal');

if (boton && menu) {
  const abrir = (abierto) => {
    boton.setAttribute('aria-expanded', String(abierto));
    menu.classList.toggle('menu--abierto', abierto);
  };
  const estaAbierto = () => boton.getAttribute('aria-expanded') === 'true';

  boton.addEventListener('click', () => abrir(!estaAbierto()));

  menu.addEventListener('click', (evento) => {
    if (evento.target.closest('a')) abrir(false);
  });

  document.addEventListener('keydown', (evento) => {
    if (evento.key === 'Escape' && estaAbierto()) {
      abrir(false);
      boton.focus();
    }
  });

  // Mismo punto de quiebre que en global.css.
  window.matchMedia('(min-width: 48rem)').addEventListener('change', () => abrir(false));
}
