"""
Memento Pattern - Padrão Comportamental

Permite que você salve e restaure o estado anterior de um objeto sem revelar 
os detalhes de sua implementação.

Este padrão é usado no sistema de bioinformática para salvar e restaurar estados
de experimentos, permitindo desfazer operações de análise genômica.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import copy
import datetime
import json


class ExperimentMemento:
    """Memento que armazena o estado de um experimento."""
    
    def __init__(self, state: Dict[str, Any], timestamp: Optional[datetime.datetime] = None):
        self._state = copy.deepcopy(state)
        self._timestamp = timestamp or datetime.datetime.now()
        self._name = f"Experiment_{self._timestamp.strftime('%Y%m%d_%H%M%S')}"
    
    @property
    def state(self) -> Dict[str, Any]:
        """Retorna o estado armazenado (somente leitura)."""
        return copy.deepcopy(self._state)
    
    @property
    def timestamp(self) -> datetime.datetime:
        """Retorna o timestamp do memento."""
        return self._timestamp
    
    @property
    def name(self) -> str:
        """Retorna o nome do memento."""
        return self._name
    
    def get_summary(self) -> str:
        """Retorna um resumo do estado armazenado."""
        sequence_length = len(self._state.get('sequence', ''))
        analysis_type = self._state.get('analysis_type', 'Unknown')
        status = self._state.get('status', 'Unknown')
        
        return f"{self.name} - {analysis_type} - {sequence_length}bp - {status}"


class Originator(ABC):
    """Interface base para objetos que podem criar mementos."""
    
    @abstractmethod
    def save(self) -> ExperimentMemento:
        """Salva o estado atual em um memento."""
        pass
    
    @abstractmethod
    def restore(self, memento: ExperimentMemento) -> None:
        """Restaura o estado a partir de um memento."""
        pass


class GenomicExperiment(Originator):
    """Representa um experimento genômico que pode salvar/restaurar estados."""
    
    def __init__(self, experiment_id: str, sequence: str, analysis_type: str):
        self.experiment_id = experiment_id
        self.sequence = sequence.upper()
        self.analysis_type = analysis_type
        self.status = "Created"
        self.results: Dict[str, Any] = {}
        self.parameters: Dict[str, Any] = {}
        self.history: List[str] = []
        self.created_at = datetime.datetime.now()
        self.modified_at = self.created_at
        
        self._add_history(f"Experiment {experiment_id} created")
    
    def _add_history(self, event: str) -> None:
        """Adiciona um evento ao histórico."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {event}")
        self.modified_at = datetime.datetime.now()
    
    def set_parameters(self, **kwargs) -> None:
        """Define parâmetros para o experimento."""
        self.parameters.update(kwargs)
        self._add_history(f"Parameters updated: {', '.join(kwargs.keys())}")
    
    def run_analysis(self) -> None:
        """Executa a análise do experimento."""
        self.status = "Running"
        self._add_history("Analysis started")
        
        # Simulação de diferentes tipos de análise
        if self.analysis_type == "alignment":
            self._run_alignment_analysis()
        elif self.analysis_type == "assembly":
            self._run_assembly_analysis()
        elif self.analysis_type == "annotation":
            self._run_annotation_analysis()
        else:
            self._run_basic_analysis()
        
        self.status = "Completed"
        self._add_history("Analysis completed")
    
    def _run_alignment_analysis(self) -> None:
        """Executa análise de alinhamento."""
        # Simulação de resultados de alinhamento
        self.results = {
            'alignment_score': len(self.sequence) * 0.85,
            'matches': len(self.sequence) // 2,
            'mismatches': len(self.sequence) // 10,
            'gaps': len(self.sequence) // 20,
            'reference': "hg38",
            'coverage': 0.95
        }
    
    def _run_assembly_analysis(self) -> None:
        """Executa análise de montagem."""
        # Simulação de resultados de montagem
        self.results = {
            'contigs': len(self.sequence) // 1000,
            'n50': 5000,
            'total_length': len(self.sequence),
            'gc_content': self._calculate_gc_content(),
            'completeness': 0.88
        }
    
    def _run_annotation_analysis(self) -> None:
        """Executa análise de anotação."""
        # Simulação de resultados de anotação
        self.results = {
            'genes_found': len(self.sequence) // 3000,
            'proteins_found': len(self.sequence) // 3500,
            'functional_annotations': len(self.sequence) // 5000,
            'pathways': ['glycolysis', 'citric_acid_cycle'],
            'go_terms': 42
        }
    
    def _run_basic_analysis(self) -> None:
        """Executa análise básica."""
        self.results = {
            'length': len(self.sequence),
            'gc_content': self._calculate_gc_content(),
            'complexity_score': self._calculate_complexity(),
            'quality_metrics': {
                'phred_score': 35.2,
                'read_depth': 150.5
            }
        }
    
    def _calculate_gc_content(self) -> float:
        """Calcula o conteúdo GC da sequência."""
        if not self.sequence:
            return 0.0
        gc_count = sum(1 for base in self.sequence if base in ['G', 'C'])
        return gc_count / len(self.sequence)
    
    def _calculate_complexity(self) -> float:
        """Calcula um score de complexidade da sequência."""
        # Simplificação: baseado na diversidade de bases
        unique_bases = len(set(self.sequence))
        return unique_bases / 4.0  # 4 bases possíveis
    
    def modify_sequence(self, new_sequence: str) -> None:
        """Modifica a sequência do experimento."""
        old_length = len(self.sequence)
        self.sequence = new_sequence.upper()
        new_length = len(self.sequence)
        
        self.status = "Modified"
        self._add_history(f"Sequence modified: {old_length}bp -> {new_length}bp")
    
    def reset_results(self) -> None:
        """Reseta os resultados do experimento."""
        self.results.clear()
        self.status = "Reset"
        self._add_history("Results reset")
    
    def save(self) -> ExperimentMemento:
        """Salva o estado atual em um memento."""
        state = {
            'experiment_id': self.experiment_id,
            'sequence': self.sequence,
            'analysis_type': self.analysis_type,
            'status': self.status,
            'results': self.results,
            'parameters': self.parameters,
            'history': self.history.copy(),
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
        return ExperimentMemento(state)
    
    def restore(self, memento: ExperimentMemento) -> None:
        """Restaura o estado a partir de um memento."""
        state = memento.state
        
        self.experiment_id = state['experiment_id']
        self.sequence = state['sequence']
        self.analysis_type = state['analysis_type']
        self.status = state['status']
        self.results = state['results']
        self.parameters = state['parameters']
        self.history = state['history'].copy()
        self.created_at = state['created_at']
        self.modified_at = state['modified_at']
    
    def get_info(self) -> str:
        """Retorna informações sobre o experimento."""
        return (f"Experiment {self.experiment_id} - {self.analysis_type} - "
                f"{self.status} - {len(self.sequence)}bp")


class Caretaker:
    """Cuidador que gerencia os mementos."""
    
    def __init__(self, max_mementos: int = 10):
        self._mementos: List[ExperimentMemento] = []
        self._max_mementos = max_mementos
        self._current_index = -1
    
    def add_memento(self, memento: ExperimentMemento) -> None:
        """Adiciona um memento à coleção."""
        # Remove mementos futuros se estamos no meio da lista
        if self._current_index < len(self._mementos) - 1:
            self._mementos = self._mementos[:self._current_index + 1]
        
        self._mementos.append(memento)
        self._current_index = len(self._mementos) - 1
        
        # Mantém o limite máximo de mementos
        if len(self._mementos) > self._max_mementos:
            self._mementos.pop(0)
            self._current_index -= 1
    
    def get_memento(self, index: int) -> Optional[ExperimentMemento]:
        """Retorna um memento específico."""
        if 0 <= index < len(self._mementos):
            return self._mementos[index]
        return None
    
    def get_current_memento(self) -> Optional[ExperimentMemento]:
        """Retorna o memento atual."""
        if 0 <= self._current_index < len(self._mementos):
            return self._mementos[self._current_index]
        return None
    
    def get_previous_memento(self) -> Optional[ExperimentMemento]:
        """Retorna o memento anterior."""
        if self._current_index > 0:
            self._current_index -= 1
            return self._mementos[self._current_index]
        return None
    
    def get_next_memento(self) -> Optional[ExperimentMemento]:
        """Retorna o próximo memento."""
        if self._current_index < len(self._mementos) - 1:
            self._current_index += 1
            return self._mementos[self._current_index]
        return None
    
    def list_mementos(self) -> List[str]:
        """Lista todos os mementos disponíveis."""
        return [memento.get_summary() for memento in self._mementos]
    
    def clear_mementos(self) -> None:
        """Limpa todos os mementos."""
        self._mementos.clear()
        self._current_index = -1
    
    def get_memento_count(self) -> int:
        """Retorna o número de mementos."""
        return len(self._mementos)


class ExperimentManager:
    """Gerenciador de experimentos com suporte a undo/redo."""
    
    def __init__(self):
        self.experiment: Optional[GenomicExperiment] = None
        self.caretaker = Caretaker()
    
    def create_experiment(self, experiment_id: str, sequence: str, 
                         analysis_type: str) -> None:
        """Cria um novo experimento."""
        self.experiment = GenomicExperiment(experiment_id, sequence, analysis_type)
        self.caretaker.clear_mementos()
        self._save_state()
    
    def _save_state(self) -> None:
        """Salva o estado atual do experimento."""
        if self.experiment:
            memento = self.experiment.save()
            self.caretaker.add_memento(memento)
    
    def modify_experiment(self, **kwargs) -> None:
        """Modifica o experimento."""
        if not self.experiment:
            raise ValueError("No experiment created")
        
        if 'sequence' in kwargs:
            self.experiment.modify_sequence(kwargs['sequence'])
        
        if 'parameters' in kwargs:
            self.experiment.set_parameters(**kwargs['parameters'])
        
        if 'analysis_type' in kwargs:
            self.experiment.analysis_type = kwargs['analysis_type']
            self.experiment._add_history(f"Analysis type changed to {kwargs['analysis_type']}")
        
        self._save_state()
    
    def run_analysis(self) -> None:
        """Executa a análise do experimento."""
        if not self.experiment:
            raise ValueError("No experiment created")
        
        self.experiment.run_analysis()
        self._save_state()
    
    def undo(self) -> bool:
        """Desfaz a última alteração."""
        if not self.experiment:
            return False
        
        previous_memento = self.caretaker.get_previous_memento()
        if previous_memento:
            self.experiment.restore(previous_memento)
            return True
        return False
    
    def redo(self) -> bool:
        """Refaz a alteração desfeita."""
        if not self.experiment:
            return False
        
        next_memento = self.caretaker.get_next_memento()
        if next_memento:
            self.experiment.restore(next_memento)
            return True
        return False
    
    def get_history(self) -> List[str]:
        """Retorna o histórico de estados."""
        return self.caretaker.list_mementos()
    
    def get_experiment_info(self) -> str:
        """Retorna informações do experimento atual."""
        if not self.experiment:
            return "No experiment created"
        return self.experiment.get_info()


# Exemplo de uso
def main():
    """Demonstra o uso do padrão Memento."""
    print("=== Memento Pattern - Bioinformatics ===\n")
    
    # Cria o gerenciador de experimentos
    manager = ExperimentManager()
    
    # Cria um experimento
    print("1. Criando experimento...")
    manager.create_experiment("EXP001", "ATCGATCGATCGATCGATCG", "alignment")
    print(f"   {manager.get_experiment_info()}")
    
    # Modifica o experimento
    print("\n2. Modificando parâmetros...")
    manager.modify_experiment(parameters={"threshold": 0.8, "algorithm": "blast"})
    print(f"   {manager.get_experiment_info()}")
    
    # Executa análise
    print("\n3. Executando análise...")
    manager.run_analysis()
    print(f"   {manager.get_experiment_info()}")
    
    # Modifica a sequência
    print("\n4. Modificando sequência...")
    manager.modify_experiment(sequence="ATCGATCGATCGATCGATCGATCGATCG")
    print(f"   {manager.get_experiment_info()}")
    
    # Mostra histórico
    print("\n5. Histórico de estados:")
    for i, state in enumerate(manager.get_history()):
        print(f"   {i}: {state}")
    
    # Testa undo/redo
    print("\n6. Testando Undo/Redo:")
    
    print("   Undo 1:")
    if manager.undo():
        print(f"     {manager.get_experiment_info()}")
    
    print("   Undo 2:")
    if manager.undo():
        print(f"     {manager.get_experiment_info()}")
    
    print("   Redo 1:")
    if manager.redo():
        print(f"     {manager.get_experiment_info()}")
    
    print("   Redo 2:")
    if manager.redo():
        print(f"     {manager.get_experiment_info()}")


if __name__ == "__main__":
    main()
