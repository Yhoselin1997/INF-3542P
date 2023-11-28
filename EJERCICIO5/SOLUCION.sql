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
        @contador INT,
        @sql NVARCHAR(2000),
        @columna VARCHAR(4),
        @contar INT;

    SET @longitud1 = LEN(@palabra1);
    SET @longitud2 = LEN(@palabra2);

    SET @posicion = 1;
    SET @sql = 'CREATE TABLE nombre (';

    WHILE @posicion <= @longitud1
    BEGIN
        SET @letra = LEFT(@palabra1, 1);
        SET @palabra1 = RIGHT(@palabra1, LEN(@palabra1) - 1);
        SET @sql = @sql + @letra + CAST(@posicion AS VARCHAR) + ' INT, ';
        SET @posicion = @posicion + 1;
    END

    SET @sql = LEFT(@sql, LEN(@sql) - 1);
    SET @sql = @sql + ')';
    EXEC sp_executesql @sql;

    SET @posicion = 1;

    WHILE @posicion <= @longitud2
    BEGIN
        SET @letra = LEFT(@palabra2, 1);
        SET @palabra2 = RIGHT(@palabra2, LEN(@palabra2) - 1);
        SET @contar = 0;

        SELECT @contar = COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
            AND LEFT(COLUMN_NAME, 1) = @letra
            AND ORDINAL_POSITION <= @posicion;

        IF @contar > 0
        BEGIN
            SELECT TOP 1 @columna = COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'nombre'
                AND LEFT(COLUMN_NAME, 1) = @letra
                AND ORDINAL_POSITION >= @posicion;

            SET @sql = 'INSERT INTO nombre(' + @columna + ') VALUES(1)';
            EXEC sp_executesql @sql;
        END

        SET @posicion = @posicion + 1;
    END

    SET @sql = 'SELECT ';
    SET @contar = 0;

    SELECT @contar = COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'nombre';

    SET @posicion = 1;

    WHILE @posicion <= @contar
    BEGIN
        SELECT @columna = COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
            AND ORDINAL_POSITION = @posicion;

        SET @sql = @sql + 'SUM(ISNULL(' + @columna + ', 0)) + ';
        SET @posicion = @posicion + 1;
    END

    SET @sql = LEFT(@sql, LEN(@sql) - 1) + ' FROM nombre';
    EXEC sp_executesql @sql;
END;
DECLARE @palabra1 VARCHAR(20) = 'arysmendi';
DECLARE @palabra2 VARCHAR(20) = 'arizmendi';

EXEC CompararPalabras @palabra1, @palabra2;
