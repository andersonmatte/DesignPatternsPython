from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from enum import Enum


class TipoAnalise(Enum):
    GENOMICA = "genomica"
    PROTEOMICA = "proteomica"
    TRANSCRIPTOMICA = "transcriptomica"
    METABOLOMICA = "metabolomica"


class ResultadoPipeline:
    """Representa o resultado de um pipeline de análise."""
    
    def __init__(self, tipo_analise: TipoAnalise):
        self.tipo_analise = tipo_analise
        self.etapas_concluidas: List[str] = []
        self.resultados_etapas: Dict[str, Any] = {}
        self.erros: List[str] = []
        self.tempo_total: float = 0.0
        self.status = "iniciado"
    
    def adicionar_resultado_etapa(self, etapa: str, resultado: Any) -> None:
        """Adiciona resultado de uma etapa."""
        self.etapas_concluidas.append(etapa)
        self.resultados_etapas[etapa] = resultado
    
    def adicionar_erro(self, erro: str) -> None:
        """Adiciona erro ao pipeline."""
        self.erros.append(erro)
        self.status = "erro"
    
    def finalizar_com_sucesso(self) -> None:
        """Finaliza pipeline com sucesso."""
        self.status = "concluido"
    
    def obter_resumo(self) -> Dict[str, Any]:
        """Retorna resumo do pipeline."""
        return {
            "tipo_analise": self.tipo_analise.value,
            "status": self.status,
            "etapas_concluidas": len(self.etapas_concluidas),
            "erros": len(self.erros),
            "tempo_total": self.tempo_total,
            "resultado_final": self.resultados_etapas.get("resultado_final")
        }


