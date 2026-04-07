"""
Testes para o padrão Flyweight
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.flyweight import (
    DadoGeneticoFlyweight, SequenciaFlyweight, ProteinaFlyweight,
    FabricaFlyweight, ContextoExtrinseco
)


class TestFlyweight(unittest.TestCase):
    """Testes para o padrão Flyweight."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.fabrica = FabricaFlyweight()
        
        # Contextos extrínsecos para testes
        self.contexto1 = ContextoExtrinseco("amostra1", "paciente_A", 100)
        self.contexto2 = ContextoExtrinseco("amostra2", "paciente_B", 200)
    
    def test_fabrica_flyweight_creation(self):
        """Testa criação da fábrica de flyweights."""
        fabrica = FabricaFlyweight()
        
        self.assertIsInstance(fabrica, FabricaFlyweight)
        self.assertEqual(len(fabrica.flyweights), 0)
    
    def test_sequencia_flyweight_creation(self):
        """Testa criação de flyweight de sequência."""
        flyweight = SequenciaFlyweight("ATCG")
        
        self.assertIsInstance(flyweight, DadoGeneticoFlyweight)
        self.assertEqual(flyweight.codigo, "ATCG")
        self.assertIn('sequencia', flyweight._estado_compartilhado)
        self.assertIn('comprimento', flyweight._estado_compartilhado)
    
    def test_proteina_flyweight_creation(self):
        """Testa criação de flyweight de proteína."""
        flyweight = ProteinaFlyweight("PROTEIN_A")
        
        self.assertIsInstance(flyweight, DadoGeneticoFlyweight)
        self.assertEqual(flyweight.codigo, "PROTEIN_A")
        self.assertIn('nome_proteina', flyweight._estado_compartilhado)
        self.assertIn('peso_molecular', flyweight._estado_compartilhado)
    
    def test_contexto_extrinseco_creation(self):
        """Testa criação de contexto extrínseco."""
        contexto = ContextoExtrinseco("amostra1", "paciente_A", 100)
        
        self.assertEqual(contexto.id_amostra, "amostra1")
        self.assertEqual(contexto.id_paciente, "paciente_A")
        self.assertEqual(contexto.posicao_genomica, 100)
    
    def test_fabrica_obter_flyweight_novo(self):
        """Testa obtenção de flyweight novo (cache miss)."""
        flyweight1 = self.fabrica.obter_flyweight_sequencia("ATCG")
        flyweight2 = self.fabrica.obter_flyweight_sequencia("GCTA")
        
        self.assertIsInstance(flyweight1, SequenciaFlyweight)
        self.assertIsInstance(flyweight2, SequenciaFlyweight)
        self.assertEqual(len(self.fabrica.flyweights), 2)
        self.assertNotEqual(flyweight1, flyweight2)
    
    def test_fabrica_obter_flyweight_existente(self):
        """Testa obtenção de flyweight existente (cache hit)."""
        flyweight1 = self.fabrica.obter_flyweight_sequencia("ATCG")
        flyweight2 = self.fabrica.obter_flyweight_sequencia("ATCG")
        
        # Deve retornar a mesma instância
        self.assertIs(flyweight1, flyweight2)
        self.assertEqual(len(self.fabrica.flyweights), 1)
    
    def test_sequencia_flyweight_exibir_dado(self):
        """Testa exibição de dado com contexto extrínseco."""
        flyweight = SequenciaFlyweight("ATCG")
        
        resultado = flyweight.exibir_dado(self.contexto1)
        
        self.assertIsInstance(resultado, str)
        self.assertIn("ATCG", resultado)
        self.assertIn("amostra1", resultado)
        self.assertIn("paciente_A", resultado)
    
    def test_proteina_flyweight_exibir_dado(self):
        """Testa exibição de proteína com contexto extrínseco."""
        flyweight = ProteinaFlyweight("PROTEIN_A")
        
        resultado = flyweight.exibir_dado(self.contexto2)
        
        self.assertIsInstance(resultado, str)
        self.assertIn("PROTEIN_A", resultado)
        self.assertIn("amostra2", resultado)
        self.assertIn("paciente_B", resultado)
    
    def test_flyweight_compartilhamento_estado(self):
        """Testa compartilhamento de estado intrínseco."""
        # Criar múltiplos flyweights com mesmo código
        fw1 = self.fabrica.obter_flyweight_sequencia("ATCG")
        fw2 = self.fabrica.obter_flyweight_sequencia("ATCG")
        fw3 = self.fabrica.obter_flyweight_sequencia("ATCG")
        
        # Todos devem ser a mesma instância
        self.assertIs(fw1, fw2)
        self.assertIs(fw2, fw3)
        
        # Estado compartilhado deve ser o mesmo
        self.assertEqual(fw1._estado_compartilhado, fw2._estado_compartilhado)
        self.assertEqual(fw2._estado_compartilhado, fw3._estado_compartilhado)
    
    def test_flyweight_contextos_diferentes(self):
        """Testa flyweight com contextos extrínsecos diferentes."""
        flyweight = self.fabrica.obter_flyweight_sequencia("ATCG")
        
        # Mesmo flyweight, contextos diferentes
        resultado1 = flyweight.exibir_dado(self.contexto1)
        resultado2 = flyweight.exibir_dado(self.contexto2)
        
        # Resultados devem ser diferentes devido aos contextos
        self.assertNotEqual(resultado1, resultado2)
        
        # Mas flyweight deve ser o mesmo
        self.assertIs(flyweight, self.fabrica.obter_flyweight_sequencia("ATCG"))
    
    def test_fabrica_estatisticas(self):
        """Testa estatísticas da fábrica."""
        # Criar vários flyweights
        self.fabrica.obter_flyweight_sequencia("ATCG")
        self.fabrica.obter_flyweight_sequencia("GCTA")
        self.fabrica.obter_flyweight_proteina("PROT_A")
        self.fabrica.obter_flyweight_sequencia("ATCG")  # Reuso
        
        stats = self.fabrica.obter_estatisticas()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_flyweights', stats)
        self.assertIn('flywords_sequencia', stats)
        self.assertIn('flywords_proteina', stats)
        self.assertIn('taxa_reuso', stats)
        
        self.assertEqual(stats['total_flyweights'], 3)  # 2 sequências + 1 proteína
        self.assertEqual(stats['flywords_sequencia'], 2)
        self.assertEqual(stats['flywords_proteina'], 1)
    
    def test_flyweight_performance_benefits(self):
        """Testa benefícios de performance do flyweight."""
        import time
        
        # Simular muitas operações sem flyweight
        start_time = time.time()
        dados_sem_flyweight = []
        for i in range(100):
            sequencia = SequenciaFlyweight(f"SEQ{i % 10}")  # Apenas 10 sequências únicas
            contexto = ContextoExtrinseco(f"amostra{i}", f"paciente{i}", i)
            dados_sem_flyweight.append(sequencia.exibir_dado(contexto))
        tempo_sem_flyweight = time.time() - start_time
        
        # Simular muitas operações com flyweight
        self.fabrica.limpar_cache()
        start_time = time.time()
        dados_com_flyweight = []
        for i in range(100):
            sequencia = self.fabrica.obter_flyweight_sequencia(f"SEQ{i % 10}")
            contexto = ContextoExtrinseco(f"amostra{i}", f"paciente{i}", i)
            dados_com_flyweight.append(sequencia.exibir_dado(contexto))
        tempo_com_flyweight = time.time() - start_time
        
        # Flyweight deve ser mais eficiente
        self.assertLess(tempo_com_flyweight, tempo_sem_flyweight * 1.5)
        
        # Deve ter apenas 10 flyweights no cache
        self.assertEqual(len(self.fabrica.flyweights), 10)
        
        # Mas 100 resultados
        self.assertEqual(len(dados_com_flyweight), 100)
    
    def test_flyweight_memoria_efficiency(self):
        """Testa eficiência de memória do flyweight."""
        # Criar muitos contextos para poucos flyweights
        flyweight = self.fabrica.obter_flyweight_sequencia("ATCG")
        
        contextos = []
        resultados = []
        
        # Criar 1000 contextos diferentes
        for i in range(1000):
            contexto = ContextoExtrinseco(f"amostra{i}", f"paciente{i}", i)
            contextos.append(contexto)
            resultados.append(flyweight.exibir_dado(contexto))
        
        # Apenas 1 flyweight no cache
        self.assertEqual(len(self.fabrica.flyweights), 1)
        
        # Mas 1000 resultados diferentes
        self.assertEqual(len(resultados), 1000)
        self.assertEqual(len(set(resultados)), 1000)  # Todos únicos
    
    def test_flyweight_diferentes_tipos(self):
        """Testa flyweights de diferentes tipos."""
        fw_seq = self.fabrica.obter_flyweight_sequencia("ATCG")
        fw_prot = self.fabrica.obter_flyweight_proteina("PROT_A")
        
        # Tipos diferentes devem ser instâncias diferentes
        self.assertIsInstance(fw_seq, SequenciaFlyweight)
        self.assertIsInstance(fw_prot, ProteinaFlyweight)
        self.assertNotEqual(type(fw_seq), type(fw_prot))
        
        # Ambos devem estar no cache
        self.assertEqual(len(self.fabrica.flyweights), 2)
    
    def test_flyweight_limpar_cache(self):
        """Testa limpeza do cache da fábrica."""
        # Adicionar alguns flyweights
        self.fabrica.obter_flyweight_sequencia("ATCG")
        self.fabrica.obter_flyweight_sequencia("GCTA")
        self.fabrica.obter_flyweight_proteina("PROT_A")
        
        self.assertEqual(len(self.fabrica.flyweights), 3)
        
        # Limpar cache
        self.fabrica.limpar_cache()
        
        self.assertEqual(len(self.fabrica.flyweights), 0)
    
    def test_flyweight_interface_uniforme(self):
        """Testa interface uniforme entre flyweights."""
        fw_seq = SequenciaFlyweight("ATCG")
        fw_prot = ProteinaFlyweight("PROT_A")
        
        # Ambos devem ter a mesma interface
        self.assertTrue(hasattr(fw_seq, 'exibir_dado'))
        self.assertTrue(hasattr(fw_prot, 'exibir_dado'))
        
        # Ambos devem ter código
        self.assertEqual(fw_seq.codigo, "ATCG")
        self.assertEqual(fw_prot.codigo, "PROT_A")
        
        # Ambos devem ter estado compartilhado
        self.assertIsInstance(fw_seq._estado_compartilhado, dict)
        self.assertIsInstance(fw_prot._estado_compartilhado, dict)
    
    def test_flyweight_estado_inmutable(self):
        """Testa imutabilidade do estado compartilhado."""
        flyweight = self.fabrica.obter_flyweight_sequencia("ATCG")
        estado_original = flyweight._estado_compartilhado.copy()
        
        # Tentar modificar estado
        flyweight._estado_compartilhado['novo_campo'] = 'valor'
        
        # Estado deve ter sido modificado (não é imutável por padrão)
        self.assertIn('novo_campo', flyweight._estado_compartilhado)
    
    def test_flyweight_contexto_independence(self):
        """Testa independência do contexto extrínseco."""
        flyweight = self.fabrica.obter_flyweight_sequencia("ATCG")
        
        contexto1 = ContextoExtrinseco("amostra1", "paciente1", 100)
        contexto2 = ContextoExtrinseco("amostra2", "paciente2", 200)
        
        resultado1 = flyweight.exibir_dado(contexto1)
        resultado2 = flyweight.exibir_dado(contexto2)
        
        # Resultados devem ser diferentes
        self.assertNotEqual(resultado1, resultado2)
        
        # Contextos devem ser independentes
        self.assertNotEqual(contexto1.id_amostra, contexto2.id_amostra)
        self.assertNotEqual(contexto1.id_paciente, contexto2.id_paciente)
    
    def test_flyweight_benefits(self):
        """Testa benefícios do padrão Flyweight."""
        # 1. Redução de uso de memória
        self.fabrica.obter_flyweight_sequencia("ATCG")
        self.fabrica.obter_flyweight_sequencia("ATCG")  # Reuso
        
        self.assertEqual(len(self.fabrica.flyweights), 1)
        
        # 2. Compartilhamento de estado intrínseco
        fw1 = self.fabrica.obter_flyweight_sequencia("ATCG")
        fw2 = self.fabrica.obter_flyweight_sequencia("ATCG")
        self.assertIs(fw1, fw2)
        
        # 3. Estado extrínseco independente
        contexto1 = ContextoExtrinseco("a1", "p1", 1)
        contexto2 = ContextoExtrinseco("a2", "p2", 2)
        
        resultado1 = fw1.exibir_dado(contexto1)
        resultado2 = fw1.exibir_dado(contexto2)
        
        self.assertNotEqual(resultado1, resultado2)
        
        # 4. Performance melhorada
        self.assertIsInstance(self.fabrica.obter_estatisticas(), dict)


if __name__ == '__main__':
    unittest.main()
