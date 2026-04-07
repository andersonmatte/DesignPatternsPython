"""
Testes para o padrão Strategy
"""

import unittest
from patterns.comportamentais.strategy import (
    AlignmentStrategy, NeedlemanWunschStrategy, SmithWatermanStrategy,
    BLASTStrategy, FastAlignStrategy, SequenceAligner, AlignmentBenchmark
)


class TestStrategy(unittest.TestCase):
    """Testes para o padrão Strategy."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.seq1 = "ATCGATCGATCG"
        self.seq2 = "ATCGATCGATCG"
        self.seq3 = "GCTAGCTAGCTA"
        self.aligner = SequenceAligner(NeedlemanWunschStrategy())
    
    def test_needleman_wunsch_strategy_identical_sequences(self):
        """Testa Needleman-Wunsch com sequências idênticas."""
        strategy = NeedlemanWunschStrategy()
        result = strategy.align(self.seq1, self.seq2)
        
        self.assertEqual(result['strategy'], "Needleman-Wunsch (Global Alignment)")
        self.assertEqual(result['identity'], 1.0)
        self.assertGreater(result['score'], 0)
        self.assertEqual(result['complexity'], "O(n*m)")
        self.assertEqual(len(result['aligned_sequence1']), len(result['aligned_sequence2']))
    
    def test_needleman_wunsch_strategy_different_sequences(self):
        """Testa Needleman-Wunsch com sequências diferentes."""
        strategy = NeedlemanWunschStrategy()
        result = strategy.align(self.seq1, self.seq3)
        
        self.assertEqual(result['strategy'], "Needleman-Wunsch (Global Alignment)")
        self.assertLess(result['identity'], 1.0)
        self.assertGreaterEqual(result['identity'], 0.0)
        self.assertIn('gaps', result)
    
    def test_smith_waterman_strategy_identical_sequences(self):
        """Testa Smith-Waterman com sequências idênticas."""
        strategy = SmithWatermanStrategy()
        result = strategy.align(self.seq1, self.seq2)
        
        self.assertEqual(result['strategy'], "Smith-Waterman (Local Alignment)")
        self.assertEqual(result['identity'], 1.0)
        self.assertTrue(result['local_alignment'])
        self.assertGreater(result['score'], 0)
    
    def test_smith_waterman_strategy_different_sequences(self):
        """Testa Smith-Waterman com sequências diferentes."""
        strategy = SmithWatermanStrategy()
        result = strategy.align(self.seq1, self.seq3)
        
        self.assertEqual(result['strategy'], "Smith-Waterman (Local Alignment)")
        self.assertTrue(result['local_alignment'])
        self.assertGreaterEqual(result['identity'], 0.0)
    
    def test_blast_strategy(self):
        """Testa estratégia BLAST."""
        strategy = BLASTStrategy()
        result = strategy.align(self.seq1, self.seq2)
        
        self.assertEqual(result['strategy'], "BLAST (Heuristic Alignment)")
        self.assertTrue(result['heuristic_alignment'])
        self.assertEqual(result['complexity'], "O(n + m) (heuristic)")
        self.assertIn('high_scoring_words', result)
    
    def test_fast_align_strategy(self):
        """Testa estratégia Fast Align."""
        strategy = FastAlignStrategy()
        result = strategy.align(self.seq1, self.seq2)
        
        self.assertEqual(result['strategy'], "Fast K-mer Alignment")
        self.assertEqual(result['complexity'], "O(n + m)")
        self.assertTrue(result['approximate'])
        self.assertIn('kmer_similarity', result)
    
    def test_sequence_aligner_set_strategy(self):
        """Testa mudança de estratégia no alinhador."""
        # Verifica estratégia inicial
        self.assertIn("Needleman-Wunsch", self.aligner.get_strategy_info())
        
        # Muda estratégia
        new_strategy = SmithWatermanStrategy()
        self.aligner.set_strategy(new_strategy)
        
        # Verifica mudança
        self.assertIn("Smith-Waterman", self.aligner.get_strategy_info())
        
        # Testa alinhamento com nova estratégia
        result = self.aligner.align_sequences(self.seq1, self.seq2)
        self.assertEqual(result['strategy'], "Smith-Waterman (Local Alignment)")
    
    def test_sequence_aligner_align_sequences(self):
        """Testa alinhamento de sequências."""
        result = self.aligner.align_sequences(self.seq1, self.seq2)
        
        self.assertIn('strategy', result)
        self.assertIn('score', result)
        self.assertIn('identity', result)
        self.assertIn('aligned_sequence1', result)
        self.assertIn('aligned_sequence2', result)
        self.assertIn('alignment_length', result)
        self.assertIn('gaps', result)
        self.assertIn('complexity', result)
    
    def test_alignment_benchmark_initialization(self):
        """Testa inicialização do benchmark."""
        benchmark = AlignmentBenchmark()
        
        self.assertEqual(len(benchmark.strategies), 4)
        strategy_names = [s.get_name() for s in benchmark.strategies]
        self.assertIn("Needleman-Wunsch (Global Alignment)", strategy_names)
        self.assertIn("Smith-Waterman (Local Alignment)", strategy_names)
        self.assertIn("BLAST (Heuristic Alignment)", strategy_names)
        self.assertIn("Fast K-mer Alignment", strategy_names)
    
    def test_alignment_benchmark_benchmark_strategies(self):
        """Testa benchmark de estratégias."""
        benchmark = AlignmentBenchmark()
        results = benchmark.benchmark_strategies(self.seq1, self.seq2)
        
        self.assertEqual(len(results), 4)
        for strategy_name, result in results.items():
            self.assertIn('strategy', result)
            self.assertIn('score', result)
            self.assertIn('identity', result)
    
    def test_alignment_benchmark_get_best_strategy_identity(self):
        """Testa seleção da melhor estratégia por identidade."""
        benchmark = AlignmentBenchmark()
        best_name, best_result = benchmark.get_best_strategy(self.seq1, self.seq2, "identity")
        
        self.assertIn(best_name, [s.get_name() for s in benchmark.strategies])
        self.assertIn('identity', best_result)
        self.assertIn('score', best_result)
    
    def test_alignment_benchmark_get_best_strategy_score(self):
        """Testa seleção da melhor estratégia por score."""
        benchmark = AlignmentBenchmark()
        best_name, best_result = benchmark.get_best_strategy(self.seq1, self.seq2, "score")
        
        self.assertIn(best_name, [s.get_name() for s in benchmark.strategies])
        self.assertIn('identity', best_result)
        self.assertIn('score', best_result)
    
    def test_alignment_benchmark_get_best_strategy_speed(self):
        """Testa seleção da melhor estratégia por velocidade."""
        benchmark = AlignmentBenchmark()
        best_name, best_result = benchmark.get_best_strategy(self.seq1, self.seq2, "speed")
        
        self.assertIn(best_name, [s.get_name() for s in benchmark.strategies])
        # Deve preferir estratégias heurísticas
        self.assertTrue(best_result.get('heuristic_alignment', False) or 
                       best_result.get('approximate', False))
    
    def test_needleman_wunsch_matrix_initialization(self):
        """Testa inicialização da matriz Needleman-Wunsch."""
        strategy = NeedlemanWunschStrategy()
        
        # Sequências de tamanhos diferentes
        result = strategy.align("ATCG", "GCTAGCTA")
        
        self.assertEqual(len(result['aligned_sequence1']), len(result['aligned_sequence2']))
        self.assertGreater(result['alignment_length'], 0)
    
    def test_smith_waterman_local_alignment(self):
        """Testa alinhamento local do Smith-Waterman."""
        strategy = SmithWatermanStrategy()
        
        # Sequências com pequena região de similaridade
        seq1 = "AAAAAAAAATCGAAAAAAAA"
        seq2 = "TTTTTTTTTATCGTTTTTTTT"
        
        result = strategy.align(seq1, seq2)
        
        # Deve encontrar apenas a região local similar
        self.assertTrue(result['local_alignment'])
        self.assertLess(result['alignment_length'], len(seq1))
        self.assertLess(result['alignment_length'], len(seq2))
    
    def test_blast_high_scoring_words(self):
        """Testa busca de high-scoring words no BLAST."""
        strategy = BLASTStrategy(word_size=3, threshold=0.7)
        
        # Sequências com palavras idênticas
        seq1 = "ATCGATCGATCG"
        seq2 = "ATCGGCTAGCTA"
        
        result = strategy.align(seq1, seq2)
        
        self.assertGreater(result['high_scoring_words'], 0)
        self.assertIn('ATC', seq1)  # Deve encontrar palavras de tamanho 3
    
    def test_fast_align_kmers(self):
        """Testa cálculo de k-mers no Fast Align."""
        strategy = FastAlignStrategy()
        
        kmers = strategy._get_kmers("ATCGATCG", 3)
        
        self.assertIn("ATC", kmers)
        self.assertIn("TCG", kmers)
        self.assertIn("CGA", kmers)
        self.assertEqual(len(kmers), 6)  # 9 - 3 + 1 = 6 k-mers
    
    def test_strategy_interface_compliance(self):
        """Testa conformidade com a interface Strategy."""
        strategies = [
            NeedlemanWunschStrategy(),
            SmithWatermanStrategy(),
            BLASTStrategy(),
            FastAlignStrategy()
        ]
        
        for strategy in strategies:
            # Todas devem implementar os métodos obrigatórios
            self.assertTrue(hasattr(strategy, 'align'))
            self.assertTrue(hasattr(strategy, 'get_name'))
            self.assertTrue(hasattr(strategy, 'get_complexity'))
            
            # Testa chamada dos métodos
            result = strategy.align("ATCG", "ATCG")
            self.assertIsInstance(result, dict)
            self.assertIn('strategy', result)
            
            name = strategy.get_name()
            self.assertIsInstance(name, str)
            self.assertGreater(len(name), 0)
            
            complexity = strategy.get_complexity()
            self.assertIsInstance(complexity, str)
            self.assertGreater(len(complexity), 0)
    
    def test_empty_sequences(self):
        """Testa alinhamento com sequências vazias."""
        strategy = NeedlemanWunschStrategy()
        result = strategy.align("", "")
        
        self.assertEqual(result['identity'], 0.0)
        self.assertEqual(result['alignment_length'], 0)
    
    def test_single_character_sequences(self):
        """Testa alinhamento com sequências de um caractere."""
        strategy = NeedlemanWunschStrategy()
        result = strategy.align("A", "A")
        
        self.assertEqual(result['identity'], 1.0)
        self.assertEqual(result['alignment_length'], 1)
    
    def test_strategy_parameters_customization(self):
        """Testa customização de parâmetros das estratégias."""
        # Needleman-Wunsch com parâmetros customizados
        strategy = NeedlemanWunschStrategy(match_score=3, mismatch_penalty=-2, gap_penalty=-2)
        result = strategy.align("ATCG", "ATCG")
        
        self.assertGreater(result['score'], 0)
        
        # BLAST com parâmetros customizados
        strategy = BLASTStrategy(word_size=2, threshold=0.8)
        result = strategy.align("ATCGATCG", "ATCGATCG")
        
        self.assertIn('high_scoring_words', result)
    
    def test_alignment_quality_metrics(self):
        """Testa métricas de qualidade do alinhamento."""
        strategies = [
            NeedlemanWunschStrategy(),
            SmithWatermanStrategy(),
            BLASTStrategy(),
            FastAlignStrategy()
        ]
        
        for strategy in strategies:
            result = strategy.align(self.seq1, self.seq3)
            
            # Todas as estratégias devem retornar métricas básicas
            self.assertIn('identity', result)
            self.assertIn('score', result)
            self.assertIn('alignment_length', result)
            self.assertIn('gaps', result)
            
            # Valores devem estar em faixas razoáveis
            self.assertGreaterEqual(result['identity'], 0.0)
            self.assertLessEqual(result['identity'], 1.0)
            self.assertGreaterEqual(result['gaps'], 0)
    
    def test_sequence_aligner_info(self):
        """Testa obtenção de informações do alinhador."""
        info = self.aligner.get_strategy_info()
        
        self.assertIn("Needleman-Wunsch", info)
        self.assertIn("O(n*m)", info)
    
    def test_benchmark_comparison_consistency(self):
        """Testa consistência na comparação de benchmark."""
        benchmark = AlignmentBenchmark()
        
        # Executa benchmark múltiplas vezes
        results1 = benchmark.benchmark_strategies(self.seq1, self.seq2)
        results2 = benchmark.benchmark_strategies(self.seq1, self.seq2)
        
        # Resultados devem ser consistentes
        for strategy_name in results1:
            self.assertEqual(results1[strategy_name]['strategy'], 
                           results2[strategy_name]['strategy'])
            self.assertEqual(results1[strategy_name]['identity'], 
                           results2[strategy_name]['identity'])


if __name__ == '__main__':
    unittest.main()
