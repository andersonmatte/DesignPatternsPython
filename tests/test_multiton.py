import unittest
import sys
import os
import threading
import time

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.criacionais.multiton import (
    MultitonFactory, AnalisadorRapido, AnalisadorPreciso, AnalisadorEspecializado
)


class TestMultiton(unittest.TestCase):
    """Testes para o padrão Multiton."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        MultitonFactory.limpar_instancias()
    
    def test_criar_analisador_rapido(self):
        """Testa criação de analisador rápido."""
        analisador = MultitonFactory.get_instancia("rapido", "config_padrao")
        self.assertIsInstance(analisador, AnalisadorRapido)
    
    def test_criar_analisador_preciso(self):
        """Testa criação de analisador preciso."""
        analisador = MultitonFactory.get_instancia("preciso", "config_alta")
        self.assertIsInstance(analisador, AnalisadorPreciso)
    
    def test_criar_analisador_especializado(self):
        """Testa criação de analisador especializado."""
        analisador = MultitonFactory.get_instancia("especializado", "config_custom")
        self.assertIsInstance(analisador, AnalisadorEspecializado)
    
    def test_mesma_instancia_mesma_chave(self):
        """Testa se mesma chave retorna mesma instância."""
        analisador1 = MultitonFactory.get_instancia("rapido", "config_teste")
        analisador2 = MultitonFactory.get_instancia("rapido", "config_teste")
        
        self.assertIs(analisador1, analisador2)
    
    def test_instancias_diferentes_chaves_diferentes(self):
        """Testa se chaves diferentes retornam instâncias diferentes."""
        analisador1 = MultitonFactory.get_instancia("rapido", "config1")
        analisador2 = MultitonFactory.get_instancia("rapido", "config2")
        
        self.assertIsNot(analisador1, analisador2)
        self.assertEqual(type(analisador1), type(analisador2))
    
    def test_tipos_diferentes_chaves_diferentes(self):
        """Testa se tipos diferentes com mesma chave retornam instâncias diferentes."""
        analisador1 = MultitonFactory.get_instancia("rapido", "config_teste")
        analisador2 = MultitonFactory.get_instancia("preciso", "config_teste")
        
        self.assertIsNot(analisador1, analisador2)
    
    def test_thread_safety(self):
        """Testa se o multiton é thread-safe."""
        instancias = []
        
        def criar_instancia():
            instancias.append(MultitonFactory.get_instancia("rapido", "thread_test"))
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=criar_instancia)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verifica se todas as instâncias são a mesma
        primeira = instancias[0]
        for instancia in instancias[1:]:
            self.assertIs(instancia, primeira)
    
    def test_funcionalidade_analisador_rapido(self):
        """Testa funcionalidade do analisador rápido."""
        analisador = MultitonFactory.get_instancia("rapido", "test")
        resultado = analisador.analisar("ATCGATCG")
        
        self.assertEqual(resultado["tipo"], "rapido")
        self.assertEqual(resultado["sequencia"], "ATCGATCG")
        self.assertIn("tempo_execucao", resultado)
        self.assertIn("precisao", resultado)
        self.assertLess(resultado["tempo_execucao"], 1.0)  # Rápido
    
    def test_funcionalidade_analisador_preciso(self):
        """Testa funcionalidade do analisador preciso."""
        analisador = MultitonFactory.get_instancia("preciso", "test")
        resultado = analisador.analisar("ATCGATCG")
        
        self.assertEqual(resultado["tipo"], "preciso")
        self.assertEqual(resultado["sequencia"], "ATCGATCG")
        self.assertIn("tempo_execucao", resultado)
        self.assertIn("precisao", resultado)
        self.assertGreater(resultado["precisao"], 0.9)  # Alta precisão
    
    def test_funcionalidade_analisador_especializado(self):
        """Testa funcionalidade do analisador especializado."""
        analisador = MultitonFactory.get_instancia("especializado", "test")
        resultado = analisador.analisar("ATCGATCG", "genetica")
        
        self.assertEqual(resultado["tipo"], "especializado")
        self.assertEqual(resultado["sequencia"], "ATCGATCG")
        self.assertEqual(resultado["especialidade"], "genetica")
        self.assertIn("analise_detalhada", resultado)
    
    def test_tipo_invalido(self):
        """Testa criação com tipo inválido."""
        with self.assertRaises(ValueError):
            MultitonFactory.get_instancia("invalido", "config")
    
    def test_listar_instancias(self):
        """Testa listagem de instâncias."""
        # Criar algumas instâncias
        MultitonFactory.get_instancia("rapido", "config1")
        MultitonFactory.get_instancia("rapido", "config2")
        MultitonFactory.get_instancia("preciso", "config1")
        
        instancias = MultitonFactory.listar_instancias()
        
        self.assertEqual(len(instancias), 3)
        self.assertIn("rapido:config1", instancias)
        self.assertIn("rapido:config2", instancias)
        self.assertIn("preciso:config1", instancias)
    
    def test_remover_instancia(self):
        """Testa remoção de instância."""
        # Criar instância
        analisador = MultitonFactory.get_instancia("rapido", "remover_test")
        
        # Verificar que existe
        instancias_antes = MultitonFactory.listar_instancias()
        self.assertIn("rapido:remover_test", instancias_antes)
        
        # Remover
        resultado = MultitonFactory.remover_instancia("rapido", "remover_test")
        self.assertTrue(resultado)
        
        # Verificar que foi removida
        instancias_depois = MultitonFactory.listar_instancias()
        self.assertNotIn("rapido:remover_test", instancias_depois)
    
    def test_remover_instancia_inexistente(self):
        """Testa remoção de instância inexistente."""
        resultado = MultitonFactory.remover_instancia("rapido", "inexistente")
        self.assertFalse(resultado)
    
    def test_limpar_instancias(self):
        """Testa limpeza de todas as instâncias."""
        # Criar algumas instâncias
        MultitonFactory.get_instancia("rapido", "config1")
        MultitonFactory.get_instancia("preciso", "config1")
        
        # Verificar que existem
        instancias_antes = MultitonFactory.listar_instancias()
        self.assertGreater(len(instancias_antes), 0)
        
        # Limpar
        MultitonFactory.limpar_instancias()
        
        # Verificar que foram removidas
        instancias_depois = MultitonFactory.listar_instancias()
        self.assertEqual(len(instancias_depois), 0)
    
    def test_estatisticas(self):
        """Testa estatísticas do multiton."""
        # Criar algumas instâncias
        MultitonFactory.get_instancia("rapido", "config1")
        MultitonFactory.get_instancia("rapido", "config2")
        MultitonFactory.get_instancia("preciso", "config1")
        MultitonFactory.get_instancia("especializado", "config1")
        
        # Recriar uma instância existente
        MultitonFactory.get_instancia("rapido", "config1")
        
        stats = MultitonFactory.obter_estatisticas()
        
        self.assertEqual(stats["total_instancias"], 4)
        self.assertEqual(stats["por_tipo"]["rapido"], 2)
        self.assertEqual(stats["por_tipo"]["preciso"], 1)
        self.assertEqual(stats["por_tipo"]["especializado"], 1)
        self.assertGreater(stats["reusos"], 0)
    
    def test_configuracoes_diferentes_mesmo_tipo(self):
        """Testa configurações diferentes no mesmo tipo."""
        rapido1 = MultitonFactory.get_instancia("rapido", "config_normal")
        rapido2 = MultitonFactory.get_instancia("rapido", "config_turbo")
        
        self.assertIsNot(rapido1, rapido2)
        
        resultado1 = rapido1.analisar("ATCG")
        resultado2 = rapido2.analisar("ATCG")
        
        # Devem ter resultados diferentes devido a configurações diferentes
        self.assertNotEqual(resultado1["configuracao"], resultado2["configuracao"])
    
    def test_analise_com_parametros(self):
        """Testa análise com parâmetros adicionais."""
        analisador = MultitonFactory.get_instancia("especializado", "param_test")
        
        resultado1 = analisador.analisar("ATCG", "genetica")
        resultado2 = analisador.analisar("ATCG", "proteomica")
        
        self.assertEqual(resultado1["especialidade"], "genetica")
        self.assertEqual(resultado2["especialidade"], "proteomica")
        self.assertNotEqual(resultado1["analise_detalhada"], resultado2["analise_detalhada"])
    
    def test_performance_reuso(self):
        """Testa performance de reuso de instâncias."""
        import time
        
        # Medir tempo de criação de nova instância
        inicio = time.time()
        analisador1 = MultitonFactory.get_instancia("preciso", "perf_test")
        tempo_criacao = time.time() - inicio
        
        # Medir tempo de reuso
        inicio = time.time()
        analisador2 = MultitonFactory.get_instancia("preciso", "perf_test")
        tempo_reuso = time.time() - inicio
        
        # Reuso deve ser mais rápido
        self.assertLess(tempo_reuso, tempo_criacao)
        self.assertIs(analisador1, analisador2)


if __name__ == "__main__":
    unittest.main()
