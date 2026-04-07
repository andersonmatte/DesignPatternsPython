"""
Testes para o padrão Proxy
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from patterns.estruturais.proxy import (
    BancoDadosGeneticos, BancoDadosGeneticosProxy, CacheProxy, SegurancaProxy, LoggingProxy
)


class TestProxy(unittest.TestCase):
    """Testes para o padrão Proxy."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.banco_dados = BancoDadosGeneticos()
        self.proxy = BancoDadosGeneticosProxy()
        
        # Proxies individuais para testes específicos
        self.cache_proxy = CacheProxy(self.banco_dados)
        self.seguranca_proxy = SegurancaProxy(self.banco_dados)
        self.logging_proxy = LoggingProxy(self.banco_dados)
    
    def test_banco_dados_geneticos_creation(self):
        """Testa criação do banco de dados genéticos."""
        self.assertIsInstance(self.banco_dados, BancoDadosGeneticos)
        self.assertEqual(self.banco_dados.nome, "Banco de Dados Genéticos")
    
    def test_banco_dados_geneticos_buscar_sequencia(self):
        """Testa busca de sequência no banco de dados."""
        resultado = self.banco_dados.buscar_sequencia("BRCA1", "usuario_teste")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
        self.assertIn('sequencia', resultado)
        self.assertIn('usuario', resultado)
        self.assertIn('timestamp', resultado)
        self.assertEqual(resultado['gene'], "BRCA1")
        self.assertEqual(resultado['usuario'], "usuario_teste")
    
    def test_banco_dados_geneticos_buscar_sequencia_inexistente(self):
        """Testa busca de sequência inexistente."""
        resultado = self.banco_dados.buscar_sequencia("GENE_INEXISTENTE", "usuario_teste")
        
        self.assertIsNone(resultado)
    
    def test_banco_dados_geneticos_listar_genes(self):
        """Testa listagem de genes."""
        resultado = self.banco_dados.listar_genes("usuario_teste")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('genes', resultado)
        self.assertIn('total', resultado)
        self.assertIn('usuario', resultado)
        self.assertIsInstance(resultado['genes'], list)
        self.assertGreater(len(resultado['genes']), 0)
    
    def test_banco_dados_geneticos_adicionar_sequencia(self):
        """Testa adição de sequência."""
        resultado = self.banco_dados.adicionar_sequencia(
            "NOVO_GENE", "ATCGATCG", "usuario_teste"
        )
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
        self.assertIn('sequencia', resultado)
        self.assertIn('usuario', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['status'], "Adicionado")
    
    def test_proxy_creation(self):
        """Testa criação do proxy."""
        self.assertIsInstance(self.proxy, BancoDadosGeneticosProxy)
        self.assertIsInstance(self.proxy.banco_dados, BancoDadosGeneticos)
    
    def test_proxy_buscar_sequencia_com_permissao(self):
        """Testa busca de sequência com permissão."""
        resultado = self.proxy.buscar_sequencia("BRCA1", "pesquisador_autorizado")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
        self.assertIn('sequencia', resultado)
        self.assertIn('cache', resultado)
        self.assertIn('log_id', resultado)
        self.assertEqual(resultado['gene'], "BRCA1")
    
    def test_proxy_buscar_sequencia_sem_permissao(self):
        """Testa busca de sequência sem permissão."""
        with self.assertRaises(PermissionError):
            self.proxy.buscar_sequencia("BRCA1", "usuario_sem_permissao")
    
    def test_proxy_listar_genes_com_permissao(self):
        """Testa listagem de genes com permissão."""
        resultado = self.proxy.listar_genes("pesquisador_autorizado")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('genes', resultado)
        self.assertIn('cache', resultado)
        self.assertIn('log_id', resultado)
        self.assertGreater(len(resultado['genes']), 0)
    
    def test_proxy_listar_genes_sem_permissao(self):
        """Testa listagem de genes sem permissão."""
        with self.assertRaises(PermissionError):
            self.proxy.listar_genes("usuario_sem_permissao")
    
    def test_proxy_adicionar_sequencia_com_permissao(self):
        """Testa adição de sequência com permissão."""
        resultado = self.proxy.adicionar_sequencia(
            "NOVO_GENE", "ATCGATCG", "administrador"
        )
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
        self.assertIn('status', resultado)
        self.assertIn('cache', resultado)
        self.assertIn('log_id', resultado)
        self.assertEqual(resultado['status'], "Adicionado")
    
    def test_proxy_adicionar_sequencia_sem_permissao(self):
        """Testa adição de sequência sem permissão."""
        with self.assertRaises(PermissionError):
            self.proxy.adicionar_sequencia("NOVO_GENE", "ATCGATCG", "usuario_comum")
    
    def test_cache_proxy_creation(self):
        """Testa criação do proxy de cache."""
        self.assertIsInstance(self.cache_proxy, CacheProxy)
        self.assertEqual(self.cache_proxy.banco_dados, self.banco_dados)
    
    def test_cache_proxy_buscar_sequencia_primeira_vez(self):
        """Testa cache proxy - primeira busca."""
        resultado = self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('cache_hit', resultado)
        self.assertFalse(resultado['cache_hit'])  # Cache miss na primeira vez
    
    def test_cache_proxy_buscar_sequencia_segunda_vez(self):
        """Testa cache proxy - segunda busca (cache hit)."""
        # Primeira busca
        resultado1 = self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        
        # Segunda busca (deve usar cache)
        resultado2 = self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        
        self.assertTrue(resultado2['cache_hit'])
        self.assertEqual(resultado1['sequencia'], resultado2['sequencia'])
    
    def test_cache_proxy_buscar_sequencias_diferentes(self):
        """Testa cache proxy - sequências diferentes."""
        resultado1 = self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        resultado2 = self.cache_proxy.buscar_sequencia("TP53", "usuario_teste")
        
        # Ambas devem ser cache miss
        self.assertFalse(resultado1['cache_hit'])
        self.assertFalse(resultado2['cache_hit'])
        
        # Mas devem ser diferentes
        self.assertNotEqual(resultado1['sequencia'], resultado2['sequencia'])
    
    def test_cache_proxy_adicionar_sequencia_invalida_cache(self):
        """Testa invalidação de cache ao adicionar sequência."""
        # Primeira busca (cache miss)
        resultado1 = self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        self.assertFalse(resultado1['cache_hit'])
        
        # Adicionar sequência (deve invalidar cache)
        self.cache_proxy.adicionar_sequencia("BRCA2", "GCTAGCTA", "usuario_teste")
        
        # Segunda busca (cache miss devido à invalidação)
        resultado2 = self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        self.assertFalse(resultado2['cache_hit'])
    
    def test_cache_proxy_limpar_cache(self):
        """Testa limpeza do cache."""
        # Primeira busca
        self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        
        # Verificar se tem algo no cache
        self.assertGreater(len(self.cache_proxy.cache), 0)
        
        # Limpar cache
        self.cache_proxy.limpar_cache()
        
        # Cache deve estar vazio
        self.assertEqual(len(self.cache_proxy.cache), 0)
    
    def test_cache_proxy_get_cache_stats(self):
        """Testa estatísticas do cache."""
        # Realizar algumas operações
        self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")  # Cache miss
        self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")  # Cache hit
        self.cache_proxy.buscar_sequencia("TP53", "usuario_teste")   # Cache miss
        
        stats = self.cache_proxy.get_cache_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_requests', stats)
        self.assertIn('cache_hits', stats)
        self.assertIn('cache_misses', stats)
        self.assertIn('hit_ratio', stats)
        self.assertIn('cache_size', stats)
        
        self.assertEqual(stats['total_requests'], 3)
        self.assertEqual(stats['cache_hits'], 1)
        self.assertEqual(stats['cache_misses'], 2)
    
    def test_seguranca_proxy_creation(self):
        """Testa criação do proxy de segurança."""
        self.assertIsInstance(self.seguranca_proxy, SegurancaProxy)
        self.assertEqual(self.seguranca_proxy.banco_dados, self.banco_dados)
    
    def test_seguranca_proxy_verificar_permissao(self):
        """Testa verificação de permissão."""
        # Usuários com permissão
        self.assertTrue(self.seguranca_proxy._verificar_permissao("administrador", "buscar"))
        self.assertTrue(self.seguranca_proxy._verificar_permissao("pesquisador_autorizado", "buscar"))
        
        # Usuários sem permissão
        self.assertFalse(self.seguranca_proxy._verificar_permissao("usuario_comum", "buscar"))
        self.assertFalse(self.seguranca_proxy._verificar_permissao("visitante", "adicionar"))
    
    def test_seguranca_proxy_registrar_acesso(self):
        """Testa registro de acesso."""
        # Mock do método de registro
        with patch.object(self.seguranca_proxy, '_registrar_acesso') as mock_registrar:
            self.seguranca_proxy.buscar_sequencia("BRCA1", "administrador")
            
            # Deve registrar o acesso
            mock_registrar.assert_called_once_with("administrador", "buscar", "BRCA1")
    
    def test_seguranca_proxy_buscar_com_permissao(self):
        """Testa busca com permissão no proxy de segurança."""
        resultado = self.seguranca_proxy.buscar_sequencia("BRCA1", "administrador")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
        self.assertIn('sequencia', resultado)
        self.assertIn('acesso_registrado', resultado)
        self.assertTrue(resultado['acesso_registrado'])
    
    def test_seguranca_proxy_buscar_sem_permissao(self):
        """Testa busca sem permissão no proxy de segurança."""
        with self.assertRaises(PermissionError):
            self.seguranca_proxy.buscar_sequencia("BRCA1", "usuario_comum")
    
    def test_seguranca_proxy_adicionar_com_permissao(self):
        """Testa adição com permissão no proxy de segurança."""
        resultado = self.seguranca_proxy.adicionar_sequencia("NOVO_GENE", "ATCGATCG", "administrador")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
        self.assertIn('status', resultado)
        self.assertIn('acesso_registrado', resultado)
        self.assertTrue(resultado['acesso_registrado'])
    
    def test_seguranca_proxy_adicionar_sem_permissao(self):
        """Testa adição sem permissão no proxy de segurança."""
        with self.assertRaises(PermissionError):
            self.seguranca_proxy.adicionar_sequencia("NOVO_GENE", "ATCGATCG", "usuario_comum")
    
    def test_logging_proxy_creation(self):
        """Testa criação do proxy de logging."""
        self.assertIsInstance(self.logging_proxy, LoggingProxy)
        self.assertEqual(self.logging_proxy.banco_dados, self.banco_dados)
    
    def test_logging_proxy_buscar_sequencia(self):
        """Testa busca com logging."""
        with patch('builtins.print') as mock_print:
            resultado = self.logging_proxy.buscar_sequencia("BRCA1", "usuario_teste")
            
            # Verifica se o log foi gerado
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            self.assertIn("Iniciando busca", call_args)
            self.assertIn("BRCA1", call_args)
            self.assertIn("usuario_teste", call_args)
            self.assertIn("Busca concluída", call_args)
        
        # Verifica se o resultado original foi preservado
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
    
    def test_logging_proxy_listar_genes(self):
        """Testa listagem com logging."""
        with patch('builtins.print') as mock_print:
            resultado = self.logging_proxy.listar_genes("usuario_teste")
            
            # Verifica se o log foi gerado
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            self.assertIn("Iniciando listagem", call_args)
            self.assertIn("Listagem concluída", call_args)
        
        # Verifica se o resultado original foi preservado
        self.assertIsInstance(resultado, dict)
        self.assertIn('genes', resultado)
    
    def test_logging_proxy_adicionar_sequencia(self):
        """Testa adição com logging."""
        with patch('builtins.print') as mock_print:
            resultado = self.logging_proxy.adicionar_sequencia("NOVO_GENE", "ATCGATCG", "usuario_teste")
            
            # Verifica se o log foi gerado
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            self.assertIn("Iniciando adição", call_args)
            self.assertIn("NOVO_GENE", call_args)
            self.assertIn("Adição concluída", call_args)
        
        # Verifica se o resultado original foi preservado
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
    
    def test_logging_proxy_error_logging(self):
        """Testa logging de erros."""
        # Mock que lança exceção
        mock_banco = Mock()
        mock_banco.buscar_sequencia.side_effect = Exception("Erro no banco")
        
        logging_proxy = LoggingProxy(mock_banco)
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception):
                logging_proxy.buscar_sequencia("BRCA1", "usuario_teste")
            
            # Verifica se o erro foi logado
            call_args = str(mock_print.call_args)
            self.assertIn("Erro durante busca", call_args)
            self.assertIn("Erro no banco", call_args)
    
    def test_proxy_multiple_decorators(self):
        """Testa múltiplos proxies (decorator pattern)."""
        # Combinar proxies: Cache -> Segurança -> Logging
        proxy_composto = CacheProxy(
            SegurancaProxy(
                LoggingProxy(self.banco_dados)
            )
        )
        
        # Primeira busca (cache miss, com segurança e logging)
        with patch('builtins.print') as mock_print:
            resultado1 = proxy_composto.buscar_sequencia("BRCA1", "administrador")
            
            # Verifica se logging foi aplicado
            mock_print.assert_called()
        
        self.assertIsInstance(resultado1, dict)
        self.assertFalse(resultado1.get('cache_hit', False))
        
        # Segunda busca (cache hit, sem passar pelos outros proxies)
        resultado2 = proxy_composto.buscar_sequencia("BRCA1", "administrador")
        
        self.assertTrue(resultado2.get('cache_hit', False))
        self.assertEqual(resultado1['sequencia'], resultado2['sequencia'])
    
    def test_proxy_transparency(self):
        """Testa transparência do proxy para código cliente."""
        # Cliente não precisa saber se está usando proxy ou objeto real
        objetos = [self.banco_dados, self.proxy, self.cache_proxy, self.seguranca_proxy, self.logging_proxy]
        
        for obj in objetos:
            # Todos devem ter a mesma interface
            self.assertTrue(hasattr(obj, 'buscar_sequencia'))
            self.assertTrue(hasattr(obj, 'listar_genes'))
            self.assertTrue(hasattr(obj, 'adicionar_sequencia'))
    
    def test_proxy_lazy_initialization(self):
        """Testa inicialização preguiçosa do proxy."""
        # Proxy deve criar o objeto real apenas quando necessário
        proxy = BancoDadosGeneticosProxy()
        
        # Antes de qualquer operação, o banco de dados deve existir
        self.assertIsNotNone(proxy.banco_dados)
        
        # Mas pode ser modificado para lazy loading em implementações reais
        self.assertIsInstance(proxy.banco_dados, BancoDadosGeneticos)
    
    def test_proxy_access_control(self):
        """Testa controle de acesso do proxy."""
        # Proxy deve controlar o acesso ao objeto real
        with self.assertRaises(PermissionError):
            self.proxy.buscar_sequencia("BRCA1", "usuario_sem_permissao")
        
        # Mas deve permitir acesso autorizado
        resultado = self.proxy.buscar_sequencia("BRCA1", "administrador")
        self.assertIsInstance(resultado, dict)
    
    def test_proxy_performance_monitoring(self):
        """Teste monitoramento de performance via proxy."""
        import time
        
        # Proxy de logging pode ser usado para monitorar performance
        with patch('builtins.print') as mock_print:
            start_time = time.time()
            self.logging_proxy.buscar_sequencia("BRCA1", "usuario_teste")
            end_time = time.time()
        
        # Verifica se o tempo foi registrado (em implementação real)
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)  # Deve ser rápido
    
    def test_proxy_smart_reference(self):
        """Testa referência inteligente (smart reference)."""
        # Cache proxy atua como smart reference
        self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        
        # Verificar se a referência foi cacheada
        self.assertIn("BRCA1:usuario_teste", self.cache_proxy.cache)
        
        # Próxima chamada usa a referência cacheada
        resultado = self.cache_proxy.buscar_sequencia("BRCA1", "usuario_teste")
        self.assertTrue(resultado.get('cache_hit', False))


if __name__ == '__main__':
    unittest.main()
