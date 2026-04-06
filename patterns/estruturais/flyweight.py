from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import weakref


class DadoGeneticoFlyweight(ABC):
    """Interface base para flyweights de dados genéticos."""
    
    def __init__(self, codigo: str):
        self.codigo = codigo
        self._estado_compartilhado = self._criar_estado_compartilhado()
    
    @abstractmethod
    def _criar_estado_compartilhado(self) -> Dict[str, Any]:
        """Cria o estado intrínseco compartilhado."""
        pass
    
    @abstractmethod
    def exibir_dado(self, contexto_extrinseco: Dict[str, Any]) -> str:
        """Exibe o dado com contexto extrínseco."""
        pass
    
    def obter_info_compartilhada(self) -> Dict[str, Any]:
        """Retorna informações do estado compartilhado."""
        return self._estado_compartilhado.copy()


class SequenciaProteicaFlyweight(DadoGeneticoFlyweight):
    """Flyweight para sequências de aminoácidos compartilhadas."""
    
    def _criar_estado_compartilhado(self) -> Dict[str, Any]:
        """Cria estado compartilhado para sequência proteica."""
        return {
            "sequencia": "",
            "peso_molecular": 0.0,
            "ponto_isoeletrico": 0.0,
            "dominios": [],
            "funcao": ""
        }
    
    def definir_sequencia(self, sequencia: str) -> None:
        """Define a sequência de aminoácidos."""
        self._estado_compartilhado["sequencia"] = sequencia
        self._estado_compartilhado["peso_molecular"] = self._calcular_peso_molecular(sequencia)
        self._estado_compartilhado["ponto_isoeletrico"] = self._estimar_pi(sequencia)
    
    def adicionar_dominio(self, dominio: str) -> None:
        """Adiciona domínio funcional."""
        if dominio not in self._estado_compartilhado["dominios"]:
            self._estado_compartilhado["dominios"].append(dominio)
    
    def definir_funcao(self, funcao: str) -> None:
        """Define a função da proteína."""
        self._estado_compartilhado["funcao"] = funcao
    
    def exibir_dado(self, contexto_extrinseco: Dict[str, Any]) -> str:
        """Exibe a sequência proteica com contexto."""
        estado = self._estado_compartilhado
        return f"""Proteína {self.codigo}:
        Sequência: {estado['sequencia'][:30]}{'...' if len(estado['sequencia']) > 30 else ''}
        Peso Molecular: {estado['peso_molecular']:.2f} Da
        pI: {estado['ponto_isoeletrico']:.2f}
        Domínios: {', '.join(estado['dominios'])}
        Função: {estado['funcao']}
        Contexto: {contexto_extrinseco.get('amostra', 'N/A')} - {contexto_extrinseco.get('condicao', 'N/A')}"""
    
    def _calcular_peso_molecular(self, sequencia: str) -> float:
        """Calcula peso molecular da sequência."""
        pesos = {
            'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.15,
            'E': 147.13, 'Q': 146.15, 'G': 75.07, 'H': 155.16, 'I': 131.17,
            'L': 131.17, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
            'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
        }
        
        peso_total = 0.0
        for aa in sequencia.upper():
            peso_total += pesos.get(aa, 110.0)
        
        return peso_total
    
    def _estimar_pi(self, sequencia: str) -> float:
        """Estima ponto isoelétrico."""
        acidic = sequencia.upper().count('D') + sequencia.upper().count('E')
        basic = sequencia.upper().count('K') + sequencia.upper().count('R') + sequencia.upper().count('H')
        
        if basic > acidic:
            return 7.5 + (basic - acidic) * 0.3
        else:
            return 6.5 - (acidic - basic) * 0.2