class PipelineAnaliseBiologica(ABC):
    """Classe abstrata base para pipelines de análise biológica."""
    
    def __init__(self, nome: str, tipo_analise: TipoAnalise):
        self.nome = nome
        self.tipo_analise = tipo_analise
        self.resultado = ResultadoPipeline(tipo_analise)
        self.parametros: Dict[str, Any] = {}
    
    def executar_analise_completa(self, dados_entrada: Any, 
                                   parametros: Dict[str, Any] = None) -> ResultadoPipeline:
        """Método template que define o esqueleto do algoritmo."""
        inicio = time.time()
        
        try:
            print(f"\n=== Iniciando Pipeline: {self.nome} ===")
            print(f"Tipo de Análise: {self.tipo_analise.value}")
            
            # Definir parâmetros
            self.parametros = parametros or {}
            self.configurar_parametros_especificos()
            
            # Etapa 1: Preparação
            print("\n1. Preparando dados...")
            dados_preparados = self.preparar_dados(dados_entrada)
            self.resultado.adicionar_resultado_etapa("preparacao", dados_preparados)
            
            # Etapa 2: Extração
            print("\n2. Extraindo dados biológicos...")
            dados_extraidos = self.extrair_dados_biologicos(dados_preparados)
            self.resultado.adicionar_resultado_etapa("extracao", dados_extraidos)
            
            # Etapa 3: Processamento
            print("\n3. Processando dados...")
            dados_processados = self.processar_dados(dados_extraidos)
            self.resultado.adicionar_resultado_etapa("processamento", dados_processados)
            
            # Etapa 4: Análise Específica (implementada por subclasses)
            print("\n4. Executando análise específica...")
            resultado_especifico = self.realizar_analise_especifica(dados_processados)
            self.resultado.adicionar_resultado_etapa("analise_especifica", resultado_especifico)
            
            # Etapa 5: Validação
            print("\n5. Validando resultados...")
            validacao = self.validar_resultados(resultado_especifico)
            self.resultado.adicionar_resultado_etapa("validacao", validacao)
            
            # Etapa 6: Geração de Relatório
            print("\n6. Gerando relatório final...")
            relatorio = self.gerar_relatorio_final(resultado_especifico)
            self.resultado.adicionar_resultado_etapa("relatorio", relatorio)
            
            # Etapa 7: Finalização
            print("\n7. Finalizando análise...")
            resultado_final = self.finalizar_analise(resultado_especifico, relatorio)
            self.resultado.adicionar_resultado_etapa("resultado_final", resultado_final)
            
            self.resultado.finalizar_com_sucesso()
            
            # Calcular tempo total
            self.resultado.tempo_total = time.time() - inicio
            
            print(f"\n=== Pipeline Concluído com Sucesso ===")
            print(f"Tempo total: {self.resultado.tempo_total:.2f} segundos")
            print(f"Etapas concluídas: {len(self.resultado.etapas_concluidas)}")
            
            return self.resultado
            
        except Exception as e:
            self.resultado.adicionar_erro(f"Erro no pipeline: {str(e)}")
            self.resultado.tempo_total = time.time() - inicio
            
            print(f"\n=== Pipeline Falhou ===")
            print(f"Erro: {str(e)}")
            print(f"Tempo executado: {self.resultado.tempo_total:.2f} segundos")
            
            return self.resultado
    
    # Métodos abstratos a serem implementados por subclasses
    @abstractmethod
    def configurar_parametros_especificos(self) -> None:
        """Configura parâmetros específicos do tipo de análise."""
        pass
    
    @abstractmethod
    def realizar_analise_especifica(self, dados_processados: Any) -> Any:
        """Realiza a análise específica do tipo biológico."""
        pass
    
    # Métodos com implementação padrão (podem ser sobrescritos)
    def preparar_dados(self, dados_entrada: Any) -> Dict[str, Any]:
        """Prepara dados para análise (implementação padrão)."""
        print("   - Validando formato dos dados")
        print("   - Limpando dados inválidos")
        print("   - Normalizando valores")
        
        time.sleep(0.3)  # Simula tempo de processamento
        
        return {
            "dados_originais": dados_entrada,
            "dados_limpos": f"dados_limpos_{len(str(dados_entrada))}",
            "metadados": {"tamanho": len(str(dados_entrada)), "formato": "padrao"}
        }
    
    def extrair_dados_biologicos(self, dados_preparados: Any) -> Dict[str, Any]:
        """Extrai dados biológicos (implementação padrão)."""
        print("   - Extraindo sequências")
        print("   - Identificando marcadores")
        print("   - Filtrando ruído")
        
        time.sleep(0.4)
        
        return {
            "sequencias_extras": ["SEQ001", "SEQ002", "SEQ003"],
            "marcadores": ["MARCA_A", "MARCA_B"],
            "qualidade": 0.95,
            "dados_filtrados": "dados_processados"
        }
    
    def processar_dados(self, dados_extraidos: Any) -> Dict[str, Any]:
        """Processa dados extraídos (implementação padrão)."""
        print("   - Aplicando algoritmos de processamento")
        print("   - Calculando estatísticas")
        print("   - Otimizando parâmetros")
        
        time.sleep(0.5)
        
        return {
            "dados_processados": "dados_finalizados",
            "estatisticas": {"media": 0.75, "desvio": 0.12},
            "parametros_otimizados": {"threshold": 0.8, "iteracoes": 100}
        }
    
    def validar_resultados(self, resultado_especifico: Any) -> Dict[str, Any]:
        """Valida resultados (implementação padrão)."""
        print("   - Verificando consistência")
        print("   - Validando estatisticamente")
        print("   - Comparando com referências")
        
        time.sleep(0.2)
        
        return {
            "validacao": "aprovado",
            "confianca": 0.92,
            "erros_encontrados": 0,
            "avisos": []
        }
    
    def gerar_relatorio_final(self, resultado_especifico: Any) -> Dict[str, Any]:
        """Gera relatório final (implementação padrão)."""
        print("   - Compilando resultados")
        print("   - Gerando visualizações")
        print("   - Criando documentação")
        
        time.sleep(0.3)
        
        return {
            "relatorio_id": f"REL_{int(time.time())}",
            "formato": "pdf",
            "paginas": 15,
            "resumo": f"Análise {self.tipo_analise.value} concluída com sucesso",
            "arquivo": f"relatorio_{self.tipo_analise.value}_{int(time.time())}.pdf"
        }
    
    def finalizar_analise(self, resultado_especifico: Any, relatorio: Dict[str, Any]) -> Dict[str, Any]:
        """Finaliza análise (implementação padrão)."""
        print("   - Salvando resultados")
        print("   - Arquivando dados")
        print("   - Notificando conclusão")
        
        time.sleep(0.2)
        
        return {
            "status": "concluido",
            "resultado_principal": resultado_especifico,
            "relatorio": relatorio,
            "timestamp": time.time(),
            "pipeline": self.nome
        }


