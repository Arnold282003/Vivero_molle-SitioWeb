const moneda = new Intl.NumberFormat('es-PE', {
  style: 'currency',
  currency: 'PEN',
});

export const soles = (valor) => moneda.format(valor);
