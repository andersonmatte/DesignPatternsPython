from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from enum import Enum


class TipoMensagem(Enum):
    SEQUENCIAMENTO_CONCLUIDO = "sequenciamento_concluido"
    ALINHAMENTO_CONCLUIDO = "alinhamento_concluido"
    ANALISE_CONCLUIDA = "analise_concluida"
    ERRO_PROCESSAMENTO = "erro_processamento"
    RECURSO_LIBERADO = "recurso_liberado"
    RECURSO_RESERVADO = "recurso_reservado"


class Mensagem:
    """Representa uma mensagem entre componentes."""
    
    def __init__(self, tipo: TipoMensagem, remetente: str, destinatario: str = "", 
                 dados: Dict[str, Any] = None):
        self.tipo = tipo
        self.remetente = remetente
        self.destinatario = destinatario
        self.dados = dados or {}
        self.timestamp = time.time()
    
    def __str__(self) -> str:
        return f"Mensagem({self.tipo.value}, {self.remetente} -> {self.destinatario or 'todos'})"


class MediadorInterface(ABC):
    """Interface para mediador de componentes."""
    
    @abstractmethod
    def registrar_componente(self, componente: 'ComponenteBioinformatica') -> None:
        """Registra um componente no mediador."""
        pass
    
    @abstractmethod
    def enviar_mensagem(self, mensagem: Mensagem) -> None:
        """Envia mensagem através do mediador."""
        pass
    
    @abstractmethod
    def broadcast_mensagem(self, mensagem: Mensagem) -> None:
        """Envia mensagem para todos os componentes."""
        pass


class ComponenteBioinformatica(ABC):
    """Classe base para componentes bioinformáticos."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.mediador: Optional[MediadorInterface] = None
        self.estado = "inativo"
        self.historico_mensagens: List[Mensagem] = []
        self.ultimas_atividades: List[str] = []
    
    def definir_mediador(self, mediador: MediadorInterface) -> None:
        """Define o mediador para o componente."""
        self.mediador = mediador
        mediador.registrar_componente(self)
    
    def receber_mensagem(self, mensagem: Mensagem) -> None:
        """Recebe mensagem do mediador."""
        self.historico_mensagens.append(mensagem)
        self._processar_mensagem(mensagem)
    
    @abstractmethod
    def _processar_mensagem(self, mensagem: Mensagem) -> None:
        """Processa mensagem específica do componente."""
        pass
    
    def enviar_mensagem(self, tipo: TipoMensagem, destinatario: str = "", 
                       dados: Dict[str, Any] = None) -> None:
        """Envia mensagem através do mediador."""
        if self.mediador:
            mensagem = Mensagem(tipo, self.nome, destinatario, dados)
            self.mediador.enviar_mensagem(mensagem)
    
    def broadcast_mensagem(self, tipo: TipoMensagem, dados: Dict[str, Any] = None) -> None:
        """Envia mensagem para todos os componentes."""
        if self.mediador:
            mensagem = Mensagem(tipo, self.nome, "", dados)
            self.mediador.broadcast_mensagem(mensagem)
    
    def _registrar_atividade(self, atividade: str) -> None:
        """Registra atividade do componente."""
        self.ultimas_atividades.append(f"[{time.strftime('%H:%M:%S')}] {atividade}")
        
        # Mantém apenas últimas 10 atividades
        if len(self.ultimas_atividades) > 10:
            self.ultimas_atividades = self.ultimas_atividades[-10:]
    
    def obter_status(self) -> Dict[str, Any]:
        """Retorna status do componente."""
        return {
            "nome": self.nome,
            "estado": self.estado,
            "mensagens_recebidas": len(self.historico_mensagens),
            "ultimas_atividades": self.ultimas_atividades[-5:]
        }


class Sequenciador(ComponenteBioinformatica):
    """Componente responsável pelo sequenciamento."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.amostras_em_processamento: List[str] = []
        self.capacidade_maxima = 3
    
    def sequenciar_amostra(self, amostra: str) -> bool:
        """Inicia sequenciamento de uma amostra."""
        if len(self.amostras_em_processamento) >= self.capacidade_maxima:
            print(f"[{self.nome}] Capacidade máxima atingida. Amostra {amostra} na fila.")
            return False
        
        self.estado = "processando"
        self.amostras_em_processamento.append(amostra)
        self._registrar_atividade(f"Iniciou sequenciamento da amostra {amostra}")
        
        # Simula processamento
        import threading
        threading.Thread(target=self._processar_sequenciamento, args=(amostra,), daemon=True).start()
        
        return True
    
    def _processar_sequenciamento(self, amostra: str) -> None:
        """Processa sequenciamento em background."""
        time.sleep(2)  # Simula tempo de processamento
        
        # Remove da lista de processamento
        if amostra in self.amostras_em_processamento:
            self.amostras_em_processamento.remove(amostra)
        
        # Notifica conclusão
        self.estado = "concluido"
        self._registrar_atividade(f"Concluiu sequenciamento da amostra {amostra}")
        
        # Envia mensagem para o mediador
        self.broadcast_mensagem(
            TipoMensagem.SEQUENCIAMENTO_CONCLUIDO,
            {
                "amostra": amostra,
                "arquivo_gerado": f"sequenciamento_{amostra}.fastq",
                "plataforma": "Illumina",
                "reads": 50000000
            }
        )
        
        # Verifica se há mais trabalho
        if not self.amostras_em_processamento:
            self.estado = "inativo"
    
    def _processar_mensagem(self, mensagem: Mensagem) -> None:
        """Processa mensagens recebidas."""
        if mensagem.tipo == TipoMensagem.RECURSO_LIBERADO:
            self._registrar_atividade(f"Recurso liberado por {mensagem.remetente}")
        elif mensagem.tipo == TipoMensagem.ERRO_PROCESSAMENTO:
            self._registrar_atividade(f"Erro reportado por {mensagem.remetente}: {mensagem.dados.get('erro', 'Desconhecido')}")
    
    def obter_status_detalhado(self) -> Dict[str, Any]:
        """Retorna status detalhado do sequenciador."""
        status = super().obter_status()
        status.update({
            "amostras_em_processamento": len(self.amostras_em_processamento),
            "capacidade_maxima": self.capacidade_maxima,
            "fila_disponivel": len(self.amostras_em_processamento) < self.capacidade_maxima
        })
        return status


