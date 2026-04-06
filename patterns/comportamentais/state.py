from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
from enum import Enum


class StatusEquipamento(Enum):
    DISPONIVEL = "disponivel"
    EM_USO = "em_uso"
    MANUTENCAO = "manutencao"
    CALIBRACAO = "calibracao"
    DESLIGADO = "desligado"
    ERRO = "erro"


class EstadoEquipamento(ABC):
    """Classe base para estados de equipamento."""
    
    def __init__(self, nome: str):
        self.nome = nome
    
    @abstractmethod
    def ligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        """Liga o equipamento."""
        pass
    
    @abstractmethod
    def desligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        """Desliga o equipamento."""
        pass
    
    @abstractmethod
    def iniciar_uso(self, equipamento: 'EquipamentoLaboratorial', usuario: str) -> str:
        """Inicia uso do equipamento."""
        pass
    
    @abstractmethod
    def finalizar_uso(self, equipamento: 'EquipamentoLaboratorial') -> str:
        """Finaliza uso do equipamento."""
        pass
    
    @abstractmethod
    def iniciar_manutencao(self, equipamento: 'EquipamentoLaboratorial', tecnico: str) -> str:
        """Inicia manutenção do equipamento."""
        pass
    
    @abstractmethod
    def finalizar_manutencao(self, equipamento: 'EquipamentoLaboratorial') -> str:
        """Finaliza manutenção do equipamento."""
        pass
    
    @abstractmethod
    def calibrar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        """Calibra o equipamento."""
        pass
    
    @abstractmethod
    def verificar_status(self, equipamento: 'EquipamentoLaboratorial') -> Dict[str, Any]:
        """Verifica status atual do equipamento."""
        pass
    
    def __str__(self) -> str:
        return f"Estado({self.nome})"


