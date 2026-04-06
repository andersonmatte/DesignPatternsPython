from abc import ABC, abstractmethod
from typing import Dict, Any
from domain.analise import AlgoritmoAnalise, NeedlemanWunsch, BLAST, SmithWaterman


class AlgoritmoProcessamento(ABC):
    """Abstração para algoritmos de processamento de dados genéticos."""
    
    @abstractmethod
    def processar_dados(self, dados: Any) -> Dict[str, Any]:
        """Processa os dados usando o algoritmo específico."""
        pass


class AlinhamentoGlobal(AlgoritmoProcessamento):
    """Implementação de alinhamento global."""
    
    def processar_dados(self, dados: Any) -> Dict[str, Any]:
        sequencia1, sequencia2 = dados
        return {
            "tipo_alinhamento": "global",
            "algoritmo": "Needleman-Wunsch",
            "sequencia1": sequencia1,
            "sequencia2": sequencia2,
            "score": self._calcular_score_global(sequencia1, sequencia2),
            "alinhamento": self._alinhar_global(sequencia1, sequencia2)
        }
    
    def _calcular_score_global(self, seq1: str, seq2: str) -> int:
        """Cálculo simplificado de score de alinhamento global."""
        match = 2
        mismatch = -1
        gap = -1
        
        score = 0
        min_len = min(len(seq1), len(seq2))
        
        for i in range(min_len):
            if seq1[i] == seq2[i]:
                score += match
            else:
                score += mismatch
        
        # Penalidade por gaps
        score += abs(len(seq1) - len(seq2)) * gap
        
        return score
    
    def _alinhar_global(self, seq1: str, seq2: str) -> str:
        """Simplificação de alinhamento global."""
        return f"{seq1[:10]}... | {seq2[:10]}..."


class AlinhamentoLocal(AlgoritmoProcessamento):
    """Implementação de alinhamento local."""
    
    def processar_dados(self, dados: Any) -> Dict[str, Any]:
        sequencia1, sequencia2 = dados
        return {
            "tipo_alinhamento": "local",
            "algoritmo": "Smith-Waterman",
            "sequencia1": sequencia1,
            "sequencia2": sequencia2,
            "melhor_score": self._encontrar_melhor_score_local(sequencia1, sequencia2),
            "regiao_alinhada": self._encontrar_regiao_local(sequencia1, sequencia2)
        }
    
    def _encontrar_melhor_score_local(self, seq1: str, seq2: str) -> int:
        """Encontra o melhor score de alinhamento local."""
        match = 2
        mismatch = -1
        
        melhor_score = 0
        score_atual = 0
        
        for i in range(len(seq1)):
            for j in range(len(seq2)):
                if seq1[i] == seq2[j]:
                    score_atual += match
                else:
                    score_atual += mismatch
                
                if score_atual > melhor_score:
                    melhor_score = score_atual
                
                if score_atual < 0:
                    score_atual = 0
        
        return melhor_score
    
    def _encontrar_regiao_local(self, seq1: str, seq2: str) -> str:
        """Encontra a melhor região de alinhamento local."""
        # Simplificação - retorna substring mais longa em comum
        maior_substring = ""
        for i in range(len(seq1)):
            for j in range(len(seq2)):
                k = 0
                while i + k < len(seq1) and j + k < len(seq2) and seq1[i + k] == seq2[j + k]:
                    k += 1
                if k > len(maior_substring):
                    maior_substring = seq1[i:i + k]
        
        return maior_substring


