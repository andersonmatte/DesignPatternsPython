"""
Padrões Criacionais - Design Patterns GoF

Este módulo contém os 5 padrões criacionais clássicos:
- Abstract Factory: Cria famílias de objetos relacionados
- Builder: Constrói objetos complexos passo a passo
- Factory Method: Define interface para criação de objetos
- Prototype: Cria objetos copiando outros existentes
- Singleton: Garante uma única instância global
"""

from .abstract_factory import *
from .builder import *
from .factory_method import *
from .prototype import *
from .singleton import *

__all__ = [
    # Abstract Factory
    'FabricaEquipamentos',
    'FabricaEquipamentosGenetica',
    'FabricaEquipamentosBioquimica',
    'SequenciadorDNA',
    'AlinhadorGenetico',
    'Espectrometro',
    'Cromatografo',
    
    # Builder
    'ExperimentoBuilder',
    'ExperimentoGenomicoBuilder',
    'ExperimentoProteomicoBuilder',
    'DiretorExperimento',
    
    # Factory Method
    'AnalisadorFactory',
    'AnalisadorFASTA',
    'AnalisadorGenBank',
    'AnalisadorProteina',
    
    # Prototype
    'SequenciaBiologica',
    'Proteina',
    'Gene',
    'RegistroPrototipos',
    
    # Singleton
    'LaboratorioSingleton',
    'GerenteRecursos',
    'CacheResultados',
]