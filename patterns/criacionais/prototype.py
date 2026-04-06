from abc import ABC, abstractmethod
import copy
from typing import List, Dict, Any
from domain.amostra_biologica import AmostraBiologica


class PrototipoAmostra(ABC):
    """Interface base para protótipos de amostras biológicas."""
    
    @abstractmethod
    def clonar(self) -> 'PrototipoAmostra':
        """Cria uma cópia exata do protótipo."""
        pass
    
    @abstractmethod
    def clonar_profundo(self) -> 'PrototipoAmostra':
        """Cria uma cópia profunda do protótipo."""
        pass


class AmostraDNA(PrototipoAmostra):
    """Amostra de DNA que pode ser clonada para experimentos replicáveis."""
    
    def __init__(self, codigo: str, sequencia: str = ""):
        self.codigo = codigo
        self.sequencia = sequencia
        self.concentracao_ng_ul: float = 0.0
        self.pureza_260_280: float = 0.0
        self.marcadores_geneticos: List[str] = []
        self.metadados: Dict[str, Any] = {}
    
    def adicionar_marcador(self, marcador: str) -> None:
        """Adiciona um marcador genético à amostra."""
        self.marcadores_geneticos.append(marcador)
    
    def definir_concentracao(self, concentracao: float) -> None:
        """Define a concentração de DNA em ng/μL."""
        self.concentracao_ng_ul = concentracao
    
    def definir_pureza(self, pureza: float) -> None:
        """Define a pureza (razão 260/280)."""
        self.pureza_260_280 = pureza
    
    def adicionar_metadado(self, chave: str, valor: Any) -> None:
        """Adiciona metadados à amostra."""
        self.metadados[chave] = valor
    
    def clonar(self) -> 'AmostraDNA':
        """Cria uma cópia superficial da amostra."""
        nova_amostra = AmostraDNA(self.codigo, self.sequencia)
        nova_amostra.concentracao_ng_ul = self.concentracao_ng_ul
        nova_amostra.pureza_260_280 = self.pureza_260_280
        nova_amostra.marcadores_geneticos = self.marcadores_geneticos.copy()
        nova_amostra.metadados = self.metadados.copy()
        return nova_amostra
    
    def clonar_profundo(self) -> 'AmostraDNA':
        """Cria uma cópia profunda da amostra."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return f"""AmostraDNA(
            codigo={self.codigo},
            sequencia={self.sequencia[:20]}{'...' if len(self.sequencia) > 20 else ''},
            concentracao={self.concentracao_ng_ul} ng/μL,
            pureza={self.pureza_260_280},
            marcadores={len(self.marcadores_geneticos)}
        )"""


class AmostraRNA(PrototipoAmostra):
    """Amostra de RNA que pode ser clonada para experimentos replicáveis."""
    
    def __init__(self, codigo: str, tipo_rna: str = "mRNA"):
        self.codigo = codigo
        self.tipo_rna = tipo_rna  # mRNA, tRNA, rRNA
        self.integridade_rin: float = 0.0
        self.concentracao_ng_ul: float = 0.0
        self.genes_expressos: List[str] = []
        self.qualidade: Dict[str, Any] = {}
    
    def definir_integridade(self, rin: float) -> None:
        """Define a integridade do RNA (RIN - RNA Integrity Number)."""
        self.integridade_rin = rin
    
    def adicionar_gene_expresso(self, gene: str) -> None:
        """Adiciona um gene expresso na amostra."""
        self.genes_expressos.append(gene)
    
    def definir_qualidade(self, metrica: str, valor: Any) -> None:
        """Define métricas de qualidade."""
        self.qualidade[metrica] = valor
    
    def clonar(self) -> 'AmostraRNA':
        """Cria uma cópia superficial da amostra."""
        nova_amostra = AmostraRNA(self.codigo, self.tipo_rna)
        nova_amostra.integridade_rin = self.integridade_rin
        nova_amostra.concentracao_ng_ul = self.concentracao_ng_ul
        nova_amostra.genes_expressos = self.genes_expressos.copy()
        nova_amostra.qualidade = self.qualidade.copy()
        return nova_amostra
    
    def clonar_profundo(self) -> 'AmostraRNA':
        """Cria uma cópia profunda da amostra."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return f"""AmostraRNA(
            codigo={self.codigo},
            tipo={self.tipo_rna},
            integridade={self.integridade_rin},
            concentracao={self.concentracao_ng_ul} ng/μL,
            genes_expressos={len(self.genes_expressos)}
        )"""


class RegistroPrototipos:
    """Registro para gerenciar protótipos de amostras."""
    
    def __init__(self):
        self.prototipos: Dict[str, PrototipoAmostra] = {}
    
    def adicionar_prototipo(self, chave: str, prototipo: PrototipoAmostra) -> None:
        """Adiciona um protótipo ao registro."""
        self.prototipos[chave] = prototipo
    
    def obter_prototipo(self, chave: str) -> PrototipoAmostra:
        """Obtém um protótipo do registro."""
        if chave not in self.prototipos:
            raise ValueError(f"Protótipo '{chave}' não encontrado")
        return self.prototipos[chave].clonar()
    
    def obter_prototipo_profundo(self, chave: str) -> PrototipoAmostra:
        """Obtém uma cópia profunda do protótipo."""
        if chave not in self.prototipos:
            raise ValueError(f"Protótipo '{chave}' não encontrado")
        return self.prototipos[chave].clonar_profundo()
    
    def listar_prototipos(self) -> List[str]:
        """Lista todas as chaves de protótipos disponíveis."""
        return list(self.prototipos.keys())


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Clonagem de Amostra DNA ===")
    # Criar amostra original
    amostra_original = AmostraDNA("AMOSTRA_001", "ATCGATCGATCGATCGATCG")
    amostra_original.definir_concentracao(50.0)
    amostra_original.definir_pureza(1.8)
    amostra_original.adicionar_marcador("BRCA1")
    amostra_original.adicionar_marcador("TP53")
    amostra_original.adicionar_metadado("origem", "Sangue periférico")
    
    print("Amostra Original:")
    print(amostra_original)
    
    # Clonar amostra para múltiplos testes
    amostra_clonada = amostra_original.clonar()
    amostra_clonada.codigo = "AMOSTRA_001_CLONE"
    
    print("\nAmostra Clonada:")
    print(amostra_clonada)
    
    # Modificar a amostra clonada não afeta a original
    amostra_clonada.adicionar_marcador("EGFR")
    print(f"\nMarcadores Original: {amostra_original.marcadores_geneticos}")
    print(f"Marcadores Clonada: {amostra_clonada.marcadores_geneticos}")
    
    print("\n=== Exemplo 2: Clonagem de Amostra RNA ===")
    # Criar amostra RNA original
    rna_original = AmostraRNA("RNA_001", "mRNA")
    rna_original.definir_integridade(8.5)
    rna_original.definir_concentracao(100.0)
    rna_original.adicionar_gene_expresso("ACTB")
    rna_original.adicionar_gene_expresso("GAPDH")
    rna_original.definir_qualidade("A260", 2.0)
    rna_original.definir_qualidade("A280", 1.0)
    
    print("RNA Original:")
    print(rna_original)
    
    # Clonagem profunda para experimento independente
    rna_clonado = rna_original.clonar_profundo()
    rna_clonado.codigo = "RNA_001_CLONE"
    rna_clonado.adicionar_gene_expresso("B2M")
    
    print("\nRNA Clonado:")
    print(rna_clonado)
    
    print("\n=== Exemplo 3: Registro de Protótipos ===")
    # Criar registro de protótipos
    registro = RegistroPrototipos()
    
    # Adicionar protótipos padrão
    dna_padrao = AmostraDNA("DNA_PADRAO", "ATCGATCG")
    dna_padrao.definir_concentracao(25.0)
    dna_padrao.definir_pureza(1.8)
    
    rna_padrao = AmostraRNA("RNA_PADRAO", "mRNA")
    rna_padrao.definir_integridade(9.0)
    rna_padrao.definir_concentracao(75.0)
    
    registro.adicionar_prototipo("dna_controle", dna_padrao)
    registro.adicionar_prototipo("rna_controle", rna_padrao)
    
    print(f"Protótipos disponíveis: {registro.listar_prototipos()}")
    
    # Obter clones dos protótipos
    clone_dna = registro.obter_prototipo("dna_controle")
    clone_dna.codigo = "DNA_EXPERIMENTO_1"
    
    clone_rna = registro.obter_prototipo_profundo("rna_controle")
    clone_rna.codigo = "RNA_EXPERIMENTO_1"
    
    print("\nClones obtidos do registro:")
    print(clone_dna)
    print(clone_rna)
