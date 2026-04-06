from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Iterator as PyIterator
from enum import Enum


class TipoDado(Enum):
    SEQUENCIA = "sequencia"
    PROTEINA = "proteina"
    VARIAÇÃO = "variacao"
    EXPRESSAO = "expressao"


class ResultadoAnalise:
    """Representa um resultado de análise bioinformática."""
    
    def __init__(self, id_resultado: str, tipo: TipoDado, dados: Dict[str, Any]):
        self.id_resultado = id_resultado
        self.tipo = tipo
        self.dados = dados
        self.timestamp = self._gerar_timestamp()
    
    def _gerar_timestamp(self) -> float:
        """Gera timestamp atual."""
        import time
        return time.time()
    
    def __str__(self) -> str:
        return f"Resultado({self.id_resultado}, {self.tipo.value})"


class IteradorResultados(ABC):
    """Interface base para iteradores de resultados."""
    
    @abstractmethod
    def tem_proximo(self) -> bool:
        """Verifica se há próximo elemento."""
        pass
    
    @abstractmethod
    def proximo(self) -> Optional[ResultadoAnalise]:
        """Retorna próximo elemento."""
        pass
    
    @abstractmethod
    def resetar(self) -> None:
        """Reseta o iterador para o início."""
        pass


class ColecaoResultados(ABC):
    """Interface base para coleções de resultados."""
    
    @abstractmethod
    def criar_iterador(self) -> IteradorResultados:
        """Cria iterador para a coleção."""
        pass
    
    @abstractmethod
    def adicionar(self, resultado: ResultadoAnalise) -> None:
        """Adiciona resultado à coleção."""
        pass
    
    @abstractmethod
    def obter_total(self) -> int:
        """Retorna total de resultados."""
        pass


class ResultadosSequenciamento(ColecaoResultados):
    """Coleção de resultados de sequenciamento."""
    
    def __init__(self):
        self.resultados: List[ResultadoAnalise] = []
    
    def adicionar(self, resultado: ResultadoAnalise) -> None:
        """Adiciona resultado de sequenciamento."""
        if resultado.tipo == TipoDado.SEQUENCIA:
            self.resultados.append(resultado)
        else:
            raise ValueError("Tipo de resultado inválido para esta coleção")
    
    def criar_iterador(self) -> IteradorResultados:
        """Cria iterador para resultados de sequenciamento."""
        return IteradorSequenciamento(self.resultados)
    
    def obter_total(self) -> int:
        """Retorna total de resultados de sequenciamento."""
        return len(self.resultados)
    
    def obter_por_plataforma(self, plataforma: str) -> List[ResultadoAnalise]:
        """Filtra resultados por plataforma."""
        return [r for r in self.resultados 
                if r.dados.get("plataforma", "").lower() == plataforma.lower()]


class ResultadosProteomicos(ColecaoResultados):
    """Coleção de resultados proteômicos."""
    
    def __init__(self):
        self.resultados: List[ResultadoAnalise] = []
    
    def adicionar(self, resultado: ResultadoAnalise) -> None:
        """Adiciona resultado proteômico."""
        if resultado.tipo == TipoDado.PROTEINA:
            self.resultados.append(resultado)
        else:
            raise ValueError("Tipo de resultado inválido para esta coleção")
    
    def criar_iterador(self) -> IteradorResultados:
        """Cria iterador para resultados proteômicos."""
        return IteradorProteomicos(self.resultados)
    
    def obter_total(self) -> int:
        """Retorna total de resultados proteômicos."""
        return len(self.resultados)
    
    def obter_por_peso_molecular(self, peso_min: float, peso_max: float) -> List[ResultadoAnalise]:
        """Filtra por peso molecular."""
        return [r for r in self.resultados 
                if peso_min <= r.dados.get("peso_molecular", 0) <= peso_max]


class ResultadosVariacao(ColecaoResultados):
    """Coleção de resultados de variação genética."""
    
    def __init__(self):
        self.resultados: List[ResultadoAnalise] = []
    
    def adicionar(self, resultado: ResultadoAnalise) -> None:
        """Adiciona resultado de variação."""
        if resultado.tipo == TipoDado.VARIAÇÃO:
            self.resultados.append(resultado)
        else:
            raise ValueError("Tipo de resultado inválido para esta coleção")
    
    def criar_iterador(self) -> IteradorResultados:
        """Cria iterador para resultados de variação."""
        return IteradorVariacao(self.resultados)
    
    def obter_total(self) -> int:
        """Retorna total de resultados de variação."""
        return len(self.resultados)
    
    def obter_por_impacto(self, impacto: str) -> List[ResultadoAnalise]:
        """Filtra por impacto clínico."""
        return [r for r in self.resultados 
                if r.dados.get("impacto_clinico", "").lower() == impacto.lower()]