class GeneFlyweight(DadoGeneticoFlyweight):
    """Flyweight para informações de genes compartilhadas."""
    
    def _criar_estado_compartilhado(self) -> Dict[str, Any]:
        """Cria estado compartilhado para gene."""
        return {
            "sequencia_dna": "",
            "sequencia_rna": "",
            "cromossomo": "",
            "posicao": 0,
            "exons": [],
            "introns": [],
            "promotores": [],
            "funcao": ""
        }
    
    def definir_sequencias(self, dna: str, rna: str = "") -> None:
        """Define as sequências de DNA e RNA."""
        self._estado_compartilhado["sequencia_dna"] = dna
        if rna:
            self._estado_compartilhado["sequencia_rna"] = rna
        else:
            # Transcreve automaticamente
            self._estado_compartilhado["sequencia_rna"] = dna.replace('T', 'U')
    
    def definir_localizacao(self, cromossomo: str, posicao: int) -> None:
        """Define localização cromossômica."""
        self._estado_compartilhado["cromossomo"] = cromossomo
        self._estado_compartilhado["posicao"] = posicao
    
    def adicionar_exon(self, exon: Dict[str, Any]) -> None:
        """Adiciona informação de exon."""
        self._estado_compartilhado["exons"].append(exon)
    
    def adicionar_promotor(self, promotor: str) -> None:
        """Adiciona sequência promotora."""
        self._estado_compartilhado["promotores"].append(promotor)
    
    def definir_funcao(self, funcao: str) -> None:
        """Define função do gene."""
        self._estado_compartilhado["funcao"] = funcao
    
    def exibir_dado(self, contexto_extrinseco: Dict[str, Any]) -> str:
        """Exibe informações do gene com contexto."""
        estado = self._estado_compartilhado
        return f"""Gene {self.codigo}:
        Localização: {estado['cromossomo']}:{estado['posicao']}
        Tamanho DNA: {len(estado['sequencia_dna'])} bp
        Exons: {len(estado['exons'])}
        Promotores: {len(estado['promotores'])}
        Função: {estado['funcao']}
        Contexto: {contexto_extrinseco.get('paciente', 'N/A')} - {contexto_extrinseco.get('tecido', 'N/A')}"""
    
    def transcrever(self) -> str:
        """Retorna sequência de RNA transcrita."""
        return self._estado_compartilhado["sequencia_rna"]
    
    def traduzir(self) -> str:
        """Traduz para proteína (simplificado)."""
        rna = self._estado_compartilhado["sequencia_rna"]
        
        # Tabela de códons simplificada
        codons = {
            'AUG': 'M', 'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
            'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
            'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
            'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W'
        }
        
        proteina = ""
        for i in range(0, len(rna) - 2, 3):
            codon = rna[i:i+3]
            aa = codons.get(codon, 'X')
            if aa == '*':
                break
            proteina += aa
        
        return proteina


class ViaMetabolicaFlyweight(DadoGeneticoFlyweight):
    """Flyweight para vias metabólicas compartilhadas."""
    
    def _criar_estado_compartilhado(self) -> Dict[str, Any]:
        """Cria estado compartilhado para via metabólica."""
        return {
            "enzimas": [],
            "substratos": [],
            "produtos": [],
            "reguladores": [],
            "localizacao_celular": "",
            "descricao": ""
        }
    
    def adicionar_enzima(self, enzima: str) -> None:
        """Adiciona enzima à via."""
        if enzima not in self._estado_compartilhado["enzimas"]:
            self._estado_compartilhado["enzimas"].append(enzima)
    
    def adicionar_substrato(self, substrato: str) -> None:
        """Adiciona substrato à via."""
        if substrato not in self._estado_compartilhado["substratos"]:
            self._estado_compartilhado["substratos"].append(substrato)
    
    def adicionar_produto(self, produto: str) -> None:
        """Adiciona produto à via."""
        if produto not in self._estado_compartilhado["produtos"]:
            self._estado_compartilhado["produtos"].append(produto)
    
    def definir_localizacao(self, localizacao: str) -> None:
        """Define localização celular."""
        self._estado_compartilhado["localizacao_celular"] = localizacao
    
    def definir_descricao(self, descricao: str) -> None:
        """Define descrição da via."""
        self._estado_compartilhado["descricao"] = descricao
    
    def exibir_dado(self, contexto_extrinseco: Dict[str, Any]) -> str:
        """Exibe informações da via metabólica com contexto."""
        estado = self._estado_compartilhado
        return f"""Via Metabólica {self.codigo}:
        Localização: {estado['localizacao_celular']}
        Enzimas: {', '.join(estado['enzimas'][:3])}{'...' if len(estado['enzimas']) > 3 else ''}
        Substratos: {', '.join(estado['substratos'][:3])}{'...' if len(estado['substratos']) > 3 else ''}
        Produtos: {', '.join(estado['produtos'][:3])}{'...' if len(estado['produtos']) > 3 else ''}
        Descrição: {estado['descricao'][:100]}{'...' if len(estado['descricao']) > 100 else ''}
        Contexto: {contexto_extrinseco.get('condicao_experimental', 'N/A')}"""


