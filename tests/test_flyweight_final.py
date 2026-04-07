"""
Testes para o padrão Flyweight
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.flyweight import (
    DadoGeneticoFlyweight, SequenciaProteicaFlyweight, FabricaFlyweight
)


class TestFlyweight(unittest.TestCase):
    """Testes para o padrão Flyweight."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.fabrica = FabricaFlyweight()
    
    def test_fabrica_flyweight_creation(self):
        """Testa criação da fábrica de flyweights."""
        fabrica = FabricaFlyweight()
        
        self.assertIsInstance(fabrica, FabricaFlyweight)
        self.assertEqual(len(fabrica.flyweights), 0)
    
    def test_sequencia_proteica_flyweight_creation(self):
        """Testa criação de flyweight de sequência proteica."""
        flyweight = SequenciaProteicaFlyweight("PROT001")
        
        self.assertIsInstance(flyweight, DadoGeneticoFlyweight)
        self.assertIsInstance(flyweight, SequenciaProteicaFlyweight)
        self.assertEqual(flyweight.codigo, "PROT001")
    
    def test_sequencia_proteica_definir_sequencia(self):
        """Testa definição de sequência no flyweight."""
        flyweight = SequenciaProteicaFlyweight("PROT001")
        flyweight.definir_sequencia("ATCG")
        
        self.assertEqual(flyweight._estado_compartilhado["sequencia"], "ATCG")
        self.assertGreater(flyweight._estado_compartilhado["peso_molecular"], 0)
    
    def test_sequencia_proteica_adicionar_dominio(self):
        """Testa adição de domínio no flyweight."""
        flyweight = SequenciaProteicaFlyweight("PROT001")
        flyweight.adicionar_dominio("DNA-binding")
        flyweight.adicionar_dominio("ATP-binding")
        
        dominios = flyweight._estado_compartilhado["dominios"]
        self.assertIn("DNA-binding", dominios)
        self.assertIn("ATP-binding", dominios)
        self.assertEqual(len(dominios), 2)
    
    def test_sequencia_proteica_definir_funcao(self):
        """Testa definição de função no flyweight."""
        flyweight = SequenciaProteicaFlyweight("PROT001")
        flyweight.definir_funcao("Enzima")
        
        self.assertEqual(flyweight._estado_compartilhado["funcao"], "Enzima")
    
    def test_sequencia_proteica_exibir_dado(self):
        """Testa exibição de dado com contexto."""
        flyweight = SequenciaProteicaFlyweight("PROT001")
        flyweight.definir_sequencia("ATCGATCG")
        flyweight.definir_funcao("Transportador")
        
        contexto = {"amostra": "SAMPLE001", "condicao": "experimental"}
        resultado = flyweight.exibir_dado(contexto)
        
        self.assertIsInstance(resultado, str)
        self.assertIn("PROT001", resultado)
        self.assertIn("ATCGATCG", resultado)
        self.assertIn("Transportador", resultado)
        self.assertIn("SAMPLE001", resultado)
    
    def test_fabrica_obter_flyweight_novo(self):
        """Testa obtenção de flyweight novo (cache miss)."""
        flyweight1 = self.fabrica.obter_flyweight_proteico("PROT001")
        flyweight2 = self.fabrica.obter_flyweight_proteico("PROT002")
        
        self.assertIsInstance(flyweight1, SequenciaProteicaFlyweight)
        self.assertIsInstance(flyweight2, SequenciaProteicaFlyweight)
        self.assertEqual(len(self.fabrica.flyweights), 2)
        self.assertNotEqual(flyweight1, flyweight2)
    
    def test_fabrica_obter_flyweight_existente(self):
        """Testa obtenção de flyweight existente (cache hit)."""
        flyweight1 = self.fabrica.obter_flyweight_proteico("PROT001")
        flyweight2 = self.fabrica.obter_flyweight_proteico("PROT001")
        
        # Deve retornar a mesma instância
        self.assertIs(flyweight1, flyweight2)
        self.assertEqual(len(self.fabrica.flyweights), 1)
    
    def test_fabrica_limpar_cache(self):
        """Testa limpeza do cache da fábrica."""
        # Adicionar flyweights
        self.fabrica.obter_flyweight_proteico("PROT001")
        self.fabrica.obter_flyweight_proteico("PROT002")
        
        self.assertEqual(len(self.fabrica.flyweights), 2)
        
        # Limpar cache
        self.fabrica.limpar_cache()
        
        self.assertEqual(len(self.fabrica.flyweights), 0)
    
    def test_flyweight_compartilhamento_estado(self):
        """Testa compartilhamento de estado entre flyweights."""
        # Criar flyweight e configurar
        fw1 = self.fabrica.obter_flyweight_proteico("PROT001")
        fw1.definir_sequencia("ATCG")
        fw1.definir_funcao("Enzima")
        
        # Obter mesmo flyweight
        fw2 = self.fabrica.obter_flyweight_proteico("PROT001")
        
        # Deve ser a mesma instância
        self.assertIs(fw1, fw2)
        
        # Estado compartilhado deve ser o mesmo
        self.assertEqual(fw1._estado_compartilhado, fw2._estado_compartilhado)
        self.assertEqual(fw2._estado_compartilhado["sequencia"], "ATCG")
        self.assertEqual(fw2._estado_compartilhado["funcao"], "Enzima")
    
    def test_flyweight_contextos_diferentes(self):
        """Testa flyweight com contextos extrínsecos diferentes."""
        flyweight = self.fabrica.obter_flyweight_proteico("PROT001")
        flyweight.definir_sequencia("ATCG")
        
        contexto1 = {"amostra": "SAMPLE001", "condicao": "normal"}
        contexto2 = {"amostra": "SAMPLE002", "condicao": "experimental"}
        
        resultado1 = flyweight.exibir_dado(contexto1)
        resultado2 = flyweight.exibir_dado(contexto2)
        
        # Resultados devem ser diferentes devido aos contextos
        self.assertNotEqual(resultado1, resultado2)
        
        # Mas flyweight deve ser o mesmo
        self.assertIs(flyweight, self.fabrica.obter_flyweight_proteico("PROT001"))
    
    def test_flyweight_performance_benefits(self):
        """Testa benefícios de performance do flyweight."""
        import time
        
        # Criar muitos flyweights sem reuso
        start_time = time.time()
        flyweights_sem_reuso = []
        for i in range(100):
            fw = SequenciaProteicaFlyweight(f"PROT{i}")
            fw.definir_sequencia(f"SEQ{i % 10}")  # Apenas 10 sequências únicas
            flyweights_sem_reuso.append(fw)
        tempo_sem_reuso = time.time() - start_time
        
        # Criar muitos flyweights com reuso
        self.fabrica.limpar_cache()
        start_time = time.time()
        flyweights_com_reuso = []
        for i in range(100):
            fw = self.fabrica.obter_flyweight_proteico(f"PROT{i % 10}")
            fw.definir_sequencia(f"SEQ{i % 10}")
            flyweights_com_reuso.append(fw)
        tempo_com_reuso = time.time() - start_time
        
        # Com reuso deve ter menos flyweights únicos
        self.assertEqual(len(self.fabrica.flyweights), 10)
        
        # Performance deve ser melhor com reuso
        self.assertLess(tempo_com_reuso, tempo_sem_reuso * 1.2)
        
        # Mas número de resultados deve ser o mesmo
        self.assertEqual(len(flyweights_sem_reuso), len(flyweights_com_reuso))
    
    def test_flyweight_memoria_efficiency(self):
        """Testa eficiência de memória do flyweight."""
        # Criar muitos contextos para poucos flyweights
        flyweight = self.fabrica.obter_flyweight_proteico("PROT001")
        flyweight.definir_sequencia("ATCGATCG")
        
        resultados = []
        contextos = []
        
        # Criar 1000 contextos diferentes
        for i in range(1000):
            contexto = {"amostra": f"SAMPLE{i:03d}", "condicao": f"cond{i}"}
            contextos.append(contexto)
            resultados.append(flyweight.exibir_dado(contexto))
        
        # Apenas 1 flyweight no cache
        self.assertEqual(len(self.fabrica.flyweights), 1)
        
        # Mas 1000 resultados diferentes
        self.assertEqual(len(resultados), 1000)
        self.assertEqual(len(set(resultados)), 1000)  # Todos únicos
    
    def test_flyweight_interface_uniforme(self):
        """Testa interface uniforme entre flyweights."""
        flyweight1 = SequenciaProteicaFlyweight("PROT001")
        flyweight2 = SequenciaProteicaFlyweight("PROT002")
        
        # Ambos devem ter a mesma interface
        self.assertTrue(hasattr(flyweight1, 'definir_sequencia'))
        self.assertTrue(hasattr(flyweight1, 'adicionar_dominio'))
        self.assertTrue(hasattr(flyweight1, 'definir_funcao'))
        self.assertTrue(hasattr(flyweight1, 'exibir_dado'))
        
        self.assertTrue(hasattr(flyweight2, 'definir_sequencia'))
        self.assertTrue(hasattr(flyweight2, 'adicionar_dominio'))
        self.assertTrue(hasattr(flyweight2, 'definir_funcao'))
        self.assertTrue(hasattr(flyweight2, 'exibir_dado'))
    
    def test_flyweight_estado_intrinsic_vs_extrinsic(self):
        """Testa separação entre estado intrínseco e extrínseco."""
        flyweight = self.fabrica.obter_flyweight_proteico("PROT001")
        
        # Estado intrínseco (compartilhado)
        flyweight.definir_sequencia("ATCG")
        flyweight.definir_funcao("Enzima")
        
        estado_intrinsic = flyweight.obter_info_compartilhada()
        self.assertIsInstance(estado_intrinsic, dict)
        self.assertIn('sequencia', estado_intrinsic)
        self.assertIn('funcao', estado_intrinsic)
        
        # Estado extrínseco (contexto)
        contexto1 = {"amostra": "SAMPLE001"}
        contexto2 = {"amostra": "SAMPLE002"}
        
        resultado1 = flyweight.exibir_dado(contexto1)
        resultado2 = flyweight.exibir_dado(contexto2)
        
        # Estado intrínseco deve ser o mesmo
        self.assertEqual(flyweight.obter_info_compartilhada(), flyweight.obter_info_compartilhada())
        
        # Mas resultados devem ser diferentes devido ao contexto extrínseco
        self.assertNotEqual(resultado1, resultado2)
    
    def test_flyweight_benefits(self):
        """Testa benefícios do padrão Flyweight."""
        # 1. Redução de uso de memória
        self.fabrica.obter_flyweight_proteico("PROT001")
        self.fabrica.obter_flyweight_proteico("PROT001")  # Reuso
        
        self.assertEqual(len(self.fabrica.flyweights), 1)
        
        # 2. Compartilhamento de estado intrínseco
        fw1 = self.fabrica.obter_flyweight_proteico("PROT001")
        fw2 = self.fabrica.obter_flyweight_proteico("PROT001")
        self.assertIs(fw1, fw2)
        
        # 3. Estado extrínseco independente
        contexto1 = {"amostra": "SAMPLE001"}
        contexto2 = {"amostra": "SAMPLE002"}
        
        resultado1 = fw1.exibir_dado(contexto1)
        resultado2 = fw1.exibir_dado(contexto2)
        
        self.assertNotEqual(resultado1, resultado2)
        
        # 4. Performance melhorada
        self.assertIsInstance(self.fabrica.flyweights, dict)


if __name__ == '__main__':
    unittest.main()
