<?php
/**
 * Recibe el formulario de contacto y lo guarda en MySQL.
 * Responde JSON a las peticiones con "Accept: application/json"
 * y una página sencilla si el formulario se envía sin JavaScript.
 */

declare(strict_types=1);

ini_set('display_errors', '0');

const ASUNTOS = ['producto', 'servicio', 'visita', 'otro'];
const TAMANO_MAXIMO = 20000; // bytes de la petición

function responder(int $codigo, bool $ok, string $mensaje, array $errores = []): never
{
    http_response_code($codigo);
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');

    if (str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json')) {
        header('Content-Type: application/json; charset=utf-8');
        $cuerpo = ['ok' => $ok, 'mensaje' => $mensaje];
        if ($errores) {
            $cuerpo['errores'] = $errores;
        }
        echo json_encode($cuerpo, JSON_UNESCAPED_UNICODE);
        exit;
    }

    header('Content-Type: text/html; charset=utf-8');
    $escapar = static fn (string $t): string => htmlspecialchars($t, ENT_QUOTES, 'UTF-8');
    $lista = '';
    foreach ($errores as $error) {
        $lista .= '<li>' . $escapar($error) . '</li>';
    }
    echo '<!doctype html><html lang="es-PE"><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width, initial-scale=1">'
        . '<title>Contacto | Molle &amp; Tara</title>'
        . '<body style="font-family:system-ui,sans-serif;max-width:32rem;margin:3rem auto;padding:0 1rem">'
        . '<h1>' . $escapar($mensaje) . '</h1>'
        . ($lista !== '' ? "<ul>$lista</ul>" : '')
        . '<p>Usa el botón «Atrás» de tu navegador para volver al sitio.</p>';
    exit;
}

/** Lee un campo de texto y elimina caracteres de control y etiquetas HTML. */
function campo(string $nombre, bool $multilinea = false): string
{
    $valor = $_POST[$nombre] ?? '';
    // Descarta arreglos (campo[]=x) y texto que no sea UTF-8 válido.
    if (!is_string($valor) || !mb_check_encoding($valor, 'UTF-8')) {
        return '';
    }
    $valor = str_replace(["\r\n", "\r"], "\n", $valor);
    $valor = preg_replace('/[^\P{Cc}\n\t]/u', '', $valor);
    // Se repite por si al quitar una etiqueta se forma otra.
    do {
        $valor = preg_replace('/<\/?[a-z!][^<>]*>/iu', '', $valor, -1, $quitadas);
    } while ($quitadas > 0);
    if (!$multilinea) {
        $valor = preg_replace('/\s+/u', ' ', $valor);
    }
    return trim($valor);
}

function validar(array $d): array
{
    $errores = [];

    $largoNombre = mb_strlen($d['nombre']);
    if ($largoNombre < 2 || $largoNombre > 80) {
        $errores['nombre'] = 'El nombre debe tener entre 2 y 80 caracteres.';
    } elseif (!preg_match('/^[\p{L}\p{M} .\'’-]+$/u', $d['nombre'])) {
        $errores['nombre'] = 'Usa solo letras, espacios, puntos o guiones.';
    }

    if (strlen($d['correo']) > 120 || filter_var($d['correo'], FILTER_VALIDATE_EMAIL) === false) {
        $errores['correo'] = 'Revisa el formato del correo.';
    }

    if ($d['telefono'] !== '') {
        $digitos = strlen(preg_replace('/\D/', '', $d['telefono']));
        if (!preg_match('/^\+?[\d ()-]{6,20}$/D', $d['telefono']) || $digitos < 6 || $digitos > 15) {
            $errores['telefono'] = 'Escribe un teléfono válido o deja el campo vacío.';
        }
    }

    if (!in_array($d['asunto'], ASUNTOS, true)) {
        $errores['asunto'] = 'Elige un asunto de la lista.';
    }

    $largoMensaje = mb_strlen($d['mensaje']);
    if ($largoMensaje < 10 || $largoMensaje > 1000) {
        $errores['mensaje'] = 'El mensaje debe tener entre 10 y 1000 caracteres.';
    }

    if ($d['consentimiento'] !== '1') {
        $errores['consentimiento'] = 'Necesitamos tu aceptación para responderte.';
    }

    return $errores;
}

