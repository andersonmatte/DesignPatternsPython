from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum


class TipoAnalise(Enum):
    SEQUENCIAMENTO = "Sequenciamento"
    ALINHAMENTO = "Alinhamento"
    EXPRESSAO = "Expressão Gênica"
    PROTEOMICA = "Proteômica"


class AlgoritmoAnalise(ABC):
    """Interface base para algoritmos de análise."""
    
    @abstractmethod
    def processar(self, dados: Any) -> Dict[str, Any]:
        """Processa os dados usando o algoritmo específico."""
        pass


class NeedlemanWunsch(AlgoritmoAnalise):
    """Algoritmo de alinhamento global."""
    
    def processar(self, dados: Any) -> Dict[str, Any]:
        return {
            "algoritmo": "Needleman-Wunsch",
            "tipo": "Alinhamento Global",
            "resultado": "Alinhamento executado com sucesso"
        }


class BLAST(AlgoritmoAnalise):
    """Algoritmo de busca em bancos de dados."""
    
    def processar(self, dados: Any) -> Dict[str, Any]:
        return {
            "algoritmo": "BLAST",
            "tipo": "Busca Local",
            "resultado": "Busca executada com sucesso"
        }


class SmithWaterman(AlgoritmoAnalise):
    """Algoritmo de alinhamento local."""
    
    def processar(self, dados: Any) -> Dict[str, Any]:
        return {
            "algoritmo": "Smith-Waterman",
            "tipo": "Alinhamento Local",
            "resultado": "Alinhamento local executado com sucesso"
        }


class AnaliseGenomica:
    """Representa uma análise genômica com tipo e algoritmo específicos."""
    
    def __init__(self, nome: str, tipo: TipoAnalise, algoritmo: AlgoritmoAnalise):
        self.nome = nome
        self.tipo = tipo
        self.algoritmo = algoritmo
        self.dados_entrada: Any = None
        self.resultado: Dict[str, Any] = None
    
    def executar_analise(self, dados: Any) -> Dict[str, Any]:
        """Executa a análise usando o algoritmo configurado."""
        self.dados_entrada = dados
        self.resultado = self.algoritmo.processar(dados)
        return self.resultado
    
    def __str__(self) -> str:
        return f"AnaliseGenomica(nome={self.nome}, tipo={self.tipo.value})"


class AnaliseBio(ABC):
    """Interface base para análises biológicas."""
    
    @abstractmethod
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa a análise."""
        pass


class AnaliseBasica(AnaliseBio):
    """Implementação básica de análise."""
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        return {
            "tipo": "Análise Básica",
            "status": "Concluída",
            "dados_processados": len(str(dados))
        }


class ProtocoloExperimental:
    """Representa um protocolo experimental com múltiplos parâmetros."""
    
    def __init__(self):
        self.nome_pesquisador: str = ""
        self.volume_amostra: float = 0.0
        self.tipo_analise: str = ""
        self.metodologia: str = ""
        self.parametros_adicionais: Dict[str, Any] = {}
    
    def __str__(self) -> str:
        return f"""ProtocoloExperimental(
            pesquisador={self.nome_pesquisador},
            volume={self.volume_amostra}ml,
            analise={self.tipo_analise},
            metodologia={self.metodologia}
        )"""
