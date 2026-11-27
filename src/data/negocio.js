// Datos del negocio: se usan en el pie, la página de contacto y el JSON-LD.
export const negocio = {
  nombre: 'Vivero Molle & Tara',
  descripcion:
    'Vivero familiar en Pachacámac con plantas de interior y exterior, frutales, huerto en casa y servicios de jardinería.',
  telefono: '+51900000000',
  telefonoVisible: '+51 900 000 000',
  correo: 'hola@molleytara.example',
  direccion: {
    calle: 'Av. Los Huarangos 482',
    distrito: 'Pachacámac',
    region: 'Lima',
    pais: 'PE',
  },
  horarios: [
    {
      texto: 'Martes a viernes',
      horas: '9:00 a. m. – 5:30 p. m.',
      dias: ['Tuesday', 'Wednesday', 'Thursday', 'Friday'],
      abre: '09:00',
      cierra: '17:30',
    },
    {
      texto: 'Sábados y domingos',
      horas: '9:00 a. m. – 6:00 p. m.',
      dias: ['Saturday', 'Sunday'],
      abre: '09:00',
      cierra: '18:00',
    },
  ],
  diaCerrado: 'Lunes cerrado',
};
