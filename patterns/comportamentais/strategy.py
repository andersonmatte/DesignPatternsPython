"""
Strategy Pattern - Padrão Comportamental

Permite que você defina uma família de algoritmos, coloque-os em classes separadas, 
e faça os objetos deles intercambiáveis.

Este padrão é usado no sistema de bioinformática para implementar diferentes algoritmos
de alinhamento de sequências, permitindo trocar a estratégia conforme necessário.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
import random
import math


class AlignmentStrategy(ABC):
    """Interface base para estratégias de alinhamento."""
    
    @abstractmethod
    def align(self, sequence1: str, sequence2: str) -> Dict[str, Any]:
        """Alinha duas sequências usando a estratégia específica."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome da estratégia."""
        pass
    
    @abstractmethod
    def get_complexity(self) -> str:
        """Retorna a complexidade computacional da estratégia."""
        pass


class NeedlemanWunschStrategy(AlignmentStrategy):
    """Implementação do algoritmo Needleman-Wunsch (alinhamento global)."""
    
    def __init__(self, match_score: int = 2, mismatch_penalty: int = -1, gap_penalty: int = -1):
        self.match_score = match_score
        self.mismatch_penalty = mismatch_penalty
        self.gap_penalty = gap_penalty
    
    def align(self, sequence1: str, sequence2: str) -> Dict[str, Any]:
        """Executa alinhamento global usando Needleman-Wunsch."""
        # Inicializa matriz de scores
        rows = len(sequence1) + 1
        cols = len(sequence2) + 1
        score_matrix = [[0] * cols for _ in range(rows)]
        
        # Inicializa primeira linha e coluna
        for i in range(1, rows):
            score_matrix[i][0] = i * self.gap_penalty
        for j in range(1, cols):
            score_matrix[0][j] = j * self.gap_penalty
        
        # Preenche matriz
        for i in range(1, rows):
            for j in range(1, cols):
                match = score_matrix[i-1][j-1] + (
                    self.match_score if sequence1[i-1] == sequence2[j-1] 
                    else self.mismatch_penalty
                )
                delete = score_matrix[i-1][j] + self.gap_penalty
                insert = score_matrix[i][j-1] + self.gap_penalty
                score_matrix[i][j] = max(match, delete, insert)
        
        # Backtracking para obter o alinhamento
        aligned_seq1, aligned_seq2 = self._backtrack(score_matrix, sequence1, sequence2)
        
        # Calcula estatísticas
        score = score_matrix[rows-1][cols-1]
        identity = self._calculate_identity(aligned_seq1, aligned_seq2)
        
        return {
            'strategy': self.get_name(),
            'score': score,
            'identity': identity,
            'aligned_sequence1': aligned_seq1,
            'aligned_sequence2': aligned_seq2,
            'alignment_length': len(aligned_seq1),
            'gaps': aligned_seq1.count('-') + aligned_seq2.count('-'),
            'complexity': self.get_complexity()
        }
    
    def _backtrack(self, score_matrix: List[List[int]], seq1: str, seq2: str) -> Tuple[str, str]:
        """Realiza o backtracking para reconstruir o alinhamento."""
        aligned_seq1 = ""
        aligned_seq2 = ""
        i, j = len(seq1), len(seq2)
        
        while i > 0 or j > 0:
            if i > 0 and j > 0:
                current_score = score_matrix[i][j]
                diagonal_score = score_matrix[i-1][j-1]
                
                if seq1[i-1] == seq2[j-1]:
                    expected_diagonal = diagonal_score + self.match_score
                else:
                    expected_diagonal = diagonal_score + self.mismatch_penalty
                
                if current_score == expected_diagonal:
                    aligned_seq1 = seq1[i-1] + aligned_seq1
                    aligned_seq2 = seq2[j-1] + aligned_seq2
                    i -= 1
                    j -= 1
                    continue
            
            if i > 0 and score_matrix[i][j] == score_matrix[i-1][j] + self.gap_penalty:
                aligned_seq1 = seq1[i-1] + aligned_seq1
                aligned_seq2 = "-" + aligned_seq2
                i -= 1
            elif j > 0 and score_matrix[i][j] == score_matrix[i][j-1] + self.gap_penalty:
                aligned_seq1 = "-" + aligned_seq1
                aligned_seq2 = seq2[j-1] + aligned_seq2
                j -= 1
            else:
                break
        
        return aligned_seq1, aligned_seq2
    
    def _calculate_identity(self, seq1: str, seq2: str) -> float:
        """Calcula a percentagem de identidade."""
        matches = sum(1 for a, b in zip(seq1, seq2) if a == b and a != '-')
        total_length = sum(1 for a, b in zip(seq1, seq2) if a != '-' or b != '-')
        return matches / total_length if total_length > 0 else 0.0
    
    def get_name(self) -> str:
        return "Needleman-Wunsch (Global Alignment)"
    
    def get_complexity(self) -> str:
        return "O(n*m)"