class DadoGeneticoFlyweightFactory:
    """Factory para gerenciar flyweights de dados genéticos."""
    
    _flyweights: Dict[str, DadoGeneticoFlyweight] = {}
    _stats = {
        "total_criados": 0,
        "reusos": 0,
        "memoria_economizada": 0
    }
    
    @classmethod
    def obter_flyweight(cls, tipo: str, codigo: str) -> DadoGeneticoFlyweight:
        """Obtém flyweight existente ou cria novo."""
        chave = f"{tipo}:{codigo}"
        
        if chave not in cls._flyweights:
            if tipo == "proteina":
                flyweight = SequenciaProteicaFlyweight(codigo)
            elif tipo == "gene":
                flyweight = GeneFlyweight(codigo)
            elif tipo == "via_metabolica":
                flyweight = ViaMetabolicaFlyweight(codigo)
            else:
                raise ValueError(f"Tipo de flyweight não suportado: {tipo}")
            
            cls._flyweights[chave] = flyweight
            cls._stats["total_criados"] += 1
        else:
            cls._stats["reusos"] += 1
        
        return cls._flyweights[chave]
    
    @classmethod
    def obter_stats(cls) -> Dict[str, Any]:
        """Retorna estatísticas de uso."""
        total_acessos = cls._stats["total_criados"] + cls._stats["reusos"]
        taxa_reuso = (cls._stats["reusos"] / total_acessos * 100) if total_acessos > 0 else 0
        
        return {
            **cls._stats,
            "total_acessos": total_acessos,
            "taxa_reuso": taxa_reuso,
            "flywords_ativos": len(cls._flyweights)
        }
    
    @classmethod
    def limpar_cache(cls) -> None:
        """Limpa todos os flyweights."""
        cls._flyweights.clear()
        cls._stats = {
            "total_criados": 0,
            "reusos": 0,
            "memoria_economizada": 0
        }
    
    @classmethod
    def listar_flyweights(cls) -> List[str]:
        """Lista todos os flyweights ativos."""
        return list(cls._flyweights.keys())