class ResultadosExpressao(ColecaoResultados):
    """Coleção de resultados de expressão gênica."""
    
    def __init__(self):
        self.resultados: List[ResultadoAnalise] = []
    
    def adicionar(self, resultado: ResultadoAnalise) -> None:
        """Adiciona resultado de expressão."""
        if resultado.tipo == TipoDado.EXPRESSAO:
            self.resultados.append(resultado)
        else:
            raise ValueError("Tipo de resultado inválido para esta coleção")
    
    def criar_iterador(self) -> IteradorResultados:
        """Cria iterador para resultados de expressão."""
        return IteradorExpressao(self.resultados)
    
    def obter_total(self) -> int:
        """Retorna total de resultados de expressão."""
        return len(self.resultados)
    
    def obter_por_fold_change(self, fold_min: float) -> List[ResultadoAnalise]:
        """Filtra por fold change mínimo."""
        return [r for r in self.resultados 
                if abs(r.dados.get("fold_change", 0)) >= fold_min]


class IteradorSequenciamento(IteradorResultados):
    """Iterador específico para resultados de sequenciamento."""
    
    def __init__(self, resultados: List[ResultadoAnalise]):
        self.resultados = resultados
        self.posicao_atual = 0
        self.filtro_plataforma: Optional[str] = None
    
    def tem_proximo(self) -> bool:
        """Verifica se há próximo resultado."""
        return self._encontrar_proximo_valido() is not None
    
    def proximo(self) -> Optional[ResultadoAnalise]:
        """Retorna próximo resultado de sequenciamento."""
        proximo_idx = self._encontrar_proximo_valido()
        if proximo_idx is not None:
            self.posicao_atual = proximo_idx + 1
            return self.resultados[proximo_idx]
        return None
    
    def resetar(self) -> None:
        """Reseta iterador."""
        self.posicao_atual = 0
    
    def definir_filtro_plataforma(self, plataforma: str) -> None:
        """Define filtro por plataforma."""
        self.filtro_plataforma = plataforma
        self.resetar()
    
    def _encontrar_proximo_valido(self) -> Optional[int]:
        """Encontra próximo índice válido."""
        for i in range(self.posicao_atual, len(self.resultados)):
            resultado = self.resultados[i]
            if self.filtro_plataforma:
                if resultado.dados.get("plataforma", "").lower() == self.filtro_plataforma.lower():
                    return i
            else:
                return i
        return None


class IteradorProteomicos(IteradorResultados):
    """Iterador específico para resultados proteômicos."""
    
    def __init__(self, resultados: List[ResultadoAnalise]):
        self.resultados = resultados
        self.posicao_atual = 0
        self.filtro_peso_min: Optional[float] = None
        self.filtro_peso_max: Optional[float] = None
        self.ordem_peso: bool = False  # False = normal, True = por peso
    
    def tem_proximo(self) -> bool:
        """Verifica se há próximo resultado."""
        return self._encontrar_proximo_valido() is not None
    
    def proximo(self) -> Optional[ResultadoAnalise]:
        """Retorna próximo resultado proteômico."""
        proximo_idx = self._encontrar_proximo_valido()
        if proximo_idx is not None:
            resultado = self.resultados[proximo_idx]
            if not self.ordem_peso:
                self.posicao_atual = proximo_idx + 1
            return resultado
        return None
    
    def resetar(self) -> None:
        """Reseta iterador."""
        self.posicao_atual = 0
        if self.ordem_peso:
            self.resultados.sort(key=lambda r: r.dados.get("peso_molecular", 0))
    
    def definir_filtro_peso(self, peso_min: float = None, peso_max: float = None) -> None:
        """Define filtro por peso molecular."""
        self.filtro_peso_min = peso_min
        self.filtro_peso_max = peso_max
        self.resetar()
    
    def definir_ordem_peso(self, crescente: bool = True) -> None:
        """Define ordenação por peso molecular."""
        self.ordem_peso = True
        self.resultados.sort(key=lambda r: r.dados.get("peso_molecular", 0), reverse=not crescente)
        self.resetar()
    
    def _encontrar_proximo_valido(self) -> Optional[int]:
        """Encontra próximo índice válido."""
        for i in range(self.posicao_atual, len(self.resultados)):
            resultado = self.resultados[i]
            peso = resultado.dados.get("peso_molecular", 0)
            
            if self.filtro_peso_min is not None and peso < self.filtro_peso_min:
                continue
            if self.filtro_peso_max is not None and peso > self.filtro_peso_max:
                continue
            
            return i
        return None