class SmithWatermanStrategy(AlignmentStrategy):
    """Implementação do algoritmo Smith-Waterman (alinhamento local)."""
    
    def __init__(self, match_score: int = 2, mismatch_penalty: int = -1, gap_penalty: int = -1):
        self.match_score = match_score
        self.mismatch_penalty = mismatch_penalty
        self.gap_penalty = gap_penalty
    
    def align(self, sequence1: str, sequence2: str) -> Dict[str, Any]:
        """Executa alinhamento local usando Smith-Waterman."""
        rows = len(sequence1) + 1
        cols = len(sequence2) + 1
        score_matrix = [[0] * cols for _ in range(rows)]
        max_score = 0
        max_pos = (0, 0)
        
        # Preenche matriz
        for i in range(1, rows):
            for j in range(1, cols):
                match = score_matrix[i-1][j-1] + (
                    self.match_score if sequence1[i-1] == sequence2[j-1] 
                    else self.mismatch_penalty
                )
                delete = score_matrix[i-1][j] + self.gap_penalty
                insert = score_matrix[i][j-1] + self.gap_penalty
                score_matrix[i][j] = max(0, match, delete, insert)
                
                if score_matrix[i][j] > max_score:
                    max_score = score_matrix[i][j]
                    max_pos = (i, j)
        
        # Backtracking a partir do score máximo
        aligned_seq1, aligned_seq2 = self._backtrack_local(score_matrix, sequence1, sequence2, max_pos)
        
        identity = self._calculate_identity(aligned_seq1, aligned_seq2)
        
        return {
            'strategy': self.get_name(),
            'score': max_score,
            'identity': identity,
            'aligned_sequence1': aligned_seq1,
            'aligned_sequence2': aligned_seq2,
            'alignment_length': len(aligned_seq1),
            'gaps': aligned_seq1.count('-') + aligned_seq2.count('-'),
            'complexity': self.get_complexity(),
            'local_alignment': True
        }
    
    def _backtrack_local(self, score_matrix: List[List[int]], seq1: str, seq2: str, 
                        max_pos: Tuple[int, int]) -> Tuple[str, str]:
        """Backtracking para alinhamento local."""
        aligned_seq1 = ""
        aligned_seq2 = ""
        i, j = max_pos
        
        while i > 0 and j > 0 and score_matrix[i][j] > 0:
            current_score = score_matrix[i][j]
            diagonal_score = score_matrix[i-1][j-1]
            
            if seq1[i-1] == seq2[j-1]:
                expected_diagonal = diagonal_score + self.match_score
            else:
                expected_diagonal = diagonal_score + self.mismatch_penalty
            
            if current_score == expected_diagonal:
                aligned_seq1 = seq1[i-1] + aligned_seq1
                aligned_seq2 = seq2[j-1] + aligned_seq2
                i -= 1
                j -= 1
            elif i > 0 and current_score == score_matrix[i-1][j] + self.gap_penalty:
                aligned_seq1 = seq1[i-1] + aligned_seq1
                aligned_seq2 = "-" + aligned_seq2
                i -= 1
            elif j > 0 and current_score == score_matrix[i][j-1] + self.gap_penalty:
                aligned_seq1 = "-" + aligned_seq1
                aligned_seq2 = seq2[j-1] + aligned_seq2
                j -= 1
            else:
                break
        
        return aligned_seq1, aligned_seq2
    
    def _calculate_identity(self, seq1: str, seq2: str) -> float:
        """Calcula a percentagem de identidade."""
        matches = sum(1 for a, b in zip(seq1, seq2) if a == b and a != '-')
        total_length = sum(1 for a, b in zip(seq1, seq2) if a != '-' or b != '-')
        return matches / total_length if total_length > 0 else 0.0
    
    def get_name(self) -> str:
        return "Smith-Waterman (Local Alignment)"
    
    def get_complexity(self) -> str:
        return "O(n*m)"