class BuscaBancoDados(AlgoritmoProcessamento):
    """Implementação de busca em banco de dados."""
    
    def processar_dados(self, dados: Any) -> Dict[str, Any]:
        query, database = dados
        return {
            "tipo_busca": "banco_dados",
            "algoritmo": "BLAST",
            "query": query,
            "database": database,
            "hits": self._buscar_similares(query, database),
            "e_value": self._calcular_e_value(query, database)
        }
    
    def _buscar_similares(self, query: str, database: str) -> list:
        """Busca sequências similares no banco de dados."""
        # Simulação de busca
        hits = []
        sequencias_db = ["ATCGATCG", "GCTAGCTA", "TATATATA", "CGCGCGCG"]
        
        for i, seq_db in enumerate(sequencias_db):
            similaridade = self._calcular_similaridade(query, seq_db)
            if similaridade > 0.5:
                hits.append({
                    "id": f"SEQ_{i+1:03d}",
                    "sequencia": seq_db,
                    "similaridade": similaridade
                })
        
        return hits
    
    def _calcular_similaridade(self, seq1: str, seq2: str) -> float:
        """Calcula similaridade entre duas sequências."""
        matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
        max_len = max(len(seq1), len(seq2))
        return matches / max_len if max_len > 0 else 0
    
    def _calcular_e_value(self, query: str, database: str) -> float:
        """Calcula E-value (simplificado)."""
        return 0.001 / len(query) if len(query) > 0 else 1.0


class AnaliseGenetica(ABC):
    """Abstração para análises genéticas."""
    
    def __init__(self, nome: str, algoritmo: AlgoritmoProcessamento):
        self.nome = nome
        self.algoritmo = algoritmo
    
    @abstractmethod
    def executar_analise(self, dados: Any) -> Dict[str, Any]:
        """Executa a análise usando o algoritmo configurado."""
        pass
    
    def mudar_algoritmo(self, novo_algoritmo: AlgoritmoProcessamento) -> None:
        """Permite trocar o algoritmo de processamento."""
        self.algoritmo = novo_algoritmo
    
    def __str__(self) -> str:
        return f"AnaliseGenetica(nome={self.nome}, algoritmo={type(self.algoritmo).__name__})"


class AnaliseSequenciamento(AnaliseGenetica):
    """Análise especializada em sequenciamento."""
    
    def executar_analise(self, dados: Any) -> Dict[str, Any]:
        """Executa análise de sequenciamento."""
        resultado_base = self.algoritmo.processar_dados(dados)
        
        return {
            "tipo_analise": "sequenciamento",
            "nome_analise": self.nome,
            "resultado_base": resultado_base,
            "qualidade_sequenciamento": self._avaliar_qualidade(dados),
            "cobertura": self._calcular_cobertura(dados)
        }
    
    def _avaliar_qualidade(self, dados: Any) -> Dict[str, float]:
        """Avalia qualidade do sequenciamento."""
        if isinstance(dados, tuple):
            sequencia = dados[0] if dados else ""
        else:
            sequencia = str(dados)
        
        # Métricas simplificadas de qualidade
        qualidade_media = 30.0  # Phred score médio
        q30 = 85.0  # Porcentagem de bases com Q > 30
        
        return {
            "qualidade_media": qualidade_media,
            "q30": q30,
            "comprimento_medio": len(sequencia)
        }
    
    def _calcular_cobertura(self, dados: Any) -> float:
        """Calcula cobertura do sequenciamento."""
        if isinstance(dados, tuple):
            sequencia = dados[0] if dados else ""
        else:
            sequencia = str(dados)
        
        # Simplificação - baseado no comprimento
        return min(100.0, len(sequencia) / 10.0)


class AnaliseExpressao(AnaliseGenetica):
    """Análise especializada em expressão gênica."""
    
    def executar_analise(self, dados: Any) -> Dict[str, Any]:
        """Executa análise de expressão gênica."""
        resultado_base = self.algoritmo.processar_dados(dados)
        
        return {
            "tipo_analise": "expressao_genica",
            "nome_analise": self.nome,
            "resultado_base": resultado_base,
            "niveis_expressao": self._calcular_niveis_expressao(dados),
            "genes_regulados": self._identificar_genes_regulados(dados)
        }
    
    def _calcular_niveis_expressao(self, dados: Any) -> Dict[str, float]:
        """Calcula níveis de expressão gênica."""
        # Simulação de dados de expressão
        return {
            "gene_A": 15.5,
            "gene_B": 8.2,
            "gene_C": 23.7,
            "gene_D": 3.1
        }
    
    def _identificar_genes_regulados(self, dados: Any) -> list:
        """Identifica genes regulados."""
        # Simulação de genes diferencialmente expressos
        return ["BRCA1", "TP53", "EGFR", "MYC"]