class IteradorVariacao(IteradorResultados):
    """Iterador específico para resultados de variação."""
    
    def __init__(self, resultados: List[ResultadoAnalise]):
        self.resultados = resultados
        self.posicao_atual = 0
        self.filtro_impacto: Optional[str] = None
        self.filtro_frequencia_max: Optional[float] = None
    
    def tem_proximo(self) -> bool:
        """Verifica se há próximo resultado."""
        return self._encontrar_proximo_valido() is not None
    
    def proximo(self) -> Optional[ResultadoAnalise]:
        """Retorna próximo resultado de variação."""
        proximo_idx = self._encontrar_proximo_valido()
        if proximo_idx is not None:
            self.posicao_atual = proximo_idx + 1
            return self.resultados[proximo_idx]
        return None
    
    def resetar(self) -> None:
        """Reseta iterador."""
        self.posicao_atual = 0
    
    def definir_filtro_impacto(self, impacto: str) -> None:
        """Define filtro por impacto clínico."""
        self.filtro_impacto = impacto
        self.resetar()
    
    def definir_filtro_frequencia(self, freq_max: float) -> None:
        """Define filtro por frequência máxima."""
        self.filtro_frequencia_max = freq_max
        self.resetar()
    
    def _encontrar_proximo_valido(self) -> Optional[int]:
        """Encontra próximo índice válido."""
        for i in range(self.posicao_atual, len(self.resultados)):
            resultado = self.resultados[i]
            
            if self.filtro_impacto:
                if resultado.dados.get("impacto_clinico", "").lower() != self.filtro_impacto.lower():
                    continue
            
            if self.filtro_frequencia_max is not None:
                freq = resultado.dados.get("frequencia", 1.0)
                if freq > self.filtro_frequencia_max:
                    continue
            
            return i
        return None


class IteradorExpressao(IteradorResultados):
    """Iterador específico para resultados de expressão."""
    
    def __init__(self, resultados: List[ResultadoAnalise]):
        self.resultados = resultados
        self.posicao_atual = 0
        self.filtro_fold_change: Optional[float] = None
        self.filtro_regulacao: Optional[str] = None  # "up", "down", "all"
        self.ordem_fold_change: bool = False
    
    def tem_proximo(self) -> bool:
        """Verifica se há próximo resultado."""
        return self._encontrar_proximo_valido() is not None
    
    def proximo(self) -> Optional[ResultadoAnalise]:
        """Retorna próximo resultado de expressão."""
        proximo_idx = self._encontrar_proximo_valido()
        if proximo_idx is not None:
            resultado = self.resultados[proximo_idx]
            if not self.ordem_fold_change:
                self.posicao_atual = proximo_idx + 1
            return resultado
        return None
    
    def resetar(self) -> None:
        """Reseta iterador."""
        self.posicao_atual = 0
        if self.ordem_fold_change:
            self.resultados.sort(key=lambda r: abs(r.dados.get("fold_change", 0)), reverse=True)
    
    def definir_filtro_fold_change(self, fold_min: float) -> None:
        """Define filtro por fold change mínimo."""
        self.filtro_fold_change = fold_min
        self.resetar()
    
    def definir_filtro_regulacao(self, tipo: str) -> None:
        """Define filtro por tipo de regulação."""
        self.filtro_regulacao = tipo.lower()
        self.resetar()
    
    def definir_ordem_fold_change(self) -> None:
        """Define ordenação por fold change."""
        self.ordem_fold_change = True
        self.resultados.sort(key=lambda r: abs(r.dados.get("fold_change", 0)), reverse=True)
        self.resetar()
    
    def _encontrar_proximo_valido(self) -> Optional[int]:
        """Encontra próximo índice válido."""
        for i in range(self.posicao_atual, len(self.resultados)):
            resultado = self.resultados[i]
            
            if self.filtro_fold_change is not None:
                fold = resultado.dados.get("fold_change", 0)
                if abs(fold) < self.filtro_fold_change:
                    continue
            
            if self.filtro_regulacao and self.filtro_regulacao != "all":
                fold = resultado.dados.get("fold_change", 0)
                if self.filtro_regulacao == "up" and fold <= 0:
                    continue
                if self.filtro_regulacao == "down" and fold >= 0:
                    continue
            
            return i
        return None


