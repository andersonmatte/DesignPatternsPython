import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.estruturais.adapter import (
    AdapterFASTA, AdapterGenBank, AdapterUnificado, FabricaAdapters
)


class TestAdapter(unittest.TestCase):
    """Testes para o padrão Adapter."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.fabrica = FabricaAdapters()
        self.sequencia_valida = "ATCGATCGATCGATCG"
        self.dados_fasta = ">seq1\nATCGATCGATCGATCG"
        self.dados_genbank = """LOCUS       SCU49845     5028 bp    DNA     UNK 01-JAN-1980
DEFINITION  Saccharomyces cerevisiae TCP1-beta gene, partial cds.
ORIGIN
        1 gatcctccat atacaacggt atctccacct caggtttaga tctcaacaac ggaaccattg
"""
    
    def test_criar_adapter_fasta(self):
        """Testa criação de adapter FASTA."""
        adapter = self.fabrica.criar_adapter("FASTA")
        self.assertIsInstance(adapter, AdapterFASTA)
    
    def test_criar_adapter_genbank(self):
        """Testa criação de adapter GenBank."""
        adapter = self.fabrica.criar_adapter("GENBANK")
        self.assertIsInstance(adapter, AdapterGenBank)
    
    def test_criar_adapter_unificado(self):
        """Testa criação de adapter unificado."""
        adapter = self.fabrica.criar_adapter("UNIFICADO")
        self.assertIsInstance(adapter, AdapterUnificado)
    
    def test_criar_adapter_invalido(self):
        """Testa criação de adapter inválido."""
        with self.assertRaises(ValueError):
            self.fabrica.criar_adapter("INVALIDO")
    
    def test_adapter_fasta_analisar(self):
        """Testa análise com adapter FASTA."""
        adapter = self.fabrica.criar_adapter("FASTA")
        resultado = adapter.analisar_sequencia(self.sequencia_valida)
        
        self.assertEqual(resultado["formato"], "FASTA")
        self.assertEqual(resultado["sequencia"], self.sequencia_valida)
        self.assertEqual(resultado["comprimento"], len(self.sequencia_valida))
        self.assertIn("composicao", resultado)
    
    def test_adapter_fasta_com_cabecalho(self):
        """Testa análise FASTA com cabeçalho."""
        adapter = self.fabrica.criar_adapter("FASTA")
        resultado = adapter.analisar_sequencia(self.dados_fasta)
        
        self.assertEqual(resultado["formato"], "FASTA")
        self.assertEqual(resultado["sequencia"], "ATCGATCGATCGATCG")
        self.assertEqual(resultado["cabecalho"], ">seq1")
    
    def test_adapter_genbank_analisar(self):
        """Testa análise com adapter GenBank."""
        adapter = self.fabrica.criar_adapter("GENBANK")
        resultado = adapter.analisar_sequencia(self.dados_genbank)
        
        self.assertEqual(resultado["formato"], "GenBank")
        self.assertIn("locus", resultado)
        self.assertIn("definicao", resultado)
        self.assertIn("sequencia", resultado)
    
    def test_adapter_unificado_analisar_fasta(self):
        """Testa adapter unificado com dados FASTA."""
        adapter = self.fabrica.criar_adapter("UNIFICADO")
        resultado = adapter.analisar_sequencia(self.dados_fasta)
        
        self.assertEqual(resultado["formato"], "FASTA")
        self.assertEqual(resultado["sequencia"], "ATCGATCGATCGATCG")
    
    def test_adapter_unificado_analisar_genbank(self):
        """Testa adapter unificado com dados GenBank."""
        adapter = self.fabrica.criar_adapter("UNIFICADO")
        resultado = adapter.analisar_sequencia(self.dados_genbank)
        
        self.assertEqual(resultado["formato"], "GenBank")
        self.assertIn("locus", resultado)
    
    def test_adapter_unificado_detectar_formato(self):
        """Testa detecção automática de formato."""
        adapter = self.fabrica.criar_adapter("UNIFICADO")
        
        # Deve detectar como FASTA
        resultado_fasta = adapter.analisar_sequencia(self.dados_fasta)
        self.assertEqual(resultado_fasta["formato"], "FASTA")
        
        # Deve detectar como GenBank
        resultado_genbank = adapter.analisar_sequencia(self.dados_genbank)
        self.assertEqual(resultado_genbank["formato"], "GenBank")
    
    def test_composicao_nucleotideos_adapter(self):
        """Testa cálculo de composição via adapter."""
        adapter = self.fabrica.criar_adapter("FASTA")
        resultado = adapter.analisar_sequencia("ATCGATCG")
        
        composicao = resultado["composicao"]
        self.assertEqual(composicao["A"], 2)
        self.assertEqual(composicao["T"], 2)
        self.assertEqual(composicao["C"], 2)
        self.assertEqual(composicao["G"], 2)
    
    def test_adapter_fasta_sequencia_invalida(self):
        """Testa adapter FASTA com sequência inválida."""
        adapter = self.fabrica.criar_adapter("FASTA")
        
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia("ATCG#INVALIDO")
    
    def test_adapter_genbank_sequencia_invalida(self):
        """Testa adapter GenBank com sequência inválida."""
        adapter = self.fabrica.criar_adapter("GENBANK")
        
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia("sem_locus_nem_origin")
    
    def test_adapter_unificado_sequencia_nao_reconhecida(self):
        """Testa adapter unificado com formato não reconhecido."""
        adapter = self.fabrica.criar_adapter("UNIFICADO")
        
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia("formato_desconhecido")
    
    def test_adapter_fasta_gc_content(self):
        """Testa cálculo de GC content no adapter FASTA."""
        adapter = self.fabrica.criar_adapter("FASTA")
        resultado = adapter.analisar_sequencia("ATCGATCG")
        
        self.assertIn("gc_content", resultado)
        self.assertEqual(resultado["gc_content"], 50.0)  # 50% GC
    
    def test_adapter_genbank_extrair_metadados(self):
        """Testa extração de metadados no adapter GenBank."""
        adapter = self.fabrica.criar_adapter("GENBANK")
        resultado = adapter.analisar_sequencia(self.dados_genbank)
        
        self.assertIn("metadados", resultado)
        metadados = resultado["metadados"]
        self.assertEqual(metadados["locus"], "SCU49845")
        self.assertEqual(metadados["comprimento"], 5028)
        self.assertEqual(metadados["molécula"], "DNA")
    
    def test_adapter_fasta_multiplos_registros(self):
        """Testa adapter FASTA com múltiplos registros."""
        adapter = self.fabrica.criar_adapter("FASTA")
        dados_multiplas = """>seq1\nATCGATCG\n>seq2\nGCTAGCTA\n"""
        
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia(dados_multiplas)
    
    def test_adapter_fasta_vazio(self):
        """Testa adapter FASTA com sequência vazia."""
        adapter = self.fabrica.criar_adapter("FASTA")
        
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia("")
    
    def test_adapter_genbank_origin_vazio(self):
        """Testa adapter GenBank com ORIGIN vazio."""
        adapter = self.fabrica.criar_adapter("GENBANK")
        dados_sem_origin = """LOCUS       TESTE     100 bp    DNA     UNK