class PipelineGenomica(PipelineAnaliseBiologica):
    """Pipeline especializado para análise genômica."""
    
    def __init__(self, nome: str = "Pipeline Genômica Padrão"):
        super().__init__(nome, TipoAnalise.GENOMICA)
        self.referencia_genoma = "hg38"
        self.algoritmo_alinhamento = "BWA-MEM"
    
    def configurar_parametros_especificos(self) -> None:
        """Configura parâmetros específicos da análise genômica."""
        print("   - Configurando parâmetros genômicos")
        self.referencia_genoma = self.parametros.get("referencia", "hg38")
        self.algoritmo_alinhamento = self.parametros.get("algoritmo", "BWA-MEM")
        print(f"   - Referência: {self.referencia_genoma}")
        print(f"   - Algoritmo: {self.algoritmo_alinhamento}")
    
    def realizar_analise_especifica(self, dados_processados: Any) -> Dict[str, Any]:
        """Realiza análise genômica específica."""
        print("   - Alinhando sequências ao genoma de referência")
        print("   - Detectando variantes genéticas")
        print("   - Anotando genes e regiões funcionais")
        
        time.sleep(0.8)
        
        return {
            "tipo": "genomica",
            "alinhamento": {
                "taxa_alinhamento": 98.5,
                "cobertura": 95.2,
                "qualidade_media": "Q30"
            },
            "variantes": {
                "snp_count": 4200,
                "indel_count": 300,
                "variantes_raras": 150,
                "variantes_patogenicas": 25
            },
            "anotacao": {
                "genes_afetados": 250,
                "regioes_regulatorias": 45,
                "elementos_funcionais": 180
            }
        }
    
    def extrair_dados_biologicos(self, dados_preparados: Any) -> Dict[str, Any]:
        """Extração específica para dados genômicos."""
        print("   - Extraindo sequências de DNA/RNA")
        print("   - Verificando qualidade de leituras")
        print("   - Removendo adaptadores e primers")
        
        time.sleep(0.5)
        
        return {
            "sequencias_extras": ["DNA_SEQ_001", "RNA_SEQ_002"],
            "qualidade_leituras": 0.93,
            "adaptadores_removidos": True,
            "dados_filtrados": "dados_genomicos"
        }
    
    def validar_resultados(self, resultado_especifico: Any) -> Dict[str, Any]:
        """Validação específica para resultados genômicos."""
        print("   - Validando taxa de alinhamento")
        print("   - Verificando cobertura do genoma")
        print("   - Validando chamada de variantes")
        
        time.sleep(0.3)
        
        taxa_alinhamento = resultado_especifico["alinhamento"]["taxa_alinhamento"]
        cobertura = resultado_especifico["alinhamento"]["cobertura"]
        
        validacao = "aprovado" if taxa_alinhamento > 95 and cobertura > 90 else "reprovado"
        
        return {
            "validacao": validacao,
            "confianca": 0.89 if validacao == "aprovado" else 0.65,
            "taxa_alinhamento": taxa_alinhamento,
            "cobertura": cobertura,
            "erros_encontrados": 0 if validacao == "aprovado" else 3
        }


