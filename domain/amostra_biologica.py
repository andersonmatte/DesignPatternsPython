from abc import ABC, abstractmethod
from typing import Any, Dict, List
import copy


class AmostraBiologica:
    """Representa uma amostra biológica para análise genômica."""
    
    def __init__(self, codigo: str, tipo: str = "DNA"):
        self.codigo = codigo
        self.tipo = tipo  # DNA, RNA, Proteína
        self.dados: Dict[str, Any] = {}
        self.marcadores: List[str] = []
    
    def adicionar_dado(self, chave: str, valor: Any) -> None:
        """Adiciona dados à amostra."""
        self.dados[chave] = valor
    
    def adicionar_marcador(self, marcador: str) -> None:
        """Adiciona marcador genético à amostra."""
        self.marcadores.append(marcador)
    
    def clonar(self) -> 'AmostraBiologica':
        """Cria uma cópia exata da amostra para experimentos replicáveis."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return f"AmostraBiologica(codigo={self.codigo}, tipo={self.tipo})"


class ComponenteGenetico(ABC):
    """Interface base para componentes genéticos."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.filhos: List['ComponenteGenetico'] = []
    
    @abstractmethod
    def adicionar(self, componente: 'ComponenteGenetico') -> None:
        """Adiciona um componente filho."""
        pass
    
    @abstractmethod
    def remover(self, componente: 'ComponenteGenetico') -> None:
        """Remove um componente filho."""
        pass
    
    @abstractmethod
    def exibir(self, indent: int = 0) -> str:
        """Exibe a estrutura do componente."""
        pass
    
    def __str__(self) -> str:
        return self.exibir()


class Nucleotideo(ComponenteGenetico):
    """Representa um nucleotídeo individual."""
    
    def __init__(self, base: str):
        super().__init__(f"Nucleotideo_{base}")
        self.base = base
    
    def adicionar(self, componente: ComponenteGenetico) -> None:
        raise Exception("Nucleotídeo não pode ter filhos")
    
    def remover(self, componente: ComponenteGenetico) -> None:
        raise Exception("Nucleotídeo não pode ter filhos")
    
    def exibir(self, indent: int = 0) -> str:
        return "  " * indent + f"Nucleotideo: {self.base}"


class Gene(ComponenteGenetico):
    """Representa um gene composto por múltiplos nucleotídeos."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
    
    def adicionar(self, componente: ComponenteGenetico) -> None:
        self.filhos.append(componente)
    
    def remover(self, componente: ComponenteGenetico) -> None:
        self.filhos.remove(componente)
    
    def exibir(self, indent: int = 0) -> str:
        resultado = "  " * indent + f"Gene: {self.nome}\n"
        for filho in self.filhos:
            resultado += filho.exibir(indent + 1) + "\n"
        return resultado.rstrip()


class Proteina(ComponenteGenetico):
    """Representa uma proteína composta por aminoácidos."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.sequencia_aminoacidos: List[str] = []
    
    def adicionar(self, componente: ComponenteGenetico) -> None:
        self.filhos.append(componente)
    
    def remover(self, componente: ComponenteGenetico) -> None:
        self.filhos.remove(componente)
    
    def adicionar_aminoacido(self, aminoacido: str) -> None:
        """Adiciona um aminoácido à sequência."""
        self.sequencia_aminoacidos.append(aminoacido)
    
    def exibir(self, indent: int = 0) -> str:
        resultado = "  " * indent + f"Proteína: {self.nome}\n"
        resultado += "  " * (indent + 1) + f"Sequência: {''.join(self.sequencia_aminoacidos)}\n"
        for filho in self.filhos:
            resultado += filho.exibir(indent + 1) + "\n"
        return resultado.rstrip()


class ResultadoAnalise:
    """Representa o resultado de uma análise bioinformática."""
    
    def __init__(self, tipo_analise: str, dados: Dict[str, Any]):
        self.tipo_analise = tipo_analise
        self.dados = dados
        self.timestamp = None
    
    def __str__(self) -> str:
        return f"ResultadoAnalise(tipo={self.tipo_analise}, dados={len(self.dados)} itens)"


class EquipamentoLaboratorial:
    """Representa equipamentos de laboratório."""
    
    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.tipo = tipo
        self.disponivel = True
        self.em_uso_por: str = None
    
    def reservar(self, pesquisador: str) -> bool:
        """Reserva o equipamento para um pesquisador."""
        if self.disponivel:
            self.disponivel = False
            self.em_uso_por = pesquisador
            return True
        return False
    
    def liberar(self) -> None:
        """Libera o equipamento."""
        self.disponivel = True
        self.em_uso_por = None
    
    def __str__(self) -> str:
        status = "Disponível" if self.disponivel else f"Em uso por {self.em_uso_por}"
        return f"Equipamento({self.nome}, {self.tipo}, {status})"
