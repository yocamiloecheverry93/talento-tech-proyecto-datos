-- 1. Creación y uso de la base de datos
CREATE DATABASE IF NOT EXISTS energia_solar_db;
USE energia_solar_db;

-- 2. Creación de Tablas Padre (Sin dependencias)

CREATE TABLE ubicacion (
    gem_location_id VARCHAR(50) PRIMARY KEY,
    region VARCHAR(50),
    subregion VARCHAR(50),
    pais VARCHAR(50),
    estado_provincia VARCHAR(100),
    ciudad VARCHAR(100),
    latitud DECIMAL(10,6),
    longitud DECIMAL(10,6),
    precision_ubicacion VARCHAR(50)
);

CREATE TABLE empresa (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    nombre_empresa VARCHAR(150),
    nombre_local VARCHAR(150)
);

-- 3. Creación de Tablas Hijas (Con dependencias de las Padre)

CREATE TABLE proyecto (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    gem_location_id VARCHAR(50),
    nombre_proyecto VARCHAR(150),
    nombre_local VARCHAR(150),
    wiki_url VARCHAR(255),
    FOREIGN KEY (gem_location_id) REFERENCES ubicacion(gem_location_id)
);

CREATE TABLE fase_solar (
    gem_phase_id VARCHAR(50) PRIMARY KEY,
    id_proyecto INT,
    nombre_fase VARCHAR(150),
    capacidad_mw DECIMAL(10,2),
    tecnologia VARCHAR(50),
    estado_operativo VARCHAR(50),
    anio_inicio INT,
    anio_retiro INT,
    tiene_hidrogeno VARCHAR(10),
    almacenamiento_asociado VARCHAR(100),
    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto)
);

-- 4. Creación de Tabla Intermedia (Relación Muchos a Muchos)

CREATE TABLE participacion_empresa (
    gem_phase_id VARCHAR(50),
    id_empresa INT,
    rol VARCHAR(50),
    PRIMARY KEY (gem_phase_id, id_empresa),
    FOREIGN KEY (gem_phase_id) REFERENCES fase_solar(gem_phase_id),
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa)
);