"""
Padrões Comportamentais - Design Patterns GoF

Este módulo contém os 11 padrões comportamentais clássicos:
- Chain of Responsibility: Passa requisições por corrente de handlers
- Command: Encapsula requisições como objetos
- Iterator: Acessa elementos de coleções sem expor estrutura
- Mediator: Centraliza comunicação entre objetos
- Memento: Salva/restaura estado de objetos
- Observer: Notifica múltiplos objetos sobre eventos
- State: Muda comportamento baseado em estado interno
- Strategy: Define família de algoritmos intercambiáveis
- Template Method: Define esqueleto de algoritmo
- Visitor: Adiciona operações sem modificar classes
"""

from .chain_of_responsibility import *
from .command import *
from .iterator import *
from .mediator import *
from .memento import *
from .observer import *
from .state import *
from .strategy import *
from .template_method import *
from .visitor import *

__all__ = [
    # Chain of Responsibility
    'SequenceRequest',
    'SequenceHandler', 
    'DNAValidator',
    'RNAValidator',
    'SequenceQualityChecker',
    'ContaminationChecker',
    'SequenceProcessor',
    'SequenceAnalysisSystem',
    
    # Command
    'Command',
    'SequenciarCommand',
    'AlinharCommand',
    'AnalisarCommand',
    'InvocadorComandos',
    
    # Iterator
    'ResultadoAnalise',
    'TipoDado',
    'IteratorResultados',
    'ColecaoResultados',
    'ResultadosSequenciamento',
    'ResultadosProteomicos',
    
    # Mediator
    'ComponenteLaboratorial',
    'MediatorLaboratorial',
    'Sequenciador',
    'Alinhador',
    'Analisador',
    'MediatorConcreto',
    
    # Memento
    'ExperimentMemento',
    'Originator',
    'GenomicExperiment',
    'Caretaker',
    'ExperimentManager',
    
    # Observer
    'Evento',
    'TipoEvento',
    'Observador',
    'Sujeito',
    'Pesquisador',
    'SistemaAlerta',
    'AnaliseGenomica',
    
    # State
    'EstadoEquipamento',
    'DisponivelState',
    'EmUsoState',
    'ManutencaoState',
    'EquipamentoLaboratorial',
    
    # Strategy
    'AlignmentStrategy',
    'NeedlemanWunschStrategy',
    'SmithWatermanStrategy',
    'BLASTStrategy',
    'FastAlignStrategy',
    'SequenceAligner',
    'AlignmentBenchmark',
    
    # Template Method
    'PipelineAnalise',
    'PipelineGenomica',
    'PipelineProteomica',
    'PipelineTranscriptomica',
    
    # Visitor
    'ElementoGenetico',
    'Gene',
    'GeneProteina',
    'GeneRegulador',
    'GeneEstrutural',
    'GeneHousekeeping',
    'VisitorGenetico',
    'AnalisadorMolecular',
    'OtimizadorTerapeutico',
]