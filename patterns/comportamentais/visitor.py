from abc import ABC, abstractmethod
from typing import Dict, Any, List
import time
from enum import Enum


class TipoComponente(Enum):
    GENE_PROTEINA = "gene_proteina"
    GENE_REGULADOR = "gene_regulador"
    GENE_ESTRUTURAL = "gene_estrutural"
    GENE_HOUSEKEEPING = "gene_housekeeping"


class ComponenteGenetico(ABC):
    """Interface base para componentes genéticos."""
    
    def __init__(self, nome: str, cromossomo: str, posicao: int):
        self.nome = nome
        self.cromossomo = cromossomo
        self.posicao = posicao
        self.sequencia = ""
        self.expressao = 0.0
        self.metadados: Dict[str, Any] = {}
    
    @abstractmethod
    def aceitar(self, visitante: 'VisitanteGenetico') -> Any:
        """Aceita um visitante para análise."""
        pass
    
    @abstractmethod
    def obter_tipo(self) -> TipoComponente:
        """Retorna o tipo do componente."""
        pass
    
    def definir_sequencia(self, sequencia: str) -> None:
        """Define a sequência do componente."""
        self.sequencia = sequencia
    
    def definir_expressao(self, expressao: float) -> None:
        """Define o nível de expressão."""
        self.expressao = expressao
    
    def adicionar_metadado(self, chave: str, valor: Any) -> None:
        """Adiciona metadado."""
        self.metadados[chave] = valor
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.nome}, {self.cromossomo}:{self.posicao})"


class GeneProteina(ComponenteGenetico):
    """Gene que codifica uma proteína."""
    
    def __init__(self, nome: str, cromossomo: str, posicao: int, proteina: str):
        super().__init__(nome, cromossomo, posicao)
        self.proteina_codificada = proteina
        self.dominios_proteicos: List[str] = []
        self.peso_molecular = 0.0
    
    def obter_tipo(self) -> TipoComponente:
        """Retorna tipo do componente."""
        return TipoComponente.GENE_PROTEINA
    
    def aceitar(self, visitante: 'VisitanteGenetico') -> Any:
        """Aceita visitante para análise de expressão gênica."""
        return visitante.visitar_gene_proteina(self)
    
    def adicionar_dominio(self, dominio: str) -> None:
        """Adiciona domínio proteico."""
        if dominio not in self.dominios_proteicos:
            self.dominios_proteicos.append(dominio)
    
    def definir_peso_molecular(self, peso: float) -> None:
        """Define peso molecular da proteína."""
        self.peso_molecular = peso


class GeneRegulador(ComponenteGenetico):
    """Gene que regula expressão de outros genes."""
    
    def __init__(self, nome: str, cromossomo: str, posicao: int, tipo_regulacao: str):
        super().__init__(nome, cromossomo, posicao)
        self.tipo_regulacao = tipo_regulacao  # "ativador" ou "repressor"
        self.alvos_regulacao: List[str] = []
        self.sites_ligacao: List[str] = []
        self.forca_regulacao = 0.0
    
    def obter_tipo(self) -> TipoComponente:
        """Retorna tipo do componente."""
        return TipoComponente.GENE_REGULADOR
    
    def aceitar(self, visitante: 'VisitanteGenetico') -> Any:
        """Aceita visitante para análise de função regulatória."""
        return visitante.visitar_gene_regulador(self)
    
    def adicionar_alvo(self, gene_alvo: str) -> None:
        """Adiciona gene alvo da regulação."""
        if gene_alvo not in self.alvos_regulacao:
            self.alvos_regulacao.append(gene_alvo)
    
    def adicionar_site_ligacao(self, site: str) -> None:
        """Adiciona sítio de ligação."""
        if site not in self.sites_ligacao:
            self.sites_ligacao.append(site)
    
    def definir_forca_regulacao(self, forca: float) -> None:
        """Define força da regulação."""
        self.forca_regulacao = forca


class GeneEstrutural(ComponenteGenetico):
    """Gene estrutural com função celular."""
    
    def __init__(self, nome: str, cromossomo: str, posicao: int, funcao_celular: str):
        super().__init__(nome, cromossomo, posicao)
        self.funcao_celular = funcao_celular
        self.compartimento_celular = ""
        self.interacoes_proteicas: List[str] = []
        self.essencialidade = False
    
    def obter_tipo(self) -> TipoComponente:
        """Retorna tipo do componente."""
        return TipoComponente.GENE_ESTRUTURAL
    
    def aceitar(self, visitante: 'VisitanteGenetico') -> Any:
        """Aceita visitante para análise funcional."""
        return visitante.visitar_gene_estrutural(self)
    
    def definir_compartimento(self, compartimento: str) -> None:
        """Define compartimento celular."""
        self.compartimento_celular = compartimento
    
    def adicionar_interacao(self, proteina: str) -> None:
        """Adiciona interação proteica."""
        if proteina not in self.interacoes_proteicas:
            self.interacoes_proteicas.append(proteina)
    
    def definir_essencialidade(self, essencial: bool) -> None:
        """Define se gene é essencial."""
        self.essencialidade = essencial


