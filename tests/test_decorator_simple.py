"""
Testes para o padrão Decorator
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.decorator import (
    AnaliseBioInterface, AnaliseBasica, AnaliseDecorator,
    AnaliseComValidacao
)


class TestDecorator(unittest.TestCase):
    """Testes para o padrão Decorator."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.analise_basica = AnaliseBasica("Análise Teste")
        self.decorator_validacao = AnaliseComValidacao(self.analise_basica)
    
    def test_analise_basica_creation(self):
        """Testa criação da análise básica."""
        analise = AnaliseBasica("Test Analysis")
        
        self.assertIsInstance(analise, AnaliseBioInterface)
        self.assertEqual(analise.nome, "Test Analysis")
        self.assertEqual(analise.custo_base, 100.0)
    
    def test_analise_basica_executar(self):
        """Testa execução da análise básica."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        resultado = self.analise_basica.executar(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo', resultado)
        self.assertIn('nome', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['tipo'], "básica")
        self.assertEqual(resultado['nome'], "Análise Teste")
        self.assertEqual(resultado['status'], "concluída")
    
    def test_decorator_validacao_creation(self):
        """Testa criação do decorador de validação."""
        decorator = AnaliseComValidacao(self.analise_basica)
        
        self.assertIsInstance(decorator, AnaliseDecorator)
        self.assertIsInstance(decorator, AnaliseBioInterface)
        self.assertEqual(decorator._analise, self.analise_basica)
    
    def test_decorator_validacao_executar(self):
        """Testa execução do decorador de validação."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        resultado = self.decorator_validacao.executar(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo', resultado)
        self.assertIn('status', resultado)
        
        # Pode ser "concluída" ou "validacao_falhou" dependendo dos dados
        self.assertIn(resultado['status'], ["concluída", "validacao_falhou"])
    
    def test_decorator_transparencia_interface(self):
        """Testa transparência da interface do decorator."""
        componentes = [self.analise_basica, self.decorator_validacao]
        
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        for componente in componentes:
            # Todos devem ter a mesma interface
            self.assertTrue(hasattr(componente, 'executar'))
            
            # Todos devem retornar resultados consistentes
            resultado = componente.executar(dados)
            self.assertIsInstance(resultado, dict)
            self.assertIn('tipo', resultado)
    
    def test_decorator_adicao_comportamento(self):
        """Testa adição de comportamento pelo decorator."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        resultado_basico = self.analise_basica.executar(dados)
        resultado_com_validacao = self.decorator_validacao.executar(dados)
        
        # Resultados devem ter estruturas diferentes
        self.assertNotEqual(resultado_basico['tipo'], resultado_com_validacao['tipo'])
        
        # Mas decorator deve preservar funcionalidade base
        if resultado_com_validacao['status'] == 'concluída':
            self.assertIn('resultado_original', resultado_com_validacao)
    
    def test_decorator_composicao(self):
        """Testa composição de múltiplos decorators."""
        # Criar decorator aninhado
        decorator_aninhado = AnaliseComValidacao(self.decorator_validacao)
        
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        resultado = decorator_aninhado.executar(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo', resultado)
        self.assertIn('status', resultado)
    
    def test_decorator_benefits(self):
        """Testa benefícios do padrão Decorator."""
        # 1. Adição de comportamento sem modificar classe original
        self.assertIsInstance(self.decorator_validacao, AnaliseBioInterface)
        self.assertNotEqual(type(self.decorator_validacao), type(self.analise_basica))
        
        # 2. Composição flexível
        self.assertEqual(self.decorator_validacao._analise, self.analise_basica)
        
        # 3. Transparência
        self.assertTrue(hasattr(self.decorator_validacao, 'executar'))
        
        # 4. Múltiplos decorators
        decorator_duplo = AnaliseComValidacao(self.decorator_validacao)
        self.assertIsInstance(decorator_duplo, AnaliseBioInterface)


if __name__ == '__main__':
    unittest.main()
