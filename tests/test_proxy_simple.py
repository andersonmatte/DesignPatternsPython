"""
Testes para o padrão Proxy
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.proxy import (
    BancoDadosGeneticosInterface, BancoDadosGeneticosReal, 
    BancoDadosProxy, CacheProxy, SegurancaProxy
)


class TestProxy(unittest.TestCase):
    """Testes para o padrão Proxy."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.banco_real = BancoDadosGeneticosReal()
        self.proxy_cache = CacheProxy(self.banco_real)
        self.proxy_seguranca = SegurancaProxy(self.banco_real)
    
    def test_banco_dados_interface(self):
        """Testa interface do banco de dados."""
        self.assertTrue(hasattr(self.banco_real, 'buscar_sequencia'))
        self.assertTrue(hasattr(self.banco_real, 'buscar_variantes'))
        
        # Deve implementar a interface
        self.assertIsInstance(self.banco_real, BancoDadosGeneticosInterface)
    
    def test_banco_dados_real_buscar_sequencia(self):
        """Testa busca de sequência no banco real."""
        resultado = self.banco_real.buscar_sequencia("SEQ001", "user1")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('id', resultado)
        self.assertIn('sequencia', resultado)
        self.assertIn('descricao', resultado)
        self.assertEqual(resultado['id'], "SEQ001")
    
    def test_banco_dados_real_buscar_variantes(self):
        """Testa busca de variantes no banco real."""
        resultado = self.banco_real.buscar_variantes("BRCA1", "user1")
        
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)
        
        for variante in resultado:
            self.assertIsInstance(variante, dict)
            self.assertIn('gene', variante)
            self.assertIn('posicao', variante)
            self.assertIn('tipo', variante)
    
    def test_proxy_cache_creation(self):
        """Testa criação do proxy de cache."""
        proxy = CacheProxy(self.banco_real)
        
        self.assertIsInstance(proxy, BancoDadosProxy)
        self.assertIsInstance(proxy, BancoDadosGeneticosInterface)
        self.assertEqual(proxy.banco_dados, self.banco_real)
    
    def test_proxy_seguranca_creation(self):
        """Testa criação do proxy de segurança."""
        proxy = SegurancaProxy(self.banco_real)
        
        self.assertIsInstance(proxy, BancoDadosProxy)
        self.assertIsInstance(proxy, BancoDadosGeneticosInterface)
        self.assertEqual(proxy.banco_dados, self.banco_real)
    
    def test_proxy_cache_buscar_sequencia_primeira_vez(self):
        """Testa cache proxy - primeira busca."""
        resultado = self.proxy_cache.buscar_sequencia("SEQ001", "user1")
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['id'], "SEQ001")
        
        # Cache deve estar populado
        self.assertIn("SEQ001", self.proxy_cache.cache_sequencias)
    
    def test_proxy_cache_buscar_sequencia_segunda_vez(self):
        """Testa cache proxy - segunda busca (cache hit)."""
        # Primeira busca
        resultado1 = self.proxy_cache.buscar_sequencia("SEQ001", "user1")
        
        # Segunda busca deve usar cache
        resultado2 = self.proxy_cache.buscar_sequencia("SEQ001", "user1")
        
        # Resultados devem ser idênticos
        self.assertEqual(resultado1, resultado2)
        
        # Cache deve conter o resultado
        self.assertIn("SEQ001", self.proxy_cache.cache_sequencias)
    
    def test_proxy_cache_buscar_variantes(self):
        """Testa cache proxy - busca de variantes."""
        resultado = self.proxy_cache.buscar_variantes("BRCA1", "user1")
        
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)
        
        # Cache deve estar populado
        self.assertIn("BRCA1", self.proxy_cache.cache_variantes)
    
    def test_proxy_seguranca_autorizado(self):
        """Testa proxy de segurança - usuário autorizado."""
        resultado = self.proxy_seguranca.buscar_sequencia("SEQ001", "admin")
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['id'], "SEQ001")
    
    def test_proxy_seguranca_nao_autorizado(self):
        """Testa proxy de segurança - usuário não autorizado."""
        resultado = self.proxy_seguranca.buscar_sequencia("SEQ001", "guest")
        
        # Deve retornar None ou erro
        self.assertIsNone(resultado)
    
    def test_proxy_limpar_cache(self):
        """Testa limpeza do cache."""
        # Popular cache
        self.proxy_cache.buscar_sequencia("SEQ001", "user1")
        self.proxy_cache.buscar_variantes("BRCA1", "user1")
        
        # Verificar cache populado
        self.assertGreater(len(self.proxy_cache.cache_sequencias), 0)
        self.assertGreater(len(self.proxy_cache.cache_variantes), 0)
        
        # Limpar cache
        self.proxy_cache.limpar_cache()
        
        # Verificar cache limpo
        self.assertEqual(len(self.proxy_cache.cache_sequencias), 0)
        self.assertEqual(len(self.proxy_cache.cache_variantes), 0)
    
    def test_proxy_estatisticas_cache(self):
        """Testa estatísticas do cache proxy."""
        # Realizar algumas operações
        self.proxy_cache.buscar_sequencia("SEQ001", "user1")
        self.proxy_cache.buscar_sequencia("SEQ001", "user1")  # Cache hit
        self.proxy_cache.buscar_variantes("BRCA1", "user1")
        
        stats = self.proxy_cache.obter_estatisticas()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('cache_sequencias', stats)
        self.assertIn('cache_variantes', stats)
        self.assertIn('hit_rate', stats)
    
    def test_proxy_transparencia_interface(self):
        """Testa transparência da interface do proxy."""
        # Proxy deve ser transparente para o cliente
        self.assertIsInstance(self.proxy_cache, BancoDadosGeneticosInterface)
        self.assertIsInstance(self.proxy_seguranca, BancoDadosGeneticosInterface)
        
        # Deve ter os mesmos métodos
        self.assertTrue(hasattr(self.proxy_cache, 'buscar_sequencia'))
        self.assertTrue(hasattr(self.proxy_cache, 'buscar_variantes'))
        self.assertTrue(hasattr(self.proxy_seguranca, 'buscar_sequencia'))
        self.assertTrue(hasattr(self.proxy_seguranca, 'buscar_variantes'))
    
    def test_proxy_composicao(self):
        """Testa composição de proxies."""
        # Proxy aninhado: Segurança -> Cache -> Banco Real
        proxy_composto = SegurancaProxy(CacheProxy(self.banco_real))
        
        resultado = proxy_composto.buscar_sequencia("SEQ001", "admin")
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['id'], "SEQ001")
    
    def test_proxy_performance_benefits(self):
        """Testa benefícios de performance do proxy."""
        import time
        
        # Medir tempo sem cache
        start_time = time.time()
        for i in range(10):
            self.banco_real.buscar_sequencia("SEQ001", "user1")
        tempo_sem_cache = time.time() - start_time
        
        # Medir tempo com cache
        start_time = time.time()
        for i in range(10):
            self.proxy_cache.buscar_sequencia("SEQ001", "user1")
        tempo_com_cache = time.time() - start_time
        
        # Cache deve ser mais rápido
        self.assertLess(tempo_com_cache, tempo_sem_cache)
    
    def test_proxy_acesso_controlado(self):
        """Testa controle de acesso via proxy."""
        # Usuário não autorizado não deve acessar
        resultado_nao_autorizado = self.proxy_seguranca.buscar_sequencia("SEQ001", "guest")
        self.assertIsNone(resultado_nao_autorizado)
        
        # Usuário autorizado deve acessar
        resultado_autorizado = self.proxy_seguranca.buscar_sequencia("SEQ001", "admin")
        self.assertIsNotNone(resultado_autorizado)
    
    def test_proxy_lazy_loading(self):
        """Testa lazy loading via proxy."""
        # Banco real só deve ser acessado quando necessário
        with patch.object(self.banco_real, 'buscar_sequencia') as mock_buscar:
            mock_buscar.return_value = {"id": "SEQ001", "sequencia": "ATCG"}
            
            # Primeira chamada deve acessar o banco real
            resultado1 = self.proxy_cache.buscar_sequencia("SEQ001", "user1")
            mock_buscar.assert_called_once()
            
            # Segunda chamada não deve acessar o banco real (cache)
            resultado2 = self.proxy_cache.buscar_sequencia("SEQ001", "user1")
            mock_buscar.assert_called_once()  # Ainda apenas uma chamada
    
    def test_proxy_logging(self):
        """Testa logging via proxy."""
        with patch('builtins.print') as mock_print:
            self.proxy_seguranca.buscar_sequencia("SEQ001", "admin")
            
            # Deve ter gerado logs
            mock_print.assert_called()
            calls = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("Verificando permissões" in call for call in calls))
    
    def test_proxy_benefits(self):
        """Testa benefícios do padrão Proxy."""
        # 1. Controle de acesso
        self.assertIsInstance(self.proxy_seguranca, BancoDadosGeneticosInterface)
        resultado_autorizado = self.proxy_seguranca.buscar_sequencia("SEQ001", "admin")
        resultado_nao_autorizado = self.proxy_seguranca.buscar_sequencia("SEQ001", "guest")
        self.assertIsNotNone(resultado_autorizado)
        self.assertIsNone(resultado_nao_autorizado)
        
        # 2. Cache
        self.assertIsInstance(self.proxy_cache, BancoDadosGeneticosInterface)
        self.proxy_cache.buscar_sequencia("SEQ001", "user1")
        self.assertIn("SEQ001", self.proxy_cache.cache_sequencias)
        
        # 3. Transparência
        self.assertTrue(hasattr(self.proxy_cache, 'buscar_sequencia'))
        self.assertTrue(hasattr(self.proxy_seguranca, 'buscar_sequencia'))
        
        # 4. Composição
        proxy_composto = SegurancaProxy(CacheProxy(self.banco_real))
        self.assertIsInstance(proxy_composto, BancoDadosGeneticosInterface)


if __name__ == '__main__':
    unittest.main()