class Alinhador(ComponenteBioinformatica):
    """Componente responsável pelo alinhamento."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.arquivos_pendentes: List[str] = []
        self.em_processamento: bool = False
    
    def _processar_mensagem(self, mensagem: Mensagem) -> None:
        """Processa mensagens recebidas."""
        if mensagem.tipo == TipoMensagem.SEQUENCIAMENTO_CONCLUIDO:
            arquivo = mensagem.dados.get("arquivo_gerado")
            if arquivo:
                self.arquivos_pendentes.append(arquivo)
                self._registrar_atividade(f"Arquivo {arquivo} adicionado à fila de alinhamento")
                self._processar_proximo_arquivo()
        elif mensagem.tipo == TipoMensagem.ERRO_PROCESSAMENTO:
            self._registrar_atividade(f"Erro no sequenciamento: {mensagem.dados.get('erro')}")
    
    def _processar_proximo_arquivo(self) -> None:
        """Processa próximo arquivo da fila."""
        if self.em_processamento or not self.arquivos_pendentes:
            return
        
        arquivo = self.arquivos_pendentes.pop(0)
        self.em_processamento = True
        self.estado = "processando"
        self._registrar_atividade(f"Iniciando alinhamento do arquivo {arquivo}")
        
        # Simula processamento
        import threading
        threading.Thread(target=self._executar_alinhamento, args=(arquivo,), daemon=True).start()
    
    def _executar_alinhamento(self, arquivo: str) -> None:
        """Executa alinhamento em background."""
        time.sleep(1.5)  # Simula tempo de processamento
        
        self.em_processamento = False
        self.estado = "concluido"
        self._registrar_atividade(f"Concluiu alinhamento do arquivo {arquivo}")
        
        # Notifica conclusão
        self.broadcast_mensagem(
            TipoMensagem.ALINHAMENTO_CONCLUIDO,
            {
                "arquivo_entrada": arquivo,
                "arquivo_saida": f"alinhado_{arquivo.replace('.fastq', '.bam')}",
                "referencia": "hg38",
                "taxa_alinhamento": 98.5
            }
        )
        
        # Processa próximo se houver
        self._processar_proximo_arquivo()
        
        if not self.arquivos_pendentes:
            self.estado = "inativo"
    
    def obter_status_detalhado(self) -> Dict[str, Any]:
        """Retorna status detalhado do alinhador."""
        status = super().obter_status()
        status.update({
            "arquivos_pendentes": len(self.arquivos_pendentes),
            "em_processamento": self.em_processamento
        })
        return status


class Analisador(ComponenteBioinformatica):
    """Componente responsável pela análise."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.arquivos_analise: List[str] = []
        self.analises_em_execucao: int = 0
        self.max_analises_simultaneas = 2
    
    def _processar_mensagem(self, mensagem: Mensagem) -> None:
        """Processa mensagens recebidas."""
        if mensagem.tipo == TipoMensagem.ALINHAMENTO_CONCLUIDO:
            arquivo = mensagem.dados.get("arquivo_saida")
            if arquivo:
                self.arquivos_analise.append(arquivo)
                self._registrar_atividade(f"Arquivo {arquivo} adicionado para análise")
                self._executar_analise_se_possivel()
        elif mensagem.tipo == TipoMensagem.SEQUENCIAMENTO_CONCLUIDO:
            self._registrar_atividade(f"Sequenciamento concluído: {mensagem.dados.get('amostra')}")
    
    def _executar_analise_se_possivel(self) -> None:
        """Executa análise se houver capacidade."""
        if (self.analises_em_execucao >= self.max_analises_simultaneas or 
            not self.arquivos_analise):
            return
        
        arquivo = self.arquivos_analise.pop(0)
        self.analises_em_execucao += 1
        self.estado = "processando"
        self._registrar_atividade(f"Iniciando análise do arquivo {arquivo}")
        
        # Simula processamento
        import threading
        threading.Thread(target=self._executar_analise, args=(arquivo,), daemon=True).start()
    
    def _executar_analise(self, arquivo: str) -> None:
        """Executa análise em background."""
        time.sleep(1)  # Simula tempo de processamento
        
        self.analises_em_execucao -= 1
        self._registrar_atividade(f"Concluiu análise do arquivo {arquivo}")
        
        # Notifica conclusão
        self.broadcast_mensagem(
            TipoMensagem.ANALISE_CONCLUIDA,
            {
                "arquivo_analisado": arquivo,
                "variantes_encontradas": 4500,
                "genes_regulados": 1200,
                "relatorio_gerado": f"relatorio_{arquivo.replace('.bam', '.pdf')}"
            }
        )
        
        # Continua processando se houver mais arquivos
        self._executar_analise_se_possivel()
        
        if self.analises_em_execucao == 0 and not self.arquivos_analise:
            self.estado = "inativo"
    
    def obter_status_detalhado(self) -> Dict[str, Any]:
        """Retorna status detalhado do analisador."""
        status = super().obter_status()
        status.update({
            "arquivos_pendentes": len(self.arquivos_analise),
            "analises_em_execucao": self.analises_em_execucao,
            "capacidade_disponivel": self.analises_em_execucao < self.max_analises_simultaneas
        })
        return status


