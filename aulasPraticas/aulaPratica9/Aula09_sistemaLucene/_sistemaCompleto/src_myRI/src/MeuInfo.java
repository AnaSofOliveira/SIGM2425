/**
 * @author Paulo Trigo Silva (PTS)
 */



import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.Terms;

//import org.apache.lucene.index.DocsEnum;
//PTS-2015 import org.apache.lucene.index.DocsAndPositionsEnum;
import org.apache.lucene.index.PostingsEnum;

import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.index.Fields;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.util.BytesRef;

import org.apache.lucene.search.DocIdSetIterator;
import org.apache.lucene.store.FSDirectory;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.File;
import java.io.PrintWriter;




public class MeuInfo
implements I_Config
{
   public static void main( String[] args )
   {
      MeuInfo info = new MeuInfo();
      info.obterTermos( _kDirectorioComOsIndices );
      System.out.println( "" );
      System.out.println( "===== // =====" );
      System.out.println( "" );
      info.obterVectorDeFrequenciaDeCadaTermo( _kDirectorioComOsIndices );
   }

   
   private IndexReader obterLeitorDoIndice( String a_directorioComOsIndices )
   {
      IndexReader leitorDoIndice = null; 
      try
      {
         //PTS-2015 File INDEX_DIR = new File( a_directorioComOsIndices )
         Path INDEX_DIR = Paths.get( a_directorioComOsIndices );
         leitorDoIndice = DirectoryReader.open( FSDirectory.open( INDEX_DIR ) );
      }
      catch( Exception e ) { System.out.println( "Erro MeuInfo (a)" ); }
      
      return leitorDoIndice;
   }

   
   public void obterTermos( String a_directorioComOsIndices )
   {      
      IndexReader leitorDoIndice = obterLeitorDoIndice( a_directorioComOsIndices );
      try
      {
         Fields listaDeCampos = MultiFields.getFields( leitorDoIndice );
         for( String lstr_campo : listaDeCampos  )
         {
            Terms listaDeTermos = listaDeCampos.terms( lstr_campo );
            //::PTS-2015:: TermsEnum listaDeTermosIter = listaDeTermos.iterator( null );
            TermsEnum listaDeTermosIter = listaDeTermos.iterator();
            BytesRef texto;
            while( ( texto = listaDeTermosIter.next() ) != null )
            {
               String lstr_termo = texto.utf8ToString();
               int numeroDeDocumentosComTermo = listaDeTermosIter.docFreq();
               System.out.println( "< " +
                                   lstr_termo +
                                   ", campo=\"" +
                                   lstr_campo +
                                   "\"" +
                                   ", df=" +
                                   numeroDeDocumentosComTermo +
                                   " >" );
            }
         }
         
      }
      catch( Exception e )
      {}    
   }



   public void obterVectorDeFrequenciaDeCadaTermo( String a_directorioComOsIndices )
   {      
      IndexReader leitorDoIndice = obterLeitorDoIndice( a_directorioComOsIndices );

      int numeroDeDocumentos = leitorDoIndice.numDocs();
      for( int iLoop = 0; iLoop < numeroDeDocumentos; iLoop++ )
      {
         try
         {
            Terms vector_termoFrequencia =
               leitorDoIndice.getTermVector( iLoop, "conteudo" );
            
            if( vector_termoFrequencia == null )
            {
               System.out.println( "Nao existe informação de frequências em \"conteudo\"" );
               System.out.println( "(criar índice para campo \"conteudo\" com \"Field.TermVector\")" );
               return;
            }
            Document documento = leitorDoIndice.document( iLoop );
            apresentarVectorTermoFrequencia( documento, vector_termoFrequencia );
         }
         catch( Exception e ) { System.out.println( "Erro MeuInfo (b)" ); }
      }
   }



   private void apresentarVectorTermoFrequencia( Document documento, Terms vector_termoFrequencia )
   {
      if( vector_termoFrequencia == null ) return;

      String lstr_localizacao = documento.get( "localizacao" );
      System.out.println( "" );
      System.out.println( lstr_localizacao );
      
      try
      {
         long numeroDeTermos = vector_termoFrequencia.size();
         //::PTS-2015:: TermsEnum vector_termoFrequenciaIter = vector_termoFrequencia.iterator( null );
         TermsEnum vector_termoFrequenciaIter = vector_termoFrequencia.iterator();

         System.out.print( "[ " );
         BytesRef texto = null;
         int iLoop = 0;
         while( ( texto = vector_termoFrequenciaIter.next() ) != null )
         {
            String lstr_termo = texto.utf8ToString();
            long frequenciaDoTermoNoDoc = vector_termoFrequenciaIter.totalTermFreq();
            //::PTS-2015:: DocsAndPositionsEnum docsPosicoesIter = vector_termoFrequenciaIter.docsAndPositions( null, null );
            PostingsEnum docsPosicoesIter = vector_termoFrequenciaIter.postings( null );
            String lstr_listaDePosicoesNoTermo = obterListaDePosicoesNoTermo( docsPosicoesIter );

            System.out.print( "<" +
                              lstr_termo +
                              ", " +
                              frequenciaDoTermoNoDoc +
                              ( lstr_listaDePosicoesNoTermo.isEmpty()? "" : ", " +
                               lstr_listaDePosicoesNoTermo ) +
                               ">" +
                              ( ( iLoop < numeroDeTermos - 1 )? ", " : "" ) );
            iLoop++;
         }
      }
      catch( Exception e ) { System.out.println( "Erro MeuInfo (c)" ); }
      System.out.print( " ]" );
      System.out.println( "" );
   }



   private String obterListaDePosicoesNoTermo( PostingsEnum docsPosicoesIter )
   {
      String resultado = "";
      if( docsPosicoesIter == null )
      {
         System.out.println( "Não existem termos com posições em \"conteudo\"" );
         System.out.println( "(criar índice para campo \"conteudo\" com \"Field.TermVector.WITH_POSITIONS_OFFSETS\")" );
         return resultado;
      }

      try
      {
         if( docsPosicoesIter.nextDoc() == DocIdSetIterator.NO_MORE_DOCS ) return resultado;
         int dimensao = docsPosicoesIter.freq();

         resultado = resultado + ( ( dimensao > 0 )? "|" : "" ); 
         for( int iLoop = 0; iLoop < dimensao; iLoop++ )
         {
            resultado = resultado +
               Integer.toString( docsPosicoesIter.nextPosition() ) +
               ( ( iLoop < dimensao - 1 )? "," : "" );
         }
         resultado = resultado + ( ( dimensao > 0 )? "|" : "" );
      }
      catch( Exception e ) { System.out.println( "Erro MeuInfo (d)" ); }

      return resultado;
   }
}


