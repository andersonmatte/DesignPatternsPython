import unittest
import sys
import os
import threading
import time

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.criacionais.object_pool import (
    ObjectPool, EquipamentoPool, CentrifugaPool, PoolManager
)


class TestObjectPool(unittest.TestCase):
    """Testes para o padrão Object Pool."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.pool = EquipamentoPool(3)  # Pool com capacidade para 3 equipamentos
        self.centrifuga_pool = CentrifugaPool(2)
        self.manager = PoolManager()
    
    def test_criar_pool_com_capacidade(self):
        """Testa criação de pool com capacidade definida."""
        self.assertEqual(self.pool.max_size, 3)
        self.assertEqual(self.pool.current_size, 0)
    
    def test_adquirir_equipamento_disponivel(self):
        """Testa aquisição de equipamento disponível."""
        equipamento = self.pool.adquirir_equipamento("Microscopio")
        
        self.assertIsNotNone(equipamento)
        self.assertEqual(equipamento.tipo, "Microscopio")
        self.assertEqual(equipamento.em_uso, True)
        self.assertEqual(self.pool.current_size, 1)
    
    def test_adquirir_equipamento_pool_cheio(self):
        """Testa aquisição quando pool está cheio."""
        # Preencher o pool
        for i in range(3):
            self.pool.adquirir_equipamento("Equipamento")
        
        # Tentar adquirir mais um
        equipamento = self.pool.adquirir_equipamento("Extra")
        self.assertIsNone(equipamento)
    
    def test_liberar_equipamento(self):
        """Testa liberação de equipamento."""
        equipamento = self.pool.adquirir_equipamento("Microscopio")
        self.assertEqual(self.pool.current_size, 1)
        
        resultado = self.pool.liberar_equipamento(equipamento)
        self.assertTrue(resultado)
        self.assertEqual(equipamento.em_uso, False)
        self.assertEqual(self.pool.current_size, 0)
    
    def test_liberar_equipamento_nao_pertencente(self):
        """Testa liberação de equipamento que não pertence ao pool."""
        equipamento = self.pool.adquirir_equipamento("Teste")
        self.pool.liberar_equipamento(equipamento)
        
        # Tentar liberar novamente
        resultado = self.pool.liberar_equipamento(equipamento)
        self.assertFalse(resultado)
    
    def test_pool_status(self):
        """Testa status do pool."""
        status = self.pool.obter_status()
        
        self.assertEqual(status["max_size"], 3)
        self.assertEqual(status["current_size"], 0)
        self.assertEqual(status["disponiveis"], 3)
        
        # Adquirir um equipamento
        self.pool.adquirir_equipamento("Teste")
        status = self.pool.obter_status()
        
        self.assertEqual(status["current_size"], 1)
        self.assertEqual(status["disponiveis"], 2)
    
    def test_centrifuga_pool(self):
        """Testa pool específico de centrífugas."""
        centrifuga = self.centrifuga_pool.adquirir_centrifuga()
        
        self.assertIsNotNone(centrifuga)
        self.assertEqual(centrifuga.modelo, "Centrífuga Padrão")
        self.assertEqual(centrifuga.velocidade_max, 15000)
        self.assertEqual(centrifuga.em_uso, True)
        
        # Testar método específico
        resultado = centrifuga.centrifugar("amostra", 10000)
        self.assertIn("Centrífuga Padrão", resultado)
        self.assertIn("10000 RPM", resultado)
        
        # Liberar
        self.centrifuga_pool.liberar_centrifuga(centrifuga)
        self.assertEqual(centrifuga.em_uso, False)
    
    def test_pool_manager(self):
        """Testa gerenciador de pools."""
        # Criar pools via manager
        pool_microscopios = self.manager.criar_pool("microscopios", 2)
        pool_espectrofotometros = self.manager.criar_pool("espectrofotometros", 3)
        
        self.assertIsNotNone(pool_microscopios)
        self.assertIsNotNone(pool_espectrofotometros)
        
        # Verificar que pools foram registrados
        pools = self.manager.listar_pools()
        self.assertIn("microscopios", pools)
        self.assertIn("espectrofotometros", pools)
        
        # Obter pool existente
        pool_mesmo = self.manager.obter_pool("microscopios")
        self.assertIs(pool_microscopios, pool_mesmo)
    
    def test_pool_manager_remover_pool(self):
        """Testa remoção de pool via manager."""
        pool_teste = self.manager.criar_pool("teste", 2)
        
        # Verificar que existe
        self.assertIsNotNone(self.manager.obter_pool("teste"))
        
        # Remover
        resultado = self.manager.remover_pool("teste")
        self.assertTrue(resultado)
        
        # Verificar que não existe mais
        self.assertIsNone(self.manager.obter_pool("teste"))
    
    def test_thread_safety(self):
        """Testa se o pool é thread-safe."""
        resultados = []
        erros = []
        
        def adquirir_e_liberar():
            try:
                equipamento = self.pool.adquirir_equipamento("ThreadTest")
                if equipamento:
                    time.sleep(0.1)  # Simula uso
                    self.pool.liberar_equipamento(equipamento)
                    resultados.append(True)
                else:
                    resultados.append(False)
            except Exception as e:
                erros.append(e)
        
        # Criar múltiplas threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=adquirir_e_liberar)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verificar que não houve erros
        self.assertEqual(len(erros), 0)
        self.assertEqual(len(resultados), 10)
        
        # Pool deve estar vazio no final
        self.assertEqual(self.pool.current_size, 0)
    
    def test_reutilizacao_equipamentos(self):
        """Testa reutilização de equipamentos."""
        equipamento1 = self.pool.adquirir_equipamento("Teste")
        id1 = id(equipamento1)
        self.pool.liberar_equipamento(equipamento1)
        
        equipamento2 = self.pool.adquirir_equipamento("Teste")
        id2 = id(equipamento2)
        
        # Deve ser o mesmo objeto reutilizado
        self.assertEqual(id1, id2)
    
    def test_limpar_pool(self):
        """Testa limpeza do pool."""
        # Adicionar alguns equipamentos
        self.pool.adquirir_equipamento("Teste1")
        self.pool.adquirir_equipamento("Teste2")
        
        self.assertEqual(self.pool.current_size, 2)
        
        # Limpar pool
        self.pool.limpar_pool()
        
        self.assertEqual(self.pool.current_size, 0)
        self.assertEqual(len(self.pool.equipamentos), 0)
    
    def test_estatisticas_pool(self):
        """Testa estatísticas do pool."""
        # Realizar algumas operações
        equip1 = self.pool.adquirir_equipamento("Teste1")
        equip2 = self.pool.adquirir_equipamento("Teste2")
        
        self.pool.liberar_equipamento(equip1)
        self.pool.liberar_equipamento(equip2)
        
        equip3 = self.pool.adquirir_equipamento("Teste3")
        self.pool.liberar_equipamento(equip3)
        
        stats = self.pool.obter_estatisticas()
        
        self.assertEqual(stats["total_adquiricoes"], 3)
        self.assertEqual(stats["total_liberacoes"], 3)
        self.assertEqual(stats["max_size"], 3)
        self.assertGreater(stats["tempo_medio_uso"], 0)
    
    def test_pool_com_diferentes_tipos(self):
        """Testa pool com diferentes tipos de equipamentos."""
        microscopio = self.pool.adquirir_equipamento("Microscopio")
        espectrofotometro = self.pool.adquirir_equipamento("Espectrofotometro")
        termociclador = self.pool.adquirir_equipamento("Termociclador")
        
        self.assertEqual(microscopio.tipo, "Microscopio")
        self.assertEqual(espectrofotometro.tipo, "Espectrofotometro")
        self.assertEqual(termociclador.tipo, "Termociclador")
        
        # Liberar em ordem diferente
        self.pool.liberar_equipamento(termociclador)
        self.pool.liberar_equipamento(microscopio)
        self.pool.liberar_equipamento(espectrofotometro)
        
        self.assertEqual(self.pool.current_size, 0)
    
    def test_timeout_adquirir(self):
        """Testa timeout na aquisição de equipamento."""
        # Preencher o pool
        for i in range(3):
            self.pool.adquirir_equipamento("Teste")
        
        # Tentar adquirir com timeout
        inicio = time.time()
        equipamento = self.pool.adquirir_equipamento("Timeout", timeout=0.1)
        fim = time.time()
        
        self.assertIsNone(equipamento)
        self.assertGreaterEqual(fim - inicio, 0.1)  # Deve esperar pelo menos o timeout
    
    def test_pool_manager_estatisticas_globais(self):
        """Testa estatísticas globais do manager."""
        # Criar alguns pools
        self.manager.criar_pool("pool1", 2)
        self.manager.criar_pool("pool2", 3)
        
        # Realizar operações
        pool1 = self.manager.obter_pool("pool1")
        pool2 = self.manager.obter_pool("pool2")
        
        pool1.adquirir_equipamento("Teste")
        pool2.adquirir_equipamento("Teste")
        
        stats = self.manager.obter_estatisticas_globais()
        
        self.assertEqual(stats["total_pools"], 2)
        self.assertEqual(stats["total_equipamentos"], 2)
        self.assertIn("pool1", stats["pools"])
        self.assertIn("pool2", stats["pools"])


if __name__ == "__main__":
    unittest.main()
