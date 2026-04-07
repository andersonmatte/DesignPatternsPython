"""
Testes para o padrão Flyweight
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.flyweight import (
    DadoGeneticoFlyweight, SequenciaProteicaFlyweight, DadoGeneticoFlyweightFactory
)


class TestFlyweight(unittest.TestCase):
    """Testes para o padrão Flyweight."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        # Limpar cache antes de cada teste
        DadoGeneticoFlyweightFactory.limpar_cache()
    
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
    
    def test_factory_obter_flyweight_novo(self):
        """Testa obtenção de flyweight novo (cache miss)."""
        fw1 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        fw2 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT002")
        
        self.assertIsInstance(fw1, SequenciaProteicaFlyweight)
        self.assertIsInstance(fw2, SequenciaProteicaFlyweight)
        self.assertNotEqual(fw1, fw2)
    
    def test_factory_obter_flyweight_existente(self):
        """Testa obtenção de flyweight existente (cache hit)."""
        fw1 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        fw2 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        
        # Deve retornar a mesma instância
        self.assertIs(fw1, fw2)
    
    def test_factory_obter_stats(self):
        """Testa obtenção de estatísticas da fábrica."""
        # Criar alguns flyweights
        DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT002")
        DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")  # Reuso
        
        stats = DadoGeneticoFlyweightFactory.obter_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_flyweights', stats)
        self.assertIn('flywords_proteina', stats)
        self.assertIn('taxa_reuso', stats)
        
        self.assertEqual(stats['total_flyweights'], 2)  # Apenas 2 únicos
        self.assertEqual(stats['flywords_proteina'], 2)
    
    def test_factory_limpar_cache(self):
        """Testa limpeza do cache da fábrica."""
        # Adicionar flyweights
        DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT002")
        
        stats_antes = DadoGeneticoFlyweightFactory.obter_stats()
        self.assertGreater(stats_antes['total_flyweights'], 0)
        
        # Limpar cache
        DadoGeneticoFlyweightFactory.limpar_cache()
        
        stats_depois = DadoGeneticoFlyweightFactory.obter_stats()
        self.assertEqual(stats_depois['total_flyweights'], 0)
    
    def test_flyweight_compartilhamento_estado(self):
        """Testa compartilhamento de estado entre flyweights."""
        # Criar flyweight e configurar
        fw1 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        fw1.definir_sequencia("ATCG")
        fw1.definir_funcao("Enzima")
        
        # Obter mesmo flyweight
        fw2 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        
        # Deve ser a mesma instância
        self.assertIs(fw1, fw2)
        
        # Estado compartilhado deve ser o mesmo
        self.assertEqual(fw1._estado_compartilhado, fw2._estado_compartilhado)
        self.assertEqual(fw2._estado_compartilhado["sequencia"], "ATCG")
        self.assertEqual(fw2._estado_compartilhado["funcao"], "Enzima")
    
    def test_flyweight_contextos_diferentes(self):
        """Testa flyweight com contextos extrínsecos diferentes."""
        fw = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        fw.definir_sequencia("ATCG")
        
        contexto1 = {"amostra": "SAMPLE001", "condicao": "normal"}
        contexto2 = {"amostra": "SAMPLE002", "condicao": "experimental"}
        
        resultado1 = fw.exibir_dado(contexto1)
        resultado2 = fw.exibir_dado(contexto2)
        
        # Resultados devem ser diferentes devido aos contextos
        self.assertNotEqual(resultado1, resultado2)
        
        # Mas flyweight deve ser o mesmo
        self.assertIs(fw, DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001"))
    
    def test_flyweight_performance_benefits(self):
        """Testa benefícios de performance do flyweight."""
        import time
        
        # Criar muitos flyweights sem reuso
        DadoGeneticoFlyweightFactory.limpar_cache()
        start_time = time.time()
        flyweights_sem_reuso = []
        for i in range(50):
            fw = SequenciaProteicaFlyweight(f"PROT{i % 10}")  # Apenas 10 únicos
            fw.definir_sequencia(f"SEQ{i % 5}")
            flyweights_sem_reuso.append(fw)
        tempo_sem_reuso = time.time() - start_time
        
        # Criar muitos flyweights com reuso
        DadoGeneticoFlyweightFactory.limpar_cache()
        start_time = time.time()
        flyweights_com_reuso = []
        for i in range(50):
            fw = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", f"PROT{i % 10}")
            if not fw._estado_compartilhado["sequencia"]:
                fw.definir_sequencia(f"SEQ{i % 5}")
            flyweights_com_reuso.append(fw)
        tempo_com_reuso = time.time() - start_time
        
        # Com reuso deve ter menos flyweights únicos
        stats = DadoGeneticoFlyweightFactory.obter_stats()
        self.assertEqual(stats['total_flyweights'], 10)
        
        # Performance deve ser melhor com reuso
        self.assertLess(tempo_com_reuso, tempo_sem_reuso * 1.5)
        
        # Mas número de resultados deve ser o mesmo
        self.assertEqual(len(flyweights_sem_reuso), len(flyweights_com_reuso))
    
    def test_flyweight_memoria_efficiency(self):
        """Testa eficiência de memória do flyweight."""
        # Criar flyweight
        fw = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        fw.definir_sequencia("ATCGATCG")
        
        resultados = []
        
        # Criar 100 contextos diferentes
        for i in range(100):
            contexto = {"amostra": f"SAMPLE{i:03d}", "condicao": f"cond{i}"}
            resultado = fw.exibir_dado(contexto)
            resultados.append(resultado)
        
        # Apenas 1 flyweight no cache
        stats = DadoGeneticoFlyweightFactory.obter_stats()
        self.assertEqual(stats['total_flyweights'], 1)
        
        # Mas 100 resultados diferentes
        self.assertEqual(len(resultados), 100)
        self.assertEqual(len(set(resultados)), 100)  # Todos únicos
    
    def test_flyweight_interface_uniforme(self):
        """Testa interface uniforme entre flyweights."""
        fw = SequenciaProteicaFlyweight("PROT001")
        
        # Deve ter métodos da interface
        self.assertTrue(hasattr(fw, 'definir_sequencia'))
        self.assertTrue(hasattr(fw, 'adicionar_dominio'))
        self.assertTrue(hasattr(fw, 'definir_funcao'))
        self.assertTrue(hasattr(fw, 'exibir_dado'))
        self.assertTrue(hasattr(fw, 'obter_info_compartilhada'))
        
        # Deve ter código
        self.assertEqual(fw.codigo, "PROT001")
        
        # Deve ter estado compartilhado
        self.assertIsInstance(fw._estado_compartilhado, dict)
    
    def test_flyweight_estado_intrinsic_vs_extrinsic(self):
        """Testa separação entre estado intrínseco e extrínseco."""
        fw = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        
        # Estado intrínseco (compartilhado)
        fw.definir_sequencia("ATCG")
        fw.definir_funcao("Enzima")
        
        estado_intrinsic = fw.obter_info_compartilhada()
        self.assertIsInstance(estado_intrinsic, dict)
        self.assertIn('sequencia', estado_intrinsic)
        self.assertIn('funcao', estado_intrinsic)
        
        # Estado extrínseco (contexto)
        contexto1 = {"amostra": "SAMPLE001"}
        contexto2 = {"amostra": "SAMPLE002"}
        
        resultado1 = fw.exibir_dado(contexto1)
        resultado2 = fw.exibir_dado(contexto2)
        
        # Estado intrínseco deve ser o mesmo
        self.assertEqual(fw.obter_info_compartilhada(), fw.obter_info_compartilhada())
        
        # Mas resultados devem ser diferentes devido ao contexto extrínseco
        self.assertNotEqual(resultado1, resultado2)
    
    def test_flyweight_benefits(self):
        """Testa benefícios do padrão Flyweight."""
        # 1. Redução de uso de memória
        DadoGeneticoFlyweightFactory.limpar_cache()
        fw1 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")
        fw2 = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", "PROT001")  # Reuso
        
        stats = DadoGeneticoFlyweightFactory.obter_stats()
        self.assertEqual(stats['total_flyweights'], 1)
        
        # 2. Compartilhamento de estado intrínseco
        self.assertIs(fw1, fw2)
        self.assertEqual(fw1._estado_compartilhado, fw2._estado_compartilhado)
        
        # 3. Estado extrínseco independente
        contexto1 = {"amostra": "SAMPLE001"}
        contexto2 = {"amostra": "SAMPLE002"}
        
        resultado1 = fw1.exibir_dado(contexto1)
        resultado2 = fw1.exibir_dado(contexto2)
        
        self.assertNotEqual(resultado1, resultado2)
        
        # 4. Performance melhorada
        self.assertIsInstance(stats, dict)
        self.assertIn('taxa_reuso', stats)


if __name__ == '__main__':
    unittest.main()
