/**
 * @author Paulo Trigo Silva (PTS)
 */


import java.util.Date;
import java.util.Iterator;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.util.Version;
import org.apache.lucene.document.DateTools;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.index.DirectoryReader;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.File;
import java.io.PrintWriter;



public class MeuInterrogador
implements I_Config
{
   //PTS-2015 private final Version _VERSION = Version.LUCENE_46;

   public static void main( String[] args )
   {
      System.out.println( "O Meu Interrogador!" );
      MeuInterrogador meuInterrogador = new MeuInterrogador();
      meuInterrogador.interrogar();
   }


   public void interrogar()
   {
      IndexReader leitorDoIndice = null; 
      try
      {
         //PTS-2015 File INDEX_DIR = new File( _kDirectorioComOsIndices )
         Path INDEX_DIR = Paths.get( _kDirectorioComOsIndices );
         leitorDoIndice = DirectoryReader.open( FSDirectory.open( INDEX_DIR ) );
      }
      catch( Exception e ) { System.out.println( "Erro MeuInterrogador (a)" ); }
      
      IndexSearcher pesquisador = new IndexSearcher( leitorDoIndice );
      // Notar que o analisador aqui usado deve ser o mesmo que o usado durante o processo de indexacao
      //PTS-2015 Analyzer analisador = new StandardAnalyzer( _VERSION, CharArraySet.EMPTY_SET );
      Analyzer analisador = new StandardAnalyzer( CharArraySet.EMPTY_SET );
      // para tratar caracteres acentuados e eliminar "stop words" usar o "MeuAnalisador"
      // Analyzer analisador = new MeuAnalisador( "_asMinhasStopWords.txt" );
            
      try
      {
         String lstr_campo = obterCampoParaInterrogacao();
         //PTS-2015 QueryParser analisadorInterrogacao = new QueryParser( _VERSION, lstr_campo, analisador );
         QueryParser analisadorInterrogacao = new QueryParser( lstr_campo, analisador );
         
         String lstr_interrogacao = obterInterrogacao();
         if( lstr_interrogacao.isEmpty() ) return;
         
         Query documentoInterrogacao = analisadorInterrogacao.parse( lstr_interrogacao );
         int maxDocumentos = leitorDoIndice.maxDoc();
         //PTS-2015 ScoreDoc[] resposta = pesquisador.search( documentoInterrogacao, null, maxDocumentos ).scoreDocs;
         ScoreDoc[] resposta = pesquisador.search( documentoInterrogacao,  maxDocumentos ).scoreDocs;
         apresentarResposta( resposta, pesquisador );
      }
      catch( Exception e ) { System.out.println( "Erro MeuInterrogador (b)" ); }      
   }
 
   
   private String obterCampoParaInterrogacao()
   {
      System.out.println( "Campo = { titulo, autor, tema, conteudo } [conteudo] ");
      System.out.print( "? > ");
      String campo = U_LeitorEscritorLinha.ler();
      
      // Por omissão considera-se o campo "conteúdo"
      campo = campo.trim().isEmpty() ? "conteudo" : campo;
      
      System.out.println( "%" + campo + "%" );
      System.out.println();
      
      return campo;
   }


   private String obterInterrogacao()
   {      
      System.out.print( "? > ");
      String interrogacao = U_LeitorEscritorLinha.ler();    
      
      System.out.println( "%" + interrogacao + "%" );
      System.out.println();
      
      return interrogacao;
   }
   
   
   private void apresentarResposta( ScoreDoc[] resposta, IndexSearcher pesquisador )
   throws Exception
   {
      for ( int ordem = 0; ordem < resposta.length; ordem++ ) 
      {
         int idDoc = resposta[ ordem ].doc;
         Document documento = pesquisador.doc( idDoc );
         apresentarDetalhe( documento, ordem + 1 );
      }

      System.out.println( "Numero de documentos encontrados: " + resposta.length );
   }


   private void apresentarDetalhe( Document documento, int ordem )
   throws Exception
   {
      String lstr_localizacao = documento.get( "localizacao" );
      String lstr_ultimaDataDeEscrita = documento.get( "ultimaDataDeEscrita" );
      
      String lstr_titulo = documento.get( "titulo" );
      String lstr_autor = documento.get( "autor" );
      String lstr_tema = documento.get( "tema" );
      
      Date lobj_ultimaDataDeEscrita = null;
      try
      {
         lobj_ultimaDataDeEscrita = DateTools.stringToDate( lstr_ultimaDataDeEscrita );
      } catch( Exception e )
      {
         System.out.println( "Erro MeuInterrogador::apresentarDetalhe" );
      }
      
      System.out.print("[" + ordem + "] ");
      System.out.println( "\"" + lstr_titulo + "\"" + "; " + "\"" + lstr_autor + "\"" + "; " + "\"" + lstr_tema + "\"" );
      System.out.println( lstr_localizacao + " [" + lobj_ultimaDataDeEscrita + "]" );
      System.out.println();
   }
}
