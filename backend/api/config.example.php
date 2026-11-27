<?php
// Copia este archivo como config.php y completa tus datos.
// config.php está en .gitignore: no lo subas al repositorio.

return [
    'bd' => [
        'host'    => '127.0.0.1',
        'puerto'  => 3306,
        'nombre'  => 'molle_tara',
        'usuario' => 'tu_usuario',
        'clave'   => 'tu_clave',
    ],

    // Orígenes externos que pueden enviar el formulario (sin barra final).
    // El mismo dominio donde está este archivo siempre se permite.
    'origenes_permitidos' => [
        'http://localhost:4321', // npm run dev
        // 'https://tu-sitio.netlify.app',
    ],

    // Texto largo y aleatorio para anonimizar la IP.
    'sal' => 'cambia-este-texto-por-uno-aleatorio',

    'envios_por_10_min' => 5,
];
