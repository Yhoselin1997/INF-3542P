-- Crear el procedimiento almacenado
CREATE PROCEDURE CompararPalabras
    @palabra1 VARCHAR(20),
    @palabra2 VARCHAR(20)
AS
BEGIN
    DECLARE
        @longitud1 INT,
        @longitud2 INT,
        @posicion INT,
        @letra VARCHAR(2),
        @sql NVARCHAR(MAX),
        @columna VARCHAR(4);

    -- Calcular las longitudes de las palabras
    SET @longitud1 = LEN(@palabra1);
    SET @longitud2 = LEN(@palabra2);

    -- Crear la tabla temporal
    SET @posicion = 1;
    SET @sql = N'CREATE TABLE nombre (';

    WHILE @posicion <= @longitud1
    BEGIN
        SET @letra = LEFT(@palabra1, 1);
        SET @palabra1 = RIGHT(@palabra1, LEN(@palabra1) - 1);
        SET @sql = @sql + @letra + CAST(@posicion AS VARCHAR) + ' INT, ';
        SET @posicion = @posicion + 1;
    END

    SET @sql = LEFT(@sql, LEN(@sql) - 1);
    SET @sql = @sql + N')';
    EXEC sp_executesql @sql;

    -- Insertar datos en la tabla
    SET @posicion = 1;

    WHILE @posicion <= @longitud2
    BEGIN
        SET @letra = LEFT(@palabra2, 1);
        SET @palabra2 = RIGHT(@palabra2, LEN(@palabra2) - 1);

        IF EXISTS (
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'nombre'
                AND LEFT(COLUMN_NAME, 1) = @letra
                AND ORDINAL_POSITION <= @posicion
        )
        BEGIN
            SELECT TOP 1 @columna = COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'nombre'
                AND LEFT(COLUMN_NAME, 1) = @letra
                AND ORDINAL_POSITION >= @posicion;

            SET @sql = N'INSERT INTO nombre(' + @columna + N') VALUES(1)';
            EXEC sp_executesql @sql;
        END

        SET @posicion = @posicion + 1;
    END

    -- Realizar la suma de las letras
    SET @sql = N'SELECT ';
    SET @sql = @sql + STUFF((
        SELECT N', SUM(ISNULL(' + COLUMN_NAME + N', 0))'
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
        ORDER BY ORDINAL_POSITION
        FOR XML PATH('')
    ), 1, 2, N'') + N' FROM nombre';

    EXEC sp_executesql @sql;

    -- Eliminar la tabla temporal
    EXEC sp_executesql N'DROP TABLE nombre';
END;

-- Declarar variables para las palabras
DECLARE @palabra1 VARCHAR(20) = 'arismendi';
DECLARE @palabra2 VARCHAR(20) = 'arizmendY';

-- Ejecutar el procedimiento almacenado
EXEC CompararPalabras @palabra1, @palabra2;