class ContextoAnalise:
    """Contexto extrínseco para flyweights."""
    
    def __init__(self, amostra: str, paciente: str = "", tecido: str = "", 
                 condicao: str = "", experimento: str = ""):
        self.amostra = amostra
        self.paciente = paciente
        self.tecido = tecido
        self.condicao = condicao
        self.experimento = experimento
        self.timestamp = self._obter_timestamp()
    
    def _obter_timestamp(self) -> str:
        """Obtém timestamp atual."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def para_dict(self) -> Dict[str, str]:
        """Converte contexto para dicionário."""
        return {
            "amostra": self.amostra,
            "paciente": self.paciente,
            "tecido": self.tecido,
            "condicao": self.condicao,
            "experimento": self.experimento,
            "timestamp": self.timestamp
        }


class AnaliseGenomicaComFlyweight:
    """Sistema de análise genômica usando flyweights."""
    
    def __init__(self):
        self.analises_realizadas = []
    
    def analisar_proteina(self, codigo_proteina: str, sequencia: str, 
                         contexto: ContextoAnalise) -> Dict[str, Any]:
        """Analisa proteína usando flyweight."""
        # Obtém flyweight da proteína
        proteina_fw = DadoGeneticoFlyweightFactory.obter_flyweight("proteina", codigo_proteina)
        
        # Configura estado compartilhado (só na primeira vez)
        if not proteina_fw.obter_info_compartilhada()["sequencia"]:
            proteina_fw.definir_sequencia(sequencia)
            proteina_fw.adicionar_dominio("Dominio_1")
            proteina_fw.adicionar_dominio("Dominio_2")
            proteina_fw.definir_funcao("Função proteica")
        
        # Exibe com contexto específico
        resultado = proteina_fw.exibir_dado(contexto.para_dict())
        
        # Registra análise
        self.analises_realizadas.append({
            "tipo": "proteina",
            "codigo": codigo_proteina,
            "contexto": contexto.para_dict(),
            "resultado": resultado
        })
        
        return {
            "proteina": codigo_proteina,
            "contexto": contexto.para_dict(),
            "resultado": resultado
        }
    
    def analisar_gene(self, codigo_gene: str, sequencia_dna: str, 
                     cromossomo: str, posicao: int, contexto: ContextoAnalise) -> Dict[str, Any]:
        """Analisa gene usando flyweight."""
        # Obtém flyweight do gene
        gene_fw = DadoGeneticoFlyweightFactory.obter_flyweight("gene", codigo_gene)
        
        # Configura estado compartilhado
        if not gene_fw.obter_info_compartilhada()["sequencia_dna"]:
            gene_fw.definir_sequencias(sequencia_dna)
            gene_fw.definir_localizacao(cromossomo, posicao)
            gene_fw.adicionar_exon({"inicio": 100, "fim": 500})
            gene_fw.adicionar_exon({"inicio": 800, "fim": 1200})
            gene_fw.adicionar_promotor("TATA_box")
            gene_fw.definir_funcao("Regulação transcricional")
        
        # Exibe com contexto específico
        resultado = gene_fw.exibir_dado(contexto.para_dict())
        
        # Registra análise
        self.analises_realizadas.append({
            "tipo": "gene",
            "codigo": codigo_gene,
            "contexto": contexto.para_dict(),
            "resultado": resultado
        })
        
        return {
            "gene": codigo_gene,
            "contexto": contexto.para_dict(),
            "resultado": resultado
        }
    
    def analisar_via_metabolica(self, codigo_via: str, enzimas: List[str], 
                              substratos: List[str], contexto: ContextoAnalise) -> Dict[str, Any]:
        """Analisa via metabólica usando flyweight."""
        # Obtém flyweight da via
        via_fw = DadoGeneticoFlyweightFactory.obter_flyweight("via_metabolica", codigo_via)
        
        # Configura estado compartilhado
        if not via_fw.obter_info_compartilhada()["enzimas"]:
            for enzima in enzimas:
                via_fw.adicionar_enzima(enzima)
            for substrato in substratos:
                via_fw.adicionar_substrato(substrato)
            via_fw.adicionar_produto("Produto_Final")
            via_fw.definir_localizacao("Citoplasma")
            via_fw.definir_descricao("Via metabólica importante para metabolismo celular")
        
        # Exibe com contexto específico
        resultado = via_fw.exibir_dado(contexto.para_dict())
        
        # Registra análise
        self.analises_realizadas.append({
            "tipo": "via_metabolica",
            "codigo": codigo_via,
            "contexto": contexto.para_dict(),
            "resultado": resultado
        })
        
        return {
            "via": codigo_via,
            "contexto": contexto.para_dict(),
            "resultado": resultado
        }
    
    def obter_estatisticas_flyweight(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso dos flyweights."""
        return DadoGeneticoFlyweightFactory.obter_stats()
    
    def obter_resumo_analises(self) -> Dict[str, Any]:
        """Retorna resumo das análises realizadas."""
        total_analises = len(self.analises_realizadas)
        tipos_analise = {}
        
        for analise in self.analises_realizadas:
            tipo = analise["tipo"]
            tipos_analise[tipo] = tipos_analise.get(tipo, 0) + 1
        
        return {
            "total_analises": total_analises,
            "tipos_analise": tipos_analise,
            "contexts_unicos": len(set(a["contexto"]["amostra"] for a in self.analises_realizadas))
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Análise de Proteínas com Flyweight ===")
    
    analise = AnaliseGenomicaComFlyweight()
    
    # Criar contextos diferentes para mesma proteína
    contexto1 = ContextoAnalise("Amostra_001", "Paciente_A", "Sangue", "Doença", "Exp_001")
    contexto2 = ContextoAnalise("Amostra_002", "Paciente_B", "Tecido", "Normal", "Exp_001")
    contexto3 = ContextoAnalise("Amostra_003", "Paciente_C", "Sangue", "Doença", "Exp_002")
    
    # Analisar mesma proteína em contextos diferentes
    resultado1 = analise.analisar_proteina("HBB", "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK", contexto1)
    resultado2 = analise.analisar_proteina("HBB", "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK", contexto2)
    resultado3 = analise.analisar_proteina("HBB", "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK", contexto3)
    
    print("Análise 1 (Paciente A - Sangue - Doença):")
    print(resultado1["resultado"])
    
    print("\nAnálise 2 (Paciente B - Tecido - Normal):")
    print(resultado2["resultado"])
    
    print("\n=== Exemplo 2: Análise de Genes com Flyweight ===")
    
    # Analisar genes
    contexto_gene1 = ContextoAnalise("DNA_001", "Paciente_X", "Célula", "Câncer", "Gen_001")
    contexto_gene2 = ContextoAnalise("DNA_002", "Paciente_Y", "Célula", "Normal", "Gen_001")
    
    resultado_gene1 = analise.analisar_gene("BRCA1", "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCA", "17", 43044295, contexto_gene1)
    resultado_gene2 = analise.analisar_gene("BRCA1", "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCA", "17", 43044295, contexto_gene2)
    
    print("Análise Gene BRCA1 (Paciente X - Câncer):")
    print(resultado_gene1["resultado"])
    
    print("\n=== Exemplo 3: Análise de Vias Metabólicas ===")
    
    contexto_via = ContextoAnalise("Metab_001", "Paciente_Z", "Fígado", "Metabólico", "Met_001")
    
    resultado_via = analise.analisar_via_metabolica(
        "Glicolise",
        ["Hexoquinase", "Fosfofrutoquinase", "Piruvato quinase"],
        ["Glicose", "ATP"],
        contexto_via
    )
    
    print("Análise Via Glicolise:")
    print(resultado_via["resultado"])
    
    print("\n=== Exemplo 4: Estatísticas de Uso do Flyweight ===")
    
    stats_flyweight = analise.obter_estatisticas_flyweight()
    print("Estatísticas do Flyweight:")
    for chave, valor in stats_flyweight.items():
        print(f"  {chave}: {valor}")
    
    resumo_analises = analise.obter_resumo_analises()
    print("\nResumo das Análises:")
    for chave, valor in resumo_analises.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 5: Demonstração de Reuso ===")
    
    # Criar muitas análises reutilizando os mesmos flyweights
    print("Criando 100 análises reutilizando flyweights...")
    
    for i in range(100):
        contexto_massa = ContextoAnalise(f"Amostra_{i:03d}", f"Paciente_{i%10}", "Sangue", "Variado", f"Exp_{i%5}")
        
        if i % 3 == 0:
            analise.analisar_proteina("HBB", "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK", contexto_massa)
        elif i % 3 == 1:
            analise.analisar_gene("BRCA1", "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCA", "17", 43044295, contexto_massa)
        else:
            analise.analisar_via_metabolica("Glicolise", ["Hexoquinase"], ["Glicose"], contexto_massa)
    
    stats_finais = analise.obter_estatisticas_flyweight()
    print("\nEstatísticas Finais:")
    for chave, valor in stats_finais.items():
        if isinstance(valor, float):
            print(f"  {chave}: {valor:.2f}")
        else:
            print(f"  {chave}: {valor}")
    
    print(f"\nFlyweights ativos: {DadoGeneticoFlyweightFactory.listar_flyweights()}")
    
    print("\nFlyweight pattern implementado com sucesso!")
