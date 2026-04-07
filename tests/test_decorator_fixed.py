"""
Testes para o padrão Decorator
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.decorator import (
    AnaliseBioInterface, AnaliseBasica, AnaliseDecorator,
    DecoradorValidacao, DecoradorCache, DecoradorLog, DecoradorPerformance
)


class TestDecorator(unittest.TestCase):
    """Testes para o padrão Decorator."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.analise_basica = AnaliseBasica("Análise Teste")
        
        self.decorator_validacao = DecoradorValidacao(self.analise_basica)
        self.decorator_cache = DecoradorCache(self.analise_basica)
        self.decorator_log = DecoradorLog(self.analise_basica)
        self.decorator_performance = DecoradorPerformance(self.analise_basica)
    
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
        self.assertIn('nome_analise', resultado)
        self.assertIn('resultado', resultado)
        self.assertIn('custo', resultado)
        self.assertIn('timestamp', resultado)
        self.assertEqual(resultado['nome_analise'], "Análise Teste")
    
    def test_decorator_validacao_creation(self):
        """Testa criação do decorador de validação."""
        decorator = DecoradorValidacao(self.analise_basica)
        
        self.assertIsInstance(decorator, AnaliseDecorator)
        self.assertIsInstance(decorator, AnaliseBioInterface)
        self.assertEqual(decorator.componente, self.analise_basica)
    
    def test_decorator_validacao_executar_com_dados_validos(self):
        """Testa execução do decorador de validação com dados válidos."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        resultado = self.decorator_validacao.executar(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('nome_analise', resultado)
        self.assertIn('resultado', resultado)
        self.assertIn('validado', resultado)
        self.assertTrue(resultado['validado'])
    
    def test_decorator_validacao_executar_com_dados_invalidos(self):
        """Testa execução do decorador de validação com dados inválidos."""
        dados = {"sequencia": "", "parametro": "valor"}
        
        with self.assertRaises(ValueError):
            self.decorator_validacao.executar(dados)
    
    def test_decorator_cache_creation(self):
        """Testa criação do decorador de cache."""
        decorator = DecoradorCache(self.analise_basica)
        
        self.assertIsInstance(decorator, AnaliseDecorator)
        self.assertIsInstance(decorator, AnaliseBioInterface)
        self.assertEqual(decorator.componente, self.analise_basica)
    
    def test_decorator_cache_executar_primeira_vez(self):
        """Testa execução do decorador de cache - primeira vez."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        resultado1 = self.decorator_cache.executar(dados)
        
        self.assertIsInstance(resultado1, dict)
        self.assertIn('cache_hit', resultado1)
        self.assertFalse(resultado1['cache_hit'])
    
    def test_decorator_cache_executar_segunda_vez(self):
        """Testa execução do decorador de cache - segunda vez."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        # Primeira execução
        resultado1 = self.decorator_cache.executar(dados)
        
        # Segunda execução (deve usar cache)
        resultado2 = self.decorator_cache.executar(dados)
        
        self.assertTrue(resultado2['cache_hit'])
        self.assertEqual(resultado1['resultado'], resultado2['resultado'])
    
    def test_decorator_log_creation(self):
        """Testa criação do decorador de log."""
        decorator = DecoradorLog(self.analise_basica)
        
        self.assertIsInstance(decorator, AnaliseDecorator)
        self.assertIsInstance(decorator, AnaliseBioInterface)
        self.assertEqual(decorator.componente, self.analise_basica)
    
    def test_decorator_log_executar(self):
        """Testa execução do decorador de log."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        with patch('builtins.print') as mock_print:
            resultado = self.decorator_log.executar(dados)
            
            # Verifica se o log foi gerado
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            self.assertIn("Iniciando análise", call_args)
            self.assertIn("Análise Teste", call_args)
            self.assertIn("Análise concluída", call_args)
        
        # Verifica se o resultado foi preservado
        self.assertIsInstance(resultado, dict)
        self.assertIn('nome_analise', resultado)
    
    def test_decorator_performance_creation(self):
        """Testa criação do decorador de performance."""
        decorator = DecoradorPerformance(self.analise_basica)
        
        self.assertIsInstance(decorator, AnaliseDecorator)
        self.assertIsInstance(decorator, AnaliseBioInterface)
        self.assertEqual(decorator.componente, self.analise_basica)
    
    def test_decorator_performance_executar(self):
        """Testa execução do decorador de performance."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        resultado = self.decorator_performance.executar(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tempo_execucao', resultado)
        self.assertIn('performance_stats', resultado)
        self.assertIsInstance(resultado['tempo_execucao'], float)
        self.assertGreater(resultado['tempo_execucao'], 0)
    
    def test_decorator_composicao(self):
        """Testa composição de múltiplos decorators."""
        # Compor decorators: Cache -> Validação -> Log -> Análise Básica
        decorator_composto = DecoradorCache(
            DecoradorValidacao(
                DecoradorLog(self.analise_basica)
            )
        )
        
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        # Primeira execução
        resultado1 = decorator_composto.executar(dados)
        
        # Segunda execução (deve usar cache)
        resultado2 = decorator_composto.executar(dados)
        
        # Verificar comportamento
        self.assertIn('cache_hit', resultado1)
        self.assertFalse(resultado1['cache_hit'])
        
        self.assertIn('cache_hit', resultado2)
        self.assertTrue(resultado2['cache_hit'])
        
        # Resultados devem ser iguais
        self.assertEqual(resultado1['resultado'], resultado2['resultado'])
    
    def test_decorator_transparencia_interface(self):
        """Testa transparência da interface do decorator."""
        decorators = [
            self.analise_basica,
            self.decorator_validacao,
            self.decorator_cache,
            self.decorator_log,
            self.decorator_performance
        ]
        
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        for decorator in decorators:
            # Todos devem ter a mesma interface
            self.assertTrue(hasattr(decorator, 'executar'))
            
            # Todos devem retornar resultados consistentes
            resultado = decorator.executar(dados)
            self.assertIsInstance(resultado, dict)
            self.assertIn('nome_analise', resultado)
    
    def test_decorator_adicao_comportamento(self):
        """Testa adição de comportamento pelo decorator."""
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        resultado_basico = self.analise_basica.executar(dados)
        resultado_com_log = self.decorator_log.executar(dados)
        
        # Resultado base deve estar contido no resultado com decorator
        self.assertEqual(
            resultado_basico['resultado'],
            resultado_com_log['resultado']
        )
        
        # Mas decorator adiciona informações
        self.assertIn('log_info', resultado_com_log)
        self.assertNotIn('log_info', resultado_basico)
    
    def test_decorator_remocao_dinamica(self):
        """Testa remoção dinâmica de decorators."""
        # Criar cadeia de decorators
        decorator_composto = DecoradorCache(
            DecoradorLog(self.analise_basica)
        )
        
        # Executar com decorators
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        resultado_com_decorators = decorator_composto.executar(dados)
        
        # Remover decorators (acessar componente original)
        resultado_sem_decorators = decorator_composto.componente.executar(dados)
        
        # Resultados devem ser diferentes
        self.assertNotEqual(
            resultado_com_decorators.get('cache_hit'),
            resultado_sem_decorators.get('cache_hit')
        )
    
    def test_decorator_stack_multiple(self):
        """Testa stack de múltiplos decorators."""
        # Criar stack: Performance -> Cache -> Validação -> Básico
        stack = DecoradorPerformance(
            DecoradorCache(
                DecoradorValidacao(self.analise_basica)
            )
        )
        
        dados = {"sequencia": "ATCG", "parametro": "valor"}
        
        # Primeira execução
        resultado1 = stack.executar(dados)
        
        # Segunda execução
        resultado2 = stack.executar(dados)
        
        # Verificar comportamento do stack
        self.assertIn('tempo_execucao', resultado1)
        self.assertIn('cache_hit', resultado1)
        self.assertFalse(resultado1['cache_hit'])
        
        self.assertIn('tempo_execucao', resultado2)
        self.assertIn('cache_hit', resultado2)
        self.assertTrue(resultado2['cache_hit'])
    
    def test_decorator_error_propagation(self):
        """Testa propagação de erros no decorator."""
        # Mock que lança exceção
        mock_analise = Mock()
        mock_analise.executar.side_effect = Exception("Erro de teste")
        
        decorator = DecoradorLog(mock_analise)
        
        with self.assertRaises(Exception):
            decorator.executar({"sequencia": "ATCG"})
    
    def test_decorator_benefits(self):
        """Testa benefícios do padrão Decorator."""
        # 1. Adição de comportamento sem modificar classe original
        self.assertIsInstance(self.decorator_log, AnaliseBioInterface)
        self.assertNotEqual(type(self.decorator_log), type(self.analise_basica))
        
        # 2. Composição flexível
        decorator_composto = DecoradorCache(DecoradorLog(self.analise_basica))
        self.assertIsInstance(decorator_composto, AnaliseBioInterface)
        
        # 3. Remoção dinâmica
        self.assertEqual(decorator_composto.componente.componente, self.analise_basica)
        
        # 4. Transparência
        self.assertTrue(hasattr(self.decorator_log, 'executar'))


if __name__ == '__main__':
    unittest.main()
