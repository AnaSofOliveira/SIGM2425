/**
 * @author Paulo Trigo Silva (PTS)
 */



import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


public class U_LeitorEscritorLinha
{
   public U_LeitorEscritorLinha() 
   {
   }


   public static String ler() 
   {
      String lstr_string = "";
      BufferedReader lcl_leitor;
      lcl_leitor = new BufferedReader( new InputStreamReader( System.in ) );
 	  try
	  {
         lstr_string = lcl_leitor.readLine();
      }
	  catch( IOException excepcao )
	  {
         System.err.println( "ERRO: #U_LeitorEscritorLinha# \"IOException ...\"" );
	  }
	  return lstr_string;
   }

   
   public static void escrever(String astr_string) 
   {
      System.out.print( astr_string );
      System.out.println();
   }


   public static void escreverMesmaLinha(String astr_string)
   {
      System.out.print( astr_string );
   }


   public static void escrever(String[] astr_string) 
   {
      for( int lint_ciclo = 0; lint_ciclo < astr_string.length; lint_ciclo++ )
      {
         escrever( astr_string[ lint_ciclo ] );
      }
   }
   

   public static void escrever(int aint_valor) 
   {
      escrever( Integer.toString( aint_valor ) );
   }
   

   /**
    * Tratar a excepcao do tipo java.lang.Exception
    * presentando a informacao nela contida
    */
   public static void escrever(Exception acl_excepcao) 
   {
      acl_excepcao.printStackTrace();
   }


   public static void escreverBinario( byte[] abyt_vectorBytes )
   {
      escreverBinario( abyt_vectorBytes, abyt_vectorBytes.length );
   }


   public static void escreverBinario( byte[] abyt_vectorBytes, int aint_dimensao )
   {
      escrever( "Conteudo do Vector de Bytes:" );
      for( int lint_ciclo = 0; lint_ciclo < aint_dimensao; lint_ciclo++ )
      {
         escreverBinario( abyt_vectorBytes[ lint_ciclo ] );
         escreverMesmaLinha( ( ( ( lint_ciclo + 1 ) % 4 ) == 0 ) ? "\n" : " " );
      }
      escrever( "" );
   }


   public static void escreverBinario( byte abyt_valor )
   {
      int lint_mascara = 0x80;
      for( int lint_ciclo = 0; lint_ciclo < 8; lint_ciclo++ )
      {
         escreverMesmaLinha( ( ( abyt_valor & lint_mascara ) == 0 ) ? "0" : "1" );
         lint_mascara = ( lint_mascara >>> 1 );
      }
   }


   public static void escreverBinario( int aint_valor )
   {
      escrever( "" );
      escreverMesmaLinha( "Escrever Binario: " );
      escrever( aint_valor );

      int lint_mascara = 0x80000000;
      int lint_numeroBitsDoInt = ( int )Math.ceil( Math.log( Integer.MAX_VALUE ) / Math.log( 2 ) ) + 1;
      for( int lint_ciclo = 0; lint_ciclo < lint_numeroBitsDoInt; lint_ciclo++ )
      {
         escreverMesmaLinha( ( ( aint_valor & lint_mascara ) == 0 ) ? "0" : "1" );
         escreverMesmaLinha( ( ( ( lint_ciclo + 1 ) % 8 ) == 0 ) ? " " : "" );
         lint_mascara = ( lint_mascara >>> 1 );
      }
      escrever( "" );
   }


   /**
    * Tratar a excepcao do tipo java.lang.Exception
    * presentando a informacao nela contida
    * Criado: (2/16/00 11:45:41 PM)
    * @author: Paulo Trigo Silva
    * @param acl_excepcao java.lang.Throwable
    */
   public static void escrever(Throwable acl_excepcao) 
   {
      acl_excepcao.printStackTrace();
   }
}
