"""
Testes para o padrão Bridge
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.bridge import (
    AlgoritmoProcessamento, AlinhamentoGlobal, AlinhamentoLocal,
    ProcessadorDados, ProcessadorBasico, ProcessadorAvancado
)


class TestBridge(unittest.TestCase):
    """Testes para o padrão Bridge."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.alinhamento_global = AlinhamentoGlobal()
        self.alinhamento_local = AlinhamentoLocal()
        
        self.processador_basico_global = ProcessadorBasico(self.alinhamento_global)
        self.processador_basico_local = ProcessadorBasico(self.alinhamento_local)
        
        self.processador_avancado_global = ProcessadorAvancado(self.alinhamento_global)
        self.processador_avancado_local = ProcessadorAvancado(self.alinhamento_local)
    
    def test_alinhamento_global_creation(self):
        """Testa criação do alinhamento global."""
        alinhamento = AlinhamentoGlobal()
        
        self.assertIsInstance(alinhamento, AlgoritmoProcessamento)
        self.assertEqual(alinhamento.nome, "Alinhamento Global")
    
    def test_alinhamento_local_creation(self):
        """Testa criação do alinhamento local."""
        alinhamento = AlinhamentoLocal()
        
        self.assertIsInstance(alinhamento, AlgoritmoProcessamento)
        self.assertEqual(alinhamento.nome, "Alinhamento Local")
    
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
        self.assertIn('score', resultado)
        self.assertEqual(resultado['tipo_alinhamento'], "local")
    
    def test_processador_basico_creation(self):
        """Testa criação do processador básico."""
        processador = ProcessadorBasico(self.alinhamento_global)
        
        self.assertIsInstance(processador, ProcessadorDados)
        self.assertEqual(processador.nome, "Processador Básico")
        self.assertEqual(processador.algoritmo, self.alinhamento_global)
    
    def test_processador_avancado_creation(self):
        """Testa criação do processador avançado."""
        processador = ProcessadorAvancado(self.alinhamento_local)
        
        self.assertIsInstance(processador, ProcessadorDados)
        self.assertEqual(processador.nome, "Processador Avançado")
        self.assertEqual(processador.algoritmo, self.alinhamento_local)
    
    def test_processador_basico_executar(self):
        """Testa execução do processador básico."""
        dados = ("ATCGATCG", "GCTAGCTA")
        resultado = self.processador_basico_global.executar(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('processador', resultado)
        self.assertIn('algoritmo', resultado)
        self.assertIn('resultado_processamento', resultado)
        self.assertEqual(resultado['processador'], "Processador Básico")
    
    def test_processador_avancado_executar(self):
        """Testa execução do processador avançado."""
        dados = ("ATCGATCG", "GCTAGCTA")
        resultado = self.processador_avancado_local.executar(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('processador', resultado)
        self.assertIn('algoritmo', resultado)
        self.assertIn('resultado_processamento', resultado)
        self.assertIn('estatisticas_avancadas', resultado)
        self.assertEqual(resultado['processador'], "Processador Avançado")


if __name__ == '__main__':
    unittest.main()
