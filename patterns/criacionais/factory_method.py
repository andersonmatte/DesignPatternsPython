from abc import ABC, abstractmethod
from typing import Dict, Any


class AnalisadorSequencias(ABC):
    """Classe abstrata base para analisadores de sequências."""
    
    @abstractmethod
    def analisar_sequencia(self, sequencia: str) -> Dict[str, Any]:
        """Analisa uma sequência biológica."""
        pass
    
    @abstractmethod
    def validar_formato(self, dados: str) -> bool:
        """Valida se os dados estão no formato correto."""
        pass


class AnalisadorFASTA(AnalisadorSequencias):
    """Analisador especializado em formato FASTA."""
    
    def analisar_sequencia(self, sequencia: str) -> Dict[str, Any]:
        if not self.validar_formato(sequencia):
            raise ValueError("Formato FASTA inválido")
        
        return {
            "formato": "FASTA",
            "sequencia": sequencia,
            "comprimento": len(sequencia),
            "composicao": self._calcular_composicao(sequencia)
        }
    
    def validar_formato(self, dados: str) -> bool:
        # Validação simplificada para formato FASTA
        return dados.startswith(">") or all(base.upper() in "ATCGN" for base in dados)
    
    def _calcular_composicao(self, sequencia: str) -> Dict[str, int]:
        composicao = {"A": 0, "T": 0, "C": 0, "G": 0, "N": 0}
        for base in sequencia.upper():
            if base in composicao:
                composicao[base] += 1
        return composicao


class AnalisadorGenBank(AnalisadorSequencias):
    """Analisador especializado em formato GenBank."""
    
    def analisar_sequencia(self, sequencia: str) -> Dict[str, Any]:
        if not self.validar_formato(sequencia):
            raise ValueError("Formato GenBank inválido")
        
        return {
            "formato": "GenBank",
            "sequencia": sequencia,
            "metadados": self._extrair_metadados(sequencia),
            "features": self._extrair_features(sequencia)
        }
    
    def validar_formato(self, dados: str) -> bool:
        # Validação simplificada para formato GenBank
        return "LOCUS" in dados.upper() and "ORIGIN" in dados.upper()
    
    def _extrair_metadados(self, dados: str) -> Dict[str, str]:
        # Extração simplificada de metadados
        metadados = {}
        linhas = dados.split('\n')
        for linha in linhas:
            if linha.startswith('LOCUS'):
                metadados['locus'] = linha[6:].strip()
            elif linha.startswith('DEFINITION'):
                metadados['definition'] = linha[10:].strip()
        return metadados
    
    def _extrair_features(self, dados: str) -> list:
        # Extração simplificada de features
        return ["gene", "CDS", "mRNA"]


class AnalisadorFactory:
    """Factory Method para criação de analisadores especializados."""
    
    @staticmethod
    def criar_analisador(tipo_formato: str) -> AnalisadorSequencias:
        """Cria um analisador baseado no tipo de formato."""
        if tipo_formato.upper() == "FASTA":
            return AnalisadorFASTA()
        elif tipo_formato.upper() == "GENBANK":
            return AnalisadorGenBank()
        else:
            raise ValueError(f"Formato não suportado: {tipo_formato}")


# Exemplo de uso
if __name__ == "__main__":
    # Criação baseada no tipo de formato
    factory = AnalisadorFactory()
    
    # Criar analisador FASTA
    analisador_fasta = factory.criar_analisador("FASTA")
    resultado_fasta = analisador_fasta.analisar_sequencia("ATCGATCGATCG")
    print("Resultado FASTA:", resultado_fasta)
    
    # Criar analisador GenBank
    analisador_genbank = factory.criar_analisador("GENBANK")
    dados_genbank = """LOCUS       SCU49845     5028 bp    DNA     UNK 01-JAN-1980
DEFINITION  Saccharomyces cerevisiae TCP1-beta gene, partial cds.
ORIGIN
        1 gatcctccat atacaacggt atctccacct caggtttaga tctcaacaac ggaaccattg
       61 ccgacatgag acagttaggt atcgtcgaga gttccaagcc acactgtcaa cttgccactg
"""
    resultado_genbank = analisador_genbank.analisar_sequencia(dados_genbank)
    print("Resultado GenBank:", resultado_genbank)
