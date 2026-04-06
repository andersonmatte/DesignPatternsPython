import unittest
import sys
import os
import threading
import time

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.criacionais.singleton import (
    GerenciadorRecursos, BancoDadosSequencias
)


class TestSingleton(unittest.TestCase):
    """Testes para o padrão Singleton."""
    
    def test_unicidade_gerenciador_recursos(self):
        """Testa se apenas uma instância do GerenciadorRecursos é criada."""
        gerenciador1 = GerenciadorRecursos.get_instancia()
        gerenciador2 = GerenciadorRecursos.get_instancia()
        gerenciador3 = GerenciadorRecursos()
        
        self.assertIs(gerenciador1, gerenciador2)
        self.assertIs(gerenciador1, gerenciador3)
    
    def test_unicidade_banco_dados(self):
        """Testa se apenas uma instância do BancoDadosSequencias é criada."""
        banco1 = BancoDadosSequencias.get_instancia()
        banco2 = BancoDadosSequencias.get_instancia()
        banco3 = BancoDadosSequencias()
        
        self.assertIs(banco1, banco2)
        self.assertIs(banco1, banco3)
    
    def test_thread_safety(self):
        """Testa se o singleton é thread-safe."""
        instancias = []
        
        def criar_instancia():
            instancias.append(GerenciadorRecursos.get_instancia())
        
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
    
    def test_funcionalidade_gerenciador(self):
        """Testa funcionalidade básica do GerenciadorRecursos."""
        gerenciador = GerenciadorRecursos.get_instancia()
        
        # Adicionar recurso
        gerenciador.adicionar_recurso("test_recurso", "teste")
        
        # Obter recurso
        recurso = gerenciador.obter_recurso("test_recurso", "test_user")
        self.assertEqual(recurso, "teste")
        
        # Liberar recurso
        gerenciador.liberar_recurso("test_recurso")
        
        # Verificar estatísticas
        stats = gerenciador.obter_estatisticas()
        self.assertIn("total_acessos", stats)
    
    def test_funcionalidade_banco_dados(self):
        """Testa funcionalidade básica do BancoDadosSequencias."""
        banco = BancoDadosSequencias.get_instancia()
        
        # Adicionar sequência
        banco.adicionar_sequencia("test_seq", "ATCGATCG", especie="teste")
        
        # Buscar sequência
        sequencia = banco.buscar_sequencia("test_seq")
        self.assertEqual(sequencia, "ATCGATCG")
        
        # Buscar por padrão
        resultados = banco.buscar_sequencia_por_padrao("ATCG")
        self.assertIn("test_seq", resultados)
        
        # Verificar estatísticas
        stats = banco.obter_estatisticas()
        self.assertEqual(stats["total_sequencias"], 1)


if __name__ == "__main__":
    unittest.main()