$rutaConfig = __DIR__ . '/config.php';
if (!is_file($rutaConfig)) {
    error_log('Contacto: falta config.php (copia config.example.php).');
    responder(500, false, 'El formulario no está disponible por el momento.');
}
$config = require $rutaConfig;

// Solo se aceptan envíos del mismo sitio o de los orígenes autorizados.
$origen = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origen !== '') {
    $partes = parse_url($origen);
    $anfitrion = ($partes['host'] ?? '') . (isset($partes['port']) ? ':' . $partes['port'] : '');
    $mismoSitio = $anfitrion === ($_SERVER['HTTP_HOST'] ?? '');
    $autorizado = in_array($origen, $config['origenes_permitidos'], true);

    if (!$mismoSitio && !$autorizado) {
        responder(403, false, 'Origen no autorizado.');
    }
    if ($autorizado) {
        header("Access-Control-Allow-Origin: $origen");
        header('Vary: Origin');
    }
}

$metodo = $_SERVER['REQUEST_METHOD'] ?? '';
if ($metodo === 'OPTIONS') {
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Accept');
    http_response_code(204);
    exit;
}
if ($metodo !== 'POST') {
    header('Allow: POST, OPTIONS');
    responder(405, false, 'Método no permitido.');
}
if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > TAMANO_MAXIMO) {
    responder(413, false, 'El envío es demasiado grande.');
}

$exito = 'Gracias, recibimos tu mensaje. Te responderemos pronto.';

// Si el campo trampa viene lleno es un bot: se simula el éxito y no se guarda.
if (($_POST['sitio_web'] ?? '') !== '') {
    responder(200, true, $exito);
}

$datos = [
    'nombre'         => campo('nombre'),
    'correo'         => campo('correo'),
    'telefono'       => campo('telefono'),
    'asunto'         => campo('asunto'),
    'mensaje'        => campo('mensaje', true),
    'consentimiento' => campo('consentimiento'),
];

$errores = validar($datos);
if ($errores) {
    responder(422, false, 'Revisa los campos marcados.', $errores);
}

try {
    $bd = $config['bd'];
    $pdo = new PDO(
        sprintf(
            'mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',
            $bd['host'],
            $bd['puerto'],
            $bd['nombre'],
        ),
        $bd['usuario'],
        $bd['clave'],
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_EMULATE_PREPARES => false,
        ],
    );

    // La IP no se guarda en claro: solo un resumen para limitar envíos repetidos.
    $huella = hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? '', $config['sal']);

    $recientes = $pdo->prepare(
        'SELECT COUNT(*) FROM mensajes_contacto
         WHERE huella_ip = :huella AND creado_en > NOW() - INTERVAL 10 MINUTE'
    );
    $recientes->execute([':huella' => $huella]);
    if ((int) $recientes->fetchColumn() >= $config['envios_por_10_min']) {
        responder(429, false, 'Recibimos varios mensajes seguidos. Espera unos minutos.');
    }

    $insertar = $pdo->prepare(
        'INSERT INTO mensajes_contacto (nombre, correo, telefono, asunto, mensaje, huella_ip)
         VALUES (:nombre, :correo, :telefono, :asunto, :mensaje, :huella)'
    );
    $insertar->execute([
        ':nombre'   => $datos['nombre'],
        ':correo'   => $datos['correo'],
        ':telefono' => $datos['telefono'] !== '' ? $datos['telefono'] : null,
        ':asunto'   => $datos['asunto'],
        ':mensaje'  => $datos['mensaje'],
        ':huella'   => $huella,
    ]);
} catch (PDOException $error) {
    // El detalle queda en el registro del servidor, nunca en la respuesta.
    error_log('Contacto: ' . $error->getMessage());
    responder(500, false, 'No pudimos guardar tu mensaje. Inténtalo más tarde.');
}

responder(201, true, $exito);