class GeneHousekeeping(ComponenteGenetico):
    """Gene housekeeping com expressão constitutiva."""
    
    def __init__(self, nome: str, cromossomo: str, posicao: int, via_metabolica: str):
        super().__init__(nome, cromossomo, posicao)
        self.via_metabolica = via_metabolica
        self.nivel_basal = 1.0
        self.condicoes_experimento: List[str] = []
        self.estabilidade_mrna = 0.0
    
    def obter_tipo(self) -> TipoComponente:
        """Retorna tipo do componente."""
        return TipoComponente.GENE_HOUSEKEEPING
    
    def aceitar(self, visitante: 'VisitanteGenetico') -> Any:
        """Aceita visitante para análise de estabilidade."""
        return visitante.visitar_gene_housekeeping(self)
    
    def definir_nivel_basal(self, nivel: float) -> None:
        """Define nível basal de expressão."""
        self.nivel_basal = nivel
    
    def adicionar_condicao(self, condicao: str) -> None:
        """Adiciona condição experimental."""
        if condicao not in self.condicoes_experimento:
            self.condicoes_experimento.append(condicao)
    
    def definir_estabilidade_mrna(self, estabilidade: float) -> None:
        """Define estabilidade do mRNA."""
        self.estabilidade_mrna = estabilidade


class VisitanteGenetico(ABC):
    """Interface base para visitantes genéticos."""
    
    @abstractmethod
    def visitar_gene_proteina(self, gene: GeneProteina) -> Any:
        """Visita gene de proteína."""
        pass
    
    @abstractmethod
    def visitar_gene_regulador(self, gene: GeneRegulador) -> Any:
        """Visita gene regulador."""
        pass
    
    @abstractmethod
    def visitar_gene_estrutural(self, gene: GeneEstrutural) -> Any:
        """Visita gene estrutural."""
        pass
    
    @abstractmethod
    def visitar_gene_housekeeping(self, gene: GeneHousekeeping) -> Any:
        """Visita gene housekeeping."""
        pass


