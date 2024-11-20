@ECHO OFF
:: [PTS: AJUSTAR]
set raster="C:\Program Files\PostgreSQL\16\bin\raster2pgsql"


:: povoar com o raster_ilhaDasFlores_1.tif
%raster% -s 4236 -I -d -M ..\raster_ilhaDasFlores_1.tif T_RASTER > ..\out_raster.txt
type .\_script_CONNECT_INIT_BD.txt ..\out_raster.txt > .\01_script_POVOAR_T_RASTER.txt

_go01.bat

:: povoar com o raster_ilhaDasFlores_2.tif
:: nesta execucao nao se usa a opcao "-d" (para nao se fazer "drop" 'a tabela que suporta o raster)
:: nesta execucao usa-se a opcao "-a" (para fazer "append" a uma tabela ja' existente)
:: nesta execucao tambem nao se usa a opcao "-I" pois o indice ja' foi construido
::%raster% -s 4236 -a -M ..\raster_ilhaDasFlores_2.tif T_RASTER > ..\out_raster.txt
::type .\_script_CONNECT_INIT_BD.txt ..\out_raster.txt > .\01_script_POVOAR_T_RASTER.txt

::_go01.bat