class AnaliseMutacao(AnaliseGenetica):
    """Análise especializada em detecção de mutações."""
    
    def executar_analise(self, dados: Any) -> Dict[str, Any]:
        """Executa análise de mutações."""
        resultado_base = self.algoritmo.processar_dados(dados)
        
        return {
            "tipo_analise": "detecao_mutacao",
            "nome_analise": self.nome,
            "resultado_base": resultado_base,
            "mutacoes_encontradas": self._detectar_mutacoes(dados),
            "impacto_clinico": self._avaliar_impacto_clinico(dados)
        }
    
    def _detectar_mutacoes(self, dados: Any) -> list:
        """Detecta mutações nas sequências."""
        # Simulação de mutações encontradas
        return [
            {"posicao": 123, "tipo": "SNP", "referencia": "A", "alternativa": "G"},
            {"posicao": 456, "tipo": "INDEL", "referencia": "AT", "alternativa": "A"},
            {"posicao": 789, "tipo": "SNP", "referencia": "C", "alternativa": "T"}
        ]
    
    def _avaliar_impacto_clinico(self, dados: Any) -> Dict[str, str]:
        """Avalia impacto clínico das mutações."""
        return {
            "patogenicidade": "Provavelmente patogênico",
            "classificacao": "Classe 4",
            "recomendacao": "Confirmar com Sanger"
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Combinação de Análises e Algoritmos ===")
    
    # Criar diferentes algoritmos de processamento
    alinhamento_global = AlinhamentoGlobal()
    alinhamento_local = AlinhamentoLocal()
    busca_bd = BuscaBancoDados()
    
    # Criar diferentes tipos de análises
    analise_seq = AnaliseSequenciamento("Seq_001", alinhamento_global)
    analise_exp = AnaliseExpressao("Exp_001", alinhamento_local)
    analise_mut = AnaliseMutacao("Mut_001", busca_bd)
    
    # Dados de teste
    dados_alinhamento = ("ATCGATCGATCG", "ATCGATCGATAG")
    dados_busca = ("ATCGATCG", "ref_db")
    
    # Executar análises
    resultado_seq = analise_seq.executar_analise(dados_alinhamento)
    resultado_exp = analise_exp.executar_analise(dados_alinhamento)
    resultado_mut = analise_mut.executar_analise(dados_busca)
    
    print("Resultado Análise Sequenciamento:")
    print(f"  Tipo: {resultado_seq['tipo_analise']}")
    print(f"  Alinhamento: {resultado_seq['resultado_base']['tipo_alinhamento']}")
    print(f"  Score: {resultado_seq['resultado_base']['score']}")
    
    print("\nResultado Análise Expressão:")
    print(f"  Tipo: {resultado_exp['tipo_analise']}")
    print(f"  Alinhamento: {resultado_exp['resultado_base']['tipo_alinhamento']}")
    print(f"  Melhor score: {resultado_exp['resultado_base']['melhor_score']}")
    
    print("\nResultado Análise Mutação:")
    print(f"  Tipo: {resultado_mut['tipo_analise']}")
    print(f"  Busca: {resultado_mut['resultado_base']['tipo_busca']}")
    print(f"  Hits encontrados: {len(resultado_mut['resultado_base']['hits'])}")
    
    print("\n=== Exemplo 2: Mudança Dinâmica de Algoritmo ===")
    
    print("Análise original:")
    print(f"  {analise_seq}")
    resultado_original = analise_seq.executar_analise(dados_alinhamento)
    print(f"  Score original: {resultado_original['resultado_base']['score']}")
    
    # Mudar para alinhamento local
    print("\nMudando para alinhamento local...")
    analise_seq.mudar_algoritmo(alinhamento_local)
    print(f"  {analise_seq}")
    resultado_novo = analise_seq.executar_analise(dados_alinhamento)
    print(f"  Melhor score local: {resultado_novo['resultado_base']['melhor_score']}")
    
    # Mudar para busca em banco de dados
    print("\nMudando para busca em banco de dados...")
    analise_seq.mudar_algoritmo(busca_bd)
    print(f"  {analise_seq}")
    resultado_busca_resultado = analise_seq.executar_analise(dados_busca)
    print(f"  Hits encontrados: {len(resultado_busca_resultado['resultado_base']['hits'])}")
    
    print("\n=== Exemplo 3: Extensão com Novos Algoritmos ===")
    
    class AlgoritmoPersonalizado(AlgoritmoProcessamento):
        """Novo algoritmo personalizado."""
        
        def processar_dados(self, dados: Any) -> Dict[str, Any]:
            sequencia = dados if isinstance(dados, str) else str(dados[0])
            return {
                "tipo_alinhamento": "personalizado",
                "algoritmo": "Custom Algorithm v1.0",
                "sequencia": sequencia,
                "complexidade": self._calcular_complexidade(sequencia),
                "entropia": self._calcular_entropia(sequencia)
            }
        
        def _calcular_complexidade(self, sequencia: str) -> float:
            """Calcula complexidade da sequência."""
            bases_unicas = len(set(sequencia.upper()))
            return (bases_unicas / min(4, len(sequencia))) * 100
        
        def _calcular_entropia(self, sequencia: str) -> float:
            """Calcula entropia da sequência."""
            from collections import Counter
            import math
            
            contador = Counter(sequencia.upper())
            total = len(sequencia)
            entropia = 0
            
            for count in contador.values():
                prob = count / total
                entropia -= prob * math.log2(prob)
            
            return entropia
    
    # Usar novo algoritmo
    algoritmo_custom = AlgoritmoPersonalizado()
    analise_seq.mudar_algoritmo(algoritmo_custom)
    
    resultado_custom = analise_seq.executar_analise("ATCGATCGATCG")
    print("Resultado com algoritmo personalizado:")
    print(f"  Algoritmo: {resultado_custom['resultado_base']['algoritmo']}")
    print(f"  Complexidade: {resultado_custom['resultado_base']['complexidade']:.2f}%")
    print(f"  Entropia: {resultado_custom['resultado_base']['entropia']:.3f}")
    
    print("\n=== Exemplo 4: Novo Tipo de Análise ===")
    
    class AnaliseFilogenetica(AnaliseGenetica):
        """Nova análise especializada em filogenia."""
        
        def executar_analise(self, dados: Any) -> Dict[str, Any]:
            resultado_base = self.algoritmo.processar_dados(dados)
            
            return {
                "tipo_analise": "filogenetica",
                "nome_analise": self.nome,
                "resultado_base": resultado_base,
                "arvore_filogenetico": self._construir_arvore(dados),
                "distancias_evolutivas": self._calcular_distancias(dados)
            }
        
        def _construir_arvore(self, dados: Any) -> str:
            """Constrói árvore filogenética (simplificado)."""
            return "((A,B),(C,D));"
        
        def _calcular_distancias(self, dados: Any) -> Dict[str, float]:
            """Calcula distâncias evolutivas."""
            return {"A-B": 0.1, "A-C": 0.3, "B-C": 0.25, "A-D": 0.4}
    
    # Usar nova análise
    analise_filo = AnaliseFilogenetica("Filo_001", alinhamento_global)
    resultado_filo = analise_filo.executar_analise(dados_alinhamento)
    
    print("Resultado análise filogenética:")
    print(f"  Tipo: {resultado_filo['tipo_analise']}")
    print(f"  Árvore: {resultado_filo['arvore_filogenetico']}")
    print(f"  Distâncias: {resultado_filo['distancias_evolutivas']}")
    
    print("\nBridge pattern implementado com sucesso!")