class AnalisadorMolecular(VisitanteGenetico):
    """Visitante que realiza análise molecular dos genes."""
    
    def __init__(self):
        self.resultados_analise: List[Dict[str, Any]] = []
        self.estatisticas = {
            "genes_analisados": 0,
            "tipos_analisados": {},
            "tempo_total": 0.0
        }
    
    def visitar_gene_proteina(self, gene: GeneProteina) -> Dict[str, Any]:
        """Analisa gene de proteína."""
        inicio = time.time()
        
        print(f"Analisando gene de proteína: {gene.nome}")
        
        # Análise de composição da sequência
        composicao = self._analisar_composicao(gene.sequencia)
        
        # Análise de propriedades da proteína
        propriedades = self._analisar_propriedades_proteina(gene)
        
        # Análise de domínios funcionais
        analise_dominios = self._analisar_dominios(gene.dominios_proteicos)
        
        resultado = {
            "gene": gene.nome,
            "tipo": "gene_proteina",
            "proteina": gene.proteina_codificada,
            "composicao_sequencia": composicao,
            "propriedades_proteina": propriedades,
            "analise_dominios": analise_dominios,
            "expressao": gene.expressao,
            "peso_molecular": gene.peso_molecular,
            "timestamp": time.time()
        }
        
        self.resultados_analise.append(resultado)
        self._atualizar_estatisticas("gene_proteina")
        
        tempo_analise = time.time() - inicio
        self.estatisticas["tempo_total"] += tempo_analise
        
        print(f"  Análise concluída em {tempo_analise:.3f}s")
        return resultado
    
    def visitar_gene_regulador(self, gene: GeneRegulador) -> Dict[str, Any]:
        """Analisa gene regulador."""
        inicio = time.time()
        
        print(f"Analisando gene regulador: {gene.nome}")
        
        # Análise de sítios de ligação
        analise_sites = self._analisar_sites_ligacao(gene.sites_ligacao)
        
        # Análise de alvos de regulação
        analise_alvos = self._analisar_alvos_regulacao(gene.alvos_regulacao)
        
        # Análise de força regulatória
        analise_forca = self._analisar_forca_regulatoria(gene.forca_regulacao, gene.tipo_regulacao)
        
        resultado = {
            "gene": gene.nome,
            "tipo": "gene_regulador",
            "tipo_regulacao": gene.tipo_regulacao,
            "analise_sites": analise_sites,
            "analise_alvos": analise_alvos,
            "analise_forca": analise_forca,
            "expressao": gene.expressao,
            "timestamp": time.time()
        }
        
        self.resultados_analise.append(resultado)
        self._atualizar_estatisticas("gene_regulador")
        
        tempo_analise = time.time() - inicio
        self.estatisticas["tempo_total"] += tempo_analise
        
        print(f"  Análise concluída em {tempo_analise:.3f}s")
        return resultado
    
    def visitar_gene_estrutural(self, gene: GeneEstrutural) -> Dict[str, Any]:
        """Analisa gene estrutural."""
        inicio = time.time()
        
        print(f"Analisando gene estrutural: {gene.nome}")
        
        # Análise funcional
        analise_funcional = self._analisar_funcao_celular(gene.funcao_celular, gene.compartimento_celular)
        
        # Análise de interações
        analise_interacoes = self._analisar_interacoes_proteicas(gene.interacoes_proteicas)
        
        # Análise de essencialidade
        analise_essencialidade = self._analisar_essencialidade(gene.essencialidade, gene.expressao)
        
        resultado = {
            "gene": gene.nome,
            "tipo": "gene_estrutural",
            "funcao_celular": gene.funcao_celular,
            "compartimento": gene.compartimento_celular,
            "analise_funcional": analise_funcional,
            "analise_interacoes": analise_interacoes,
            "analise_essencialidade": analise_essencialidade,
            "expressao": gene.expressao,
            "timestamp": time.time()
        }
        
        self.resultados_analise.append(resultado)
        self._atualizar_estatisticas("gene_estrutural")
        
        tempo_analise = time.time() - inicio
        self.estatisticas["tempo_total"] += tempo_analise
        
        print(f"  Análise concluída em {tempo_analise:.3f}s")
        return resultado
    
    def visitar_gene_housekeeping(self, gene: GeneHousekeeping) -> Dict[str, Any]:
        """Analisa gene housekeeping."""
        inicio = time.time()
        
        print(f"Analisando gene housekeeping: {gene.nome}")
        
        # Análise de estabilidade
        analise_estabilidade = self._analisar_estabilidade_mrna(gene.estabilidade_mrna, gene.nivel_basal)
        
        # Análise de via metabólica
        analise_via = self._analisar_via_metabolica(gene.via_metabolica)
        
        # Análise de condições experimentais
        analise_condicoes = self._analisar_condicoes_experimento(gene.condicoes_experimento, gene.expressao)
        
        resultado = {
            "gene": gene.nome,
            "tipo": "gene_housekeeping",
            "via_metabolica": gene.via_metabolica,
            "nivel_basal": gene.nivel_basal,
            "analise_estabilidade": analise_estabilidade,
            "analise_via": analise_via,
            "analise_condicoes": analise_condicoes,
            "expressao": gene.expressao,
            "timestamp": time.time()
        }
        
        self.resultados_analise.append(resultado)
        self._atualizar_estatisticas("gene_housekeeping")
        
        tempo_analise = time.time() - inicio
        self.estatisticas["tempo_total"] += tempo_analise
        
        print(f"  Análise concluída em {tempo_analise:.3f}s")
        return resultado
    
    def _analisar_composicao(self, sequencia: str) -> Dict[str, Any]:
        """Analisa composição da sequência."""
        if not sequencia:
            return {"erro": "Sequência vazia"}
        
        composicao = {"A": 0, "T": 0, "C": 0, "G": 0, "N": 0}
        for base in sequencia.upper():
            if base in composicao:
                composicao[base] += 1
        
        total = sum(composicao.values())
        gc_content = (composicao["G"] + composicao["C"]) / total * 100 if total > 0 else 0
        
        return {
            "composicao": composicao,
            "total_bases": total,
            "gc_content": gc_content,
            "complexidade": len(set(sequencia.upper())) / min(4, total) * 100
        }
    
    def _analisar_propriedades_proteina(self, gene: GeneProteina) -> Dict[str, Any]:
        """Analisa propriedades da proteína codificada."""
        return {
            "peso_molecular": gene.peso_molecular,
            "dominios_count": len(gene.dominios_proteicos),
            "dominios": gene.dominios_proteicos,
            "predicao_toxicidade": "baixa",
            "solubilidade": "alta"
        }
    
    def _analisar_dominios(self, dominios: List[str]) -> Dict[str, Any]:
        """Analisa domínios funcionais."""
        return {
            "total_dominios": len(dominios),
            "dominios": dominios,
            "dominios_conservados": len([d for d in dominios if "conserved" in d.lower()]),
            "predicao_funcional": "ativa"
        }
    
    def _analisar_sites_ligacao(self, sites: List[str]) -> Dict[str, Any]:
        """Analisa sítios de ligação."""
        return {
            "total_sites": len(sites),
            "sites": sites,
            "consenso_encontrado": len([s for s in sites if "TATA" in s or "CAAT" in s]),
            "afinidade_media": "alta"
        }
    
    def _analisar_alvos_regulacao(self, alvos: List[str]) -> Dict[str, Any]:
        """Analisa alvos de regulação."""
        return {
            "total_alvos": len(alvos),
            "alvos": alvos,
            "categorias_alvos": ["metabolismo", "crescimento", "resposta_ao_estresse"],
            "rede_regulatoria": "complexa"
        }
    
    def _analisar_forca_regulatoria(self, forca: float, tipo: str) -> Dict[str, Any]:
        """Analisa força regulatória."""
        nivel = "forte" if abs(forca) > 0.7 else "moderada" if abs(forca) > 0.3 else "fraca"
        
        return {
            "forca_regulatoria": forca,
            "nivel": nivel,
            "tipo_regulacao": tipo,
            "eficiencia": "alta" if nivel == "forte" else "media"
        }
    
    def _analisar_funcao_celular(self, funcao: str, compartimento: str) -> Dict[str, Any]:
        """Analisa função celular."""
        return {
            "funcao": funcao,
            "compartimento": compartimento,
            "categoria_funcional": self._classificar_funcao(funcao),
            "via_associada": self._identificar_via(funcao)
        }
    
    def _analisar_interacoes_proteicas(self, interacoes: List[str]) -> Dict[str, Any]:
        """Analisa interações proteicas."""
        return {
            "total_interacoes": len(interacoes),
            "interacoes": interacoes,
            "grau_conectividade": "alto" if len(interacoes) > 5 else "medio",
            "hub_proteico": len(interacoes) > 10
        }
    
    def _analisar_essencialidade(self, essencial: bool, expressao: float) -> Dict[str, Any]:
        """Analisa essencialidade do gene."""
        return {
            "essencial": essencial,
            "expressao": expressao,
            "viabilidade_celular": "critica" if essencial else "normal",
            "alvo_terapeutico": essencial and expressao > 1.0
        }
    
    def _analisar_estabilidade_mrna(self, estabilidade: float, nivel_basal: float) -> Dict[str, Any]:
        """Analisa estabilidade do mRNA."""
        return {
            "estabilidade": estabilidade,
            "nivel_basal": nivel_basal,
            "meia_vida": "longa" if estabilidade > 0.7 else "curta",
            "regulacao_pos_transcricional": "baixa"
        }
    
    def _analisar_via_metabolica(self, via: str) -> Dict[str, Any]:
        """Analisa via metabólica."""
        return {
            "via": via,
            "categoria": self._classificar_via(via),
            "essencialidade_via": "essencial" if via in ["glicolise", "TCA"] else "opcional",
            "complexidade": "alta"
        }
    
    def _analisar_condicoes_experimento(self, condicoes: List[str], expressao: float) -> Dict[str, Any]:
        """Analisa condições experimentais."""
        return {
            "condicoes": condicoes,
            "total_condicoes": len(condicoes),
            "variabilidade": "alta" if len(condicoes) > 5 else "baixa",
            "expressao_media": expressao
        }
    
    def _classificar_funcao(self, funcao: str) -> str:
        """Classifica função celular."""
        if "metabol" in funcao.lower():
            return "metabolismo"
        elif "transcric" in funcao.lower():
            return "transcricao"
        elif "tradu" in funcao.lower():
            return "traducao"
        else:
            return "outra"
    
    def _identificar_via(self, funcao: str) -> str:
        """Identifica via associada."""
        if "glicolise" in funcao.lower():
            return "glicolise"
        elif "DNA" in funcao:
            return "replicacao_DNA"
        else:
            return "desconhecida"
    
    def _classificar_via(self, via: str) -> str:
        """Classifica via metabólica."""
        if "glicolise" in via.lower() or "TCA" in via:
            return "central"
        elif "sintese" in via.lower():
            return "biossintese"
        else:
            return "degradacao"
    
    def _atualizar_estatisticas(self, tipo: str) -> None:
        """Atualiza estatísticas da análise."""
        self.estatisticas["genes_analisados"] += 1
        self.estatisticas["tipos_analisados"][tipo] = \
            self.estatisticas["tipos_analisados"].get(tipo, 0) + 1
    
    def obter_resultados(self) -> List[Dict[str, Any]]:
        """Retorna todos os resultados da análise."""
        return self.resultados_analise.copy()
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas da análise."""
        return self.estatisticas.copy()
    
    def limpar_resultados(self) -> None:
        """Limpa todos os resultados."""
        self.resultados_analise.clear()
        self.estatisticas = {
            "genes_analisados": 0,
            "tipos_analisados": {},
            "tempo_total": 0.0
        }


class OtimizadorTerapeutico(VisitanteGenetico):
    """Visitante que identifica alvos terapêuticos."""
    
    def __init__(self):
        self.alvos_terapeuticos: List[Dict[str, Any]] = []
        self.criterios_avaliacao = {
            "essencialidade": 0.3,
            "expressao_alta": 2.0,
            "druggability": 0.7
        }
    
    def visitar_gene_proteina(self, gene: GeneProteina) -> Dict[str, Any]:
        """Avalia gene de proteína como alvo terapêutico."""
        print(f"Avaliando gene de proteína como alvo: {gene.nome}")
        
        score = self._calcular_score_druggability(gene)
        potencial = self._avaliar_potencial_terapeutico(gene, score)
        
        resultado = {
            "gene": gene.nome,
            "proteina": gene.proteina_codificada,
            "tipo": "gene_proteina",
            "score_druggability": score,
            "potencial_terapeutico": potencial,
            "recomendacao": self._gerar_recomendacao(potencial, score),
            "timestamp": time.time()
        }
        
        if potencial["viavel"]:
            self.alvos_terapeuticos.append(resultado)
        
        return resultado
    
    def visitar_gene_regulador(self, gene: GeneRegulador) -> Dict[str, Any]:
        """Avalia gene regulador como alvo terapêutico."""
        print(f"Avaliando gene regulador como alvo: {gene.nome}")
        
        score = self._calcular_score_regulador(gene)
        potencial = self._avaliar_potencial_regulador(gene, score)
        
        resultado = {
            "gene": gene.nome,
            "tipo": "gene_regulador",
            "tipo_regulacao": gene.tipo_regulacao,
            "score_regulador": score,
            "potencial_terapeutico": potencial,
            "recomendacao": self._gerar_recomendacao_regulador(potencial, score),
            "timestamp": time.time()
        }
        
        if potencial["viavel"]:
            self.alvos_terapeuticos.append(resultado)
        
        return resultado
    
    def visitar_gene_estrutural(self, gene: GeneEstrutural) -> Dict[str, Any]:
        """Avalia gene estrutural como alvo terapêutico."""
        print(f"Avaliando gene estrutural como alvo: {gene.nome}")
        
        score = self._calcular_score_estrutural(gene)
        potencial = self._avaliar_potencial_estrutural(gene, score)
        
        resultado = {
            "gene": gene.nome,
            "tipo": "gene_estrutural",
            "funcao_celular": gene.funcao_celular,
            "score_estrutural": score,
            "potencial_terapeutico": potencial,
            "recomendacao": self._gerar_recomendacao_estrutural(potencial, score),
            "timestamp": time.time()
        }
        
        if potencial["viavel"]:
            self.alvos_terapeuticos.append(resultado)
        
        return resultado
    
    def visitar_gene_housekeeping(self, gene: GeneHousekeeping) -> Dict[str, Any]:
        """Avalia gene housekeeping como alvo terapêutico."""
        print(f"Avaliando gene housekeeping como alvo: {gene.nome}")
        
        score = self._calcular_score_housekeeping(gene)
        potencial = self._avaliar_potencial_housekeeping(gene, score)
        
        resultado = {
            "gene": gene.nome,
            "tipo": "gene_housekeeping",
            "via_metabolica": gene.via_metabolica,
            "score_housekeeping": score,
            "potencial_terapeutico": potencial,
            "recomendacao": self._gerar_recomendacao_housekeeping(potencial, score),
            "timestamp": time.time()
        }
        
        # Housekeeping genes raramente são bons alvos
        if potencial["viavel"] and score > 0.8:
            self.alvos_terapeuticos.append(resultado)
        
        return resultado
    
    def _calcular_score_druggability(self, gene: GeneProteina) -> float:
        """Calcula score de druggability para gene de proteína."""
        score = 0.0
        
        # Peso molecular adequado
        if 10000 < gene.peso_molecular < 100000:
            score += 0.3
        
        # Domínios funcionais
        if len(gene.dominios_proteicos) > 0:
            score += 0.2
        
        # Expressão moderada-alta
        if 1.0 < gene.expressao < 10.0:
            score += 0.2
        
        # Comprimento da sequência
        if 500 < len(gene.sequencia) < 5000:
            score += 0.2
        
        # Presença de domínios "druggable"
        if any("kinase" in d.lower() or "receptor" in d.lower() for d in gene.dominios_proteicos):
            score += 0.1
        
        return min(score, 1.0)
    
    def _avaliar_potencial_terapeutico(self, gene: GeneProteina, score: float) -> Dict[str, Any]:
        """Avalia potencial terapêutico de gene de proteína."""
        return {
            "viavel": score > self.criterios_avaliacao["druggability"],
            "score": score,
            "categoria": "alto" if score > 0.7 else "medio" if score > 0.4 else "baixo",
            "consideracoes": [
                "Proteína alvo viável" if score > 0.7 else "Proteína com desafios",
                "Múltiplos domínios funcionais" if len(gene.dominios_proteicos) > 2 else "Poucos domínios"
            ]
        }
    
    def _calcular_score_regulador(self, gene: GeneRegulador) -> float:
        """Calcula score para gene regulador."""
        score = 0.0
        
        # Força de regulação
        if abs(gene.forca_regulacao) > 0.7:
            score += 0.3
        
        # Múltiplos alvos
        if len(gene.alvos_regulacao) > 3:
            score += 0.2
        
        # Múltiplos sítios de ligação
        if len(gene.sites_ligacao) > 2:
            score += 0.2
        
        # Expressão moderada
        if 0.5 < gene.expressao < 5.0:
            score += 0.2
        
        # Tipo de regulação
        if gene.tipo_regulacao == "ativador":
            score += 0.1
        
        return min(score, 1.0)
    
    def _avaliar_potencial_regulador(self, gene: GeneRegulador, score: float) -> Dict[str, Any]:
        """Avalia potencial terapêutico de regulador."""
        return {
            "viavel": score > 0.6,
            "score": score,
            "categoria": "alto" if score > 0.7 else "medio" if score > 0.4 else "baixo",
            "consideracoes": [
                f"Regulador {gene.tipo_regulacao} forte" if abs(gene.forca_regulacao) > 0.7 else "Regulador moderado",
                f"Controla {len(gene.alvos_regulacao)} genes alvo"
            ]
        }
    
    def _calcular_score_estrutural(self, gene: GeneEstrutural) -> float:
        """Calcula score para gene estrutural."""
        score = 0.0
        
        # Essencialidade
        if gene.essencialidade:
            score += 0.4
        
        # Múltiplas interações
        if len(gene.interacoes_proteicas) > 5:
            score += 0.2
        
        # Expressão adequada
        if 0.1 < gene.expressao < 5.0:
            score += 0.2
        
        # Função relevante
        if any(palavra in gene.funcao_celular.lower() for palavra in ["metabolismo", "sinalizacao", "transcricao"]):
            score += 0.2
        
        return min(score, 1.0)
    
    def _avaliar_potencial_estrutural(self, gene: GeneEstrutural, score: float) -> Dict[str, Any]:
        """Avalia potencial terapêutico de estrutural."""
        return {
            "viavel": score > 0.5,
            "score": score,
            "categoria": "alto" if score > 0.7 else "medio" if score > 0.4 else "baixo",
            "consideracoes": [
                "Gene essencial" if gene.essencialidade else "Gene não essencial",
                f"Função: {gene.funcao_celular}",
                f"Intage com {len(gene.interacoes_proteicas)} proteínas"
            ]
        }
    
    def _calcular_score_housekeeping(self, gene: GeneHousekeeping) -> float:
        """Calcula score para gene housekeeping."""
        score = 0.0
        
        # Estabilidade
        if gene.estabilidade_mrna > 0.7:
            score += 0.2
        
        # Via metabólica essencial
        if gene.via_metabolica.lower() in ["glicolise", "tca", "sintese_proteica"]:
            score += 0.3
        
        # Nível basal consistente
        if 0.8 < gene.nivel_basal < 1.2:
            score += 0.2
        
        # Múltiplas condições
        if len(gene.condicoes_experimento) > 3:
            score += 0.1
        
        # Housekeeping genes geralmente não são bons alvos
        score -= 0.3
        
        return max(0.0, min(score, 1.0))
    
    def _avaliar_potencial_housekeeping(self, gene: GeneHousekeeping, score: float) -> Dict[str, Any]:
        """Avalia potencial terapêutico de housekeeping."""
        return {
            "viavel": score > 0.8,  # Critério mais alto para housekeeping
            "score": score,
            "categoria": "alto" if score > 0.7 else "medio" if score > 0.4 else "baixo",
            "consideracoes": [
                "Gene housekeeping - geralmente não alvo terapêutico",
                f"Via: {gene.via_metabolica}",
                "Alto risco de toxicidade" if score < 0.5 else "Risco moderado"
            ]
        }
    
    def _gerar_recomendacao(self, potencial: Dict[str, Any], score: float) -> str:
        """Gera recomendação para gene de proteína."""
        if potencial["viavel"]:
            return f"Excelente alvo terapêutico (score: {score:.2f}). Priorizar para desenvolvimento."
        elif score > 0.5:
            return f"Alvo promissor (score: {score:.2f}). Requer investigação adicional."
        else:
            return f"Alvo desafiador (score: {score:.2f}). Considerar abordagens alternativas."
    
    def _gerar_recomendacao_regulador(self, potencial: Dict[str, Any], score: float) -> str:
        """Gera recomendação para regulador."""
        if potencial["viavel"]:
            return f"Bom alvo regulatório (score: {score:.2f}). Modular via pequenas moléculas."
        elif score > 0.5:
            return f"Alvo regulatório moderado (score: {score:.2f}). Requer otimização."
        else:
            return f"Alvo regulatório difícil (score: {score:.2f}). Considerar outras abordagens."
    
    def _gerar_recomendacao_estrutural(self, potencial: Dict[str, Any], score: float) -> str:
        """Gera recomendação para estrutural."""
        if potencial["viavel"]:
            return f"Alvo estrutural viável (score: {score:.2f}). Focar em inibição/modulação."
        elif score > 0.5:
            return f"Alvo estrutural possível (score: {score:.2f}). Avaliar viabilidade."
        else:
            return f"Alvo estrutural limitado (score: {score:.2f}). Explorar alternativas."
    
    def _gerar_recomendacao_housekeeping(self, potencial: Dict[str, Any], score: float) -> str:
        """Gera recomendação para housekeeping."""
        if potencial["viavel"]:
            return f"Alvo housekeeping excepcional (score: {score:.2f}). Alto risco, avaliar cuidadosamente."
        else:
            return f"Alvo housekeeping não recomendado (score: {score:.2f}). Toxicidade provável."
    
    def obter_alvos_terapeuticos(self) -> List[Dict[str, Any]]:
        """Retorna lista de alvos terapêuticos identificados."""
        return sorted(self.alvos_terapeuticos, key=lambda x: x.get("score", 0), reverse=True)
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas da análise terapêutica."""
        if not self.alvos_terapeuticos:
            return {"total_alvos": 0}
        
        total = len(self.alvos_terapeuticos)
        por_tipo = {}
        scores = []
        
        for alvo in self.alvos_terapeuticos:
            tipo = alvo["tipo"]
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
            scores.append(alvo.get("score", 0))
        
        return {
            "total_alvos": total,
            "por_tipo": por_tipo,
            "score_medio": sum(scores) / len(scores) if scores else 0,
            "score_maximo": max(scores) if scores else 0,
            "alvos_alta_prioridade": len([s for s in scores if s > 0.7])
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Análise Molecular com Visitor ===")
    
    # Criar diferentes tipos de genes
    gene_proteina = GeneProteina("BRCA1", "17", 43044295, "Proteína supressora de tumor BRCA1")
    gene_proteina.definir_sequencia("ATCGATCGATCGATCGATCGATCGATCG")
    gene_proteina.definir_expressao(2.5)
    gene_proteina.adicionar_dominio("RING")
    gene_proteina.adicionar_dominio("BRCT")
    gene_proteina.definir_peso_molecular(220000.0)
    
    gene_regulador = GeneRegulador("TP53", "17", 7579472, "ativador")
    gene_regulador.definir_sequencia("GCTAGCTAGCTAGCTAGCTAG")
    gene_regulador.definir_expressao(3.2)
    gene_regulador.adicionar_alvo("MDM2")
    gene_regulador.adicionar_alvo("CDKN1A")
    gene_regulador.adicionar_site_ligacao("p53_response_element")
    gene_regulador.definir_forca_regulacao(0.85)
    
    gene_estrutural = GeneEstrutural("ACTB", "7", 5524907, "Manutenção do citoesqueleto")
    gene_estrutural.definir_sequencia("TTTTAAAATTTTAAAATTTT")
    gene_estrutural.definir_expressao(8.7)
    gene_estrutural.definir_compartimento("citoplasma")
    gene_estrutural.adicionar_interacao("Proteína X")
    gene_estrutural.adicionar_interacao("Proteína Y")
    gene_estrutural.definir_essencialidade(True)
    
    gene_housekeeping = GeneHousekeeping("GAPDH", "12", 6656342, "Glicólise")
    gene_housekeeping.definir_sequencia("CCGGCCGGCCGGCCGGCCGG")
    gene_housekeeping.definir_expressao(5.5)
    gene_housekeeping.definir_nivel_basal(1.0)
    gene_housekeeping.adicionar_condicao("controle")
    gene_housekeeping.adicionar_condicao("tratamento")
    gene_housekeeping.definir_estabilidade_mrna(0.85)
    
    # Criar visitante e analisar genes
    analisador = AnalisadorMolecular()
    genes = [gene_proteina, gene_regulador, gene_estrutural, gene_housekeeping]
    
    print("Iniciando análise molecular...")
    resultados = []
    
    for gene in genes:
        resultado = gene.aceitar(analisador)
        resultados.append(resultado)
        print()
    
    # Exibir resultados
    print("=== Resultados da Análise Molecular ===")
    for resultado in resultados:
        print(f"\nGene: {resultado['gene']} ({resultado['tipo']})")
        print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime(resultado['timestamp']))}")
        
        # Exibir informações específicas por tipo
        if resultado['tipo'] == 'gene_proteina':
            composicao = resultado['composicao_sequencia']
            print(f"  GC Content: {composicao['gc_content']:.1f}%")
            print(f"  Peso Molecular: {resultado['propriedades_proteina']['peso_molecular']:.0f} Da")
            print(f"  Domínios: {resultado['analise_dominios']['total_dominios']}")
        
        elif resultado['tipo'] == 'gene_regulador':
            print(f"  Tipo de Regulação: {resultado['tipo_regulacao']}")
            print(f"  Força Regulatória: {resultado['analise_forca']['forca_regulatoria']:.2f}")
            print(f"  Total de Alvos: {resultado['analise_alvos']['total_alvos']}")
        
        elif resultado['tipo'] == 'gene_estrutural':
            print(f"  Função Celular: {resultado['funcao_celular']}")
            print(f"  Essencial: {resultado['analise_essencialidade']['essencial']}")
            print(f"  Interações: {resultado['analise_interacoes']['total_interacoes']}")
        
        elif resultado['tipo'] == 'gene_housekeeping':
            print(f"  Via Metabólica: {resultado['via_metabolica']}")
            print(f"  Estabilidade mRNA: {resultado['analise_estabilidade']['meia_vida']}")
            print(f"  Nível Basal: {resultado['nivel_basal']:.2f}")
    
    # Estatísticas da análise
    stats = analisador.obter_estatisticas()
    print(f"\n=== Estatísticas da Análise ===")
    print(f"Total de genes analisados: {stats['genes_analisados']}")
    print(f"Tempo total de análise: {stats['tempo_total']:.3f} segundos")
    print(f"Tipos analisados: {stats['tipos_analisados']}")
    
    print("\n=== Exemplo 2: Otimização Terapêutica com Visitor ===")
    
    # Criar visitante terapêutico
    otimizador = OtimizadorTerapeutico()
    
    print("Avaliando potencial terapêutico dos genes...")
    resultados_terapeuticos = []
    
    for gene in genes:
        resultado = gene.aceitar(otimizador)
        resultados_terapeuticos.append(resultado)
        print()
    
    # Exibir recomendações
    print("=== Recomendações Terapêuticas ===")
    for resultado in resultados_terapeuticos:
        print(f"\n{resultado['gene']} ({resultado['tipo']}):")
        print(f"  Recomendação: {resultado['recomendacao']}")
        print(f"  Score: {resultado.get('score', 0):.2f}")
        print(f"  Potencial: {resultado['potencial_terapeutico']['categoria']}")
    
    # Alvos terapêuticos identificados
    alvos = otimizador.obter_alvos_terapeuticos()
    print(f"\n=== Alvos Terapêuticos Identificados ({len(alvos)}) ===")
    
    for i, alvo in enumerate(alvos, 1):
        print(f"\n{i}. {alvo['gene']} ({alvo['tipo']})")
        print(f"   Score: {alvo['score']:.2f}")
        print(f"   Recomendação: {alvo['recomendacao']}")
    
    # Estatísticas terapêuticas
    stats_terapeuticas = otimizador.obter_estatisticas()
    print(f"\n=== Estatísticas Terapêuticas ===")
    print(f"Total de alvos: {stats_terapeuticas['total_alvos']}")
    
    if stats_terapeuticas['total_alvos'] > 0:
        print(f"Score médio: {stats_terapeuticas['score_medio']:.2f}")
        print(f"Score máximo: {stats_terapeuticas['score_maximo']:.2f}")
        print(f"Alvos de alta prioridade: {stats_terapeuticas['alvos_alta_prioridade']}")
        print(f"Por tipo: {stats_terapeuticas['por_tipo']}")
    else:
        print("Nenhum alvo terapêutico identificado nesta análise.")
    
    print("\n=== Exemplo 3: Múltiplos Visitantes Simultâneos ===")
    
    # Criar coleção de genes para análise em lote
    mais_genes = [
        GeneProteina("EGFR", "7", 55019017, "Receptor de fator de crescimento epitelial"),
        GeneRegulador("MYC", "8", 128748315, "ativador"),
        GeneEstrutural("TUBA1B", "12", 40433779, "Componente do microtúbulo")
    ]
    
    # Configurar genes adicionais
    mais_genes[0].definir_sequencia("ATCGATCGATCG")
    mais_genes[0].definir_expressao(4.2)
    mais_genes[0].definir_peso_molecular(170000.0)
    
    mais_genes[1].definir_sequencia("GCTAGCTAGCTA")
    mais_genes[1].definir_expressao(6.8)
    mais_genes[1].definir_forca_regulacao(0.9)
    
    mais_genes[2].definir_sequencia("TTTTAAAATTTT")
    mais_genes[2].definir_expressao(3.1)
    mais_genes[2].definir_essencialidade(True)
    
    # Analisar com ambos os visitantes
    todos_genes = genes + mais_genes
    
    print(f"Analisando {len(todos_genes)} genes com múltiplos visitantes...")
    
    # Análise molecular
    print("\n--- Análise Molecular ---")
    analisador_lote = AnalisadorMolecular()
    for gene in todos_genes:
        gene.aceitar(analisador_lote)
    
    # Otimização terapêutica
    print("\n--- Otimização Terapêutica ---")
    otimizador_lote = OtimizadorTerapeutico()
    for gene in todos_genes:
        gene.aceitar(otimizador_lote)
    
    # Resultados finais
    stats_lote = analisador_lote.obter_estatisticas()
    alvos_lote = otimizador_lote.obter_alvos_terapeuticos()
    stats_terapeuticas_lote = otimizador_lote.obter_estatisticas()
    
    print(f"\n=== Resumo Final ===")
    print(f"Genes analisados: {stats_lote['genes_analisados']}")
    print(f"Alvos terapêuticos identificados: {len(alvos_lote)}")
    print(f"Tempo total de análise: {stats_lote['tempo_total']:.3f}s")
    print(f"Score médio dos alvos: {stats_terapeuticas_lote['score_medio']:.2f}")
    
    print("\nTop 5 alvos terapêuticos:")
    if alvos_lote:
        for i, alvo in enumerate(alvos_lote[:5], 1):
            score = alvo.get('score', 0)
            print(f"  {i}. {alvo['gene']} - Score: {score:.2f} ({alvo['tipo']})")
    else:
        print("  Nenhum alvo terapêutico identificado.")
    
    print("\nVisitor pattern implementado com sucesso!")