class EstadoDisponivel(EstadoEquipamento):
    """Estado quando o equipamento está disponível para uso."""
    
    def __init__(self):
        super().__init__("Disponível")
    
    def ligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} já está ligado e disponível"
    
    def desligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        equipamento.mudar_estado(EstadoDesligado())
        return f"Equipamento {equipamento.nome} desligado"
    
    def iniciar_uso(self, equipamento: 'EquipamentoLaboratorial', usuario: str) -> str:
        equipamento.usuario_atual = usuario
        equipamento.hora_inicio_uso = time.time()
        equipamento.mudar_estado(EstadoEmUso())
        return f"Equipamento {equipamento.nome} agora em uso por {usuario}"
    
    def finalizar_uso(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em uso"
    
    def iniciar_manutencao(self, equipamento: 'EquipamentoLaboratorial', tecnico: str) -> str:
        equipamento.tecnico_manutencao = tecnico
        equipamento.mudar_estado(EstadoManutencao())
        return f"Equipamento {equipamento.nome} em manutenção com {tecnico}"
    
    def finalizar_manutencao(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em manutenção"
    
    def calibrar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        equipamento.mudar_estado(EstadoCalibracao())
        return f"Equipamento {equipamento.nome} iniciando calibração"
    
    def verificar_status(self, equipamento: 'EquipamentoLaboratorial') -> Dict[str, Any]:
        return {
            "status": StatusEquipamento.DISPONIVEL.value,
            "usuario_atual": None,
            "disponivel_para_uso": True,
            "mensagem": "Equipamento disponível para uso"
        }


class EstadoEmUso(EstadoEquipamento):
    """Estado quando o equipamento está em uso."""
    
    def __init__(self):
        super().__init__("Em Uso")
    
    def ligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} já está ligado e em uso por {equipamento.usuario_atual}"
    
    def desligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Não é possível desligar {equipamento.nome} enquanto está em uso"
    
    def iniciar_uso(self, equipamento: 'EquipamentoLaboratorial', usuario: str) -> str:
        return f"Equipamento {equipamento.nome} já está em uso por {equipamento.usuario_atual}"
    
    def finalizar_uso(self, equipamento: 'EquipamentoLaboratorial') -> str:
        tempo_uso = time.time() - equipamento.hora_inicio_uso
        equipamento.usuario_atual = None
        equipamento.hora_inicio_uso = None
        equipamento.tempo_total_uso += tempo_uso
        equipamento.mudar_estado(EstadoDisponivel())
        return f"Equipamento {equipamento.nome} liberado após {tempo_uso:.1f} segundos de uso"
    
    def iniciar_manutencao(self, equipamento: 'EquipamentoLaboratorial', tecnico: str) -> str:
        return f"Não é possível iniciar manutenção enquanto {equipamento.nome} está em uso"
    
    def finalizar_manutencao(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em manutenção"
    
    def calibrar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Não é possível calibrar {equipamento.nome} enquanto está em uso"
    
    def verificar_status(self, equipamento: 'EquipamentoLaboratorial') -> Dict[str, Any]:
        tempo_uso_atual = time.time() - equipamento.hora_inicio_uso if equipamento.hora_inicio_uso else 0
        return {
            "status": StatusEquipamento.EM_USO.value,
            "usuario_atual": equipamento.usuario_atual,
            "tempo_uso_atual": tempo_uso_atual,
            "disponivel_para_uso": False,
            "mensagem": f"Equipamento em uso por {equipamento.usuario_atual}"
        }


class EstadoManutencao(EstadoEquipamento):
    """Estado quando o equipamento está em manutenção."""
    
    def __init__(self):
        super().__init__("Manutenção")
    
    def ligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não pode ser ligado durante manutenção"
    
    def desligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} já está desligado para manutenção"
    
    def iniciar_uso(self, equipamento: 'EquipamentoLaboratorial', usuario: str) -> str:
        return f"Equipamento {equipamento.nome} não está disponível para uso (em manutenção)"
    
    def finalizar_uso(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em uso"
    
    def iniciar_manutencao(self, equipamento: 'EquipamentoLaboratorial', tecnico: str) -> str:
        return f"Equipamento {equipamento.nome} já está em manutenção com {equipamento.tecnico_manutencao}"
    
    def finalizar_manutencao(self, equipamento: 'EquipamentoLaboratorial') -> str:
        equipamento.tecnico_manutencao = None
        equipamento.mudar_estado(EstadoDisponivel())
        return f"Equipamento {equipamento.nome} manutenção concluída, agora disponível"
    
    def calibrar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não pode ser calibrado durante manutenção"
    
    def verificar_status(self, equipamento: 'EquipamentoLaboratorial') -> Dict[str, Any]:
        return {
            "status": StatusEquipamento.MANUTENCAO.value,
            "tecnico_manutencao": equipamento.tecnico_manutencao,
            "disponivel_para_uso": False,
            "mensagem": f"Equipamento em manutenção com {equipamento.tecnico_manutencao}"
        }


class EstadoCalibracao(EstadoEquipamento):
    """Estado quando o equipamento está em calibração."""
    
    def __init__(self):
        super().__init__("Calibração")
        self.inicio_calibracao = None
    
    def ligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} já está ligado para calibração"
    
    def desligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Não é possível desligar {equipamento.nome} durante calibração"
    
    def iniciar_uso(self, equipamento: 'EquipamentoLaboratorial', usuario: str) -> str:
        return f"Equipamento {equipamento.nome} não está disponível (em calibração)"
    
    def finalizar_uso(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em uso"
    
    def iniciar_manutencao(self, equipamento: 'EquipamentoLaboratorial', tecnico: str) -> str:
        return f"Não é possível iniciar manutenção durante calibração"
    
    def finalizar_manutencao(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em manutenção"
    
    def calibrar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        if not self.inicio_calibracao:
            self.inicio_calibracao = time.time()
            return f"Calibração de {equipamento.nome} iniciada"
        else:
            tempo_calibracao = time.time() - self.inicio_calibracao
            equipamento.ultima_calibracao = time.time()
            equipamento.mudar_estado(EstadoDisponivel())
            return f"Calibração de {equipamento.nome} concluída em {tempo_calibracao:.1f} segundos"
    
    def verificar_status(self, equipamento: 'EquipamentoLaboratorial') -> Dict[str, Any]:
        tempo_calibracao = time.time() - self.inicio_calibracao if self.inicio_calibracao else 0
        return {
            "status": StatusEquipamento.CALIBRACAO.value,
            "tempo_calibracao": tempo_calibracao,
            "disponivel_para_uso": False,
            "mensagem": f"Equipamento em calibração ({tempo_calibracao:.1f}s)"
        }


class EstadoDesligado(EstadoEquipamento):
    """Estado quando o equipamento está desligado."""
    
    def __init__(self):
        super().__init__("Desligado")
    
    def ligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        # Verifica se precisa de calibração
        if equipamento.precisa_calibracao():
            equipamento.mudar_estado(EstadoCalibracao())
            return f"Equipamento {equipamento.nome} ligado, iniciando calibração necessária"
        else:
            equipamento.mudar_estado(EstadoDisponivel())
            return f"Equipamento {equipamento.nome} ligado e disponível"
    
    def desligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} já está desligado"
    
    def iniciar_uso(self, equipamento: 'EquipamentoLaboratorial', usuario: str) -> str:
        return f"Equipamento {equipamento.nome} está desligado, não é possível iniciar uso"
    
    def finalizar_uso(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em uso"
    
    def iniciar_manutencao(self, equipamento: 'EquipamentoLaboratorial', tecnico: str) -> str:
        equipamento.tecnico_manutencao = tecnico
        equipamento.mudar_estado(EstadoManutencao())
        return f"Equipamento {equipamento.nome} em manutenção (iniciado desligado)"
    
    def finalizar_manutencao(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em manutenção"
    
    def calibrar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} está desligado, não é possível calibrar"
    
    def verificar_status(self, equipamento: 'EquipamentoLaboratorial') -> Dict[str, Any]:
        return {
            "status": StatusEquipamento.DESLIGADO.value,
            "disponivel_para_uso": False,
            "mensagem": "Equipamento desligado"
        }


class EstadoErro(EstadoEquipamento):
    """Estado quando o equipamento está em erro."""
    
    def __init__(self, mensagem_erro: str = "Erro desconhecido"):
        super().__init__("Erro")
        self.mensagem_erro = mensagem_erro
        self.hora_erro = time.time()
    
    def ligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não pode ser ligado: {self.mensagem_erro}"
    
    def desligar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        equipamento.mudar_estado(EstadoDesligado())
        return f"Equipamento {equipamento.nome} desligado para correção do erro"
    
    def iniciar_uso(self, equipamento: 'EquipamentoLaboratorial', usuario: str) -> str:
        return f"Equipamento {equipamento.nome} não disponível: {self.mensagem_erro}"
    
    def finalizar_uso(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em uso"
    
    def iniciar_manutencao(self, equipamento: 'EquipamentoLaboratorial', tecnico: str) -> str:
        equipamento.tecnico_manutencao = tecnico
        equipamento.mudar_estado(EstadoManutencao())
        return f"Equipamento {equipamento.nome} em manutenção para correção: {self.mensagem_erro}"
    
    def finalizar_manutencao(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não está em manutenção"
    
    def calibrar(self, equipamento: 'EquipamentoLaboratorial') -> str:
        return f"Equipamento {equipamento.nome} não pode ser calibrado: {self.mensagem_erro}"
    
    def verificar_status(self, equipamento: 'EquipamentoLaboratorial') -> Dict[str, Any]:
        tempo_erro = time.time() - self.hora_erro
        return {
            "status": StatusEquipamento.ERRO.value,
            "mensagem_erro": self.mensagem_erro,
            "tempo_erro": tempo_erro,
            "disponivel_para_uso": False,
            "mensagem": f"Equipamento em erro: {self.mensagem_erro}"
        }


class EquipamentoLaboratorial:
    """Contexto que representa um equipamento laboratorial."""
    
    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.tipo = tipo
        self.estado: EstadoEquipamento = EstadoDesligado()
        self.usuario_atual: Optional[str] = None
        self.tecnico_manutencao: Optional[str] = None
        self.hora_inicio_uso: Optional[float] = None
        self.tempo_total_uso: float = 0.0
        self.ultima_calibracao: Optional[float] = None
        self.intervalo_calibracao: float = 86400  # 24 horas em segundos
        self.historico_estados: List[Dict[str, Any]] = []
        self.registrar_mudanca_estado()
    
    def mudar_estado(self, novo_estado: EstadoEquipamento) -> None:
        """Muda o estado do equipamento."""
        estado_anterior = self.estado.nome
        self.estado = novo_estado
        self.registrar_mudanca_estado()
        print(f"[{self.nome}] Estado mudou: {estado_anterior} -> {novo_estado.nome}")
    
    def registrar_mudanca_estado(self) -> None:
        """Registra mudança de estado no histórico."""
        self.historico_estados.append({
            "estado": self.estado.nome,
            "timestamp": time.time(),
            "usuario": self.usuario_atual,
            "tecnico": self.tecnico_manutencao
        })
        
        # Mantém apenas últimas 50 mudanças
        if len(self.historico_estados) > 50:
            self.historico_estados = self.historico_estados[-50:]
    
    def ligar(self) -> str:
        """Liga o equipamento."""
        resultado = self.estado.ligar(self)
        print(f"[{self.nome}] {resultado}")
        return resultado
    
    def desligar(self) -> str:
        """Desliga o equipamento."""
        resultado = self.estado.desligar(self)
        print(f"[{self.nome}] {resultado}")
        return resultado
    
    def iniciar_uso(self, usuario: str) -> str:
        """Inicia uso do equipamento."""
        resultado = self.estado.iniciar_uso(self, usuario)
        print(f"[{self.nome}] {resultado}")
        return resultado
    
    def finalizar_uso(self) -> str:
        """Finaliza uso do equipamento."""
        resultado = self.estado.finalizar_uso(self)
        print(f"[{self.nome}] {resultado}")
        return resultado
    
    def iniciar_manutencao(self, tecnico: str) -> str:
        """Inicia manutenção do equipamento."""
        resultado = self.estado.iniciar_manutencao(self, tecnico)
        print(f"[{self.nome}] {resultado}")
        return resultado
    
    def finalizar_manutencao(self) -> str:
        """Finaliza manutenção do equipamento."""
        resultado = self.estado.finalizar_manutencao(self)
        print(f"[{self.nome}] {resultado}")
        return resultado
    
    def calibrar(self) -> str:
        """Calibra o equipamento."""
        resultado = self.estado.calibrar(self)
        print(f"[{self.nome}] {resultado}")
        return resultado
    
    def verificar_status(self) -> Dict[str, Any]:
        """Verifica status atual do equipamento."""
        status = self.estado.verificar_status(self)
        status.update({
            "nome": self.nome,
            "tipo": self.tipo,
            "estado_atual": self.estado.nome,
            "tempo_total_uso": self.tempo_total_uso,
            "ultima_calibracao": self.ultima_calibracao,
            "precisa_calibrar": self.precisa_calibracao()
        })
        return status
    
    def precisa_calibracao(self) -> bool:
        """Verifica se equipamento precisa de calibração."""
        if not self.ultima_calibracao:
            return True
        return (time.time() - self.ultima_calibracao) > self.intervalo_calibracao
    
    def simular_erro(self, mensagem_erro: str) -> None:
        """Simula ocorrência de erro no equipamento."""
        self.mudar_estado(EstadoErro(mensagem_erro))
    
    def obter_historico_estados(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Retorna histórico de mudanças de estado."""
        return self.historico_estados[-limite:]
    
    def obter_estatisticas_uso(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso do equipamento."""
        total_mudancas = len(self.historico_estados)
        tempo_por_estado = {}
        
        # Calcula tempo gasto em cada estado
        for i in range(len(self.historico_estados) - 1):
            estado_atual = self.historico_estados[i]["estado"]
            proximo_timestamp = self.historico_estados[i + 1]["timestamp"]
            timestamp_atual = self.historico_estados[i]["timestamp"]
            
            duracao = proximo_timestamp - timestamp_atual
            tempo_por_estado[estado_atual] = tempo_por_estado.get(estado_atual, 0) + duracao
        
        # Adiciona tempo do estado atual
        if self.historico_estados:
            estado_atual = self.historico_estados[-1]["estado"]
            duracao_atual = time.time() - self.historico_estados[-1]["timestamp"]
            tempo_por_estado[estado_atual] = tempo_por_estado.get(estado_atual, 0) + duracao_atual
        
        return {
            "total_mudancas_estado": total_mudancas,
            "tempo_total_uso": self.tempo_total_uso,
            "tempo_por_estado": tempo_por_estado,
            "estado_atual": self.estado.nome,
            "ultima_calibracao": self.ultima_calibracao
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Ciclo de Vida do Equipamento ===")
    
    # Criar equipamento
    microscopio = EquipamentoLaboratorial("Microscopio_001", "Microscópio Eletrônico")
    
    print("Status inicial:")
    status = microscopio.verificar_status()
    print(f"  Estado: {status['estado_atual']}")
    print(f"  Disponível: {status['disponivel_para_uso']}")
    
    # Ligar equipamento
    print("\n1. Ligando equipamento:")
    microscopio.ligar()
    
    # Iniciar uso
    print("\n2. Iniciando uso:")
    microscopio.iniciar_uso("Dr. Silva")
    
    # Tentar usar por outro usuário
    print("\n3. Tentando uso por outro usuário:")
    microscopio.iniciar_uso("Dra. Santos")
    
    # Finalizar uso
    print("\n4. Finalizando uso:")
    microscopio.finalizar_uso()
    
    # Iniciar manutenção
    print("\n5. Iniciando manutenção:")
    microscopio.iniciar_manutencao("Técnico João")
    
    # Tentar usar durante manutenção
    print("\n6. Tentando uso durante manutenção:")
    microscopio.iniciar_uso("Dr. Silva")
    
    # Finalizar manutenção
    print("\n7. Finalizando manutenção:")
    microscopio.finalizar_manutencao()
    
    # Calibrar equipamento
    print("\n8. Calibrando equipamento:")
    microscopio.calibrar()
    microscopio.calibrar()  # Concluir calibração
    
    print("\n=== Exemplo 2: Múltiplos Usuários e Ciclos ===")
    
    # Criar centrífuga
    centrifuga = EquipamentoLaboratorial("Centrífuga_001", "Centrífuga de Alta Velocidade")
    
    # Ligar e usar por múltiplos usuários
    centrifuga.ligar()
    
    usuarios = ["Ana", "Bruno", "Carla", "Daniel"]
    for usuario in usuarios:
        print(f"\nUsuário {usuario} usando a centrífuga:")
        centrifuga.iniciar_uso(usuario)
        time.sleep(0.5)  # Simula tempo de uso
        centrifuga.finalizar_uso()
    
    # Verificar estatísticas
    stats = centrifuga.obter_estatisticas_uso()
    print(f"\nEstatísticas da centrífuga:")
    print(f"  Tempo total de uso: {stats['tempo_total_uso']:.1f} segundos")
    print(f"  Mudanças de estado: {stats['total_mudancas_estado']}")
    print(f"  Tempo por estado:")
    for estado, tempo in stats['tempo_por_estado'].items():
        print(f"    {estado}: {tempo:.1f}s")
    
    print("\n=== Exemplo 3: Tratamento de Erros ===")
    
    # Criar termociclador
    termociclador = EquipamentoLaboratorial("PCR_001", "Termociclador")
    
    termociclador.ligar()
    termociclador.iniciar_uso("Dr. Oliveira")
    
    # Simular erro
    print("\nSimulando erro no equipamento:")
    termociclador.simular_erro("Falha no sensor de temperatura")
    
    # Tentar operações em estado de erro
    print("\nTentando operações em estado de erro:")
    termociclador.iniciar_uso("Dra. Costa")
    termociclador.calibrar()
    
    # Iniciar manutenção para corrigir erro
    print("\nIniciando manutenção para corrigir erro:")
    termociclador.iniciar_manutencao("Técnico Pedro")
    
    # Finalizar manutenção
    print("\nFinalizando manutenção:")
    termociclador.finalizar_manutencao()
    
    # Verificar status final
    status_final = termociclador.verificar_status()
    print(f"\nStatus final: {status_final['estado_atual']}")
    
    print("\n=== Exemplo 4: Histórico de Estados ===")
    
    # Obter histórico de estados
    historico = microscopio.obter_historico_estados(5)
    print(f"\nHistórico recente do microscópio:")
    for i, mudanca in enumerate(historico, 1):
        timestamp = time.strftime('%H:%M:%S', time.localtime(mudanca['timestamp']))
        print(f"  {i}. [{timestamp}] {mudanca['estado']} (usuário: {mudanca['usuario'] or 'N/A'})")
    
    print("\n=== Exemplo 5: Calibração Automática ===")
    
    # Criar espectrofotômetro que precisa de calibração
    espectrofotometro = EquipamentoLaboratorial("ESPECTRO_001", "Espectrofotômetro")
    espectrofotometro.intervalo_calibracao = 10  # 10 segundos para teste
    
    espectrofotometro.ligar()
    print(f"\nPrecisa calibrar: {espectrofotometro.precisa_calibracao()}")
    
    # Tentar usar sem calibrar
    espectrofotometro.iniciar_uso("Dr. Mendes")
    espectrofotometro.finalizar_uso()
    
    # Esperar e tentar usar novamente (vai precisar calibrar)
    time.sleep(11)
    print(f"\nApós espera, precisa calibrar: {espectrofotometro.precisa_calibracao()}")
    
    espectrofotometro.iniciar_uso("Dra. Lima")
    espectrofotometro.finalizar_uso()
    
    print("\n=== Exemplo 6: Sistema de Múltiplos Equipamentos ===")
    
    # Criar múltiplos equipamentos
    equipamentos = [
        EquipamentoLaboratorial("SEQ_001", "Sequenciador"),
        EquipamentoLaboratorial("ALIN_001", "Alinhador"),
        EquipamentoLaboratorial("ANA_001", "Analisador")
    ]
    
    # Inicializar todos os equipamentos
    print("\nInicializando todos os equipamentos:")
    for equip in equipamentos:
        equip.ligar()
        time.sleep(0.2)
    
    # Usar equipamentos simultaneamente
    print("\nIniciando uso simultâneo:")
    for i, equip in enumerate(equipamentos):
        usuario = f"Pesquisador_{i+1}"
        equip.iniciar_uso(usuario)
    
    time.sleep(1)
    
    # Finalizar usos
    print("\nFinalizando usos:")
    for equip in equipamentos:
        equip.finalizar_uso()
    
    # Calibrar todos
    print("\nCalibrando todos os equipamentos:")
    for equip in equipamentos:
        equip.calibrar()
        time.sleep(0.3)
        equip.calibrar()  # Concluir calibração
    
    # Status final de todos
    print("\nStatus final dos equipamentos:")
    for equip in equipamentos:
        status = equip.verificar_status()
        print(f"  {equip.nome}: {status['estado_atual']} - Tempo uso: {status['tempo_total_uso']:.1f}s")
    
    print("\nState pattern implementado com sucesso!")