class GerenciadorRecursos(ComponenteBioinformatica):
    """Componente que gerencia recursos do laboratório."""
    
    def __init__(self, nome: str):
        super().__init__(nome)
        self.recursos: Dict[str, Dict[str, Any]] = {
            "sequenciador_illumina": {"disponivel": True, "uso": 0},
            "alinhador_cluster": {"disponivel": True, "uso": 0},
            "analise_workstation": {"disponivel": True, "uso": 0}
        }
    
    def _processar_mensagem(self, mensagem: Mensagem) -> None:
        """Processa mensagens sobre uso de recursos."""
        if mensagem.tipo == TipoMensagem.SEQUENCIAMENTO_CONCLUIDO:
            self._liberar_recurso("sequenciador_illumina")
            self._registrar_atividade(f"Liberou sequenciador após conclusão de {mensagem.dados.get('amostra')}")
        elif mensagem.tipo == TipoMensagem.ALINHAMENTO_CONCLUIDO:
            self._liberar_recurso("alinhador_cluster")
            self._registrar_atividade(f"Liberou cluster após alinhamento")
        elif mensagem.tipo == TipoMensagem.ANALISE_CONCLUIDA:
            self._liberar_recurso("analise_workstation")
            self._registrar_atividade(f"Liberou workstation após análise")
    
    def _liberar_recurso(self, recurso: str) -> None:
        """Libera um recurso."""
        if recurso in self.recursos:
            self.recursos[recurso]["disponivel"] = True
            self.recursos[recurso]["uso"] = 0
            self.broadcast_mensagem(
                TipoMensagem.RECURSO_LIBERADO,
                {"recurso": recurso, "status": "disponivel"}
            )
    
    def obter_status_detalhado(self) -> Dict[str, Any]:
        """Retorna status detalhado dos recursos."""
        status = super().obter_status()
        status.update({
            "recursos": self.recursos.copy(),
            "recursos_disponiveis": sum(1 for r in self.recursos.values() if r["disponivel"]),
            "total_recursos": len(self.recursos)
        })
        return status


