::________________________
:: Paulo Trigo Silva (PTS)
::________________________



:: Definir Caminho para "javac" e "jar" [PTS: AJUSTAR]
set javaBinPath="C:\Program Files\Java\jdk1.8.0_211\bin"


:: Definir Caminho para "lucene" [PTS: AJUSTAR]
set lucenePath="C:\Users\A40610\Desktop\SIGM2425\aulasPraticas\aulaPratica9\Aula09_sistemaLucene\_sistemaCompleto"

set core=%lucenePath%\lucene-core-7.1.0.jar
set demo=%lucenePath%\lucene-demo-7.1.0.jar
set analyzers=%lucenePath%\lucene-analyzers-common-7.1.0.jar
set queryparser=%lucenePath%\lucene-queryparser-7.1.0.jar


:: Definir Caminho para "o MEU c�digo fonte" [PTS: AJUSTAR]
set mySourcePath=%lucenePath%\src_myRI\src


:: Registar directorio corrente
set CURR_DIR=%CD%

:: Compilar
cd %mySourcePath%
%javaBinPath%\javac -classpath %core%;%demo%;%analyzers%;%queryparser% *.java -Xlint:deprecation
cd %CURR_DIR%

:: Copiar .class para directoria .\bin
if NOT EXIST .\bin mkdir .\bin
move %mySourcePath%\*.class .\bin