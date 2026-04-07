"""
Testes para o padrão Bridge
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.bridge import (
    AlgoritmoProcessamento, AlinhamentoGlobal, AlinhamentoLocal,
    AnaliseGenetica, AnaliseSequenciamento, AnaliseExpressao, AnaliseMutacao
)


class TestBridge(unittest.TestCase):
    """Testes para o padrão Bridge."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.alinhamento_global = AlinhamentoGlobal()
        self.alinhamento_local = AlinhamentoLocal()
        
        self.analise_seq_global = AnaliseSequenciamento("Seq-Global", self.alinhamento_global)
        self.analise_seq_local = AnaliseSequenciamento("Seq-Local", self.alinhamento_local)
        
        self.analise_exp_global = AnaliseExpressao("Exp-Global", self.alinhamento_global)
        self.analise_exp_local = AnaliseExpressao("Exp-Local", self.alinhamento_local)
    
    def test_alinhamento_global_creation(self):
        """Testa criação do alinhamento global."""
        alinhamento = AlinhamentoGlobal()
        
        self.assertIsInstance(alinhamento, AlgoritmoProcessamento)
        self.assertEqual(alinhamento.__class__.__name__, "AlinhamentoGlobal")
    
    def test_alinhamento_local_creation(self):
        """Testa criação do alinhamento local."""
        alinhamento = AlinhamentoLocal()
        
        self.assertIsInstance(alinhamento, AlgoritmoProcessamento)
        self.assertEqual(alinhamento.__class__.__name__, "AlinhamentoLocal")
    
    def test_alinhamento_global_processar_dados(self):
        """Testa processamento de dados com alinhamento global."""
        dados = ("ATCGATCG", "GCTAGCTA")
        resultado = self.alinhamento_global.processar_dados(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_alinhamento', resultado)
        self.assertIn('sequencia1', resultado)
        self.assertIn('sequencia2', resultado)
        self.assertIn('score', resultado)
        self.assertEqual(resultado['tipo_alinhamento'], "global")
    
    def test_alinhamento_local_processar_dados(self):
        """Testa processamento de dados com alinhamento local."""
        dados = ("ATCGATCG", "GCTAGCTA")
        resultado = self.alinhamento_local.processar_dados(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_alinhamento', resultado)
        self.assertIn('sequencia1', resultado)
        self.assertIn('sequencia2', resultado)
        self.assertIn('melhor_score', resultado)
        self.assertEqual(resultado['tipo_alinhamento'], "local")
    
    def test_analise_sequenciamento_creation(self):
        """Testa criação da análise de sequenciamento."""
        analise = AnaliseSequenciamento("Teste", self.alinhamento_global)
        
        self.assertIsInstance(analise, AnaliseGenetica)
        self.assertEqual(analise.nome, "Teste")
        self.assertEqual(analise.algoritmo, self.alinhamento_global)
    
    def test_analise_sequenciamento_executar(self):
        """Testa execução da análise de sequenciamento."""
        dados = ("ATCGATCG", "GCTAGCTA")
        resultado = self.analise_seq_global.executar_analise(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_analise', resultado)
        self.assertIn('nome_analise', resultado)
        self.assertIn('resultado_base', resultado)
        self.assertIn('qualidade_sequenciamento', resultado)
        self.assertEqual(resultado['tipo_analise'], "sequenciamento")
        self.assertEqual(resultado['nome_analise'], "Seq-Global")
    
    def test_bridge_independence(self):
        """Testa independência entre abstração e implementação."""
        # Mesma implementação, abstrações diferentes
        resultado_seq = self.analise_seq_global.executar_analise(("ATCG", "GCTA"))
        resultado_exp = self.analise_exp_global.executar_analise(("ATCG", "GCTA"))
        
        # Implementação deve ser a mesma
        self.assertEqual(
            resultado_seq['resultado_base']['tipo_alinhamento'],
            resultado_exp['resultado_base']['tipo_alinhamento']
        )
        
        # Abstração deve ser diferente
        self.assertNotEqual(
            resultado_seq['tipo_analise'],
            resultado_exp['tipo_analise']
        )
    
    def test_bridge_extensibilidade(self):
        """Testa extensibilidade do padrão Bridge."""
        # Mesma abstração, implementações diferentes
        resultado_global = self.analise_seq_global.executar_analise(("ATCG", "GCTA"))
        resultado_local = self.analise_seq_local.executar_analise(("ATCG", "GCTA"))
        
        # Abstração deve ser a mesma
        self.assertEqual(resultado_global['tipo_analise'], resultado_local['tipo_analise'])
        
        # Implementação deve ser diferente
        self.assertNotEqual(
            resultado_global['resultado_base']['tipo_alinhamento'],
            resultado_local['resultado_base']['tipo_alinhamento']
        )
    
    def test_change_implementation_runtime(self):
        """Testa mudança de implementação em tempo de execução."""
        analise = AnaliseSequenciamento("Teste", self.alinhamento_global)
        
        # Operação com implementação inicial
        resultado_global = analise.executar_analise(("ATCG", "GCTA"))
        self.assertEqual(resultado_global['resultado_base']['tipo_alinhamento'], "global")
        
        # Mudar implementação
        analise.mudar_algoritmo(self.alinhamento_local)
        
        # Operação com nova implementação
        resultado_local = analise.executar_analise(("ATCG", "GCTA"))
        self.assertEqual(resultado_local['resultado_base']['tipo_alinhamento'], "local")
    
    def test_bridge_pattern_benefits(self):
        """Testa benefícios do padrão Bridge."""
        # 1. Desacoplamento entre abstração e implementação
        self.assertNotEqual(
            type(self.analise_seq_global).__name__,
            type(self.alinhamento_global).__name__
        )
        
        # 2. Extensibilidade independente
        self.assertTrue(hasattr(self.analise_seq_global, 'executar_analise'))
        self.assertTrue(hasattr(self.alinhamento_global, 'processar_dados'))
        
        # 3. Mudança em tempo de execução
        self.assertTrue(hasattr(self.analise_seq_global, 'mudar_algoritmo'))


if __name__ == '__main__':
    unittest.main()
