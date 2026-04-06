import threading
from typing import Dict, Any, Optional
from domain.amostra_biologica import EquipamentoLaboratorial


class GerenciadorRecursos:
    """Gerenciador único de recursos laboratoriais - Padrão Singleton."""
    
    _instancia: Optional['GerenciadorRecursos'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'GerenciadorRecursos':
        """Garante que apenas uma instância seja criada."""
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super().__new__(cls)
                    cls._instancia._inicializado = False
        return cls._instancia
    
    def __init__(self):
        """Inicializa o gerenciador apenas uma vez."""
        if not self._inicializado:
            self.recursos: Dict[str, EquipamentoLaboratorial] = {}
            self.recursos_em_uso: Dict[str, str] = {}
            self.historico_uso: list = []
            self._inicializado = True
    
    @classmethod
    def get_instancia(cls) -> 'GerenciadorRecursos':
        """Método estático para obter a instância única."""
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia
    
    def adicionar_recurso(self, nome: str, equipamento: EquipamentoLaboratorial) -> None:
        """Adiciona um recurso laboratorial ao gerenciador."""
        self.recursos[nome] = equipamento
    
    def obter_recurso(self, nome: str, pesquisador: str = "") -> Optional[EquipamentoLaboratorial]:
        """Obtém um recurso laboratorial para uso."""
        if nome not in self.recursos:
            raise ValueError(f"Recurso '{nome}' não encontrado")
        
        recurso = self.recursos[nome]
        
        if recurso.disponivel:
            recurso.reservar(pesquisador)
            self.recursos_em_uso[nome] = pesquisador
            self.historico_uso.append(f"{nome} reservado por {pesquisador}")
            return recurso
        else:
            print(f"Recurso '{nome}' está em uso por {self.recursos_em_uso.get(nome, 'desconhecido')}")
            return None
    
    def liberar_recurso(self, nome: str) -> None:
        """Libera um recurso laboratorial."""
        if nome in self.recursos:
            recurso = self.recursos[nome]
            recurso.liberar()
            if nome in self.recursos_em_uso:
                pesquisador = self.recursos_em_uso[nome]
                del self.recursos_em_uso[nome]
                self.historico_uso.append(f"{nome} liberado por {pesquisador}")
    
    def listar_recursos_disponiveis(self) -> Dict[str, str]:
        """Lista todos os recursos disponíveis."""
        disponiveis = {}
        for nome, recurso in self.recursos.items():
            if recurso.disponivel:
                disponiveis[nome] = recurso.tipo
        return disponiveis
    
    def listar_recursos_em_uso(self) -> Dict[str, str]:
        """Lista todos os recursos em uso."""
        return self.recursos_em_uso.copy()
    
    def obter_historico_uso(self) -> list:
        """Retorna o histórico de uso dos recursos."""
        return self.historico_uso.copy()
    
    def limpar_historico(self) -> None:
        """Limpa o histórico de uso."""
        self.historico_uso.clear()
    
    def __str__(self) -> str:
        return f"GerenciadorRecursos(total_recursos={len(self.recursos)}, em_uso={len(self.recursos_em_uso)})"


class BancoDadosSequencias:
    """Banco de dados de sequências genéticas - Singleton thread-safe."""
    
    _instancia: Optional['BancoDadosSequencias'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'BancoDadosSequencias':
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super().__new__(cls)
                    cls._instancia._inicializado = False
        return cls._instancia
    
    def __init__(self):
        if not self._inicializado:
            self.sequencias: Dict[str, str] = {}
            self.metadados: Dict[str, Dict[str, Any]] = {}
            self.acessos: int = 0
            self._inicializado = True
    
    @classmethod
    def get_instancia(cls) -> 'BancoDadosSequencias':
        """Obtém a instância única do banco de dados."""
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia
    
    def adicionar_sequencia(self, id_sequencia: str, sequencia: str, **metadados) -> None:
        """Adiciona uma sequência ao banco."""
        self.sequencias[id_sequencia] = sequencia
        self.metadados[id_sequencia] = metadados
    
    def buscar_sequencia(self, id_sequencia: str) -> Optional[str]:
        """Busca uma sequência por ID."""
        self.acessos += 1
        return self.sequencias.get(id_sequencia)
    
    def buscar_sequencia_por_padrao(self, padrao: str) -> Dict[str, str]:
        """Busca sequências que contêm um padrão específico."""
        self.acessos += 1
        resultados = {}
        for id_seq, sequencia in self.sequencias.items():
            if padrao in sequencia:
                resultados[id_seq] = sequencia
        return resultados
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas do banco de dados."""
        return {
            "total_sequencias": len(self.sequencias),
            "total_acessos": self.acessos,
            "tamanho_total": sum(len(seq) for seq in self.sequencias.values())
        }
    
    def __str__(self) -> str:
        return f"BancoDadosSequencias(sequencias={len(self.sequencias)}, acessos={self.acessos})"


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Gerenciador de Recursos ===")
    
    # Obter a instância única
    gerenciador1 = GerenciadorRecursos.get_instancia()
    gerenciador2 = GerenciadorRecursos.get_instancia()
    
    print(f"Mesma instância? {gerenciador1 is gerenciador2}")
    
    # Adicionar recursos
    gerenciador1.adicionar_recurso("Microscopio_1", EquipamentoLaboratorial("Microscopio_1", "Microscópio"))
    gerenciador1.adicionar_recurso("Centrifuga_1", EquipamentoLaboratorial("Centrifuga_1", "Centrífuga"))
    gerenciador1.adicionar_recurso("PCR_1", EquipamentoLaboratorial("PCR_1", "Termociclador"))
    
    print(f"Gerenciador 1: {gerenciador1}")
    print(f"Gerenciador 2: {gerenciador2}")
    
    # Usar recursos
    print("\nRecursos disponíveis:", gerenciador2.listar_recursos_disponiveis())
    
    microscopio = gerenciador1.obter_recurso("Microscopio_1", "Dr. Silva")
    if microscopio:
        print(f"Recurso obtido: {microscopio}")
    
    print("Recursos em uso:", gerenciador2.listar_recursos_em_uso())
    
    # Liberar recurso
    gerenciador1.liberar_recurso("Microscopio_1")
    print("Após liberação:", gerenciador2.listar_recursos_em_uso())
    
    print("\n=== Exemplo 2: Banco de Dados de Sequências ===")
    
    # Obter instância do banco
    banco1 = BancoDadosSequencias.get_instancia()
    banco2 = BancoDadosSequencias.get_instancia()
    
    print(f"Mesma instância do banco? {banco1 is banco2}")
    
    # Adicionar sequências
    banco1.adicionar_sequencia("SEQ001", "ATCGATCGATCG", especie="Homo sapiens", gene="BRCA1")
    banco1.adicionar_sequencia("SEQ002", "GCTAGCTAGCTA", especie="Homo sapiens", gene="TP53")
    banco1.adicionar_sequencia("SEQ003", "TTTTAAAATTTT", especie="Mus musculus", gene="p53")
    
    # Buscar sequências
    seq = banco2.buscar_sequencia("SEQ001")
    print(f"Sequência SEQ001: {seq}")
    
    # Buscar por padrão
    resultados = banco1.buscar_sequencia_por_padrao("ATCG")
    print(f"Sequências com padrão 'ATCG': {list(resultados.keys())}")
    
    # Estatísticas
    stats = banco2.obter_estatisticas()
    print(f"Estatísticas: {stats}")
    
    print("\n=== Exemplo 3: Thread Safety Test ===")
    import time
    import threading
    
    def worker(worker_id):
        gerenciador = GerenciadorRecursos.get_instancia()
        print(f"Worker {worker_id}: {id(gerenciador)}")
        time.sleep(0.1)
    
    # Criar múltiplas threads para testar thread safety
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("Thread safety test concluído!")
