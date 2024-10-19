@ECHO OFF
:: [PTS: AJUSTAR]
set psqlPath="C:\Program Files\PostgreSQL\16\bin"

:: Base de Dados e nome do utilizador
SET dataBase=postgres
SET userName=postgres
SET portNumber=5432

:: psql -h host -p port -d database -U user -f psqlFile
%psqlPath%\psql -h localhost -p %portNumber% -d %dataBase% -U %userName% -f %1




