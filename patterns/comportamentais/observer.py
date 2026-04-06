from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from enum import Enum


class TipoEvento(Enum):
    ANALISE_INICIADA = "analise_iniciada"
    ANALISE_CONCLUIDA = "analise_concluida"
    ANALISE_FALHOU = "analise_falhou"
    RECURSO_ALOCADO = "recurso_alocado"
    RECURSO_LIBERADO = "recurso_liberado"
    RESULTADO_GERADO = "resultado_gerado"
    NOTIFICACAO_SISTEMA = "notificacao_sistema"


class Evento:
    """Representa um evento no sistema bioinformático."""
    
    def __init__(self, tipo: TipoEvento, origem: str, dados: Dict[str, Any] = None):
        self.tipo = tipo
        self.origem = origem
        self.dados = dados or {}
        self.timestamp = time.time()
        self.id_evento = self._gerar_id()
    
    def _gerar_id(self) -> str:
        """Gera ID único para o evento."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def __str__(self) -> str:
        return f"Evento({self.tipo.value}, {self.origem}, {self.id_evento})"


class Observador(ABC):
    """Interface base para observadores."""
    
    @abstractmethod
    def atualizar(self, evento: Evento) -> None:
        """Recebe notificação de evento."""
        pass
    
    @abstractmethod
    def obter_nome(self) -> str:
        """Retorna nome do observador."""
        pass


class Sujeito(ABC):
    """Interface base para sujeitos observáveis."""
    
    def __init__(self):
        self.observadores: List[Observador] = []
        self.historico_eventos: List[Evento] = []
    
    def adicionar_observador(self, observador: Observador) -> None:
        """Adiciona um observador."""
        if observador not in self.observadores:
            self.observadores.append(observador)
            print(f"[{self.__class__.__name__}] Observador {observador.obter_nome()} adicionado")
    
    def remover_observador(self, observador: Observador) -> None:
        """Remove um observador."""
        if observador in self.observadores:
            self.observadores.remove(observador)
            print(f"[{self.__class__.__name__}] Observador {observador.obter_nome()} removido")
    
    def notificar_observadores(self, evento: Evento) -> None:
        """Notifica todos os observadores sobre um evento."""
        self.historico_eventos.append(evento)
        print(f"[{self.__class__.__name__}] Notificando {len(self.observadores)} observadores: {evento.tipo.value}")
        
        for observador in self.observadores:
            try:
                observador.atualizar(evento)
            except Exception as e:
                print(f"[{self.__class__.__name__}] Erro ao notificar {observador.obter_nome()}: {e}")
    
    def obter_historico_eventos(self) -> List[Evento]:
        """Retorna histórico de eventos."""
        return self.historico_eventos.copy()


class Pesquisador(Observador):
    """Observador que representa um pesquisador."""
    
    def __init__(self, nome: str, email: str, especialidade: str = "geral"):
        self.nome = nome
        self.email = email
        self.especialidade = especialidade
        self.notificacoes_recebidas: List[Evento] = []
        self.interesses: List[TipoEvento] = []
    
    def definir_interesses(self, interesses: List[TipoEvento]) -> None:
        """Define quais tipos de eventos interessam ao pesquisador."""
        self.interesses = interesses
    
    def atualizar(self, evento: Evento) -> None:
        """Recebe notificação de evento."""
        # Verifica se o evento é de interesse
        if not self.interesses or evento.tipo in self.interesses:
            self.notificacoes_recebidas.append(evento)
            self._processar_notificacao(evento)
    
    def _processar_notificacao(self, evento: Evento) -> None:
        """Processa notificação recebida."""
        print(f"\n[Pesquisador {self.nome}] Notificação recebida:")
        print(f"  Evento: {evento.tipo.value}")
        print(f"  Origem: {evento.origem}")
        print(f"  Dados: {evento.dados}")
        
        # Ações específicas baseadas no tipo de evento
        if evento.tipo == TipoEvento.ANALISE_CONCLUIDA:
            print(f"  ✓ Análise concluída! Verificar resultados.")
        elif evento.tipo == TipoEvento.ANALISE_FALHOU:
            print(f"  ⚠ Análise falhou: {evento.dados.get('erro', 'Erro desconhecido')}")
        elif evento.tipo == TipoEvento.RESULTADO_GERADO:
            print(f"  📊 Novo resultado disponível para revisão.")
    
    def obter_nome(self) -> str:
        """Retorna nome do pesquisador."""
        return f"Pesquisador-{self.nome}"
    
    def obter_resumo_notificacoes(self) -> Dict[str, Any]:
        """Retorna resumo das notificações recebidas."""
        if not self.notificacoes_recebidas:
            return {"total": 0}
        
        contagem_tipos = {}
        for notificacao in self.notificacoes_recebidas:
            tipo = notificacao.tipo.value
            contagem_tipos[tipo] = contagem_tipos.get(tipo, 0) + 1
        
        return {
            "total": len(self.notificacoes_recebidas),
            "por_tipo": contagem_tipos,
            "ultima_notificacao": self.notificacoes_recebidas[-1].timestamp
        }


class SistemaAlerta(Observador):
    """Observador que gerencia alertas do sistema."""
    
    def __init__(self, nome: str, nivel_alerte: str = "medio"):
        self.nome = nome
        self.nivel_alerte = nivel_alerte
        self.alertas: List[Dict[str, Any]] = []
        self.regras_alerta = self._definir_regras_padrao()
    
    def _definir_regras_padrao(self) -> List[Dict[str, Any]]:
        """Define regras padrão de alerta."""
        return [
            {"evento": TipoEvento.ANALISE_FALHOU, "prioridade": "alta"},
            {"evento": TipoEvento.RECURSO_LIBERADO, "prioridade": "baixa"},
            {"evento": TipoEvento.NOTIFICACAO_SISTEMA, "prioridade": "media"}
        ]
    
    def adicionar_regra_alerta(self, evento: TipoEvento, prioridade: str) -> None:
        """Adiciona regra de alerta."""
        self.regras_alerta.append({"evento": evento, "prioridade": prioridade})
    
    def atualizar(self, evento: Evento) -> None:
        """Recebe notificação e gera alerta se necessário."""
        prioridade = self._obter_prioridade(evento.tipo)
        
        if prioridade:
            alerta = {
                "timestamp": evento.timestamp,
                "evento": evento.tipo.value,
                "origem": evento.origem,
                "prioridade": prioridade,
                "dados": evento.dados,
                "mensagem": self._gerar_mensagem_alerta(evento, prioridade)
            }
            
            self.alertas.append(alerta)
            self._processar_alerta(alerta)
    
    def _obter_prioridade(self, tipo_evento: TipoEvento) -> Optional[str]:
        """Obtém prioridade do alerta baseada no tipo de evento."""
        for regra in self.regras_alerta:
            if regra["evento"] == tipo_evento:
                return regra["prioridade"]
        return None
    
    def _gerar_mensagem_alerta(self, evento: Evento, prioridade: str) -> str:
        """Gera mensagem de alerta."""
        if evento.tipo == TipoEvento.ANALISE_FALHOU:
            return f"ALERTA {prioridade.upper()}: Falha na análise em {evento.origem}"
        elif evento.tipo == TipoEvento.ANALISE_CONCLUIDA:
            return f"INFO: Análise concluída com sucesso em {evento.origem}"
        elif evento.tipo == TipoEvento.RECURSO_ALOCADO:
            return f"INFO: Recurso alocado em {evento.origem}"
        else:
            return f"{prioridade.upper()}: {evento.tipo.value} em {evento.origem}"
    
    def _processar_alerta(self, alerta: Dict[str, Any]) -> None:
        """Processa alerta gerado."""
        print(f"\n[SistemaAlerta {self.nome}] 🚨 ALERTA:")
        print(f"  Prioridade: {alerta['prioridade'].upper()}")
        print(f"  Mensagem: {alerta['mensagem']}")
        print(f"  Origem: {alerta['origem']}")
        
        # Ações específicas baseadas na prioridade
        if alerta['prioridade'] == 'alta':
            print("  📧 Enviando email de alerta crítico...")
            print("  📱 Enviando notificação push...")
        elif alerta['prioridade'] == 'media':
            print("  📧 Enviando email informativo...")
        else:
            print("  📝 Registrando no log...")
    
    def obter_nome(self) -> str:
        """Retorna nome do sistema de alerta."""
        return f"Alerta-{self.nome}"
    
    def obter_alertas_por_prioridade(self, prioridade: str) -> List[Dict[str, Any]]:
        """Retorna alertas por prioridade."""
        return [a for a in self.alertas if a['prioridade'] == prioridade]
    
    def obter_estatisticas_alertas(self) -> Dict[str, Any]:
        """Retorna estatísticas dos alertas."""
        if not self.alertas:
            return {"total": 0}
        
        contagem_prioridade = {}
        for alerta in self.alertas:
            prio = alerta['prioridade']
            contagem_prioridade[prio] = contagem_prioridade.get(prio, 0) + 1
        
        return {
            "total": len(self.alertas),
            "por_prioridade": contagem_prioridade,
            "ultimo_alerta": self.alertas[-1]['timestamp']
        }


class GerenciadorRelatorios(Observador):
    """Observador que gera relatórios automaticamente."""
    
    def __init__(self, nome: str, formato_padrao: str = "pdf"):
        self.nome = nome
        self.formato_padrao = formato_padrao
        self.relatorios_gerados: List[Dict[str, Any]] = []
        self.eventos_acumulados: List[Evento] = []
        self.limite_eventos_relatorio = 10
    
    def atualizar(self, evento: Evento) -> None:
        """Acumula eventos e gera relatórios quando necessário."""
        self.eventos_acumulados.append(evento)
        
        # Verifica se deve gerar relatório
        if self._deve_gerar_relatorio(evento):
            self._gerar_relatorio()
    
    def _deve_gerar_relatorio(self, evento: Evento) -> bool:
        """Verifica se deve gerar relatório baseado no evento."""
        # Gera relatório após análise concluída
        if evento.tipo == TipoEvento.ANALISE_CONCLUIDA:
            return True
        
        # Gera relatório se acumulou eventos suficientes
        if len(self.eventos_acumulados) >= self.limite_eventos_relatorio:
            return True
        
        return False
    
    def _gerar_relatorio(self) -> None:
        """Gera relatório dos eventos acumulados."""
        if not self.eventos_acumulados:
            return
        
        relatorio = {
            "id": f"REL_{len(self.relatorios_gerados) + 1:03d}",
            "timestamp": time.time(),
            "formato": self.formato_padrao,
            "eventos_incluidos": len(self.eventos_acumulados),
            "periodo": {
                "inicio": min(e.timestamp for e in self.eventos_acumulados),
                "fim": max(e.timestamp for e in self.eventos_acumulados)
            },
            "resumo": self._criar_resumo_eventos(),
            "arquivo": f"relatorio_{int(time.time())}.{self.formato_padrao}"
        }
        
        self.relatorios_gerados.append(relatorio)
        
        print(f"\n[GerenciadorRelatorios {self.nome}] 📊 RELATÓRIO GERADO:")
        print(f"  ID: {relatorio['id']}")
        print(f"  Formato: {relatorio['formato']}")
        print(f"  Eventos incluídos: {relatorio['eventos_incluidos']}")
        print(f"  Arquivo: {relatorio['arquivo']}")
        print(f"  Resumo: {relatorio['resumo']}")
        
        # Limpa eventos acumulados
        self.eventos_acumulados.clear()
    
    def _criar_resumo_eventos(self) -> str:
        """Cria resumo dos eventos acumulados."""
        if not self.eventos_acumulados:
            return "Nenhum evento"
        
        contagem_tipos = {}
        origens = set()
        
        for evento in self.eventos_acumulados:
            tipo = evento.tipo.value
            contagem_tipos[tipo] = contagem_tipos.get(tipo, 0) + 1
            origens.add(evento.origem)
        
        resumo = f"{len(self.eventos_acumulados)} eventos de {len(contagem_tipos)} tipos"
        if origens:
            resumo += f" em {len(origens)} origens"
        
        return resumo
    
    def obter_nome(self) -> str:
        """Retorna nome do gerenciador de relatórios."""
        return f"Relatorios-{self.nome}"
    
    def forcar_geracao_relatorio(self) -> None:
        """Força geração de relatório com eventos acumulados."""
        if self.eventos_acumulados:
            self._gerar_relatorio()
        else:
            print(f"[GerenciadorRelatorios {self.nome}] Nenhum evento acumulado para gerar relatório")


class AnaliseGenomica(Sujeito):
    """Sujeito que representa uma análise genômica."""
    
    def __init__(self, id_analise: str, descricao: str = ""):
        super().__init__()
        self.id_analise = id_analise
        self.descricao = descricao
        self.estado = "iniciada"
        self.resultado: Optional[Dict[str, Any]] = None
        self.erro: Optional[str] = None
    
    def iniciar_analise(self) -> None:
        """Inicia a análise."""
        self.estado = "em_andamento"
        self.notificar_observadores(
            Evento(
                TipoEvento.ANALISE_INICIADA,
                self.id_analise,
                {"descricao": self.descricao, "estado": self.estado}
            )
        )
    
    def concluir_analise(self, resultado: Dict[str, Any]) -> None:
        """Conclui a análise com sucesso."""
        self.estado = "concluida"
        self.resultado = resultado
        
        self.notificar_observadores(
            Evento(
                TipoEvento.ANALISE_CONCLUIDA,
                self.id_analise,
                {
                    "resultado": resultado,
                    "estado": self.estado,
                    "duracao": time.time() - self.historico_eventos[0].timestamp if self.historico_eventos else 0
                }
            )
        )
        
        # Notifica geração de resultado
        self.notificar_observadores(
            Evento(
                TipoEvento.RESULTADO_GERADO,
                self.id_analise,
                {
                    "tipo_analise": "genomica",
                    "resultado": resultado,
                    "formato": "vcf"
                }
            )
        )
    
    def falhar_analise(self, erro: str) -> None:
        """Falha a análise."""
        self.estado = "falha"
        self.erro = erro
        
        self.notificar_observadores(
            Evento(
                TipoEvento.ANALISE_FALHOU,
                self.id_analise,
                {
                    "erro": erro,
                    "estado": self.estado,
                    "duracao": time.time() - self.historico_eventos[0].timestamp if self.historico_eventos else 0
                }
            )
        )
    
    def alocar_recurso(self, recurso: str) -> None:
        """Aloca recurso para a análise."""
        self.notificar_observadores(
            Evento(
                TipoEvento.RECURSO_ALOCADO,
                self.id_analise,
                {"recurso": recurso, "estado": self.estado}
            )
        )
    
    def liberar_recurso(self, recurso: str) -> None:
        """Libera recurso da análise."""
        self.notificar_observadores(
            Evento(
                TipoEvento.RECURSO_LIBERADO,
                self.id_analise,
                {"recurso": recurso, "estado": self.estado}
            )
        )
    
    def obter_status(self) -> Dict[str, Any]:
        """Retorna status da análise."""
        return {
            "id_analise": self.id_analise,
            "descricao": self.descricao,
            "estado": self.estado,
            "resultado": self.resultado,
            "erro": self.erro,
            "observadores": len(self.observadores),
            "eventos": len(self.historico_eventos)
        }


class SistemaBioinformatica(Sujeito):
    """Sujeito principal que gerencia o sistema bioinformático."""
    
    def __init__(self):
        super().__init__()
        self.analises_ativas: Dict[str, AnaliseGenomica] = {}
        self.recursos_disponiveis: List[str] = ["sequenciador", "cluster", "workstation"]
    
    def criar_analise(self, id_analise: str, descricao: str = "") -> AnaliseGenomica:
        """Cria nova análise e adiciona observadores existentes."""
        analise = AnaliseGenomica(id_analise, descricao)
        
        # Adiciona observadores do sistema à nova análise
        for observador in self.observadores:
            analise.adicionar_observador(observador)
        
        self.analises_ativas[id_analise] = analise
        
        # Notifica criação da análise
        self.notificar_observadores(
            Evento(
                TipoEvento.NOTIFICACAO_SISTEMA,
                "SistemaBioinformatica",
                {"mensagem": f"Análise {id_analise} criada", "tipo": "criacao_analise"}
            )
        )
        
        return analise
    
    def executar_analise_completa(self, id_analise: str) -> None:
        """Executa ciclo completo de análise."""
        if id_analise not in self.analises_ativas:
            print(f"Análise {id_analise} não encontrada")
            return
        
        analise = self.analises_ativas[id_analise]
        
        try:
            # Inicia análise
            analise.iniciar_analise()
            time.sleep(0.5)
            
            # Aloca recursos
            analise.alocar_recurso("sequenciador")
            time.sleep(0.5)
            analise.alocar_recurso("cluster")
            time.sleep(0.5)
            
            # Simula processamento
            print(f"Processando análise {id_analise}...")
            time.sleep(1)
            
            # Libera recursos
            analise.liberar_recurso("cluster")
            time.sleep(0.5)
            analise.liberar_recurso("sequenciador")
            time.sleep(0.5)
            
            # Conclui com sucesso
            resultado = {
                "variantes_encontradas": 4500,
                "genes_regulados": 1200,
                "qualidade": "alta",
                "arquivo_saida": f"resultado_{id_analise}.vcf"
            }
            analise.concluir_analise(resultado)
            
        except Exception as e:
            # Falha na análise
            analise.falhar_analise(f"Erro durante processamento: {str(e)}")
    
    def obter_status_sistema(self) -> Dict[str, Any]:
        """Retorna status completo do sistema."""
        return {
            "analises_ativas": len(self.analises_ativas),
            "observadores_globais": len(self.observadores),
            "eventos_sistema": len(self.historico_eventos),
            "recursos_disponiveis": self.recursos_disponiveis.copy(),
            "analises": {id_analise: analise.obter_status() 
                        for id_analise, analise in self.analises_ativas.items()}
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Configuração do Sistema Observer ===")
    
    # Criar sistema principal
    sistema = SistemaBioinformatica()
    
    # Criar observadores
    pesquisador1 = Pesquisador("Dr. Silva", "silva@lab.com", "genomica")
    pesquisador2 = Pesquisador("Dra. Santos", "santos@lab.com", "proteomica")
    
    sistema_alerta = SistemaAlerta("Principal", "alto")
    gerenciador_relatorios = GerenciadorRelatorios("Auto", "pdf")
    
    # Definir interesses dos pesquisadores
    pesquisador1.definir_interesses([
        TipoEvento.ANALISE_CONCLUIDA,
        TipoEvento.ANALISE_FALHOU,
        TipoEvento.RESULTADO_GERADO
    ])
    
    pesquisador2.definir_interesses([
        TipoEvento.ANALISE_CONCLUIDA,
        TipoEvento.RECURSO_LIBERADO
    ])
    
    # Adicionar observadores ao sistema
    sistema.adicionar_observador(pesquisador1)
    sistema.adicionar_observador(pesquisador2)
    sistema.adicionar_observador(sistema_alerta)
    sistema.adicionar_observador(gerenciador_relatorios)
    
    print(f"Sistema configurado com {len(sistema.observadores)} observadores")
    
    print("\n=== Exemplo 2: Análise Individual com Notificações ===")
    
    # Criar e executar análise
    analise1 = sistema.criar_analise("ANALISE_001", "Análise de variação genética")
    sistema.executar_analise_completa("ANALISE_001")
    
    # Verificar notificações dos pesquisadores
    print(f"\nNotificações recebidas pelo Dr. Silva: {len(pesquisador1.notificacoes_recebidas)}")
    resumo1 = pesquisador1.obter_resumo_notificacoes()
    print(f"Resumo: {resumo1}")
    
    print(f"\nNotificações recebidas pela Dra. Santos: {len(pesquisador2.notificacoes_recebidas)}")
    resumo2 = pesquisador2.obter_resumo_notificacoes()
    print(f"Resumo: {resumo2}")
    
    print("\n=== Exemplo 3: Múltiplas Análises Simultâneas ===")
    
    # Criar múltiplas análises
    analise2 = sistema.criar_analise("ANALISE_002", "Análise de expressão gênica")
    analise3 = sistema.criar_analise("ANALISE_003", "Análise proteômica")
    
    # Executar análises
    sistema.executar_analise_completa("ANALISE_002")
    sistema.executar_analise_completa("ANALISE_003")
    
    # Forçar geração de relatório
    gerenciador_relatorios.forcar_geracao_relatorio()
    
    print("\n=== Exemplo 4: Análise com Falha ===")
    
    # Criar análise que vai falhar
    analise_falha = sistema.criar_analise("ANALISE_FALHA", "Análise com erro simulado")
    
    # Simular falha manualmente
    analise_falha.iniciar_analise()
    time.sleep(0.5)
    analise_falha.falhar_analise("Erro de conexão com banco de dados")
    
    print("\n=== Exemplo 5: Estatísticas dos Observadores ===")
    
    # Estatísticas do sistema de alerta
    stats_alerta = sistema_alerta.obter_estatisticas_alertas()
    print(f"\nEstatísticas do Sistema de Alerta:")
    print(f"  Total de alertas: {stats_alerta['total']}")
    print(f"  Por prioridade: {stats_alerta['por_prioridade']}")
    
    # Alertas de alta prioridade
    alertas_altas = sistema_alerta.obter_alertas_por_prioridade("alta")
    print(f"  Alertas de alta prioridade: {len(alertas_altas)}")
    
    # Estatísticas do gerenciador de relatórios
    print(f"\nRelatórios gerados: {len(gerenciador_relatorios.relatorios_gerados)}")
    for relatorio in gerenciador_relatorios.relatorios_gerados:
        print(f"  {relatorio['id']}: {relatorio['resumo']} ({relatorio['arquivo']})")
    
    print("\n=== Exemplo 6: Remoção de Observadores ===")
    
    # Remover um observador
    print(f"\nRemovendo {pesquisador2.obter_nome()} do sistema...")
    sistema.remover_observador(pesquisador2)
    
    # Criar nova análise
    analise4 = sistema.criar_analise("ANALISE_004", "Análise sem notificação para Dra. Santos")
    sistema.executar_analise_completa("ANALISE_004")
    
    # Verificar notificações
    print(f"\nNotificações Dra. Santos após remoção: {len(pesquisador2.notificacoes_recebidas)}")
    print(f"Notificações Dr. Silva após nova análise: {len(pesquisador1.notificacoes_recebidas)}")
    
    print("\n=== Exemplo 7: Status Completo do Sistema ===")
    
    status_sistema = sistema.obter_status_sistema()
    print(f"\nStatus do Sistema Bioinformático:")
    print(f"  Análises ativas: {status_sistema['analises_ativas']}")
    print(f"  Observadores globais: {status_sistema['observadores_globais']}")
    print(f"  Eventos do sistema: {status_sistema['eventos_sistema']}")
    
    print(f"\nDetalhes das análises:")
    for id_analise, status in status_sistema['analises'].items():
        print(f"  {id_analise}: {status['estado']} - {status['observadores']} observadores")
    
    print("\n=== Exemplo 8: Histórico de Eventos ===")
    
    # Histórico de eventos do sistema
    eventos_sistema = sistema.obter_historico_eventos()
    print(f"\nÚltimos 5 eventos do sistema:")
    for evento in eventos_sistema[-5:]:
        print(f"  {evento}")
    
    # Histórico de eventos de uma análise específica
    eventos_analise = analise1.obter_historico_eventos()
    print(f"\nEventos da ANALISE_001 ({len(eventos_analise)}):")
    for evento in eventos_analise:
        print(f"  {evento}")
    
    print("\nObserver pattern implementado com sucesso!")
