from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from enum import Enum


class StatusComando(Enum):
    PENDENTE = "pendente"
    EXECUTANDO = "executando"
    CONCLUIDO = "concluido"
    FALHOU = "falhou"
    DESFEITO = "desfeito"


class Comando(ABC):
    """Interface base para comandos laboratoriais."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.status = StatusComando.PENDENTE
        self.resultado: Any = None
        self.erro: Optional[str] = None
        self.timestamp_criacao = time.time()
        self.timestamp_execucao: Optional[float] = None
        self.timestamp_conclusao: Optional[float] = None
    
    @abstractmethod
    def executar(self) -> Any:
        """Executa o comando."""
        pass
    
    @abstractmethod
    def desfazer(self) -> bool:
        """Desfaz o comando."""
        pass
    
    def obter_info(self) -> Dict[str, Any]:
        """Retorna informações do comando."""
        return {
            "nome": self.nome,
            "status": self.status.value,
            "resultado": self.resultado,
            "erro": self.erro,
            "tempo_execucao": self._calcular_tempo_execucao()
        }
    
    def _calcular_tempo_execucao(self) -> Optional[float]:
        """Calcula tempo de execução."""
        if self.timestamp_execucao and self.timestamp_conclusao:
            return self.timestamp_conclusao - self.timestamp_execucao
        return None


class SequenciarCommand(Comando):
    """Comando para sequenciar amostra biológica."""
    
    def __init__(self, amostra: str, plataforma: str = "illumina"):
        super().__init__(f"Sequenciar {amostra}")
        self.amostra = amostra
        self.plataforma = plataforma
        self.dados_originais: Optional[Dict[str, Any]] = None
        self.arquivos_gerados: List[str] = []
    
    def executar(self) -> Dict[str, Any]:
        """Executa sequenciamento."""
        try:
            self.status = StatusComando.EXECUTANDO
            self.timestamp_execucao = time.time()
            
            print(f"Executando sequenciamento da amostra {self.amostra} com {self.plataforma}...")
            
            # Simulação do processo de sequenciamento
            time.sleep(0.2)
            
            # Dados simulados do sequenciamento
            self.dados_originais = {
                "amostra": self.amostra,
                "plataforma": self.plataforma,
                "reads_gerados": 50000000 if self.plataforma == "illumina" else 1000000,
                "qualidade": "Q30" if self.plataforma == "illumina" else "Q15",
                "tempo_estimado": "12 horas" if self.plataforma == "illumina" else "24 horas"
            }
            
            # Arquivos gerados
            arquivo_saida = f"sequenciamento_{self.amostra}_{self.plataforma}.fastq"
            self.arquivos_gerados.append(arquivo_saida)
            
            self.resultado = {
                **self.dados_originais,
                "arquivos": self.arquivos_gerados.copy(),
                "status": "concluido"
            }
            
            self.status = StatusComando.CONCLUIDO
            self.timestamp_conclusao = time.time()
            
            print(f"Sequenciamento concluído: {len(self.arquivos_gerados)} arquivos gerados")
            return self.resultado
            
        except Exception as e:
            self.erro = str(e)
            self.status = StatusComando.FALHOU
            self.timestamp_conclusao = time.time()
            raise
    
    def desfazer(self) -> bool:
        """Desfaz sequenciamento (remove arquivos gerados)."""
        try:
            if self.status != StatusComando.CONCLUIDO:
                print("Comando não foi concluído, não é possível desfazer")
                return False
            
            print(f"Desfazendo sequenciamento da amostra {self.amostra}...")
            
            # Remove arquivos gerados (simulação)
            for arquivo in self.arquivos_gerados:
                print(f"  Removendo arquivo: {arquivo}")
            
            self.arquivos_gerados.clear()
            self.resultado = None
            self.status = StatusComando.DESFEITO
            
            print("Sequenciamento desfeito com sucesso")
            return True
            
        except Exception as e:
            print(f"Erro ao desfazer sequenciamento: {e}")
            return False


class AlinharCommand(Comando):
    """Comando para alinhar sequências."""
    
    def __init__(self, arquivo_fastq: str, referencia: str = "hg38"):
        super().__init__(f"Alinhar {arquivo_fastq}")
        self.arquivo_fastq = arquivo_fastq
        self.referencia = referencia
        self.arquivos_gerados: List[str] = []
        self.alinhamento_original: Optional[Dict[str, Any]] = None
    
    def executar(self) -> Dict[str, Any]:
        """Executa alinhamento."""
        try:
            self.status = StatusComando.EXECUTANDO
            self.timestamp_execucao = time.time()
            
            print(f"Alinhando {self.arquivo_fastq} contra referência {self.referencia}...")
            
            # Simulação do processo de alinhamento
            time.sleep(0.15)
            
            # Dados simulados do alinhamento
            self.alinhamento_original = {
                "arquivo_entrada": self.arquivo_fastq,
                "referencia": self.referencia,
                "taxa_alinhamento": 98.5,
                "cobertura": 95.2,
                "algoritmo": "BWA-MEM"
            }
            
            # Arquivos gerados
            arquivo_bam = f"alinhado_{self.arquivo_fastq.replace('.fastq', '.bam')}"
            arquivo_bai = f"alinhado_{self.arquivo_fastq.replace('.fastq', '.bai')}"
            
            self.arquivos_gerados.extend([arquivo_bam, arquivo_bai])
            
            self.resultado = {
                **self.alinhamento_original,
                "arquivos": self.arquivos_gerados.copy(),
                "status": "concluido"
            }
            
            self.status = StatusComando.CONCLUIDO
            self.timestamp_conclusao = time.time()
            
            print(f"Alinhamento concluído: {len(self.arquivos_gerados)} arquivos gerados")
            return self.resultado
            
        except Exception as e:
            self.erro = str(e)
            self.status = StatusComando.FALHOU
            self.timestamp_conclusao = time.time()
            raise
    
    def desfazer(self) -> bool:
        """Desfaz alinhamento."""
        try:
            if self.status != StatusComando.CONCLUIDO:
                print("Comando não foi concluído, não é possível desfazer")
                return False
            
            print(f"Desfazendo alinhamento de {self.arquivo_fastq}...")
            
            # Remove arquivos gerados
            for arquivo in self.arquivos_gerados:
                print(f"  Removendo arquivo: {arquivo}")
            
            self.arquivos_gerados.clear()
            self.resultado = None
            self.status = StatusComando.DESFEITO
            
            print("Alinhamento desfeito com sucesso")
            return True
            
        except Exception as e:
            print(f"Erro ao desfazer alinhamento: {e}")
            return False


class AnalisarCommand(Comando):
    """Comando para análise de dados genômicos."""
    
    def __init__(self, arquivo_bam: str, tipo_analise: str = "variacao"):
        super().__init__(f"Analisar {arquivo_bam}")
        self.arquivo_bam = arquivo_bam
        self.tipo_analise = tipo_analise
        self.analise_original: Optional[Dict[str, Any]] = None
        self.arquivos_gerados: List[str] = []
    
    def executar(self) -> Dict[str, Any]:
        """Executa análise."""
        try:
            self.status = StatusComando.EXECUTANDO
            self.timestamp_execucao = time.time()
            
            print(f"Analisando {self.arquivo_bam} (tipo: {self.tipo_analise})...")
            
            # Simulação do processo de análise
            time.sleep(0.25)
            
            # Dados simulados da análise
            if self.tipo_analise == "variacao":
                self.analise_original = {
                    "variantes_encontradas": 4500,
                    "snp_count": 4200,
                    "indel_count": 300,
                    "variantes_raras": 150
                }
                arquivo_saida = f"variantes_{self.arquivo_bam.replace('.bam', '.vcf')}"
            else:
                self.analise_original = {
                    "genes_expressos": 18000,
                    "genes_regulados": 4300,
                    "caminhos_enriquecidos": ["Cell cycle", "DNA repair"]
                }
                arquivo_saida = f"expressao_{self.arquivo_bam.replace('.bam', '.csv')}"
            
            self.arquivos_gerados.append(arquivo_saida)
            
            self.resultado = {
                **self.analise_original,
                "tipo_analise": self.tipo_analise,
                "arquivos": self.arquivos_gerados.copy(),
                "status": "concluido"
            }
            
            self.status = StatusComando.CONCLUIDO
            self.timestamp_conclusao = time.time()
            
            print(f"Análise concluída: {len(self.arquivos_gerados)} arquivos gerados")
            return self.resultado
            
        except Exception as e:
            self.erro = str(e)
            self.status = StatusComando.FALHOU
            self.timestamp_conclusao = time.time()
            raise
    
    def desfazer(self) -> bool:
        """Desfaz análise."""
        try:
            if self.status != StatusComando.CONCLUIDO:
                print("Comando não foi concluído, não é possível desfazer")
                return False
            
            print(f"Desfazendo análise de {self.arquivo_bam}...")
            
            # Remove arquivos gerados
            for arquivo in self.arquivos_gerados:
                print(f"  Removendo arquivo: {arquivo}")
            
            self.arquivos_gerados.clear()
            self.resultado = None
            self.status = StatusComando.DESFEITO
            
            print("Análise desfeita com sucesso")
            return True
            
        except Exception as e:
            print(f"Erro ao desfazer análise: {e}")
            return False


class MacroCommand(Comando):
    """Macro comando que executa múltiplos comandos."""
    
    def __init__(self, nome: str, comandos: List[Comando]):
        super().__init__(nome)
        self.comandos = comandos
        self.resultados_parciais: List[Dict[str, Any]] = []
    
    def executar(self) -> List[Dict[str, Any]]:
        """Executa todos os comandos na sequência."""
        try:
            self.status = StatusComando.EXECUTANDO
            self.timestamp_execucao = time.time()
            
            print(f"Executando macro comando: {self.nome}")
            print(f"Contém {len(self.comandos)} comandos")
            
            self.resultados_parciais = []
            
            for i, comando in enumerate(self.comandos):
                print(f"\nExecutando comando {i+1}/{len(self.comandos)}: {comando.nome}")
                
                try:
                    resultado = comando.executar()
                    self.resultados_parciais.append({
                        "comando": comando.nome,
                        "status": "sucesso",
                        "resultado": resultado
                    })
                    print(f"Comando {i+1} concluído com sucesso")
                    
                except Exception as e:
                    self.resultados_parciais.append({
                        "comando": comando.nome,
                        "status": "erro",
                        "erro": str(e)
                    })
                    print(f"Comando {i+1} falhou: {e}")
                    # Continua executando os demais comandos
            
            self.resultado = {
                "nome_macro": self.nome,
                "total_comandos": len(self.comandos),
                "comandos_sucesso": sum(1 for r in self.resultados_parciais if r["status"] == "sucesso"),
                "comandos_falha": sum(1 for r in self.resultados_parciais if r["status"] == "erro"),
                "resultados": self.resultados_parciais
            }
            
            self.status = StatusComando.CONCLUIDO
            self.timestamp_conclusao = time.time()
            
            print(f"\nMacro comando concluído: {self.resultado['comandos_sucesso']}/{len(self.comandos)} comandos com sucesso")
            return self.resultado
            
        except Exception as e:
            self.erro = str(e)
            self.status = StatusComando.FALHOU
            self.timestamp_conclusao = time.time()
            raise
    
    def desfazer(self) -> bool:
        """Desfaz todos os comandos na ordem inversa."""
        try:
            if self.status != StatusComando.CONCLUIDO:
                print("Macro comando não foi concluído, não é possível desfazer")
                return False
            
            print(f"Desfazendo macro comando: {self.nome}")
            
            # Desfaz na ordem inversa
            sucesso_total = True
            for comando in reversed(self.comandos):
                if comando.status == StatusComando.CONCLUIDO:
                    print(f"  Desfazendo: {comando.nome}")
                    if not comando.desfazer():
                        sucesso_total = False
                        print(f"    Falha ao desfazer {comando.nome}")
                else:
                    print(f"  Pulando {comando.nome} (não foi concluído)")
            
            self.status = StatusComando.DESFEITO
            print("Macro comando desfeito")
            return sucesso_total
            
        except Exception as e:
            print(f"Erro ao desfazer macro comando: {e}")
            return False


class InvocadorComandos:
    """Invocador que gerencia a execução de comandos."""
    
    def __init__(self):
        self.historico_comandos: List[Comando] = []
        self.pilha_desfazer: List[Comando] = []
        self.max_historico = 100
    
    def executar_comando(self, comando: Comando) -> Any:
        """Executa um comando e adiciona ao histórico."""
        print(f"\n--- Invocador executando: {comando.nome} ---")
        
        try:
            resultado = comando.executar()
            
            # Adiciona ao histórico
            self.historico_comandos.append(comando)
            
            # Adiciona à pilha de desfazer
            if comando.status == StatusComando.CONCLUIDO:
                self.pilha_desfazer.append(comando)
            
            # Limita tamanho do histórico
            if len(self.historico_comandos) > self.max_historico:
                self.historico_comandos.pop(0)
            
            print(f"--- Comando {comando.nome} concluído ---")
            return resultado
            
        except Exception as e:
            print(f"--- Erro ao executar {comando.nome}: {e} ---")
            # Adiciona ao histórico mesmo com erro
            self.historico_comandos.append(comando)
            raise
    
    def desfazer_ultimo_comando(self) -> bool:
        """Desfaz o último comando executado."""
        if not self.pilha_desfazer:
            print("Nenhum comando para desfazer")
            return False
        
        comando = self.pilha_desfazer.pop()
        print(f"\n--- Invocador desfazendo: {comando.nome} ---")
        
        return comando.desfazer()
    
    def desfazer_todos(self) -> bool:
        """Desfaz todos os comandos."""
        if not self.pilha_desfazer:
            print("Nenhum comando para desfazer")
            return False
        
        print(f"\n--- Desfazendo {len(self.pilha_desfazer)} comandos ---")
        sucesso_total = True
        
        while self.pilha_desfazer:
            comando = self.pilha_desfazer.pop()
            if not comando.desfazer():
                sucesso_total = False
        
        print("--- Todos os comandos desfeitos ---")
        return sucesso_total
    
    def obter_historico(self) -> List[Dict[str, Any]]:
        """Retorna o histórico de comandos."""
        return [comando.obter_info() for comando in self.historico_comandos]
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas dos comandos."""
        if not self.historico_comandos:
            return {"total": 0}
        
        status_counts = {}
        tempo_total = 0
        
        for comando in self.historico_comandos:
            status = comando.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
            if comando.timestamp_execucao and comando.timestamp_conclusao:
                tempo_total += comando.timestamp_conclusao - comando.timestamp_execucao
        
        return {
            "total_comandos": len(self.historico_comandos),
            "status_counts": status_counts,
            "tempo_total_execucao": tempo_total,
            "comandos_desfaziveis": len(self.pilha_desfazer)
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Comandos Individuais ===")
    
    invocador = InvocadorComandos()
    
    # Criar comandos individuais
    cmd_sequenciar = SequenciarCommand("Amostra_001", "illumina")
    cmd_alinhar = AlinharCommand("sequenciamento_Amostra_001_illumina.fastq", "hg38")
    cmd_analisar = AnalisarCommand("alinhado_sequenciamento_Amostra_001_illumina.bam", "variacao")
    
    # Executar comandos individualmente
    resultado1 = invocador.executar_comando(cmd_sequenciar)
    print(f"Resultado sequenciamento: {resultado1['status'] if resultado1 else 'Erro'}")
    
    resultado2 = invocador.executar_comando(cmd_alinhar)
    print(f"Resultado alinhamento: {resultado2['status'] if resultado2 else 'Erro'}")
    
    resultado3 = invocador.executar_comando(cmd_analisar)
    print(f"Resultado análise: {resultado3['status'] if resultado3 else 'Erro'}")
    
    print("\n=== Exemplo 2: Desfazer Comandos ===")
    
    # Desfazer último comando
    print("\nDesfazendo último comando:")
    desfeito1 = invocador.desfazer_ultimo_comando()
    print(f"Desfeito com sucesso: {desfeito1}")
    
    # Desfazer outro comando
    print("\nDesfazendo penúltimo comando:")
    desfeito2 = invocador.desfazer_ultimo_comando()
    print(f"Desfeito com sucesso: {desfeito2}")
    
    print("\n=== Exemplo 3: Macro Comando ===")
    
    # Criar macro comando para pipeline completo
    pipeline_completo = MacroCommand(
        "Pipeline Completo",
        [
            SequenciarCommand("Amostra_002", "illumina"),
            AlinharCommand("sequenciamento_Amostra_002_illumina.fastq", "hg38"),
            AnalisarCommand("alinhado_sequenciamento_Amostra_002_illumina.bam", "variacao")
        ]
    )
    
    # Executar macro comando
    resultado_macro = invocador.executar_comando(pipeline_completo)
    print(f"\nResultado macro comando:")
    print(f"  Total comandos: {resultado_macro['total_comandos']}")
    print(f"  Sucesso: {resultado_macro['comandos_sucesso']}")
    print(f"  Falha: {resultado_macro['comandos_falha']}")
    
    print("\n=== Exemplo 4: Desfazer Macro Comando ===")
    
    # Desfazer macro comando inteiro
    print("\nDesfazendo macro comando:")
    desfeito_macro = invocador.desfazer_ultimo_comando()
    print(f"Macro comando desfeito: {desfeito_macro}")
    
    print("\n=== Exemplo 5: Histórico e Estatísticas ===")
    
    # Obter histórico
    historico = invocador.obter_historico()
    print(f"\nHistórico de comandos ({len(historico)}):")
    for i, cmd_info in enumerate(historico[-5:], 1):  # Últimos 5
        print(f"  {i}. {cmd_info['nome']} - {cmd_info['status']} - {cmd_info['tempo_execucao']:.3f}s" if cmd_info['tempo_execucao'] else f"  {i}. {cmd_info['nome']} - {cmd_info['status']}")
    
    # Estatísticas
    stats = invocador.obter_estatisticas()
    print(f"\nEstatísticas:")
    print(f"  Total comandos: {stats['total_comandos']}")
    print(f"  Por status: {stats['status_counts']}")
    print(f"  Tempo total: {stats['tempo_total_execucao']:.3f}s")
    print(f"  Comandos desfazíveis: {stats['comandos_desfaziveis']}")
    
    print("\n=== Exemplo 6: Tratamento de Erros ===")
    
    # Comando com erro (simulado)
    class ComandoComErro(Comando):
        def executar(self):
            raise Exception("Erro simulado no comando")
        
        def desfazer(self):
            return True
    
    cmd_erro = ComandoComErro("Comando com Erro")
    
    try:
        invocador.executar_comando(cmd_erro)
    except Exception as e:
        print(f"Erro capturado: {e}")
    
    # Verificar histórico após erro
    historico_pos_erro = invocador.obter_historico()
    print(f"\nHistórico após erro ({len(historico_pos_erro)} comandos):")
    for cmd_info in historico_pos_erro[-3:]:
        print(f"  - {cmd_info['nome']}: {cmd_info['status']}")
    
    print("\n=== Exemplo 7: Pipeline Complexo com Macros Aninhados ===")
    
    # Criar macros aninhados
    macro_sequenciamento = MacroCommand(
        "Sequenciamento Lote",
        [
            SequenciarCommand("Amostra_Batch_1", "illumina"),
            SequenciarCommand("Amostra_Batch_2", "illumina"),
            SequenciarCommand("Amostra_Batch_3", "ont")
        ]
    )
    
    macro_analise = MacroCommand(
        "Análise Lote",
        [
            AlinharCommand("sequenciamento_Amostra_Batch_1_illumina.fastq", "hg38"),
            AlinharCommand("sequenciamento_Amostra_Batch_2_illumina.fastq", "hg38"),
            AlinharCommand("sequenciamento_Amostra_Batch_3_ont.fastq", "hg38"),
            AnalisarCommand("alinhado_sequenciamento_Amostra_Batch_1_illumina.bam", "variacao"),
            AnalisarCommand("alinhado_sequenciamento_Amostra_Batch_2_illumina.bam", "variacao"),
            AnalisarCommand("alinhado_sequenciamento_Amostra_Batch_3_ont.bam", "variacao")
        ]
    )
    
    # Macro principal
    macro_principal = MacroCommand(
        "Pipeline Completo Lote",
        [macro_sequenciamento, macro_analise]
    )
    
    # Executar pipeline complexo
    print("\nExecutando pipeline complexo...")
    resultado_complexo = invocador.executar_comando(macro_principal)
    
    print(f"\nPipeline complexo concluído:")
    print(f"  Comandos no macro principal: {resultado_complexo['total_comandos']}")
    print(f"  Sucesso: {resultado_complexo['comandos_sucesso']}")
    
    # Estatísticas finais
    stats_finais = invocador.obter_estatisticas()
    print(f"\nEstatísticas finais:")
    print(f"  Total de comandos executados: {stats_finais['total_comandos']}")
    print(f"  Tempo total de execução: {stats_finais['tempo_total_execucao']:.3f}s")
    
    print("\nCommand pattern implementado com sucesso!")
