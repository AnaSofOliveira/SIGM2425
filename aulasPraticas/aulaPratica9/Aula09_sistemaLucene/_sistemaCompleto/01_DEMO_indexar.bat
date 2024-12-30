::________________________
:: Paulo Trigo Silva (PTS)
::________________________



:: [PTS: AJUSTAR]
set lucenePath="C:\Users\A40610\Desktop\SIGM2425\aulasPraticas\aulaPratica9\Aula09_sistemaLucene\_sistemaCompleto"


set dataPath=%lucenePath%\z_coleccao_demo

set core=%lucenePath%\lucene-core-7.1.0.jar
set demo=%lucenePath%\lucene-demo-7.1.0.jar
::set queryparser=%lucenePath%\lucene-queryparser-7.1.0.jar
::set analyzers=%lucenePath%\lucene-analyzers-common-7.1.0.jar

java -classpath %core%;%demo%;%analyzers%;%queryparser% org.apache.lucene.demo.IndexFiles -docs %dataPath%\z01_coleccao_paraIndexar -index %dataPath%\z02_coleccao_indexada -update
:: -update

:: ATENCAO - ap�s executar o script serao criados na pasta "%dataPath%\z02_coleccao_indexada" os indices relativos 'a coleccao que esta' na pasta "%dataPath%\z01_coleccao_paraIndexar"
:: ATEN��O - note que a coleccao indexada cont�m, como documentos, o codigo fonte desta demo!
:: ATEN��O - estamos a executar um c�digo DEMO muito elementar; o c�digo mais sofisticado ser� posteriormente construido