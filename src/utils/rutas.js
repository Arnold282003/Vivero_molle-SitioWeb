const base = import.meta.env.BASE_URL.replace(/\/$/, '');

/** Antepone la subcarpeta de publicación a una ruta interna. */
export const ruta = (destino = '') => `${base}/${destino.replace(/^\//, '')}`;