class PipelineProteomica(PipelineAnaliseBiologica):
    """Pipeline especializado para análise proteômica."""
    
    def __init__(self, nome: str = "Pipeline Proteômica Padrão"):
        super().__init__(nome, TipoAnalise.PROTEOMICA)
        self.banco_proteinas = "Uniprot"
        self.metodo_identificacao = "LC-MS/MS"
    
    def configurar_parametros_especificos(self) -> None:
        """Configura parâmetros específicos da análise proteômica."""
        print("   - Configurando parâmetros proteômicos")
        self.banco_proteinas = self.parametros.get("banco_proteinas", "Uniprot")
        self.metodo_identificacao = self.parametros.get("metodo", "LC-MS/MS")
        print(f"   - Banco de proteínas: {self.banco_proteinas}")
        print(f"   - Método: {self.metodo_identificacao}")
    
    def realizar_analise_especifica(self, dados_processados: Any) -> Dict[str, Any]:
        """Realiza análise proteômica específica."""
        print("   - Identificando proteínas por espectrometria de massa")
        print("   - Quantificando abundância proteica")
        print("   - Analisando modificações pós-traducionais")
        
        time.sleep(0.7)
        
        return {
            "tipo": "proteomica",
            "identificacao": {
                "proteinas_identificadas": 1850,
                "peptideos_unicos": 12500,
                "cobertura_proteoma": 65.5,
                "fdr": 0.01
            },
            "quantificacao": {
                "proteinas_quantificadas": 1420,
                "faixa_dinamica": "5 ordens de magnitude",
                "reprodutibilidade": 0.94
            },
            "modificacoes": {
                "fosforilacao": 280,
                "acetilacao": 150,
                "ubiquitinacao": 45,
                "glicosilacao": 90
            }
        }
    
    def extrair_dados_biologicos(self, dados_preparados: Any) -> Dict[str, Any]:
        """Extração específica para dados proteômicos."""
        print("   - Extraindo proteínas da amostra")
        print("   - Realizando digestão enzimática (tripsina)")
        print("   - Preparando amostras para LC-MS/MS")
        
        time.sleep(0.6)
        
        return {
            "proteinas_extras": ["PROT_001", "PROT_002"],
            "digestao_completa": True,
            "enzima_utilizada": "tripsina",
            "dados_filtrados": "dados_proteomicos"
        }
    
    def validar_resultados(self, resultado_especifico: Any) -> Dict[str, Any]:
        """Validação específica para resultados proteômicos."""
        print("   - Validando taxa de identificação de proteínas")
        print("   - Verificando FDR (False Discovery Rate)")
        print("   - Validando reprodutibilidade")
        
        time.sleep(0.3)
        
        fdr = resultado_especifico["identificacao"]["fdr"]
        reprodutibilidade = resultado_especifico["quantificacao"]["reprodutibilidade"]
        
        validacao = "aprovado" if fdr < 0.05 and reprodutibilidade > 0.8 else "reprovado"
        
        return {
            "validacao": validacao,
            "confianca": 0.91 if validacao == "aprovado" else 0.68,
            "fdr": fdr,
            "reprodutibilidade": reprodutibilidade,
            "erros_encontrados": 0 if validacao == "aprovado" else 2
        }


class PipelineTranscriptomica(PipelineAnaliseBiologica):
    """Pipeline especializado para análise transcriptômica."""
    
    def __init__(self, nome: str = "Pipeline Transcriptômica Padrão"):
        super().__init__(nome, TipoAnalise.TRANSCRIPTOMICA)
        self.referencia_transcriptoma = "GRCh38"
        self.metodo_quantificacao = "RNA-Seq"
    
    def configurar_parametros_especificos(self) -> None:
        """Configura parâmetros específicos da análise transcriptômica."""
        print("   - Configurando parâmetros transcriptômicos")
        self.referencia_transcriptoma = self.parametros.get("referencia", "GRCh38")
        self.metodo_quantificacao = self.parametros.get("metodo", "RNA-Seq")
        print(f"   - Referência: {self.referencia_transcriptoma}")
        print(f"   - Método: {self.metodo_quantificacao}")
    
    def realizar_analise_especifica(self, dados_processados: Any) -> Dict[str, Any]:
        """Realiza análise transcriptômica específica."""
        print("   - Alinhando leituras de RNA-Seq")
        print("   - Quantificando expressão gênica")
        print("   - Identificando genes diferencialmente expressos")
        print("   - Realizando análise de enriquecimento funcional")
        
        time.sleep(0.9)
        
        return {
            "tipo": "transcriptomica",
            "alinhamento": {
                "taxa_alinhamento": 92.3,
                "genes_detectados": 18500,
                "transcritos_detectados": 45000
            },
            "expressao": {
                "genes_expressos": 15200,
                "genes_regulados_positivamente": 1250,
                "genes_regulados_negativamente": 980,
                "fold_change_medio": 2.4
            },
            "analise_funcional": {
                "caminhos_enriquecidos": ["Cell cycle", "DNA repair", "Apoptosis", "Metabolism"],
                "termos_go": 245,
                "caminhos_kegg": 38
            }
        }
    
    def gerar_relatorio_final(self, resultado_especifico: Any) -> Dict[str, Any]:
        """Gera relatório específico para transcriptômica."""
        relatorio = super().gerar_relatorio_final(resultado_especifico)
        relatorio.update({
            "secoes_especiais": ["Análise de Expressão", "Genes DE", "Enriquecimento"],
            "visualizacoes": ["Heatmap", "Volcano Plot", "PCA"]
        })
        return relatorio


