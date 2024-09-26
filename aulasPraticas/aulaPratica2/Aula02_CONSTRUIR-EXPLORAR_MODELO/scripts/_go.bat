@ECHO OFF
:: [PTS: AJUSTAR]
set psqlPath="C:\Program Files\PostgreSQL\16\bin"


:: Base de Dados, nome do utilizador e porto
SET dataBase=postgres
SET userName=postgres
SET portNumber=5432

::________________________________________________________________________
:: Estabelecer conexao com base de dados e executar instrucoes em psqlFile
:: psql -h host -p port -d database -U user -f psqlFile
:: (cf. postgresql-9.6-A4.pdf)
::________________________________________________________________________
%psqlPath%\psql -h localhost -p %portNumber% -d %dataBase% -U %userName% -f %1


:: trocar os comentarios das proximas linhas caso exista incompatibilidade com a "code page"
:: mais info sobre "code page" em:
:: http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/chcp.mspx?mfr=true
:: cmd.exe /c chcp 1252
cmd.exe /c chcp 860


