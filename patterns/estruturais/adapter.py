from abc import ABC, abstractmethod
from typing import Dict, Any, List


class AnalisadorSequencias(ABC):
    """Interface alvo para analisadores de sequências."""
    
    @abstractmethod
    def analisar(self, dados: str) -> Dict[str, Any]:
        """Analisa dados de sequência."""
        pass


class AnalisadorFASTA:
    """Classe existente para analisar formato FASTA."""
    
    def processar_fasta(self, dados_fasta: str) -> Dict[str, Any]:
        """Processa dados no formato FASTA."""
        if not dados_fasta.startswith(">"):
            # Remove cabeçalho se existir
            linhas = dados_fasta.split('\n')
            sequencia = ''.join(linhas[1:]) if len(linhas) > 1 else dados_fasta
        else:
            linhas = dados_fasta.split('\n')
            cabecalho = linhas[0][1:]  # Remove '>'
            sequencia = ''.join(linhas[1:])
        
        return {
            "formato": "FASTA",
            "cabecalho": cabecalho if 'cabecalho' in locals() else "",
            "sequencia": sequencia,
            "comprimento": len(sequencia),
            "composicao": self._calcular_composicao(sequencia)
        }
    
    def _calcular_composicao(self, sequencia: str) -> Dict[str, int]:
        """Calcula composição de nucleotídeos."""
        composicao = {"A": 0, "T": 0, "C": 0, "G": 0, "N": 0}
        for base in sequencia.upper():
            if base in composicao:
                composicao[base] += 1
        return composicao


class AnalisadorGenBank:
    """Classe existente para analisar formato GenBank."""
    
    def processar_genbank(self, dados_genbank: str) -> Dict[str, Any]:
        """Processa dados no formato GenBank."""
        linhas = dados_genbank.split('\n')
        metadados = {}
        features = []
        sequencia = ""
        
        secao_atual = "header"
        
        for linha in linhas:
            linha = linha.strip()
            if linha.startswith('LOCUS'):
                metadados['locus'] = linha[6:].strip()
            elif linha.startswith('DEFINITION'):
                metadados['definition'] = linha[11:].strip()
            elif linha.startswith('ACCESSION'):
                metadados['accession'] = linha[10:].strip()
            elif linha.startswith('FEATURES'):
                secao_atual = "features"
            elif linha.startswith('ORIGIN'):
                secao_atual = "sequence"
            elif secao_atual == "features" and linha.startswith('     '):
                features.append(linha.strip())
            elif secao_atual == "sequence" and not linha.startswith('//'):
                # Remove números e espaços da sequência
                seq_parte = ''.join([c for c in linha if c.isalpha()])
                sequencia += seq_parte
        
        return {
            "formato": "GenBank",
            "metadados": metadados,
            "features": features,
            "sequencia": sequencia,
            "comprimento": len(sequencia)
        }


class AnalisadorUnificado:
    """Classe existente com interface diferente."""
    
    def executar_analise(self, tipo_dado: str, dados: Any) -> Dict[str, Any]:
        """Executa análise baseada no tipo de dado."""
        if tipo_dado == "sequencia":
            return self._analisar_sequencia(dados)
        elif tipo_dado == "proteina":
            return self._analisar_proteina(dados)
        else:
            return {"erro": "Tipo de dado não suportado"}
    
    def _analisar_sequencia(self, sequencia: str) -> Dict[str, Any]:
        """Análise específica para sequências."""
        return {
            "tipo": "sequencia_nucleotidica",
            "dados": sequencia,
            "comprimento": len(sequencia),
            "gc_content": self._calcular_gc(sequencia),
            "complexidade": self._calcular_complexidade(sequencia)
        }
    
    def _analisar_proteina(self, proteina: str) -> Dict[str, Any]:
        """Análise específica para proteínas."""
        return {
            "tipo": "proteina",
            "dados": proteina,
            "comprimento": len(proteina),
            "peso_molecular": self._calcular_peso_molecular(proteina),
            "ponto_isoeletrico": self._estimar_pi(proteina)
        }
    
    def _calcular_gc(self, sequencia: str) -> float:
        """Calcula conteúdo de GC."""
        gc_count = sequencia.upper().count('G') + sequencia.upper().count('C')
        return (gc_count / len(sequencia)) * 100 if len(sequencia) > 0 else 0
    
    def _calcular_complexidade(self, sequencia: str) -> float:
        """Calcula complexidade da sequência."""
        bases_unicas = len(set(sequencia.upper()))
        return (bases_unicas / min(4, len(sequencia))) * 100
    
    def _calcular_peso_molecular(self, proteina: str) -> float:
        """Calcula peso molecular aproximado."""
        pesos = {'A': 89, 'R': 174, 'N': 132, 'D': 133, 'C': 121, 
                'E': 147, 'Q': 146, 'G': 75, 'H': 155, 'I': 131,
                'L': 131, 'K': 146, 'M': 149, 'F': 165, 'P': 115,
                'S': 105, 'T': 119, 'W': 204, 'Y': 181, 'V': 117}
        
        peso_total = 0
        for aa in proteina.upper():
            peso_total += pesos.get(aa, 110)  # Padrão médio se não encontrado
        
        return peso_total
    
    def _estimar_pi(self, proteina: str) -> float:
        """Estima ponto isoelétrico (simplificado)."""
        # Simplificação - retorna valor baseado na composição
        acidic = proteina.upper().count('D') + proteina.upper().count('E')
        basic = proteina.upper().count('K') + proteina.upper().count('R') + proteina.upper().count('H')
        
        if basic > acidic:
            return 7.5 + (basic - acidic) * 0.3
        else:
            return 6.5 - (acidic - basic) * 0.2


