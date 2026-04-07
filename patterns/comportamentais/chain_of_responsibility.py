"""
Chain of Responsibility Pattern - Padrão Comportamental

Permite que você passe pedidos por uma corrente de handlers. Ao receber um pedido, 
cada handler decide se processa o pedido ou passa para o próximo handler da corrente.

Este padrão é usado no sistema de bioinformática para processar sequências de DNA
através de diferentes filtros e validações.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import logging


class SequenceRequest:
    """Representa uma requisição de processamento de sequência."""
    
    def __init__(self, sequence: str, sequence_type: str = "DNA", metadata: Optional[Dict] = None):
        self.sequence = sequence.upper()
        self.sequence_type = sequence_type
        self.metadata = metadata or {}
        self.processing_steps: List[str] = []
        self.is_valid = True
        self.errors: List[str] = []
    
    def add_step(self, step: str) -> None:
        """Adiciona uma etapa de processamento."""
        self.processing_steps.append(step)
    
    def add_error(self, error: str) -> None:
        """Adiciona um erro de processamento."""
        self.errors.append(error)
        self.is_valid = False


class SequenceHandler(ABC):
    """Interface base para handlers de sequência."""
    
    def __init__(self, name: str):
        self.name = name
        self._next_handler: Optional['SequenceHandler'] = None
    
    def set_next(self, handler: 'SequenceHandler') -> 'SequenceHandler':
        """Define o próximo handler na corrente."""
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, request: SequenceRequest) -> SequenceRequest:
        """Processa a requisição ou passa para o próximo handler."""
        pass
    
    def _pass_to_next(self, request: SequenceRequest) -> SequenceRequest:
        """Passa a requisição para o próximo handler."""
        if self._next_handler:
            return self._next_handler.handle(request)
        return request


class DNAValidator(SequenceHandler):
    """Valida sequências de DNA."""
    
    def __init__(self):
        super().__init__("DNA Validator")
        self.valid_bases = {'A', 'T', 'G', 'C'}
    
    def handle(self, request: SequenceRequest) -> SequenceRequest:
        """Valida se a sequência contém apenas bases válidas de DNA."""
        if request.sequence_type != "DNA":
            return self._pass_to_next(request)
        
        invalid_bases = set(request.sequence) - self.valid_bases
        if invalid_bases:
            request.add_error(f"Invalid DNA bases found: {', '.join(invalid_bases)}")
            return request
        
        request.add_step(f"DNA validation passed - Length: {len(request.sequence)}")
        logging.info(f"DNA sequence validated: {request.sequence[:20]}...")
        return self._pass_to_next(request)


class RNAValidator(SequenceHandler):
    """Valida sequências de RNA."""
    
    def __init__(self):
        super().__init__("RNA Validator")
        self.valid_bases = {'A', 'U', 'G', 'C'}
    
    def handle(self, request: SequenceRequest) -> SequenceRequest:
        """Valida se a sequência contém apenas bases válidas de RNA."""
        if request.sequence_type != "RNA":
            return self._pass_to_next(request)
        
        invalid_bases = set(request.sequence) - self.valid_bases
        if invalid_bases:
            request.add_error(f"Invalid RNA bases found: {', '.join(invalid_bases)}")
            return request
        
        request.add_step(f"RNA validation passed - Length: {len(request.sequence)}")
        logging.info(f"RNA sequence validated: {request.sequence[:20]}...")
        return self._pass_to_next(request)


class SequenceQualityChecker(SequenceHandler):
    """Verifica a qualidade da sequência."""
    
    def __init__(self, min_quality_score: float = 0.8):
        super().__init__("Quality Checker")
        self.min_quality_score = min_quality_score
    
    def handle(self, request: SequenceRequest) -> SequenceRequest:
        """Verifica a qualidade baseada em métricas da sequência."""
        # Simulação de cálculo de qualidade
        gc_content = self._calculate_gc_content(request.sequence)
        quality_score = self._calculate_quality_score(request.sequence, gc_content)
        
        request.metadata['gc_content'] = gc_content
        request.metadata['quality_score'] = quality_score
        
        if quality_score < self.min_quality_score:
            request.add_error(f"Low quality score: {quality_score:.2f} < {self.min_quality_score}")
            return request
        
        request.add_step(f"Quality check passed - Score: {quality_score:.2f}")
        logging.info(f"Quality check passed: {quality_score:.2f}")
        return self._pass_to_next(request)
    
    def _calculate_gc_content(self, sequence: str) -> float:
        """Calcula o conteúdo GC da sequência."""
        if not sequence:
            return 0.0
        gc_count = sum(1 for base in sequence if base in ['G', 'C'])
        return gc_count / len(sequence)
    
    def _calculate_quality_score(self, sequence: str, gc_content: float) -> float:
        """Calcula um score de qualidade simulado."""
        # Fatores que influenciam a qualidade
        length_factor = min(len(sequence) / 1000, 1.0)  # Sequências mais longas são melhores
        gc_factor = 1.0 - abs(gc_content - 0.5) * 2  # GC próximo a 50% é ideal
        
        return (length_factor * 0.6 + gc_factor * 0.4)


class ContaminationChecker(SequenceHandler):
    """Verifica contaminação na sequência."""
    
    def __init__(self):
        super().__init__("Contamination Checker")
        self.contaminants = ['AAAAAA', 'TTTTTT', 'GGGGGG', 'CCCCCC']  # Simplificado
    
    def handle(self, request: SequenceRequest) -> SequenceRequest:
        """Verifica se há contaminação na sequência."""
        for contaminant in self.contaminants:
            if contaminant in request.sequence:
                request.add_error(f"Contamination detected: {contaminant}")
                return request
        
        request.add_step("Contamination check passed")
        logging.info("No contamination detected")
        return self._pass_to_next(request)


class SequenceProcessor(SequenceHandler):
    """Processa a sequência para análise."""
    
    def __init__(self):
        super().__init__("Sequence Processor")
    
    def handle(self, request: SequenceRequest) -> SequenceRequest:
        """Realiza o processamento final da sequência."""
        if not request.is_valid:
            return request
        
        # Simulação de processamento
        processed_data = {
            'original_sequence': request.sequence,
            'length': len(request.sequence),
            'reverse_complement': self._get_reverse_complement(request.sequence),
            'processing_steps': request.processing_steps,
            'metadata': request.metadata
        }
        
        request.metadata['processed_data'] = processed_data
        request.add_step("Sequence processing completed")
        logging.info(f"Sequence processed successfully")
        return self._pass_to_next(request)
    
    def _get_reverse_complement(self, sequence: str) -> str:
        """Gera o reverse complement da sequência."""
        complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'U': 'A'}
        return ''.join(complement_map.get(base, base) for base in reversed(sequence))


class SequenceAnalysisSystem:
    """Sistema de análise que usa a cadeia de responsabilidade."""
    
    def __init__(self):
        self.setup_handler_chain()
    
    def setup_handler_chain(self):
        """Configura a cadeia de handlers."""
        # Cria os handlers
        validator = DNAValidator()
        rna_validator = RNAValidator()
        quality_checker = SequenceQualityChecker()
        contamination_checker = ContaminationChecker()
        processor = SequenceProcessor()
        
        # Configura a cadeia: DNA -> RNA -> Quality -> Contamination -> Processing
        validator.set_next(rna_validator).set_next(quality_checker).set_next(
            contamination_checker).set_next(processor)
        
        self.handler_chain = validator
    
    def analyze_sequence(self, sequence: str, sequence_type: str = "DNA", 
                        metadata: Optional[Dict] = None) -> SequenceRequest:
        """Analisa uma sequência usando a cadeia de handlers."""
        request = SequenceRequest(sequence, sequence_type, metadata)
        return self.handler_chain.handle(request)


# Exemplo de uso
def main():
    """Demonstra o uso do padrão Chain of Responsibility."""
    logging.basicConfig(level=logging.INFO)
    
    # Cria o sistema de análise
    analysis_system = SequenceAnalysisSystem()
    
    # Testa diferentes sequências
    test_sequences = [
        ("ATCGATCGATCG", "DNA"),  # Sequência DNA válida
        ("AUCGAUCGAUCG", "RNA"),  # Sequência RNA válida
        ("ATCGXATCG", "DNA"),     # Sequência DNA com base inválida
        ("AAAAAAATCG", "DNA"),    # Sequência com possível contaminação
        ("ATCG", "DNA"),          # Sequência muito curta (baixa qualidade)
    ]
    
    print("=== Chain of Responsibility Pattern - Bioinformatics ===\n")
    
    for sequence, seq_type in test_sequences:
        print(f"Analisando sequência {seq_type}: {sequence}")
        result = analysis_system.analyze_sequence(sequence, seq_type)
        
        if result.is_valid:
            print(f"  Status: VÁLIDA")
            print(f"  Passos: {' -> '.join(result.processing_steps)}")
            print(f"  Qualidade: {result.metadata.get('quality_score', 'N/A'):.2f}")
            print(f"  Conteúdo GC: {result.metadata.get('gc_content', 'N/A'):.2%}")
        else:
            print(f"  Status: INVÁLIDA")
            print(f"  Erros: {'; '.join(result.errors)}")
        print()


if __name__ == "__main__":
    main()