class CoordenadorAnalise(MediadorInterface):
    """Mediador que coordena comunicação entre componentes."""
    
    def __init__(self):
        self.componentes: Dict[str, ComponenteBioinformatica] = {}
        self.historico_mensagens: List[Mensagem] = []
        self.estatisticas = {
            "mensagens_trocadas": 0,
            "mensagens_por_tipo": {},
            "componentes_ativos": 0
        }
    
    def registrar_componente(self, componente: ComponenteBioinformatica) -> None:
        """Registra um componente no mediador."""
        self.componentes[componente.nome] = componente
        print(f"[Mediador] Componente {componente.nome} registrado")
        self._atualizar_estatisticas()
    
    def enviar_mensagem(self, mensagem: Mensagem) -> None:
        """Envia mensagem para destinatário específico."""
        self.historico_mensagens.append(mensagem)
        self._atualizar_estatisticas_mensagem(mensagem)
        
        if mensagem.destinatario and mensagem.destinatario in self.componentes:
            destinatario = self.componentes[mensagem.destinatario]
            destinatario.receber_mensagem(mensagem)
            print(f"[Mediador] Mensagem enviada: {mensagem.remetente} -> {mensagem.destinatario}")
        else:
            print(f"[Mediador] Destinatário {mensagem.destinatario} não encontrado")
    
    def broadcast_mensagem(self, mensagem: Mensagem) -> None:
        """Envia mensagem para todos os componentes."""
        self.historico_mensagens.append(mensagem)
        self._atualizar_estatisticas_mensagem(mensagem)
        
        print(f"[Mediador] Broadcast de {mensagem.remetente}: {mensagem.tipo.value}")
        
        for nome, componente in self.componentes.items():
            if nome != mensagem.remetente:  # Não envia para o remetente
                componente.receber_mensagem(mensagem)
    
    def _atualizar_estatisticas_mensagem(self, mensagem: Mensagem) -> None:
        """Atualiza estatísticas de mensagens."""
        self.estatisticas["mensagens_trocadas"] += 1
        tipo = mensagem.tipo.value
        self.estatisticas["mensagens_por_tipo"][tipo] = \
            self.estatisticas["mensagens_por_tipo"].get(tipo, 0) + 1
    
    def _atualizar_estatisticas(self) -> None:
        """Atualiza estatísticas dos componentes."""
        ativos = sum(1 for c in self.componentes.values() if c.estado != "inativo")
        self.estatisticas["componentes_ativos"] = ativos
    
    def obter_status_sistema(self) -> Dict[str, Any]:
        """Retorna status completo do sistema."""
        status_componentes = {}
        for nome, componente in self.componentes.items():
            if hasattr(componente, 'obter_status_detalhado'):
                status_componentes[nome] = componente.obter_status_detalhado()
            else:
                status_componentes[nome] = componente.obter_status()
        
        return {
            "mediador": "CoordenadorAnalise",
            "estatisticas": self.estatisticas.copy(),
            "componentes": status_componentes,
            "total_mensagens": len(self.historico_mensagens)
        }
    
    def obter_historico_recente(self, limite: int = 10) -> List[Mensagem]:
        """Retorna histórico recente de mensagens."""
        return self.historico_mensagens[-limite:]


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Configuração do Sistema com Mediator ===")
    
    # Criar mediador
    coordenador = CoordenadorAnalise()
    
    # Criar componentes
    sequenciador = Sequenciador("Seq_001")
    alinhador = Alinhador("Alin_001")
    analisador = Analisador("Analis_001")
    gerenciador = GerenciadorRecursos("Rec_001")
    
    # Conectar componentes ao mediador
    sequenciador.definir_mediador(coordenador)
    alinhador.definir_mediador(coordenador)
    analisador.definir_mediador(coordenador)
    gerenciador.definir_mediador(coordenador)
    
    print("Sistema configurado com 4 componentes conectados ao mediador")
    
    print("\n=== Exemplo 2: Fluxo Completo de Análise ===")
    
    # Iniciar sequenciamento de múltiplas amostras
    print("\nIniciando sequenciamento de amostras:")
    amostras = ["Amostra_A", "Amostra_B", "Amostra_C", "Amostra_D"]
    
    for amostra in amostras:
        sucesso = sequenciador.sequenciar_amostra(amostra)
        print(f"  {amostra}: {'Iniciado' if sucesso else 'Na fila'}")
    
    # Aguardar processamento
    print("\nAguardando processamento...")
    time.sleep(8)
    
    # Verificar status final
    print("\n=== Status Final do Sistema ===")
    status_final = coordenador.obter_status_sistema()
    
    for componente, info in status_final["componentes"].items():
        print(f"\n{componente}:")
        print(f"  Estado: {info['estado']}")
        print(f"  Últimas atividades: {info['ultimas_atividades']}")
        if 'amostras_em_processamento' in info:
            print(f"  Amostras em processamento: {info['amostras_em_processamento']}")
        if 'arquivos_pendentes' in info:
            print(f"  Arquivos pendentes: {info['arquivos_pendentes']}")
    
    print("\n=== Exemplo 3: Comunicação Direta entre Componentes ===")
    
    # Enviar mensagem específica
    print("\nEnviando mensagem específica:")
    sequenciador.enviar_mensagem(
        TipoMensagem.ERRO_PROCESSAMENTO,
        "Alin_001",
        {"erro": "Falha no equipamento", "codigo": "E001"}
    )
    
    time.sleep(0.5)
    
    print("\n=== Exemplo 4: Estatísticas do Sistema ===")
    
    stats = status_final["estatisticas"]
    print(f"\nEstatísticas do Mediador:")
    print(f"  Mensagens trocadas: {stats['mensagens_trocadas']}")
    print(f"  Componentes ativos: {stats['componentes_ativos']}")
    print(f"  Mensagens por tipo:")
    for tipo, count in stats['mensagens_por_tipo'].items():
        print(f"    {tipo}: {count}")
    
    print("\n=== Exemplo 5: Histórico de Mensagens ===")
    
    historico = coordenador.obter_historico_recente(5)
    print(f"\nÚltimas 5 mensagens:")
    for i, msg in enumerate(historico, 1):
        print(f"  {i}. {msg}")
    
    print("\n=== Exemplo 6: Simulação de Falha e Recuperação ===")
    
    # Simular falha no alinhador
    print("\nSimulando falha no alinhador:")
    alinhador.broadcast_mensagem(
        TipoMensagem.ERRO_PROCESSAMENTO,
        {"erro": "Falha no cluster de alinhamento", "recuperacao": "reiniciar_servicos"}
    )
    
    # Iniciar novo sequenciamento após falha
    time.sleep(1)
    print("\nIniciando novo sequenciamento após recuperação:")
    sequenciador.sequenciar_amostra("Amostra_Recuperacao")
    
    time.sleep(3)
    
    print("\n=== Exemplo 7: Múltiplos Fluxos Simultâneos ===")
    
    # Iniciar múltiplos processos simultâneos
    print("\nIniciando múltiplos fluxos:")
    
    for i in range(3):
        amostra = f"Amostra_Simultanea_{i+1}"
        sequenciador.sequenciar_amostra(amostra)
        time.sleep(0.5)  # Pequeno intervalo entre inícios
    
    print("Aguardando processamento simultâneo...")
    time.sleep(10)
    
    # Status final
    status_final_simultaneo = coordenador.obter_status_sistema()
    
    print("\n=== Status Final dos Fluxos Simultâneos ===")
    for componente, info in status_final_simultaneo["componentes"].items():
        print(f"\n{componente}:")
        print(f"  Estado: {info['estado']}")
        print(f"  Mensagens recebidas: {info['mensagens_recebidas']}")
    
    print("\nMediator pattern implementado com sucesso!")