class AdapterFASTA(AnalisadorSequencias):
    """Adapter para unificar interface do analisador FASTA."""
    
    def __init__(self, analisador_fasta: AnalisadorFASTA):
        self.analisador_fasta = analisador_fasta
    
    def analisar(self, dados: str) -> Dict[str, Any]:
        """Adapta a chamada para o método existente."""
        resultado = self.analisador_fasta.processar_fasta(dados)
        
        # Adapta o formato para a interface unificada
        return {
            "tipo_analise": "sequencia_fasta",
            "formato_original": resultado["formato"],
            "dados": resultado["sequencia"],
            "metadados": {
                "cabecalho": resultado["cabecalho"],
                "comprimento": resultado["comprimento"],
                "composicao": resultado["composicao"]
            }
        }


class AdapterGenBank(AnalisadorSequencias):
    """Adapter para unificar interface do analisador GenBank."""
    
    def __init__(self, analisador_genbank: AnalisadorGenBank):
        self.analisador_genbank = analisador_genbank
    
    def analisar(self, dados: str) -> Dict[str, Any]:
        """Adapta a chamada para o método existente."""
        resultado = self.analisador_genbank.processar_genbank(dados)
        
        # Adapta o formato para a interface unificada
        return {
            "tipo_analise": "sequencia_genbank",
            "formato_original": resultado["formato"],
            "dados": resultado["sequencia"],
            "metadados": {
                "metadados": resultado["metadados"],
                "features": resultado["features"],
                "comprimento": resultado["comprimento"]
            }
        }


class AdapterUnificado(AnalisadorSequencias):
    """Adapter para unificar interface do analisador unificado."""
    
    def __init__(self, analisador_unificado: AnalisadorUnificado):
        self.analisador_unificado = analisador_unificado
    
    def analisar(self, dados: str) -> Dict[str, Any]:
        """Adapta a chamada para o método existente."""
        # Assume que é uma sequência nucleotídica
        resultado = self.analisador_unificado.executar_analise("sequencia", dados)
        
        # Adapta o formato para a interface unificada
        return {
            "tipo_analise": "sequencia_unificada",
            "formato_original": "custom",
            "dados": resultado["dados"],
            "metadados": {
                "comprimento": resultado["comprimento"],
                "gc_content": resultado["gc_content"],
                "complexidade": resultado["complexidade"]
            }
        }


