-- Base de datos del formulario de contacto (MySQL 5.7+ o MariaDB 10.3+).
CREATE DATABASE IF NOT EXISTS molle_tara
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE molle_tara;

CREATE TABLE IF NOT EXISTS mensajes_contacto (
  id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre     VARCHAR(80)  NOT NULL,
  correo     VARCHAR(120) NOT NULL,
  telefono   VARCHAR(20)      NULL,
  asunto     ENUM('producto', 'servicio', 'visita', 'otro') NOT NULL,
  mensaje    VARCHAR(1000) NOT NULL,
  huella_ip  CHAR(64)     NOT NULL,
  creado_en  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_huella_fecha (huella_ip, creado_en)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Opcional (recomendado en producción): un usuario con permisos mínimos.
-- CREATE USER 'molle_web'@'localhost' IDENTIFIED BY 'define-una-clave-segura';
-- GRANT SELECT, INSERT ON molle_tara.mensajes_contacto TO 'molle_web'@'localhost';
