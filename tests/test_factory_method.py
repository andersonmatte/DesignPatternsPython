import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.criacionais.factory_method import (
    AnalisadorFactory, AnalisadorFASTA, AnalisadorGenBank
)


class TestFactoryMethod(unittest.TestCase):
    """Testes para o padrão Factory Method."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.factory = AnalisadorFactory()
        self.sequencia_valida = "ATCGATCGATCGATCG"
        self.dados_fasta = ">seq1\nATCGATCGATCGATCG"
        self.dados_genbank = """LOCUS       SCU49845     5028 bp    DNA     UNK 01-JAN-1980
DEFINITION  Saccharomyces cerevisiae TCP1-beta gene, partial cds.
ORIGIN
        1 gatcctccat atacaacggt atctccacct caggtttaga tctcaacaac ggaaccattg
"""
    
    def test_criar_analisador_fasta(self):
        """Testa criação de analisador FASTA."""
        analisador = self.factory.criar_analisador("FASTA")
        self.assertIsInstance(analisador, AnalisadorFASTA)
    
    def test_criar_analisador_genbank(self):
        """Testa criação de analisador GenBank."""
        analisador = self.factory.criar_analisador("GENBANK")
        self.assertIsInstance(analisador, AnalisadorGenBank)
    
    def test_criar_analisador_invalido(self):
        """Testa criação de analisador com formato inválido."""
        with self.assertRaises(ValueError):
            self.factory.criar_analisador("FORMATO_INVALIDO")
    
    def test_analisar_fasta_valido(self):
        """Testa análise de sequência FASTA válida."""
        analisador = self.factory.criar_analisador("FASTA")
        resultado = analisador.analisar_sequencia(self.sequencia_valida)
        
        self.assertEqual(resultado["formato"], "FASTA")
        self.assertEqual(resultado["sequencia"], self.sequencia_valida)
        self.assertEqual(resultado["comprimento"], len(self.sequencia_valida))
        self.assertIn("composicao", resultado)
        self.assertIn("A", resultado["composicao"])
        self.assertIn("T", resultado["composicao"])
        self.assertIn("C", resultado["composicao"])
        self.assertIn("G", resultado["composicao"])
    
    def test_analisar_fasta_com_cabecalho(self):
        """Testa análise de sequência FASTA com cabeçalho."""
        analisador = self.factory.criar_analisador("FASTA")
        resultado = analisador.analisar_sequencia(self.dados_fasta)
        
        self.assertEqual(resultado["formato"], "FASTA")
        self.assertEqual(resultado["sequencia"], "ATCGATCGATCGATCG")
        self.assertEqual(resultado["comprimento"], 16)
    
    def test_analisar_fasta_invalido(self):
        """Testa análise de sequência FASTA inválida."""
        analisador = self.factory.criar_analisador("FASTA")
        with self.assertRaises(ValueError):
            analisador.analisar_sequencia("ATCG#INVALIDO@")
    
    def test_analisar_genbank_valido(self):
        """Testa análise de sequência GenBank válida."""
        analisador = self.factory.criar_analisador("GENBANK")
        resultado = analisador.analisar_sequencia(self.dados_genbank)
        
        self.assertEqual(resultado["formato"], "GenBank")
        self.assertIn("metadados", resultado)
        self.assertIn("features", resultado)
        self.assertIn("sequencia", resultado)
        self.assertIn("comprimento", resultado)
    
    def test_analisar_genbank_invalido(self):
        """Testa análise de sequência GenBank inválida."""
        analisador = self.factory.criar_analisador("GENBANK")
        with self.assertRaises(ValueError):
            analisador.analisar_sequencia("dados inválidos sem LOCUS")
    
    def test_composicao_nucleotideos(self):
        """Testa cálculo de composição de nucleotídeos."""
        analisador = self.factory.criar_analisador("FASTA")
        resultado = analisador.analisar_sequencia("ATCGATCG")
        
        composicao = resultado["composicao"]
        self.assertEqual(composicao["A"], 2)
        self.assertEqual(composicao["T"], 2)
        self.assertEqual(composicao["C"], 2)
        self.assertEqual(composicao["G"], 2)
    
    def test_case_insensitive(self):
        """Testa se o factory é case insensitive."""
        analisador1 = self.factory.criar_analisador("fasta")
        analisador2 = self.factory.criar_analisador("FASTA")
        analisador3 = self.factory.criar_analisar("GenBank")
        analisador4 = self.factory.criar_analisar("GENBANK")
        
        self.assertEqual(type(analisador1), type(analisador2))
        self.assertEqual(type(analisador3), type(analisador4))


if __name__ == "__main__":
    unittest.main()
