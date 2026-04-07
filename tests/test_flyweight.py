"""
Testes para o padrão Flyweight
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.flyweight import (
    FlyweightSequencia, FlyweightFactory, SequenciaFlyweight
)


class TestFlyweight(unittest.TestCase):
    """Testes para o padrão Flyweight."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.factory = FlyweightFactory()
    
    def test_flyweight_factory_creation(self):
        """Testa criação da fábrica de flyweights."""
        self.assertIsInstance(self.factory, FlyweightFactory)
        self.assertEqual(len(self.factory.flyweights), 0)
    
    def test_flyweight_factory_get_flyweight_new(self):
        """Testa criação de novo flyweight."""
        flyweight = self.factory.get_flyweight("ATCG", "DNA")
        
        self.assertIsInstance(flyweight, SequenciaFlyweight)
        self.assertEqual(flyweight.sequencia, "ATCG")
        self.assertEqual(flyweight.tipo, "DNA")
        self.assertEqual(len(self.factory.flyweights), 1)
    
    def test_flyweight_factory_get_flyweight_existing(self):
        """Testa reuso de flyweight existente."""
        flyweight1 = self.factory.get_flyweight("ATCG", "DNA")
        flyweight2 = self.factory.get_flyweight("ATCG", "DNA")
        
        # Deve retornar a mesma instância
        self.assertIs(flyweight1, flyweight2)
        self.assertEqual(len(self.factory.flyweights), 1)
    
    def test_flyweight_factory_different_keys(self):
        """Testa flyweights diferentes para chaves diferentes."""
        flyweight1 = self.factory.get_flyweight("ATCG", "DNA")
        flyweight2 = self.factory.get_flyweight("GCTA", "DNA")
        flyweight3 = self.factory.get_flyweight("ATCG", "RNA")
        
        # Deve criar instâncias diferentes
        self.assertIsNot(flyweight1, flyweight2)
        self.assertIsNot(flyweight1, flyweight3)
        self.assertIsNot(flyweight2, flyweight3)
        self.assertEqual(len(self.factory.flyweights), 3)
    
    def test_flyweight_factory_get_flyweight_count(self):
        """Testa contagem de flyweights."""
        self.assertEqual(self.factory.get_flyweight_count(), 0)
        
        self.factory.get_flyweight("ATCG", "DNA")
        self.assertEqual(self.factory.get_flyweight_count(), 1)
        
        self.factory.get_flyweight("ATCG", "DNA")  # Reuso
        self.assertEqual(self.factory.get_flyweight_count(), 1)
        
        self.factory.get_flyweight("GCTA", "DNA")
        self.assertEqual(self.factory.get_flyweight_count(), 2)
    
    def test_flyweight_factory_list_flyweights(self):
        """Testa listagem de flyweights."""
        self.factory.get_flyweight("ATCG", "DNA")
        self.factory.get_flyweight("GCTA", "RNA")
        
        flyweights = self.factory.list_flyweights()
        
        self.assertEqual(len(flyweights), 2)
        self.assertIn("DNA:ATCG", flyweights)
        self.assertIn("RNA:GCTA", flyweights)
    
    def test_flyweight_factory_clear_cache(self):
        """Testa limpeza do cache."""
        self.factory.get_flyweight("ATCG", "DNA")
        self.factory.get_flyweight("GCTA", "RNA")
        
        self.assertEqual(len(self.factory.flyweights), 2)
        
        self.factory.clear_cache()
        
        self.assertEqual(len(self.factory.flyweights), 0)
    
    def test_sequencia_flyweight_creation(self):
        """Testa criação de sequência flyweight."""
        flyweight = SequenciaFlyweight("ATCGATCG", "DNA")
        
        self.assertIsInstance(flyweight, FlyweightSequencia)
        self.assertEqual(flyweight.sequencia, "ATCGATCG")
        self.assertEqual(flyweight.tipo, "DNA")
    
    def test_sequencia_flyweight_analisar(self):
        """Testa análise de sequência flyweight."""
        flyweight = SequenciaFlyweight("ATCGATCG", "DNA")
        
        # Estado extrínseco
        contexto = {
            'id_amostra': 'SAMPLE001',
            'posicao': 100,
            'qualidade': 0.95
        }
        
        resultado = flyweight.analisar(contexto)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('sequencia', resultado)
        self.assertIn('tipo', resultado)
        self.assertIn('contexto', resultado)
        self.assertIn('analise', resultado)
        self.assertEqual(resultado['sequencia'], "ATCGATCG")
        self.assertEqual(resultado['tipo'], "DNA")
        self.assertEqual(resultado['contexto'], contexto)
    
    def test_sequencia_flyweight_get_intrinsic_info(self):
        """Testa obtenção de informações intrínsecas."""
        flyweight = SequenciaFlyweight("ATCGATCG", "DNA")
        
        info = flyweight.get_intrinsic_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('sequencia', info)
        self.assertIn('tipo', info)
        self.assertIn('tamanho', info)
        self.assertIn('composicao', info)
        self.assertEqual(info['sequencia'], "ATCGATCG")
        self.assertEqual(info['tamanho'], 7)
    
    def test_sequencia_flyweight_calculate_gc_content(self):
        """Testa cálculo de conteúdo GC."""
        flyweight = SequenciaFlyweight("ATCGATCG", "DNA")
        
        gc_content = flyweight._calculate_gc_content()
        
        self.assertIsInstance(gc_content, float)
        self.assertGreaterEqual(gc_content, 0.0)
        self.assertLessEqual(gc_content, 1.0)
        
        # ATCGATCG tem 3 G/C em 8 bases = 37.5%
        self.assertAlmostEqual(gc_content, 3/7, places=2)
    
    def test_sequencia_flyweight_calculate_composition(self):
        """Testa cálculo de composição."""
        flyweight = SequenciaFlyweight("ATCGATCG", "DNA")
        
        composition = flyweight._calculate_composition()
        
        self.assertIsInstance(composition, dict)
        self.assertIn('A', composition)
        self.assertIn('T', composition)
        self.assertIn('C', composition)
        self.assertIn('G', composition)
        
        # ATCGATCG tem 2 A, 2 T, 2 C, 1 G
        self.assertEqual(composition['A'], 2)
        self.assertEqual(composition['T'], 2)
        self.assertEqual(composition['C'], 2)
        self.assertEqual(composition['G'], 1)
    
    def test_flyweight_memory_efficiency(self):
        """Testa eficiência de memória do flyweight."""
        # Criar muitas sequências com conteúdo repetido
        sequencias_base = ["ATCG", "GCTA", "TTAA", "CCGG"]
        
        # Criar 1000 instâncias contextuais
        contextos = []
        for i in range(1000):
            seq_base = sequencias_base[i % len(sequencias_base)]
            flyweight = self.factory.get_flyweight(seq_base, "DNA")
            
            contexto = {
                'id_amostra': f'SAMPLE{i:03d}',
                'posicao': i,
                'qualidade': 0.9 + (i % 10) / 100
            }
            
            resultado = flyweight.analisar(contexto)
            contextos.append(resultado)
        
        # Deve ter apenas 4 flyweights no cache
        self.assertEqual(len(self.factory.flyweights), 4)
        
        # Mas 1000 resultados contextuais
        self.assertEqual(len(contextos), 1000)
        
        # Verificar se os contextos são diferentes
        self.assertNotEqual(contextos[0]['contexto']['id_amostra'], 
                           contextos[1]['contexto']['id_amostra'])
    
    def test_flyweight_performance_benefit(self):
        """Testa benefício de performance do flyweight."""
        import time
        
        # Testar sem flyweight (criação direta)
        start_time = time.time()
        sequencias_diretas = []
        for i in range(100):
            sequencia = SequenciaFlyweight("ATCGATCG", "DNA")
            contexto = {'id_amostra': f'SAMPLE{i}', 'posicao': i}
            resultado = sequencia.analisar(contexto)
            sequencias_diretas.append(resultado)
        tempo_direto = time.time() - start_time
        
        # Limpar cache
        self.factory.clear_cache()
        
        # Testar com flyweight
        start_time = time.time()
        sequencias_flyweight = []
        for i in range(100):
            flyweight = self.factory.get_flyweight("ATCGATCG", "DNA")
            contexto = {'id_amostra': f'SAMPLE{i}', 'posicao': i}
            resultado = flyweight.analisar(contexto)
            sequencias_flyweight.append(resultado)
        tempo_flyweight = time.time() - start_time
        
        # Flyweight deve ser mais eficiente (reuso de objetos)
        self.assertLess(tempo_flyweight, tempo_direto * 1.5)  # No máximo 50% mais lento
        
        # Resultados devem ser equivalentes
        self.assertEqual(len(sequencias_diretas), len(sequencias_flyweight))
    
    def test_flyweight_thread_safety(self):
        """Testa thread safety do flyweight."""
        import threading
        
        results = []
        errors = []
        
        def worker(thread_id):
            try:
                for i in range(10):
                    flyweight = self.factory.get_flyweight("ATCG", "DNA")
                    results.append((thread_id, i, id(flyweight)))
            except Exception as e:
                errors.append((thread_id, str(e)))
        
        # Criar múltiplas threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Esperar todas as threads
        for thread in threads:
            thread.join()
        
        # Não deve ter erros
        self.assertEqual(len(errors), 0)
        
        # Todas as operações devem retornar o mesmo flyweight
        unique_ids = set(result[2] for result in results)
        self.assertEqual(len(unique_ids), 1)
    
    def test_flyweight_different_types(self):
        """Testa flyweights com diferentes tipos de sequência."""
        dna_flyweight = self.factory.get_flyweight("ATCG", "DNA")
        rna_flyweight = self.factory.get_flyweight("AUCG", "RNA")
        protein_flyweight = self.factory.get_flyweight("ATCG", "Proteína")
        
        # Deve criar flyweights diferentes
        self.assertIsNot(dna_flyweight, rna_flyweight)
        self.assertIsNot(dna_flyweight, protein_flyweight)
        self.assertIsNot(rna_flyweight, protein_flyweight)
        
        self.assertEqual(len(self.factory.flyweights), 3)
    
    def test_flyweight_context_independence(self):
        """Testa independência do contexto."""
        flyweight = self.factory.get_flyweight("ATCG", "DNA")
        
        contexto1 = {'id_amostra': 'SAMPLE1', 'posicao': 100}
        contexto2 = {'id_amostra': 'SAMPLE2', 'posicao': 200}
        
        resultado1 = flyweight.analisar(contexto1)
        resultado2 = flyweight.analisar(contexto2)
        
        # Estados intrínsecos devem ser iguais
        self.assertEqual(resultado1['sequencia'], resultado2['sequencia'])
        self.assertEqual(resultado1['tipo'], resultado2['tipo'])
        
        # Estados extrínsecos devem ser diferentes
        self.assertNotEqual(resultado1['contexto'], resultado2['contexto'])
    
    def test_flyweight_cache_key_generation(self):
        """Testa geração de chave de cache."""
        # A chave deve combinar tipo e sequência
        flyweight1 = self.factory.get_flyweight("ATCG", "DNA")
        flyweight2 = self.factory.get_flyweight("ATCG", "RNA")
        
        # Mesma sequência, tipos diferentes = chaves diferentes
        self.assertNotEqual(id(flyweight1), id(flyweight2))
        
        # Verificar chaves no cache
        keys = list(self.factory.flyweights.keys())
        self.assertIn("DNA:ATCG", keys)
        self.assertIn("RNA:ATCG", keys)
    
    def test_flyweight_empty_sequence(self):
        """Testa flyweight com sequência vazia."""
        flyweight = self.factory.get_flyweight("", "DNA")
        
        contexto = {'id_amostra': 'EMPTY', 'posicao': 0}
        resultado = flyweight.analisar(contexto)
        
        self.assertEqual(resultado['sequencia'], "")
        self.assertEqual(resultado['analise']['tamanho'], 0)
        self.assertEqual(resultado['analise']['gc_content'], 0.0)
    
    def test_flyweight_large_sequence(self):
        """Testa flyweight com sequência longa."""
        long_sequence = "ATCG" * 1000  # 4000 bases
        
        flyweight = self.factory.get_flyweight(long_sequence, "DNA")
        
        contexto = {'id_amostra': 'LONG', 'posicao': 0}
        resultado = flyweight.analisar(contexto)
        
        self.assertEqual(len(resultado['sequencia']), 4000)
        self.assertEqual(resultado['analise']['tamanho'], 4000)
    
    def test_flyweight_invalid_context(self):
        """Testa flyweight com contexto inválido."""
        flyweight = self.factory.get_flyweight("ATCG", "DNA")
        
        # Contexto vazio
        resultado = flyweight.analisar({})
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('contexto', resultado)
        self.assertEqual(resultado['contexto'], {})
    
    def test_flyweight_factory_statistics(self):
        """Testa estatísticas da fábrica."""
        # Criar vários flyweights
        self.factory.get_flyweight("ATCG", "DNA")
        self.factory.get_flyweight("GCTA", "DNA")
        self.factory.get_flyweight("ATCG", "RNA")
        
        stats = self.factory.get_statistics()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_flyweights', stats)
        self.assertIn('total_requests', stats)
        self.assertIn('cache_hit_ratio', stats)
        self.assertIn('unique_sequences', stats)
        self.assertIn('unique_types', stats)
        
        self.assertEqual(stats['total_flyweights'], 3)
        self.assertGreater(stats['total_requests'], 0)
    
    def test_flyweight_pattern_benefits(self):
        """Testa benefícios do padrão Flyweight."""
        # 1. Redução de uso de memória
        sequencias_repetidas = ["ATCG", "GCTA"] * 50
        
        for seq in sequencias_repetidas:
            self.factory.get_flyweight(seq, "DNA")
        
        # Deve ter apenas 2 flyweights para 100 requisições
        self.assertEqual(len(self.factory.flyweights), 2)
        
        # 2. Compartilhamento de estado intrínseco
        flyweight1 = self.factory.get_flyweight("ATCG", "DNA")
        flyweight2 = self.factory.get_flyweight("ATCG", "DNA")
        
        self.assertIs(flyweight1, flyweight2)
        
        # 3. Estado extrínseco independente
        contexto1 = {'id': 1}
        contexto2 = {'id': 2}
        
        resultado1 = flyweight1.analisar(contexto1)
        resultado2 = flyweight2.analisar(contexto2)
        
        self.assertNotEqual(resultado1['contexto'], resultado2)


if __name__ == '__main__':
    unittest.main()
