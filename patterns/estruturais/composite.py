from abc import ABC, abstractmethod
from typing import List, Dict, Any
from domain.amostra_biologica import ComponenteGenetico, Nucleotideo, Gene, Proteina


class ComponenteGenomico(ABC):
    """Interface base para componentes genômicos."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.pai = None
    
    @abstractmethod
    def adicionar(self, componente: 'ComponenteGenomico') -> None:
        """Adiciona um componente filho."""
        pass
    
    @abstractmethod
    def remover(self, componente: 'ComponenteGenomico') -> None:
        """Remove um componente filho."""
        pass
    
    @abstractmethod
    def obter_filho(self, indice: int) -> 'ComponenteGenomico':
        """Obtém um componente filho pelo índice."""
        pass
    
    @abstractmethod
    def exibir(self, indentacao: int = 0) -> str:
        """Exibe a estrutura do componente."""
        pass
    
    @abstractmethod
    def contar_componentes(self) -> int:
        """Contagem recursiva de componentes."""
        pass
    
    @abstractmethod
    def buscar(self, nome: str) -> List['ComponenteGenomico']:
        """Busca componentes por nome."""
        pass


class BaseNitrogenada(ComponenteGenomico):
    """Componente folha: base nitrogenada individual."""
    
    def __init__(self, base: str, posicao: int = 0):
        super().__init__(f"Base_{base}_{posicao}")
        self.base = base
        self.posicao = posicao
        self.pares_hidrogenio = self._calcular_pares_hidrogenio()
    
    def _calcular_pares_hidrogenio(self) -> int:
        """Calcula número de pares de hidrogênio."""
        pares = {"A": 2, "T": 2, "U": 2, "G": 3, "C": 3}
        return pares.get(self.base.upper(), 0)
    
    def adicionar(self, componente: ComponenteGenomico) -> None:
        """Base nitrogenada não pode ter filhos."""
        raise Exception("Base nitrogenada não pode ter componentes filhos")
    
    def remover(self, componente: ComponenteGenomico) -> None:
        """Base nitrogenada não pode ter filhos."""
        raise Exception("Base nitrogenada não pode ter componentes filhos")
    
    def obter_filho(self, indice: int) -> ComponenteGenomico:
        """Base nitrogenada não tem filhos."""
        raise Exception("Base nitrogenada não tem componentes filhos")
    
    def exibir(self, indentacao: int = 0) -> str:
        """Exibe informações da base nitrogenada."""
        indent = "  " * indentacao
        return f"{indent}Base: {self.base} (Posição: {self.posicao}, Pares H: {self.pares_hidrogenio})"
    
    def contar_componentes(self) -> int:
        """Base nitrogenada conta como 1."""
        return 1
    
    def buscar(self, nome: str) -> List[ComponenteGenomico]:
        """Busca por nome."""
        return [self] if nome in self.nome else []
    
    def complementar(self) -> 'BaseNitrogenada':
        """Retorna a base complementar."""
        complementos = {"A": "T", "T": "A", "U": "A", "G": "C", "C": "G"}
        base_comp = complementos.get(self.base.upper(), "N")
        return BaseNitrogenada(base_comp, self.posicao)


class Aminoacido(ComponenteGenomico):
    """Componente folha: aminoácido individual."""
    
    def __init__(self, codigo: str, posicao: int = 0):
        super().__init__(f"Aminoacido_{codigo}_{posicao}")
        self.codigo = codigo
        self.posicao = posicao
        self.peso_molecular = self._calcular_peso_molecular()
    
    def _calcular_peso_molecular(self) -> float:
        """Calcula peso molecular do aminoácido."""
        pesos = {
            'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.15,
            'E': 147.13, 'Q': 146.15, 'G': 75.07, 'H': 155.16, 'I': 131.17,
            'L': 131.17, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
            'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
        }
        return pesos.get(self.codigo.upper(), 110.0)
    
    def adicionar(self, componente: ComponenteGenomico) -> None:
        """Aminoácido não pode ter filhos."""
        raise Exception("Aminoácido não pode ter componentes filhos")
    
    def remover(self, componente: ComponenteGenomico) -> None:
        """Aminoácido não pode ter filhos."""
        raise Exception("Aminoácido não pode ter componentes filhos")
    
    def obter_filho(self, indice: int) -> ComponenteGenomico:
        """Aminoácido não tem filhos."""
        raise Exception("Aminoácido não tem componentes filhos")
    
    def exibir(self, indentacao: int = 0) -> str:
        """Exibe informações do aminoácido."""
        indent = "  " * indentacao
        return f"{indent}Aminoácido: {self.codigo} (Posição: {self.posicao}, Peso: {self.peso_molecular:.2f} Da)"
    
    def contar_componentes(self) -> int:
        """Aminoácido conta como 1."""
        return 1
    
    def buscar(self, nome: str) -> List[ComponenteGenomico]:
        """Busca por nome."""
        return [self] if nome in self.nome else []


class SequenciaNucleotidica(ComponenteGenomico):
    """Componente composto: sequência de nucleotídeos."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.filhos: List[ComponenteGenomico] = []
        self.tipo = "DNA"  # DNA ou RNA
    
    def adicionar(self, componente: ComponenteGenomico) -> None:
        """Adiciona um componente à sequência."""
        self.filhos.append(componente)
        componente.pai = self
    
    def remover(self, componente: ComponenteGenomico) -> None:
        """Remove um componente da sequência."""
        if componente in self.filhos:
            self.filhos.remove(componente)
            componente.pai = None
    
    def obter_filho(self, indice: int) -> ComponenteGenomico:
        """Obtém um componente filho pelo índice."""
        return self.filhos[indice] if 0 <= indice < len(self.filhos) else None
    
    def exibir(self, indentacao: int = 0) -> str:
        """Exibe a estrutura da sequência."""
        indent = "  " * indentacao
        resultado = f"{indent}Sequência: {self.nome} (Tipo: {self.tipo}, Tamanho: {len(self.filhos)})\n"
        
        for filho in self.filhos:
            resultado += filho.exibir(indentacao + 1) + "\n"
        
        return resultado.rstrip()
    
    def contar_componentes(self) -> int:
        """Conta recursivamente todos os componentes."""
        total = 1  # Conta a própria sequência
        for filho in self.filhos:
            total += filho.contar_componentes()
        return total
    
    def buscar(self, nome: str) -> List[ComponenteGenomico]:
        """Busca recursivamente por nome."""
        resultados = []
        
        if nome in self.nome:
            resultados.append(self)
        
        for filho in self.filhos:
            resultados.extend(filho.buscar(nome))
        
        return resultados
    
    def obter_sequencia_completa(self) -> str:
        """Obtém a sequência completa de bases."""
        sequencia = ""
        for filho in self.filhos:
            if isinstance(filho, BaseNitrogenada):
                sequencia += filho.base
        return sequencia
    
    def transcrever_para_rna(self) -> 'SequenciaNucleotidica':
        """Transcreve DNA para RNA."""
        if self.tipo != "DNA":
            raise Exception("Apenas DNA pode ser transcrito para RNA")
        
        rna = SequenciaNucleotidica(f"RNA_{self.nome}")
        rna.tipo = "RNA"
        
        for filho in self.filhos:
            if isinstance(filho, BaseNitrogenada):
                # Substitui T por U
                base_rna = "U" if filho.base.upper() == "T" else filho.base
                rna.adicionar(BaseNitrogenada(base_rna, filho.posicao))
        
        return rna
    
    def traduzir_para_proteina(self) -> 'ProteinaComposta':
        """Traduz sequência de RNA para proteína."""
        if self.tipo != "RNA":
            raise Exception("Apenas RNA pode ser traduzido para proteína")
        
        proteina = ProteinaComposta(f"Proteina_{self.nome}")
        
        # Tabela de códons (simplificada)
        codons = {
            'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
            'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
            'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
            'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
            'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
            'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
            'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
            'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
            'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
            'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
            'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
            'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
            'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
        }
        
        sequencia_rna = self.obter_sequencia_completa()
        
        # Traduzir códons
        for i in range(0, len(sequencia_rna) - 2, 3):
            codon = sequencia_rna[i:i+3].upper()
            aminoacido_codigo = codons.get(codon, 'X')  # X para desconhecido
            
            if aminoacido_codigo != '*':  # Stop codon
                proteina.adicionar(Aminoacido(aminoacido_codigo, i // 3))
        
        return proteina


class ProteinaComposta(ComponenteGenomico):
    """Componente composto: proteína formada por aminoácidos."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.filhos: List[ComponenteGenomico] = []
        self.dominios: List[str] = []
    
    def adicionar(self, componente: ComponenteGenomico) -> None:
        """Adiciona um componente à proteína."""
        self.filhos.append(componente)
        componente.pai = self
    
    def remover(self, componente: ComponenteGenomico) -> None:
        """Remove um componente da proteína."""
        if componente in self.filhos:
            self.filhos.remove(componente)
            componente.pai = None
    
    def obter_filho(self, indice: int) -> ComponenteGenomico:
        """Obtém um componente filho pelo índice."""
        return self.filhos[indice] if 0 <= indice < len(self.filhos) else None
    
    def exibir(self, indentacao: int = 0) -> str:
        """Exibe a estrutura da proteína."""
        indent = "  " * indentacao
        resultado = f"{indent}Proteína: {self.nome} (Tamanho: {len(self.filhos)} aa)\n"
        
        if self.dominios:
            resultado += f"{indent}  Domínios: {', '.join(self.dominios)}\n"
        
        for filho in self.filhos:
            resultado += filho.exibir(indentacao + 1) + "\n"
        
        return resultado.rstrip()
    
    def contar_componentes(self) -> int:
        """Conta recursivamente todos os componentes."""
        total = 1  # Conta a própria proteína
        for filho in self.filhos:
            total += filho.contar_componentes()
        return total
    
    def buscar(self, nome: str) -> List[ComponenteGenomico]:
        """Busca recursivamente por nome."""
        resultados = []
        
        if nome in self.nome:
            resultados.append(self)
        
        for filho in self.filhos:
            resultados.extend(filho.buscar(nome))
        
        return resultados
    
    def adicionar_dominio(self, dominio: str) -> None:
        """Adiciona um domínio funcional à proteína."""
        self.dominios.append(dominio)
    
    def obter_sequencia_aminoacidos(self) -> str:
        """Obtém a sequência completa de aminoácidos."""
        sequencia = ""
        for filho in self.filhos:
            if isinstance(filho, Aminoacido):
                sequencia += filho.codigo
        return sequencia
    
    def calcular_peso_molecular(self) -> float:
        """Calcula o peso molecular total da proteína."""
        peso_total = 0.0
        for filho in self.filhos:
            if isinstance(filho, Aminoacido):
                peso_total += filho.peso_molecular
        return peso_total


class Genoma(ComponenteGenomico):
    """Componente composto de alto nível: genoma completo."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.filhos: List[ComponenteGenomico] = []
        self.cromossomos: Dict[str, ComponenteGenomico] = {}
    
    def adicionar(self, componente: ComponenteGenomico) -> None:
        """Adiciona um componente ao genoma."""
        self.filhos.append(componente)
        componente.pai = self
        
        # Se for um cromossomo, adiciona ao dicionário
        if "cromossomo" in componente.nome.lower():
            self.cromossomos[componente.nome] = componente
    
    def remover(self, componente: ComponenteGenomico) -> None:
        """Remove um componente do genoma."""
        if componente in self.filhos:
            self.filhos.remove(componente)
            componente.pai = None
            
            # Remove do dicionário de cromossomos se necessário
            if componente.nome in self.cromossomos:
                del self.cromossomos[componente.nome]
    
    def obter_filho(self, indice: int) -> ComponenteGenomico:
        """Obtém um componente filho pelo índice."""
        return self.filhos[indice] if 0 <= indice < len(self.filhos) else None
    
    def exibir(self, indentacao: int = 0) -> str:
        """Exibe a estrutura do genoma."""
        indent = "  " * indentacao
        resultado = f"{indent}Genoma: {self.nome} (Cromossomos: {len(self.cromossomos)})\n"
        
        for nome, cromossomo in self.cromossomos.items():
            resultado += cromossomo.exibir(indentacao + 1) + "\n"
        
        return resultado.rstrip()
    
    def contar_componentes(self) -> int:
        """Conta recursivamente todos os componentes."""
        total = 1  # Conta o próprio genoma
        for filho in self.filhos:
            total += filho.contar_componentes()
        return total
    
    def buscar(self, nome: str) -> List[ComponenteGenomico]:
        """Busca recursivamente por nome."""
        resultados = []
        
        if nome in self.nome:
            resultados.append(self)
        
        for filho in self.filhos:
            resultados.extend(filho.buscar(nome))
        
        return resultados
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do genoma."""
        total_bases = 0
        total_genes = 0
        total_proteinas = 0
        
        for filho in self.filhos:
            if isinstance(filho, SequenciaNucleotidica):
                total_bases += len(filho.filhos)
            elif "gene" in filho.nome.lower():
                total_genes += 1
            elif "proteina" in filho.nome.lower():
                total_proteinas += 1
        
        return {
            "total_componentes": self.contar_componentes(),
            "total_cromossomos": len(self.cromossomos),
            "total_bases_estimado": total_bases,
            "total_genes": total_genes,
            "total_proteinas": total_proteinas
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Construção de Sequência DNA ===")
    
    # Criar sequência de DNA
    dna_hbb = SequenciaNucleotidica("Gene_HBB")
    
    # Adicionar bases nitrogenadas
    bases_hbb = "ATGTGGCACCTGACTCCTGAGGAGAAGTCTGCCGTTACT"
    for i, base in enumerate(bases_hbb):
        dna_hbb.adicionar(BaseNitrogenada(base, i))
    
    print("Estrutura do Gene HBB:")
    print(dna_hbb.exibir())
    print(f"Total de componentes: {dna_hbb.contar_componentes()}")
    print(f"Sequência completa: {dna_hbb.obter_sequencia_completa()}")
    
    print("\n=== Exemplo 2: Transcrição e Tradução ===")
    
    # Transcrever para RNA
    rna_hbb = dna_hbb.transcrever_para_rna()
    print("RNA mensageiro:")
    print(rna_hbb.exibir())
    print(f"Sequência RNA: {rna_hbb.obter_sequencia_completa()}")
    
    # Traduzir para proteína
    proteina_hbb = rna_hbb.traduzir_para_proteina()
    print("\nProteína resultante:")
    print(proteina_hbb.exibir())
    print(f"Sequência de aminoácidos: {proteina_hbb.obter_sequencia_aminoacidos()}")
    print(f"Peso molecular: {proteina_hbb.calcular_peso_molecular():.2f} Da")
    
    # Adicionar domínios funcionais
    proteina_hbb.adicionar_dominio("Globin")
    proteina_hbb.adicionar_dominio("Heme-binding")
    print(f"Domínios: {proteina_hbb.dominios}")
    
    print("\n=== Exemplo 3: Estrutura Hierárquica Complexa ===")
    
    # Criar cromossomo
    cromossomo_11 = SequenciaNucleotidica("Cromossomo_11")
    
    # Adicionar múltiplos genes
    genes = [
        ("Gene_HBB", "ATGTGGCACCTGACTCCTGAGGAGAAGTCTGCCGTTACT"),
        ("Gene_INS", "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCT"),
        ("Gene_B2M", "ATGATGGCTGAGCTGGCTGGCCGGGCTGAGCTGCTGGGCAGCTG")
    ]
    
    for nome_gene, sequencia in genes:
        gene = SequenciaNucleotidica(nome_gene)
        for i, base in enumerate(sequencia):
            gene.adicionar(BaseNitrogenada(base, i))
        cromossomo_11.adicionar(gene)
    
    print("Estrutura do Cromossomo 11:")
    print(cromossomo_11.exibir())
    print(f"Total de componentes no cromossomo: {cromossomo_11.contar_componentes()}")
    
    print("\n=== Exemplo 4: Busca em Estrutura Hierárquica ===")
    
    # Buscar componentes específicos
    resultados_busca = cromossomo_11.buscar("HBB")
    print(f"Resultados da busca por 'HBB': {len(resultados_busca)} encontrados")
    for resultado in resultados_busca:
        print(f"  - {resultado.nome}")
    
    # Buscar bases específicas
    resultados_base = cromossomo_11.buscar("Base_A")
    print(f"\nBases 'A' encontradas: {len(resultados_base)}")
    
    print("\n=== Exemplo 5: Genoma Completo ===")
    
    # Criar genoma humano simplificado
    genoma_humano = Genoma("Genoma_Humano")
    
    # Adicionar cromossomos
    for i in range(1, 4):  # Apenas 3 cromossomos para exemplo
        cromossomo = SequenciaNucleotidica(f"Cromossomo_{i}")
        
        # Adicionar alguns genes
        for j in range(2):
            gene = SequenciaNucleotidica(f"Gene_{i}_{j}")
            sequencia_gene = "ATGCGATCGATCGATCGATCGATCGATCG"
            for k, base in enumerate(sequencia_gene):
                gene.adicionar(BaseNitrogenada(base, k))
            cromossomo.adicionar(gene)
        
        genoma_humano.adicionar(cromossomo)
    
    print("Estrutura do Genoma Humano:")
    print(genoma_humano.exibir())
    
    # Estatísticas do genoma
    stats = genoma_humano.obter_estatisticas()
    print(f"\nEstatísticas do Genoma:")
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 6: Operações de Remoção ===")
    
    # Remover um gene
    gene_remover = cromossomo_11.obter_filho(0)  # Primeiro gene
    if gene_remover:
        print(f"Removendo: {gene_remover.nome}")
        cromossomo_11.remover(gene_remover)
        print(f"Componentes restantes: {cromossomo_11.contar_componentes()}")
    
    print("\nComposite pattern implementado com sucesso!")
