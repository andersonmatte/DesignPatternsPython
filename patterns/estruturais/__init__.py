"""
Padrões Estruturais - Design Patterns GoF

Este módulo contém os 7 padrões estruturais clássicos:
- Adapter: Permite colaboração entre interfaces incompatíveis
- Bridge: Divide classe em abstração e implementação
- Composite: Compõe objetos em estruturas de árvore
- Decorator: Adiciona comportamentos a objetos dinamicamente
- Facade: Fornece interface simplificada para subsistemas complexos
- Flyweight: Compartilha estado para otimizar memória
- Proxy: Fornece substituto para controlar acesso a objetos
"""

from .adapter import *
from .bridge import *
from .composite import *
from .decorator import *
from .facade import *
from .flyweight import *
from .proxy import *

__all__ = [
    # Adapter
    'AnalisadorLegado',
    'AnalisadorModerno',
    'AdapterAnalisador',
    'SistemaAnalise',
    
    # Bridge
    'ImplementacaoEquipamento',
    'SequenciadorIllumina',
    'SequenciadorOxfordNanopore',
    'AbstracaoEquipamento',
    'EquipamentoBasico',
    'EquipamentoAvancado',
    
    # Composite
    'ComponenteAnalise',
    'AnaliseAtomica',
    'AnaliseComposta',
    'PipelineAnalise',
    
    # Decorator
    'SequenciadorBase',
    'SequenciadorDecorator',
    'ValidadorQualidadeDecorator',
    'LoggerDecorator',
    'CacheDecorator',
    'FiltroContaminacaoDecorator',
    
    # Facade
    'SistemaBioinformatica',
    'GerenciadorSequenciamento',
    'GerenciadorAlinhamento',
    'GerenciadorAnalise',
    
    # Flyweight
    'FlyweightSequencia',
    'FlyweightFactory',
    'SequenciaFlyweight',
    
    # Proxy
    'BancoDadosGeneticos',
    'BancoDadosGeneticosProxy',
    'CacheProxy',
    'SegurancaProxy',
    'LoggingProxy',
]