class PipelineMetabolomica(PipelineAnaliseBiologica):
    """Pipeline especializado para análise metabolômica."""
    
    def __init__(self, nome: str = "Pipeline Metabolômica Padrão"):
        super().__init__(nome, TipoAnalise.METABOLOMICA)
        self.plataforma = "LC-MS"
        self.banco_metabolitos = "HMDB"
    
    def configurar_parametros_especificos(self) -> None:
        """Configura parâmetros específicos da análise metabolômica."""
        print("   - Configurando parâmetros metabolômicos")
        self.plataforma = self.parametros.get("plataforma", "LC-MS")
        self.banco_metabolitos = self.parametros.get("banco_metabolitos", "HMDB")
        print(f"   - Plataforma: {self.plataforma}")
        print(f"   - Banco: {self.banco_metabolitos}")
    
    def realizar_analise_especifica(self, dados_processados: Any) -> Dict[str, Any]:
        """Realiza análise metabolômica específica."""
        print("   - Detectando metabólitos por espectrometria")
        print("   - Identificando compostos químicos")
        print("   - Quantificando concentrações")
        print("   - Realizando análise de vias metabólicas")
        
        time.sleep(0.8)
        
        return {
            "tipo": "metabolomica",
            "detecao": {
                "metabolitos_detectados": 850,
                "features_unicas": 1200,
                "qualidade_identificacao": 0.87
            },
            "identificacao": {
                "metabolitos_identificados": 420,
                "nivel_confianca": "MS2",
                "classe_quimica": ["Aminoácidos", "Lipídios", "Carboidratos"]
            },
            "quantificacao": {
                "metabolitos_quantificados": 380,
                "faixa_dinamica": "4 ordens",
                "precisao": 0.08
            },
            "vias_metabolicas": {
                "vias_ativas": ["Glicólise", "TCA", "Beta-oxidação"],
                "score_enriquecimento": 0.76
            }
        }
    
    def processar_dados(self, dados_extraidos: Any) -> Dict[str, Any]:
        """Processamento específico para metabolômica."""
        print("   - Processando espectros de massa")
        print("   - Realizando alinhamento de picos")
        print("   - Normalizando intensidades")
        print("   - Removendo ruído instrumental")
        
        time.sleep(0.6)
        
        return {
            "dados_processados": "espectros_processados",
            "picos_alinhados": 2500,
            "intensidades_normalizadas": True,
            "sinal_ruido": 15.5
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Pipeline Genômica ===")
    
    # Criar e executar pipeline genômico
    pipeline_genomica = PipelineGenomica("Análise BRCA1")
    
    dados_teste = {
        "amostra": "Paciente_001",
        "tipo": "sangue",
        "sequencias": ["ATCGATCG", "GCTAGCTA"]
    }
    
    parametros_genomica = {
        "referencia": "hg38",
        "algoritmo": "BWA-MEM"
    }
    
    resultado_genomica = pipeline_genomica.executar_analise_completa(
        dados_teste, parametros_genomica
    )
    
    print(f"\nResumo Pipeline Genômica:")
    resumo_genomica = resultado_genomica.obter_resumo()
    for chave, valor in resumo_genomica.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 2: Pipeline Proteômica ===")
    
    # Criar e executar pipeline proteômico
    pipeline_proteomica = PipelineProteomica("Análise de Proteínas")
    
    dados_proteomicos = {
        "amostra": "Paciente_002",
        "tipo": "tecido",
        "preparacao": "fracionamento"
    }
    
    parametros_proteomica = {
        "banco_proteinas": "Uniprot",
        "metodo": "LC-MS/MS"
    }
    
    resultado_proteomica = pipeline_proteomica.executar_analise_completa(
        dados_proteomicos, parametros_proteomica
    )
    
    print(f"\nResumo Pipeline Proteômica:")
    resumo_proteomica = resultado_proteomica.obter_resumo()
    for chave, valor in resumo_proteomica.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 3: Pipeline Transcriptômica ===")
    
    # Criar e executar pipeline transcriptômico
    pipeline_transcriptomica = PipelineTranscriptomica("Análise de Expressão")
    
    dados_rna = {
        "amostra": "Paciente_003",
        "tipo": "RNA",
        "condicao": "tratamento"
    }
    
    resultado_transcriptomica = pipeline_transcriptomica.executar_analise_completa(dados_rna)
    
    print(f"\nResumo Pipeline Transcriptômica:")
    resumo_transcriptomica = resultado_transcriptomica.obter_resumo()
    for chave, valor in resumo_transcriptomica.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 4: Pipeline Metabolômica ===")
    
    # Criar e executar pipeline metabolômico
    pipeline_metabolomica = PipelineMetabolomica("Análise Metabólica")
    
    dados_metabolicos = {
        "amostra": "Paciente_004",
        "tipo": "soro",
        "extracao": "metanol"
    }
    
    resultado_metabolomica = pipeline_metabolomica.executar_analise_completa(dados_metabolicos)
    
    print(f"\nResumo Pipeline Metabolômica:")
    resumo_metabolomica = resultado_metabolomica.obter_resumo()
    for chave, valor in resumo_metabolomica.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 5: Comparação de Resultados ===")
    
    # Comparar resultados dos diferentes pipelines
    resultados = {
        "Genômica": resultado_genomica,
        "Proteômica": resultado_proteomica,
        "Transcriptômica": resultado_transcriptomica,
        "Metabolômica": resultado_metabolomica
    }
    
    print("\nComparação de Todos os Pipelines:")
    for nome, resultado in resultados.items():
        resumo = resultado.obter_resumo()
        print(f"\n{nome}:")
        print(f"  Status: {resumo['status']}")
        print(f"  Tempo: {resumo['tempo_total']:.2f}s")
        print(f"  Etapas: {resumo['etapas_concluidas']}")
        print(f"  Erros: {resumo['erros']}")
    
    print("\n=== Exemplo 6: Pipeline com Erro Simulado ===")
    
    # Criar pipeline que vai falhar
    class PipelineComErro(PipelineAnaliseBiologica):
        def __init__(self):
            super().__init__("Pipeline com Erro", TipoAnalise.GENOMICA)
        
        def configurar_parametros_especificos(self) -> None:
            print("   - Configurando parâmetros...")
            raise Exception("Erro simulado na configuração")
        
        def realizar_analise_especifica(self, dados_processados: Any) -> Any:
            return {"resultado": "erro"}
    
    pipeline_erro = PipelineComErro()
    resultado_erro = pipeline_erro.executar_analise_completa({"teste": "dados"})
    
    print(f"\nResumo Pipeline com Erro:")
    resumo_erro = resultado_erro.obter_resumo()
    for chave, valor in resumo_erro.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 7: Pipeline Customizado ===")
    
    # Criar pipeline customizado que sobrescreve métodos
    class PipelineCustomizado(PipelineGenomica):
        def __init__(self):
            super().__init__("Pipeline Genômico Customizado")
        
        def preparar_dados(self, dados_entrada: Any) -> Dict[str, Any]:
            """Preparação customizada com validação extra."""
            print("   - Validando formato customizado")
            print("   - Aplicando filtros avançados")
            print("   - Realizando controle de qualidade rigoroso")
            
            time.sleep(0.5)
            
            return {
                "dados_originais": dados_entrada,
                "dados_limpos": f"dados_limpos_custom_{len(str(dados_entrada))}",
                "metadados": {
                    "tamanho": len(str(dados_entrada)),
                    "formato": "custom",
                    "qualidade": "alta"
                },
                "validacao_custom": True
            }
        
        def gerar_relatorio_final(self, resultado_especifico: Any) -> Dict[str, Any]:
            """Relatório customizado com seções extras."""
            relatorio = super().gerar_relatorio_final(resultado_especifico)
            relatorio.update({
                "formato": "html_interativo",
                "secoes_especiais": ["Análise Estatística", "Visualizações 3D", "Dados Brutos"],
                "interativo": True,
                "exportacao": ["pdf", "excel", "json"]
            })
            return relatorio
    
    pipeline_custom = PipelineCustomizado()
    resultado_custom = pipeline_custom.executar_analise_completa(dados_teste)
    
    print(f"\nResumo Pipeline Customizado:")
    resumo_custom = resultado_custom.obter_resumo()
    for chave, valor in resumo_custom.items():
        print(f"  {chave}: {valor}")
    
    print("\nTemplate Method pattern implementado com sucesso!")