class IteradorMultiplasColecoes:
    """Iterador que percorre múltiplas coleções."""
    
    def __init__(self, colecoes: List[ColecaoResultados]):
        self.colecoes = colecoes
        self.indice_colecao_atual = 0
        self.iterador_atual: Optional[IteradorResultados] = None
        self._iniciar_primeira_colecao()
    
    def _iniciar_primeira_colecao(self) -> None:
        """Inicia primeira coleção."""
        if self.colecoes:
            self.iterador_atual = self.colecoes[0].criar_iterador()
    
    def tem_proximo(self) -> bool:
        """Verifica se há próximo resultado em qualquer coleção."""
        if not self.iterador_atual:
            return False
        
        if self.iterador_atual.tem_proximo():
            return True
        
        # Tenta próxima coleção
        return self._proxima_colecao_com_dados()
    
    def proximo(self) -> Optional[ResultadoAnalise]:
        """Retorna próximo resultado de qualquer coleção."""
        if not self.iterador_atual:
            return None
        
        # Tenta obter da coleção atual
        if self.iterador_atual.tem_proximo():
            return self.iterador_atual.proximo()
        
        # Se não tem mais na atual, vai para próxima
        if self._proxima_colecao_com_dados():
            return self.iterador_atual.proximo()
        
        return None
    
    def resetar(self) -> None:
        """Reseta todas as coleções."""
        self.indice_colecao_atual = 0
        self._iniciar_primeira_colecao()
    
    def _proxima_colecao_com_dados(self) -> bool:
        """Avança para próxima coleção com dados."""
        while self.indice_colecao_atual < len(self.colecoes) - 1:
            self.indice_colecao_atual += 1
            self.iterador_atual = self.colecoes[self.indice_colecao_atual].criar_iterador()
            if self.iterador_atual.tem_proximo():
                return True
        return False


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Iteração sobre Resultados de Sequenciamento ===")
    
    # Criar coleção de resultados de sequenciamento
    resultados_seq = ResultadosSequenciamento()
    
    # Adicionar resultados
    resultados_seq.adicionar(ResultadoAnalise(
        "SEQ001", TipoDado.SEQUENCIA,
        {"plataforma": "illumina", "reads": 50000000, "qualidade": "Q30"}
    ))
    resultados_seq.adicionar(ResultadoAnalise(
        "SEQ002", TipoDado.SEQUENCIA,
        {"plataforma": "ont", "reads": 1000000, "qualidade": "Q12"}
    ))
    resultados_seq.adicionar(ResultadoAnalise(
        "SEQ003", TipoDado.SEQUENCIA,
        {"plataforma": "illumina", "reads": 45000000, "qualidade": "Q32"}
    ))
    resultados_seq.adicionar(ResultadoAnalise(
        "SEQ004", TipoDado.SEQUENCIA,
        {"plataforma": "pacbio", "reads": 2000000, "qualidade": "Q25"}
    ))
    
    print(f"Total de resultados de sequenciamento: {resultados_seq.obter_total()}")
    
    # Iterar sobre todos os resultados
    print("\nIterando sobre todos os resultados:")
    iterador_seq = resultados_seq.criar_iterador()
    while iterador_seq.tem_proximo():
        resultado = iterador_seq.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['plataforma']} - {resultado.dados['reads']:,} reads")
    
    # Iterar com filtro por plataforma
    print("\nIterando apenas resultados Illumina:")
    iterador_seq.definir_filtro_plataforma("illumina")
    while iterador_seq.tem_proximo():
        resultado = iterador_seq.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['reads']:,} reads")
    
    print("\n=== Exemplo 2: Iteração sobre Resultados Proteômicos ===")
    
    # Criar coleção proteômica
    resultados_prot = ResultadosProteomicos()
    
    # Adicionar resultados
    resultados_prot.adicionar(ResultadoAnalise(
        "PROT001", TipoDado.PROTEINA,
        {"proteina": "Hemoglobina", "peso_molecular": 15867.0, "comprimento": 146}
    ))
    resultados_prot.adicionar(ResultadoAnalise(
        "PROT002", TipoDado.PROTEINA,
        {"proteina": "Mioglobina", "peso_molecular": 16950.0, "comprimento": 154}
    ))
    resultados_prot.adicionar(ResultadoAnalise(
        "PROT003", TipoDado.PROTEINA,
        {"proteina": "Albumina", "peso_molecular": 66437.0, "comprimento": 585}
    ))
    resultados_prot.adicionar(ResultadoAnalise(
        "PROT004", TipoDado.PROTEINA,
        {"proteina": "Insulina", "peso_molecular": 5808.0, "comprimento": 51}
    ))
    
    print(f"Total de resultados proteômicos: {resultados_prot.obter_total()}")
    
    # Iterar ordenado por peso molecular
    print("\nIterando ordenado por peso molecular (crescente):")
    iterador_prot = resultados_prot.criar_iterador()
    iterador_prot.definir_ordem_peso(crescente=True)
    while iterador_prot.tem_proximo():
        resultado = iterador_prot.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['proteina']} - {resultado.dados['peso_molecular']:.0f} Da")
    
    # Iterar com filtro de peso
    print("\nIterando proteínas entre 10k e 20k Da:")
    iterador_prot.definir_filtro_peso(10000, 20000)
    while iterador_prot.tem_proximo():
        resultado = iterador_prot.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['proteina']} - {resultado.dados['peso_molecular']:.0f} Da")
    
    print("\n=== Exemplo 3: Iteração sobre Resultados de Variação ===")
    
    # Criar coleção de variação
    resultados_var = ResultadosVariacao()
    
    # Adicionar resultados
    resultados_var.adicionar(ResultadoAnalise(
        "VAR001", TipoDado.VARIAÇÃO,
        {"gene": "BRCA1", "tipo": "SNP", "impacto_clinico": "patogenico", "frequencia": 0.001}
    ))
    resultados_var.adicionar(ResultadoAnalise(
        "VAR002", TipoDado.VARIAÇÃO,
        {"gene": "TP53", "tipo": "INDEL", "impacto_clinico": "benigno", "frequencia": 0.05}
    ))
    resultados_var.adicionar(ResultadoAnalise(
        "VAR003", TipoDado.VARIAÇÃO,
        {"gene": "EGFR", "tipo": "SNP", "impacto_clinico": "patogenico", "frequencia": 0.002}
    ))
    resultados_var.adicionar(ResultadoAnalise(
        "VAR004", TipoDado.VARIAÇÃO,
        {"gene": "KRAS", "tipo": "SNP", "impacto_clinico": "incerto", "frequencia": 0.01}
    ))
    
    # Iterar apenas variantes patogênicas
    print("Variantes patogênicas:")
    iterador_var = resultados_var.criar_iterador()
    iterador_var.definir_filtro_impacto("patogenico")
    while iterador_var.tem_proximo():
        resultado = iterador_var.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['gene']} - {resultado.dados['impacto_clinico']}")
    
    # Iterar variantes raras (frequência < 1%)
    print("\nVariantes raras (frequência < 1%):")
    iterador_var.resetar()
    iterador_var.definir_filtro_frequencia(0.01)
    while iterador_var.tem_proximo():
        resultado = iterador_var.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['gene']} - freq: {resultado.dados['frequencia']:.3f}")
    
    print("\n=== Exemplo 4: Iteração sobre Resultados de Expressão ===")
    
    # Criar coleção de expressão
    resultados_exp = ResultadosExpressao()
    
    # Adicionar resultados
    resultados_exp.adicionar(ResultadoAnalise(
        "EXP001", TipoDado.EXPRESSAO,
        {"gene": "BRCA1", "expressao_controle": 10.0, "expressao_tratamento": 25.0, "fold_change": 2.5}
    ))
    resultados_exp.adicionar(ResultadoAnalise(
        "EXP002", TipoDado.EXPRESSAO,
        {"gene": "TP53", "expressao_controle": 15.0, "expressao_tratamento": 7.5, "fold_change": -2.0}
    ))
    resultados_exp.adicionar(ResultadoAnalise(
        "EXP003", TipoDado.EXPRESSAO,
        {"gene": "EGFR", "expressao_controle": 8.0, "expressao_tratamento": 40.0, "fold_change": 5.0}
    ))
    resultados_exp.adicionar(ResultadoAnalise(
        "EXP004", TipoDado.EXPRESSAO,
        {"gene": "MYC", "expressao_controle": 12.0, "expressao_tratamento": 18.0, "fold_change": 1.5}
    ))
    
    # Iterar genes up-regulated (fold change > 0)
    print("Genes up-regulated:")
    iterador_exp = resultados_exp.criar_iterador()
    iterador_exp.definir_filtro_regulacao("up")
    while iterador_exp.tem_proximo():
        resultado = iterador_exp.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['gene']} - FC: {resultado.dados['fold_change']:.1f}")
    
    # Iterar por fold change mínimo
    print("\nGenes com |FC| >= 2.0:")
    iterador_exp.resetar()
    iterador_exp.definir_filtro_fold_change(2.0)
    while iterador_exp.tem_proximo():
        resultado = iterador_exp.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['gene']} - FC: {resultado.dados['fold_change']:.1f}")
    
    # Iterar ordenado por fold change
    print("\nGenes ordenados por fold change (maior para menor):")
    iterador_exp.resetar()
    iterador_exp.definir_ordem_fold_change()
    while iterador_exp.tem_proximo():
        resultado = iterador_exp.proximo()
        print(f"  {resultado.id_resultado}: {resultado.dados['gene']} - FC: {resultado.dados['fold_change']:.1f}")
    
    print("\n=== Exemplo 5: Iteração sobre Múltiplas Coleções ===")
    
    # Criar iterador múltiplo
    colecoes = [resultados_seq, resultados_prot, resultados_var, resultados_exp]
    iterador_multiplas = IteradorMultiplasColecoes(colecoes)
    
    print("Iterando sobre todas as coleções:")
    while iterador_multiplas.tem_proximo():
        resultado = iterador_multiplas.proximo()
        tipo_nome = resultado.tipo.value
        if resultado.tipo == TipoDado.SEQUENCIA:
            info = f"{resultado.dados['plataforma']} - {resultado.dados['reads']:,} reads"
        elif resultado.tipo == TipoDado.PROTEINA:
            info = f"{resultado.dados['proteina']} - {resultado.dados['peso_molecular']:.0f} Da"
        elif resultado.tipo == TipoDado.VARIAÇÃO:
            info = f"{resultado.dados['gene']} - {resultado.dados['impacto_clinico']}"
        else:  # EXPRESSAO
            info = f"{resultado.dados['gene']} - FC: {resultado.dados['fold_change']:.1f}"
        
        print(f"  {resultado.id_resultado} ({tipo_nome}): {info}")
    
    print("\n=== Exemplo 6: Iteração com Python Iterator Protocol ===")
    
    # Criar classe compatível com protocolo Python
    class ColecaoPython:
        def __init__(self, colecao: ColecaoResultados):
            self.colecao = colecao
        
        def __iter__(self) -> PyIterator[ResultadoAnalise]:
            iterador = self.colecao.criar_iterador()
            while iterador.tem_proximo():
                yield iterador.proximo()
    
    # Usar com for loop do Python
    colecao_python = ColecaoPython(resultados_seq)
    
    print("Usando for loop do Python:")
    for resultado in colecao_python:
        print(f"  {resultado.id_resultado}: {resultado.dados['plataforma']}")
    
    # Usar com list comprehension
    print("\nUsando list comprehension:")
    reads_illumina = [r.dados['reads'] for r in ColecaoPython(resultados_seq) 
                     if r.dados['plataforma'] == 'illumina']
    print(f"  Reads Illumina: {reads_illumina}")
    
    # Usar com filter
    print("\nUsando filter:")
    variantes_patogenicas = list(filter(
        lambda r: r.dados.get('impacto_clinico') == 'patogenico',
        ColecaoPython(resultados_var)
    ))
    print(f"  Variantes patogênicas: {[v.id_resultado for v in variantes_patogenicas]}")
    
    print("\nIterator pattern implementado com sucesso!")
