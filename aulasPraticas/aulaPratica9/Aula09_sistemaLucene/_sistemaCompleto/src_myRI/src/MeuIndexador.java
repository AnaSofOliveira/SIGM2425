/**
 * @author Paulo Trigo Silva (PTS)
 */


import org.apache.lucene.document.Document;
import org.apache.lucene.document.DateTools;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.FieldType;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.Term;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;


public class MeuIndexador
implements I_Config
{
   //PTS-2015 private final Version _VERSION = Version.LUCENE_46;

   public static void main( String[] args )
   {
      System.out.println( "O Meu Indexador!" );
      MeuIndexador meuIndexador = new MeuIndexador();
           
      meuIndexador.indexarArtigo( "O rato e o rei",
                                  "Desconhecido & Popular",
                                  "destrava l�nguas",
                                  "oArtigo_A.txt" );
      
      meuIndexador.indexarArtigo( "A vida",
                                  "Gato & Rato & Rei",
                                  "cr�nica",
                                  "oArtigo_B.txt" );
      
      meuIndexador.indexarArtigo( "Gato branco, gato preto",
                                  "Kusturika",
                                  "filme estrangeiro",
                                  "oArtigo_C.txt" );
   }



   public void indexarArtigo( String a_titulo, String a_listaDeAutores,
                              String a_listaDeTemas, String a_nomeDoFicheiro )
   {
      File ficheiro = new File( a_nomeDoFicheiro );
      if( ( ! ficheiro.exists() ) || ficheiro.isDirectory() )
      {
         throw new Error( "Erro MeuIndexador - leitura do ficheiro" );
      }
      try
      {
         Document documento = criarDocumento( a_titulo,
                                              a_listaDeAutores,
                                              a_listaDeTemas,
                                              ficheiro );
         indexarDocumento( documento, ficheiro );
      } 
      catch( FileNotFoundException e )
      {
         System.out.println( a_nomeDoFicheiro + ": n�o existe Meuindexador::indexarArtigo" );
      }
      catch( Exception e )
      {
         System.out.println( "Erro Meuindexador::indexarArtigo" );
      }
   }



   protected Document criarDocumento( String a_titulo, String a_listaDeAutores,
                                      String a_listaDeTemas, File a_ficheiro )
   throws IOException
   {
      Document documento = new Document();
      // Sobre t�tulo, autores e temas
      documento.add( new TextField( "titulo", a_titulo, Field.Store.YES ) );
      documento.add( new TextField( "autor", a_listaDeAutores, Field.Store.YES ) );
      documento.add( new TextField( "tema", a_listaDeTemas, Field.Store.YES ) );
      
      FieldType ft_textoCompleto = new FieldType( StringField.TYPE_STORED );
      // Sobre o ficheiro
      String l_localizacao = a_ficheiro.getAbsolutePath();
      documento.add( new Field( "localizacao", l_localizacao, ft_textoCompleto ) );
      
      String l_ultimaDataDeEscrita = DateTools.timeToString( a_ficheiro.lastModified(),
                                                          DateTools.Resolution.MINUTE );      
      documento.add( new Field( "ultimaDataDeEscrita",
                                l_ultimaDataDeEscrita,
                                ft_textoCompleto ) );
      
      // O conte�do do documento
      BufferedReader l_leitorDoConteudo =
         new BufferedReader( new InputStreamReader( new FileInputStream( a_ficheiro ), "ISO-8859-1" ) ); // "UTF-8"
      documento.add( new TextField( "conteudo", l_leitorDoConteudo ) );    

      return documento;
   }



   private void indexarDocumento( Document documento, File a_ficheiro ) throws Exception
   {
      //PTS-2015 Analyzer analisador = new StandardAnalyzer( _VERSION, CharArraySet.EMPTY_SET );
      // Analyzer analisador = new StandardAnalyzer( CharArraySet.EMPTY_SET );
      // para tratar caracteres acentuados e eliminar "stop words" usar o "MeuAnalisador"
      Analyzer analisador = new MeuAnalisador( "_asMinhasStopWords.txt" );

      File dir = new File( _kDirectorioComOsIndices );
      boolean dirEmpty = ( dir.isDirectory() && ( dir.list().length == 0 ) );
      boolean dirExists = dir.exists();
      boolean dirReadable = dir.canRead();
      boolean criarNovo = dirEmpty || ( ! dirExists ) || ( ! dirReadable );

      //PTS-2015 IndexWriterConfig indexWriterConfig = new IndexWriterConfig( _VERSION, analisador );
      IndexWriterConfig indexWriterConfig = new IndexWriterConfig( analisador );
      if( criarNovo ) indexWriterConfig.setOpenMode( OpenMode.CREATE );
      else indexWriterConfig.setOpenMode( OpenMode.CREATE_OR_APPEND );

      //PTS-2015 File INDEX_DIR = new File( _kDirectorioComOsIndices );
      Path INDEX_DIR = Paths.get( _kDirectorioComOsIndices );
      IndexWriter escritorDoIndice = new IndexWriter( FSDirectory.open( INDEX_DIR ), indexWriterConfig );
      
      if( escritorDoIndice.getConfig().getOpenMode() == OpenMode.CREATE ) {
         System.out.println( "adicionar: " + a_ficheiro );
         escritorDoIndice.addDocument( documento );
      } else {
         System.out.println( "actualizar: " + a_ficheiro );
         escritorDoIndice.updateDocument( new Term( "localizacao", a_ficheiro.getAbsolutePath() ), documento );
      }
      escritorDoIndice.commit();
      escritorDoIndice.close();
   }

}
