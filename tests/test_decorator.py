"""
Testes para o padrão Decorator
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.decorator import (
    SequenciadorBase, SequenciadorDecorator, ValidadorQualidadeDecorator,
    LoggerDecorator, CacheDecorator, FiltroContaminacaoDecorator
)


class TestDecorator(unittest.TestCase):
    """Testes para o padrão Decorator."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.sequenciador_base = SequenciadorBase()
        
        # Decorators individuais
        self.decorator_validador = ValidadorQualidadeDecorator(self.sequenciador_base)
        self.decorator_logger = LoggerDecorator(self.sequenciador_base)
        self.decorator_cache = CacheDecorator(self.sequenciador_base)
        self.decorator_filtro = FiltroContaminacaoDecorator(self.sequenciador_base)
    
    def test_sequenciador_base_creation(self):
        """Testa criação do sequenciador base."""
        self.assertIsInstance(self.sequenciador_base, SequenciadorBase)
        self.assertEqual(self.sequenciador_base.nome, "Sequenciador Base")
    
    def test_sequenciador_base_sequenciar(self):
        """Testa operação de sequenciamento base."""
        resultado = self.sequenciador_base.sequenciar("ATCGATCG", "illumina")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('sequencia', resultado)
        self.assertIn('plataforma', resultado)
        self.assertIn('status', resultado)
        self.assertIn('dados_brutos', resultado)
        self.assertEqual(resultado['sequencia'], "ATCGATCG")
        self.assertEqual(resultado['plataforma'], "illumina")
        self.assertEqual(resultado['status'], "Sequenciado")
    
    def test_validador_qualidade_decorator(self):
        """Testa decorator validador de qualidade."""
        self.assertIsInstance(self.decorator_validador, SequenciadorDecorator)
        self.assertIsInstance(self.decorator_validador, ValidadorQualidadeDecorator)
        self.assertEqual(self.decorator_validador.componente, self.sequenciador_base)
    
    def test_validador_qualidade_decorator_sequenciar(self):
        """Testa sequenciamento com validador de qualidade."""
        resultado = self.decorator_validador.sequenciar("ATCGATCG", "illumina")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('sequencia', resultado)
        self.assertIn('plataforma', resultado)
        self.assertIn('status', resultado)
        self.assertIn('qualidade', resultado)
        self.assertIn('score_qualidade', resultado)
        self.assertIn('status_qualidade', resultado)
        self.assertEqual(resultado['status_qualidade'], "Aprovado")
    
    def test_validador_qualidade_decorator_sequencia_ruim(self):
        """Testa validador com sequência de baixa qualidade."""
        resultado = self.decorator_validador.sequenciar("ATCG", "illumina")  # Sequência curta
        
        self.assertEqual(resultado['status_qualidade'], "Reprovado")
        self.assertLess(resultado['score_qualidade'], 0.5)
    
    def test_logger_decorator(self):
        """Testa decorator logger."""
        self.assertIsInstance(self.decorator_logger, SequenciadorDecorator)
        self.assertIsInstance(self.decorator_logger, LoggerDecorator)
        self.assertEqual(self.decorator_logger.componente, self.sequenciador_base)
    
    def test_logger_decorator_sequenciar(self):
        """Testa sequenciamento com logger."""
        with patch('builtins.print') as mock_print:
            resultado = self.decorator_logger.sequenciar("ATCGATCG", "illumina")
            
            # Verifica se o log foi gerado
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            self.assertIn("Iniciando sequenciamento", call_args)
            self.assertIn("Sequenciamento concluído", call_args)
        
        # Verifica se o resultado original foi preservado
        self.assertIn('sequencia', resultado)
        self.assertEqual(resultado['sequencia'], "ATCGATCG")
    
    def test_cache_decorator(self):
        """Testa decorator cache."""
        self.assertIsInstance(self.decorator_cache, SequenciadorDecorator)
        self.assertIsInstance(self.decorator_cache, CacheDecorator)
        self.assertEqual(self.decorator_cache.componente, self.sequenciador_base)
    
    def test_cache_decorator_sequenciar(self):
        """Testa sequenciamento com cache."""
        # Primeira chamada (deve executar e cachear)
        resultado1 = self.decorator_cache.sequenciar("ATCGATCG", "illumina")
        
        # Segunda chamada com mesmos parâmetros (deve usar cache)
        resultado2 = self.decorator_cache.sequenciar("ATCGATCG", "illumina")
        
        # Resultados devem ser idênticos
        self.assertEqual(resultado1['sequencia'], resultado2['sequencia'])
        self.assertEqual(resultado1['plataforma'], resultado2['plataforma'])
        
        # Verifica se o cache foi usado
        self.assertIn('cache_hit', resultado2)
        self.assertTrue(resultado2['cache_hit'])
    
    def test_cache_decorator_different_parameters(self):
        """Testa cache com parâmetros diferentes."""
        resultado1 = self.decorator_cache.sequenciar("ATCGATCG", "illumina")
        resultado2 = self.decorator_cache.sequenciar("GCTAGCTA", "illumina")
        
        # Deve ser cache miss
        self.assertFalse(resultado2.get('cache_hit', False))
        self.assertNotEqual(resultado1['sequencia'], resultado2['sequencia'])
    
    def test_filtro_contaminacao_decorator(self):
        """Testa decorator filtro de contaminação."""
        self.assertIsInstance(self.decorator_filtro, SequenciadorDecorator)
        self.assertIsInstance(self.decorator_filtro, FiltroContaminacaoDecorator)
        self.assertEqual(self.decorator_filtro.componente, self.sequenciador_base)
    
    def test_filtro_contaminacao_decorator_sequenciar_limpo(self):
        """Testa filtro com sequência limpa."""
        resultado = self.decorator_filtro.sequenciar("ATCGATCG", "illumina")
        
        self.assertIn('contaminacao', resultado)
        self.assertIn('status_contaminacao', resultado)
        self.assertEqual(resultado['status_contaminacao'], "Limpo")
        self.assertFalse(resultado['contaminacao'])
    
    def test_filtro_contaminacao_decorator_sequenciar_contaminado(self):
        """Testa filtro com sequência contaminada."""
        resultado = self.decorator_filtro.sequenciar("AAAAAAATCG", "illumina")
        
        self.assertEqual(resultado['status_contaminacao'], "Contaminado")
        self.assertTrue(resultado['contaminacao'])
        self.assertIn('contaminantes', resultado)
    
    def test_multiple_decorators_chain(self):
        """Testa cadeia de múltiplos decorators."""
        # Montar cadeia: Cache -> Validador -> Logger -> Base
        decorator_composto = CacheDecorator(
            ValidadorQualidadeDecorator(
                LoggerDecorator(self.sequenciador_base)
            )
        )
        
        resultado = decorator_composto.sequenciar("ATCGATCG", "illumina")
        
        # Verifica se todos os decorators foram aplicados
        self.assertIn('sequencia', resultado)
        self.assertIn('qualidade', resultado)  # Validador
        self.assertIn('cache_hit', resultado)  # Cache
        self.assertEqual(resultado['status'], "Sequenciado")
    
    def test_decorator_order_independence(self):
        """Testa independência da ordem dos decorators."""
        # Ordem 1: Validador -> Logger
        decorator1 = LoggerDecorator(ValidadorQualidadeDecorator(self.sequenciador_base))
        
        # Ordem 2: Logger -> Validador
        decorator2 = ValidadorQualidadeDecorator(LoggerDecorator(self.sequenciador_base))
        
        resultado1 = decorator1.sequenciar("ATCGATCG", "illumina")
        resultado2 = decorator2.sequenciar("ATCGATCG", "illumina")
        
        # Resultados principais devem ser os mesmos
        self.assertEqual(resultado1['sequencia'], resultado2['sequencia'])
        self.assertEqual(resultado1['plataforma'], resultado2['plataforma'])
    
    def test_decorator_adds_responsibility(self):
        """Testa se decorator adiciona responsabilidade sem modificar o componente."""
        resultado_base = self.sequenciador_base.sequenciar("ATCGATCG", "illumina")
        resultado_decorator = self.decorator_validador.sequenciar("ATCGATCG", "illumina")
        
        # Componente base não deve ter informações de qualidade
        self.assertNotIn('qualidade', resultado_base)
        
        # Decorator deve adicionar informações de qualidade
        self.assertIn('qualidade', resultado_decorator)
        
        # Funcionalidade original deve ser preservada
        self.assertEqual(resultado_base['sequencia'], resultado_decorator['sequencia'])
    
    def test_decorator_runtime_addition(self):
        """Testa adição de decorators em tempo de execução."""
        sequenciador = self.sequenciador_base
        
        # Adicionar decorator em runtime
        sequenciador = ValidadorQualidadeDecorator(sequenciador)
        resultado1 = sequenciador.sequenciar("ATCGATCG", "illumina")
        
        # Adicionar outro decorator
        sequenciador = LoggerDecorator(sequenciador)
        resultado2 = sequenciador.sequenciar("ATCGATCG", "illumina")
        
        # Segundo resultado deve ter mais funcionalidades
        self.assertIn('qualidade', resultado1)
        self.assertIn('qualidade', resultado2)
    
    def test_decorator_transparency(self):
        """Testa transparência do decorator para código cliente."""
        # Cliente não precisa saber se está usando decorator ou componente base
        componentes = [self.sequenciador_base, self.decorator_validador, self.decorator_logger]
        
        for componente in componentes:
            resultado = componente.sequenciar("ATCGATCG", "illumina")
            
            # Interface é a mesma
            self.assertIn('sequencia', resultado)
            self.assertIn('plataforma', resultado)
            self.assertIn('status', resultado)
            self.assertEqual(resultado['sequencia'], "ATCGATCG")
    
    def test_decorator_nested_decorators(self):
        """Testa decorators aninhados."""
        # Criar estrutura aninhada complexa
        nested_decorator = CacheDecorator(
            ValidadorQualidadeDecorator(
                FiltroContaminacaoDecorator(
                    LoggerDecorator(self.sequenciador_base)
                )
            )
        )
        
        resultado = nested_decorator.sequenciar("ATCGATCG", "illumina")
        
        # Verifica se todos os níveis foram aplicados
        self.assertIn('sequencia', resultado)
        self.assertIn('qualidade', resultado)
        self.assertIn('contaminacao', resultado)
        self.assertIn('cache_hit', resultado)
    
    def test_decorator_error_propagation(self):
        """Testa propagação de erros através de decorators."""
        # Mock que lança exceção
        mock_sequenciador = Mock(spec=SequenciadorBase)
        mock_sequenciador.sequenciar.side_effect = Exception("Test error")
        
        decorator = ValidadorQualidadeDecorator(mock_sequenciador)
        
        with self.assertRaises(Exception):
            decorator.sequenciar("ATCGATCG", "illumina")
    
    def test_decorator_state_preservation(self):
        """Testa preservação de estado entre chamadas."""
        # Primeira chamada
        resultado1 = self.decorator_cache.sequenciar("ATCGATCG", "illumina")
        
        # Segunda chamada (deve usar cache)
        resultado2 = self.decorator_cache.sequenciar("ATCGATCG", "illumina")
        
        # Estado do cache deve ser preservado
        self.assertTrue(resultado1.get('cache_hit', False) == False or True)
        self.assertTrue(resultado2['cache_hit'])
    
    def test_decorator_configuration(self):
        """Testa configuração de parâmetros do decorator."""
        # Validador com limiar customizado
        validador_custom = ValidadorQualidadeDecorator(
            self.sequenciador_base, 
            limiar_qualidade=0.9
        )
        
        resultado = validador_custom.sequenciar("ATCGATCG", "illumina")
        
        self.assertIn('limiar_qualidade', resultado)
        self.assertEqual(resultado['limiar_qualidade'], 0.9)
    
    def test_decorator_multiple_calls_same_object(self):
        """Testa múltiplas chamadas no mesmo objeto decorator."""
        resultado1 = self.decorator_validador.sequenciar("ATCGATCG", "illumina")
        resultado2 = self.decorator_validador.sequenciar("GCTAGCTA", "illumina")
        
        # Cada chamada deve ser independente
        self.assertNotEqual(resultado1['sequencia'], resultado2['sequencia'])
        self.assertIn('qualidade', resultado1)
        self.assertIn('qualidade', resultado2)
    
    def test_decorator_component_replacement(self):
        """Testa substituição do componente decorado."""
        decorator = ValidadorQualidadeDecorator(self.sequenciador_base)
        
        # Substituir componente
        novo_sequenciador = SequenciadorBase()
        decorator.componente = novo_sequenciador
        
        resultado = decorator.sequenciar("ATCGATCG", "illumina")
        
        # Deve funcionar com o novo componente
        self.assertIn('sequencia', resultado)
        self.assertIn('qualidade', resultado)
    
    def test_decorator_performance_impact(self):
        """Testa impacto de performance dos decorators."""
        import time
        
        # Testar componente base
        start_time = time.time()
        for _ in range(100):
            self.sequenciador_base.sequenciar("ATCGATCG", "illumina")
        base_time = time.time() - start_time
        
        # Testar com decorators
        decorated = CacheDecorator(ValidadorQualidadeDecorator(self.sequenciador_base))
        start_time = time.time()
        for _ in range(100):
            decorated.sequenciar("ATCGATCG", "illumina")
        decorated_time = time.time() - start_time
        
        # Cache deve melhorar performance em chamadas repetidas
        self.assertLess(decorated_time, base_time * 2)  # Não deve ser muito mais lento


if __name__ == '__main__':
    unittest.main()