DEFINITION  Teste sequence.
"""
        
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia(dados_sem_origin)
    
    def test_adapter_fasta_case_insensitive(self):
        """Testa se adapter FASTA é case insensitive."""
        adapter = self.fabrica.criar_adapter("FASTA")
        resultado = adapter.analisar_sequencia("atcgaTcg")
        
        self.assertEqual(resultado["sequencia"], "atcgaTcg")
        self.assertEqual(resultado["comprimento"], 9)
    
    def test_adapter_fasta_espacos_branco(self):
        """Testa adapter FASTA com espaços em branco."""
        adapter = self.fabrica.criar_adapter("FASTA")
        dados_com_espacos = ">seq1\nATCG ATCG\n"
        
        resultado = adapter.analisar_sequencia(dados_com_espacos)
        self.assertEqual(resultado["sequencia"], "ATCGATCG")
    
    def test_adapter_fasta_numeros(self):
        """Testa adapter FASTA com números na sequência."""
        adapter = self.fabrica.criar_adapter("FASTA")
        dados_com_numeros = ">seq1\nATCG123ATCG"
        
        resultado = adapter.analisar_sequencia(dados_com_numeros)
        self.assertEqual(resultado["sequencia"], "ATCG123ATCG")
        self.assertEqual(resultado["comprimento"], 11)
    
    def test_adapter_fasta_caracteres_especiais(self):
        """Testa adapter FASTA com caracteres especiais."""
        adapter = self.fabrica.criar_adapter("FASTA")
        dados_com_especiais = ">seq1\nATCG-ATCG"
        
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia(dados_com_especiais)
    
    def test_adapter_genbank_features(self):
        """Testa extração de features no adapter GenBank."""
        adapter = self.fabrica.criar_adapter("GENBANK")
        dados_com_features = self.dados_genbank + """FEATURES             location/qualifiers
                     source          1..5028
                                     /organism="Saccharomyces cerevisiae"
"""
        
        resultado = adapter.analisar_sequencia(dados_com_features)
        self.assertIn("features", resultado)
    
    def test_adapter_unificado_fallback(self):
        """Testa fallback do adapter unificado."""
        adapter = self.fabrica.criar_adapter("UNIFICADO")
        
        # Dados que não correspondem a nenhum formato conhecido
        with self.assertRaises(ValueError):
            adapter.analisar_sequencia("dados_invalidos")


if __name__ == "__main__":
    unittest.main()