class BLASTStrategy(AlignmentStrategy):
    """Implementação simplificada do algoritmo BLAST."""
    
    def __init__(self, word_size: int = 3, threshold: float = 0.7):
        self.word_size = word_size
        self.threshold = threshold
    
    def align(self, sequence1: str, sequence2: str) -> Dict[str, Any]:
        """Executa alinhamento usando método BLAST simplificado."""
        # Encontra palavras de alta pontuação
        high_scoring_words = self._find_high_scoring_words(sequence1, sequence2)
        
        # Estende alinhamentos
        best_alignment = self._extend_alignments(sequence1, sequence2, high_scoring_words)
        
        return {
            'strategy': self.get_name(),
            'score': best_alignment['score'],
            'identity': best_alignment['identity'],
            'aligned_sequence1': best_alignment['seq1'],
            'aligned_sequence2': best_alignment['seq2'],
            'alignment_length': len(best_alignment['seq1']),
            'gaps': best_alignment['gaps'],
            'complexity': self.get_complexity(),
            'high_scoring_words': len(high_scoring_words),
            'heuristic_alignment': True
        }
    
    def _find_high_scoring_words(self, seq1: str, seq2: str) -> List[Tuple[int, int]]:
        """Encontra palavras de alta pontuação."""
        words = []
        seq1_words = [seq1[i:i+self.word_size] for i in range(len(seq1) - self.word_size + 1)]
        seq2_words = [seq2[i:i+self.word_size] for i in range(len(seq2) - self.word_size + 1)]
        
        for i, word1 in enumerate(seq1_words):
            for j, word2 in enumerate(seq2_words):
                similarity = sum(1 for a, b in zip(word1, word2) if a == b) / self.word_size
                if similarity >= self.threshold:
                    words.append((i, j))
        
        return words
    
    def _extend_alignments(self, seq1: str, seq2: str, words: List[Tuple[int, int]]) -> Dict[str, Any]:
        """Estende os alinhamentos a partir das palavras."""
        if not words:
            return {
                'score': 0,
                'identity': 0.0,
                'seq1': '',
                'seq2': '',
                'gaps': 0
            }
        
        # Simplificação: usa a melhor palavra encontrada
        best_word = max(words, key=lambda w: self._calculate_word_score(seq1, seq2, w))
        i, j = best_word
        
        # Extende para frente e trás
        start_i, start_j = self._extend_backward(seq1, seq2, i, j)
        end_i, end_j = self._extend_forward(seq1, seq2, i + self.word_size, j + self.word_size)
        
        aligned_seq1 = seq1[start_i:end_i]
        aligned_seq2 = seq2[start_j:end_j]
        
        score = self._calculate_alignment_score(aligned_seq1, aligned_seq2)
        identity = self._calculate_identity(aligned_seq1, aligned_seq2)
        
        return {
            'score': score,
            'identity': identity,
            'seq1': aligned_seq1,
            'seq2': aligned_seq2,
            'gaps': aligned_seq1.count('-') + aligned_seq2.count('-')
        }
    
    def _calculate_word_score(self, seq1: str, seq2: str, pos: Tuple[int, int]) -> int:
        """Calcula o score de uma palavra."""
        i, j = pos
        word1 = seq1[i:i+self.word_size]
        word2 = seq2[j:j+self.word_size]
        return sum(1 for a, b in zip(word1, word2) if a == b)
    
    def _extend_backward(self, seq1: str, seq2: str, i: int, j: int) -> Tuple[int, int]:
        """Estende o alinhamento para trás."""
        while i > 0 and j > 0 and seq1[i-1] == seq2[j-1]:
            i -= 1
            j -= 1
        return i, j
    
    def _extend_forward(self, seq1: str, seq2: str, i: int, j: int) -> Tuple[int, int]:
        """Estende o alinhamento para frente."""
        while i < len(seq1) and j < len(seq2) and seq1[i] == seq2[j]:
            i += 1
            j += 1
        return i, j
    
    def _calculate_alignment_score(self, seq1: str, seq2: str) -> int:
        """Calcula o score do alinhamento."""
        return sum(2 if a == b else -1 for a, b in zip(seq1, seq2))
    
    def _calculate_identity(self, seq1: str, seq2: str) -> float:
        """Calcula a percentagem de identidade."""
        matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
        return matches / len(seq1) if len(seq1) > 0 else 0.0
    
    def get_name(self) -> str:
        return "BLAST (Heuristic Alignment)"
    
    def get_complexity(self) -> str:
        return "O(n + m) (heuristic)"


