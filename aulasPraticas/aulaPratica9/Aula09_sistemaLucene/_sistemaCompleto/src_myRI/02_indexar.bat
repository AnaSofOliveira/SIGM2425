::________________________
:: Paulo Trigo Silva (PTS)
::________________________


:: Definir Caminho para "lucene" [PTS: AJUSTAR]
set lucenePath="C:\Users\A40610\Desktop\SIGM2425\aulasPraticas\aulaPratica9\Aula09_sistemaLucene\_sistemaCompleto"

set core=%lucenePath%\lucene-core-7.1.0.jar
set demo=%lucenePath%\lucene-demo-7.1.0.jar
set analyzers=%lucenePath%\lucene-analyzers-common-7.1.0.jar
set queryparser=%lucenePath%\lucene-queryparser-7.1.0.jar


java -classpath %core%;%demo%;%analyzers%;%queryparser%;.\bin MeuIndexador
::java -classpath %core%;%demo%;%analyzers%;%queryparser%;.\bin MeuIndexadorVectorial

:: ATEN��O - ap�s executar o script ser� criado um direct�rio "_osMeusIndices" (no directorio onde iniciou o script) que cont�m os �ndices criados;
:: ATEN��O - ao executar novamente o script adiciona os novos ficheiros ao �ndice