class FabricaAdapters:
    """Factory para criar adapters baseados no formato."""
    
    @staticmethod
    def criar_adapter(tipo_formato: str) -> AnalisadorSequencias:
        """Cria o adapter apropriado para o formato."""
        if tipo_formato.upper() == "FASTA":
            return AdapterFASTA(AnalisadorFASTA())
        elif tipo_formato.upper() == "GENBANK":
            return AdapterGenBank(AnalisadorGenBank())
        elif tipo_formato.upper() == "UNIFICADO":
            return AdapterUnificado(AnalisadorUnificado())
        else:
            raise ValueError(f"Formato não suportado: {tipo_formato}")


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Adapter para formato FASTA ===")
    
    # Criar adapter para FASTA
    adapter_fasta = FabricaAdapters.criar_adapter("FASTA")
    
    dados_fasta = """>seq1
ATCGATCGATCGATCGATCG
GCTAGCTAGCTAGCTAGCTA
"""
    
    resultado_fasta = adapter_fasta.analisar(dados_fasta)
    print("Resultado análise FASTA:")
    for chave, valor in resultado_fasta.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 2: Adapter para formato GenBank ===")
    
    # Criar adapter para GenBank
    adapter_genbank = FabricaAdapters.criar_adapter("GENBANK")
    
    dados_genbank = """LOCUS       SCU49845     5028 bp    DNA     UNK 01-JAN-1980
DEFINITION  Saccharomyces cerevisiae TCP1-beta gene, partial cds.
ACCESSION   NC_001348
FEATURES             Location/Qualifiers
     gene            1..5028
ORIGIN
        1 gatcctccat atacaacggt atctccacct caggtttaga tctcaacaac ggaaccattg
       61 ccgacatgag acagttaggt atcgtcgaga gttccaagcc acactgtcaa cttgccactg
//
"""
    
    resultado_genbank = adapter_genbank.analisar(dados_genbank)
    print("Resultado análise GenBank:")
    for chave, valor in resultado_genbank.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 3: Adapter para formato Unificado ===")
    
    # Criar adapter para formato unificado
    adapter_unificado = FabricaAdapters.criar_adapter("UNIFICADO")
    
    sequencia_simples = "ATCGATCGATCGATCGATCG"
    resultado_unificado = adapter_unificado.analisar(sequencia_simples)
    print("Resultado análise unificada:")
    for chave, valor in resultado_unificado.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 4: Uso Polimórfico dos Adapters ===")
    
    # Lista de adapters para diferentes formatos
    adapters = [
        FabricaAdapters.criar_adapter("FASTA"),
        FabricaAdapters.criar_adapter("GENBANK"),
        FabricaAdapters.criar_adapter("UNIFICADO")
    ]
    
    dados_teste = [
        dados_fasta,
        dados_genbank,
        "ATCGATCGATCG"
    ]
    
    print("Análise polimórfica com diferentes adapters:")
    for i, adapter in enumerate(adapters):
        try:
            resultado = adapter.analisar(dados_teste[i])
            print(f"  Adapter {i+1}: {resultado['tipo_analise']} - Comprimento: {resultado['metadados']['comprimento']}")
        except Exception as e:
            print(f"  Adapter {i+1}: Erro - {e}")
    
    print("\n=== Exemplo 5: Extensão com Novo Formato ===")
    
    # Simulação de novo formato existente que precisa ser adaptado
    class AnalisadorNovoFormato:
        """Classe existente com interface totalmente diferente."""
        
        def parse_data(self, input_data):
            """Método com nome diferente."""
            return {
                "raw_sequence": input_data.get("seq", ""),
                "metadata": input_data.get("meta", {}),
                "quality_score": input_data.get("quality", 0)
            }
    
    class AdapterNovoFormato(AnalisadorSequencias):
        """Adapter para o novo formato."""
        
        def __init__(self, analisador_novo):
            self.analisador_novo = analisador_novo
        
        def analisar(self, dados: str) -> Dict[str, Any]:
            # Converte string para o formato esperado
            dados_formatados = {"seq": dados, "meta": {}, "quality": 95}
            resultado = self.analisador_novo.parse_data(dados_formatados)
            
            return {
                "tipo_analise": "novo_formato",
                "formato_original": "custom",
                "dados": resultado["raw_sequence"],
                "metadados": {
                    "metadata": resultado["metadata"],
                    "quality": resultado["quality_score"],
                    "comprimento": len(resultado["raw_sequence"])
                }
            }
    
    # Usar o novo adapter
    adapter_novo = AdapterNovoFormato(AnalisadorNovoFormato())
    resultado_novo = adapter_novo.analisar("ATCGATCGATCG")
    print("Resultado com novo adapter:")
    for chave, valor in resultado_novo.items():
        print(f"  {chave}: {valor}")
