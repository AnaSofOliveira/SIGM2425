@ECHO OFF
:: [PTS: AJUSTAR]
set psqlPath="C:\Program Files\PostgreSQL\16\bin"

:: Base de Dados e nome do utilizador
SET dataBase=my_gis_raster
SET userName=postgres

:: Set the PGPASSFILE environment variable
SET PGPASSWORD=123456

:: Run osm2pgsql with the necessary parameters
.\osm2pgsql-bin\osm2pgsql -c -d %dataBase% -U %userName% -H localhost -S .\default.style .\lisbon_portugal.osm.pbf