class FastAlignStrategy(AlignmentStrategy):
    """Estratégia rápida para alinhamentos aproximados."""
    
    def align(self, sequence1: str, sequence2: str) -> Dict[str, Any]:
        """Executa alinhamento rápido usando k-mers."""
        # Usa k-mers de tamanho 3 para encontrar similaridades
        k = 3
        kmers1 = self._get_kmers(sequence1, k)
        kmers2 = self._get_kmers(sequence2, k)
        
        # Calcula similaridade baseada em k-mers
        common_kmers = kmers1.intersection(kmers2)
        total_kmers = kmers1.union(kmers2)
        similarity = len(common_kmers) / len(total_kmers) if total_kmers else 0
        
        # Gera alinhamento simplificado
        min_length = min(len(sequence1), len(sequence2))
        aligned_seq1 = sequence1[:min_length]
        aligned_seq2 = sequence2[:min_length]
        
        # Adiciona gaps se necessário
        if len(sequence1) > len(sequence2):
            aligned_seq2 += '-' * (len(sequence1) - len(sequence2))
        elif len(sequence2) > len(sequence1):
            aligned_seq1 += '-' * (len(sequence2) - len(sequence1))
        
        return {
            'strategy': self.get_name(),
            'score': int(similarity * 100),
            'identity': similarity,
            'aligned_sequence1': aligned_seq1,
            'aligned_sequence2': aligned_seq2,
            'alignment_length': len(aligned_seq1),
            'gaps': aligned_seq1.count('-') + aligned_seq2.count('-'),
            'complexity': self.get_complexity(),
            'kmer_similarity': similarity,
            'approximate': True
        }
    
    def _get_kmers(self, sequence: str, k: int) -> set:
        """Gera conjunto de k-mers."""
        return {sequence[i:i+k] for i in range(len(sequence) - k + 1)}
    
    def get_name(self) -> str:
        return "Fast K-mer Alignment"
    
    def get_complexity(self) -> str:
        return "O(n + m)"


class SequenceAligner:
    """Contexto que usa diferentes estratégias de alinhamento."""
    
    def __init__(self, strategy: AlignmentStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: AlignmentStrategy) -> None:
        """Define a estratégia de alinhamento."""
        self._strategy = strategy
    
    def align_sequences(self, sequence1: str, sequence2: str) -> Dict[str, Any]:
        """Alinha duas sequências usando a estratégia atual."""
        return self._strategy.align(sequence1, sequence2)
    
    def get_strategy_info(self) -> str:
        """Retorna informações sobre a estratégia atual."""
        return f"{self._strategy.get_name()} - Complexidade: {self._strategy.get_complexity()}"


