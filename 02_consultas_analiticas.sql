USE energia_solar_db;

-- Consulta 1: Top 10 Países con mayor capacidad solar operativa (MW)
-- Objetivo: Identificar los líderes mundiales en generación solar activa.
SELECT 
    u.pais,
    COUNT(fs.gem_phase_id) AS total_fases_operativas,
    SUM(fs.capacidad_mw) AS capacidad_total_mw
FROM 
    fase_solar fs
JOIN 
    proyecto p ON fs.id_proyecto = p.id_proyecto
JOIN 
    ubicacion u ON p.gem_location_id = u.gem_location_id
WHERE 
    fs.estado_operativo = 'operating'
GROUP BY 
    u.pais
ORDER BY 
    capacidad_total_mw DESC
LIMIT 10;


-- Consulta 2: Evolución histórica de la instalación de capacidad solar por año
-- Objetivo: Analizar la tendencia de crecimiento tecnológico en la última década.
SELECT 
    anio_inicio AS anio_instalacion,
    COUNT(gem_phase_id) AS nuevos_proyectos,
    ROUND(SUM(capacidad_mw), 2) AS nueva_capacidad_mw
FROM 
    fase_solar
WHERE 
    anio_inicio IS NOT NULL 
    AND anio_inicio >= 2010
GROUP BY 
    anio_inicio
ORDER BY 
    anio_inicio ASC;


-- Consulta 3: Porcentaje de proyectos solares que cuentan con almacenamiento de energía asociado
-- Objetivo: Evaluar la viabilidad de la red al mitigar la intermitencia solar (requerimiento clave del PDF).
SELECT 
    estado_operativo,
    COUNT(*) AS total_proyectos,
    SUM(CASE WHEN almacenamiento_asociado IS NOT NULL THEN 1 ELSE 0 END) AS proyectos_con_baterias,
    ROUND((SUM(CASE WHEN almacenamiento_asociado IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS porcentaje_con_almacenamiento
FROM 
    fase_solar
GROUP BY 
    estado_operativo
ORDER BY 
    total_proyectos DESC;