class AlignmentBenchmark:
    """Utilitário para benchmarking de diferentes estratégias."""
    
    def __init__(self):
        self.strategies = [
            NeedlemanWunschStrategy(),
            SmithWatermanStrategy(),
            BLASTStrategy(),
            FastAlignStrategy()
        ]
    
    def benchmark_strategies(self, sequence1: str, sequence2: str) -> Dict[str, Dict[str, Any]]:
        """Compara todas as estratégias com as sequências fornecidas."""
        results = {}
        
        for strategy in self.strategies:
            aligner = SequenceAligner(strategy)
            result = aligner.align_sequences(sequence1, sequence2)
            results[strategy.get_name()] = result
        
        return results
    
    def get_best_strategy(self, sequence1: str, sequence2: str, 
                         criteria: str = "identity") -> Tuple[str, Dict[str, Any]]:
        """Retorna a melhor estratégia baseada em um critério."""
        results = self.benchmark_strategies(sequence1, sequence2)
        
        if criteria == "identity":
            best = max(results.items(), key=lambda x: x[1]['identity'])
        elif criteria == "score":
            best = max(results.items(), key=lambda x: x[1]['score'])
        elif criteria == "speed":
            # Simplificação: considera heurísticas mais rápidas
            heuristic_strategies = [name for name, result in results.items() 
                                 if result.get('heuristic_alignment', False) or 
                                    result.get('approximate', False)]
            if heuristic_strategies:
                best_name = heuristic_strategies[0]
                best = (best_name, results[best_name])
            else:
                best = min(results.items(), key=lambda x: len(x[1]['aligned_sequence1']))
        else:
            best = list(results.items())[0]
        
        return best


# Exemplo de uso
def main():
    """Demonstra o uso do padrão Strategy."""
    print("=== Strategy Pattern - Bioinformatics ===\n")
    
    # Sequências de teste
    seq1 = "ATCGATCGATCGATCGATCG"
    seq2 = "ATCGATCGATCGATCGATCG"
    seq3 = "ATCGATCGATCGATCGATCGATCGATCG"
    seq4 = "GCTAGCTAGCTAGCTAGCTA"
    
    # Cria o alinhador com estratégia inicial
    aligner = SequenceAligner(NeedlemanWunschStrategy())
    
    print(f"Estratégia inicial: {aligner.get_strategy_info()}")
    
    # Testa diferentes estratégias
    strategies = [
        ("Global (Needleman-Wunsch)", NeedlemanWunschStrategy()),
        ("Local (Smith-Waterman)", SmithWatermanStrategy()),
        ("Heurística (BLAST)", BLASTStrategy()),
        ("Rápida (K-mer)", FastAlignStrategy())
    ]
    
    print("\n1. Comparando estratégias de alinhamento:")
    print(f"Sequência 1: {seq1}")
    print(f"Sequência 2: {seq2}")
    print()
    
    for name, strategy in strategies:
        aligner.set_strategy(strategy)
        result = aligner.align_sequences(seq1, seq2)
        
        print(f"{name}:")
        print(f"  Score: {result['score']}")
        print(f"  Identidade: {result['identity']:.2%}")
        print(f"  Comprimento: {result['alignment_length']}")
        print(f"  Gaps: {result['gaps']}")
        print(f"  Complexidade: {result['complexity']}")
        print()
    
    # Testa com sequências diferentes
    print("2. Testando com sequências diferentes:")
    print(f"Sequência 1: {seq1}")
    print(f"Sequência 2: {seq4}")
    print()
    
    benchmark = AlignmentBenchmark()
    results = benchmark.benchmark_strategies(seq1, seq4)
    
    for strategy_name, result in results.items():
        print(f"{strategy_name}:")
        print(f"  Score: {result['score']}")
        print(f"  Identidade: {result['identity']:.2%}")
        print()
    
    # Encontra a melhor estratégia
    print("3. Melhor estratégia por diferentes critérios:")
    
    best_identity = benchmark.get_best_strategy(seq1, seq4, "identity")
    best_score = benchmark.get_best_strategy(seq1, seq4, "score")
    best_speed = benchmark.get_best_strategy(seq1, seq4, "speed")
    
    print(f"  Por identidade: {best_identity[0]} ({best_identity[1]['identity']:.2%})")
    print(f"  Por score: {best_score[0]} ({best_score[1]['score']})")
    print(f"  Por velocidade: {best_speed[0]}")


if __name__ == "__main__":
    main()
