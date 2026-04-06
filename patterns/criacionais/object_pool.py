import threading
import time
from typing import List, Optional, Dict, Any
from queue import Queue, Empty
from domain.amostra_biologica import EquipamentoLaboratorial


class ObjectPool:
    """Classe genérica para implementação de Object Pool."""
    
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.pool = Queue(maxsize=max_size)
        self.in_use = set()
        self.lock = threading.Lock()
        self.total_created = 0
        self.total_acquired = 0
        self.total_released = 0
    
    def acquire(self, timeout: float = 5.0) -> Optional[Any]:
        """Adquire um objeto do pool."""
        try:
            # Tenta obter do pool
            obj = self.pool.get(timeout=timeout)
            with self.lock:
                self.in_use.add(id(obj))
                self.total_acquired += 1
            return obj
        except Empty:
            # Se o pool está vazio, tenta criar novo objeto
            if self.total_created < self.max_size:
                with self.lock:
                    if self.total_created < self.max_size:
                        obj = self._create_object()
                        self.in_use.add(id(obj))
                        self.total_created += 1
                        self.total_acquired += 1
                        return obj
            return None
    
    def release(self, obj: Any) -> bool:
        """Libera um objeto de volta ao pool."""
        obj_id = id(obj)
        with self.lock:
            if obj_id in self.in_use:
                self.in_use.remove(obj_id)
                self.total_released += 1
                try:
                    self._reset_object(obj)
                    self.pool.put(obj, timeout=0.1)
                    return True
                except:
                    # Pool cheio, objeto descartado
                    return False
        return False
    
    def _create_object(self) -> Any:
        """Método abstrato para criar novos objetos."""
        raise NotImplementedError("Subclasses devem implementar _create_object")
    
    def _reset_object(self, obj: Any) -> None:
        """Método para resetar estado do objeto."""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do pool."""
        return {
            "max_size": self.max_size,
            "available": self.pool.qsize(),
            "in_use": len(self.in_use),
            "total_created": self.total_created,
            "total_acquired": self.total_acquired,
            "total_released": self.total_released
        }


class EquipamentoPool(ObjectPool):
    """Pool de equipamentos laboratoriais compartilhados."""
    
    def __init__(self, equipamentos: List[EquipamentoLaboratorial]):
        super().__init__(max_size=len(equipamentos))
        self.equipamentos_disponiveis = equipamentos.copy()
        
        # Adiciona equipamentos iniciais ao pool
        for equipamento in equipamentos:
            self.pool.put(equipamento)
            self.total_created += 1
    
    def _create_object(self) -> EquipamentoLaboratorial:
        """Cria um novo equipamento se necessário."""
        if self.equipamentos_disponiveis:
            return self.equipamentos_disponiveis.pop(0)
        else:
            # Cria um equipamento genérico
            return EquipamentoLaboratorial(f"Auto_{self.total_created}", "Genérico")
    
    def _reset_object(self, obj: EquipamentoLaboratorial) -> None:
        """Reseta o estado do equipamento."""
        obj.liberar()
    
    def acquire_equipamento(self, tipo: str = "", pesquisador: str = "", timeout: float = 5.0) -> Optional[EquipamentoLaboratorial]:
        """Adquire um equipamento específico por tipo."""
        equipamento = self.acquire(timeout)
        if equipamento and tipo and equipamento.tipo != tipo:
            # Se não for o tipo desejado, libera e tenta novamente
            self.release(equipamento)
            return None
        
        if equipamento and pesquisador:
            equipamento.reservar(pesquisador)
        
        return equipamento
    
    def release_equipamento(self, equipamento: EquipamentoLaboratorial) -> bool:
        """Libera um equipamento específico."""
        if equipamento:
            equipamento.liberar()
        return self.release(equipamento)


class CentrifugaPool(ObjectPool):
    """Pool especializado para centrífugas de alta velocidade."""
    
    def __init__(self, num_centrifugas: int = 5):
        super().__init__(max_size=num_centrifugas)
        self.velocidades_maximas = [15000, 20000, 25000, 30000, 35000][:num_centrifugas]
        
        # Cria centrífugas iniciais
        for i in range(num_centrifugas):
            centrifuga = self._create_object()
            self.pool.put(centrifuga)
            self.total_created += 1
    
    def _create_object(self) -> 'CentrifugaPoolItem':
        """Cria uma nova centrífuga."""
        velocidade = self.velocidades_maximas[self.total_created % len(self.velocidades_maximas)]
        return CentrifugaPoolItem(f"Centrifuga_{self.total_created + 1}", velocidade)
    
    def _reset_object(self, obj: 'CentrifugaPoolItem') -> None:
        """Reseta o estado da centrífuga."""
        obj.liberar()
    
    def acquire_centrifuga(self, velocidade_minima: int = 0, timeout: float = 5.0) -> Optional['CentrifugaPoolItem']:
        """Adquire uma centrífuga com velocidade mínima específica."""
        # Lista temporária para armazenar equipamentos que não atendem ao critério
        inadequados = []
        
        for _ in range(self.pool.qsize()):
            try:
                centrifuga = self.pool.get_nowait()
                if centrifuga.velocidade_maxima >= velocidade_minima:
                    with self.lock:
                        self.in_use.add(id(centrifuga))
                        self.total_acquired += 1
                    # Devolve os inadequados ao pool
                    for inadequado in inadequados:
                        self.pool.put(inadequado)
                    return centrifuga
                else:
                    inadequados.append(centrifuga)
            except Empty:
                break
        
        # Devolve todos os inadequados ao pool
        for inadequado in inadequados:
            self.pool.put(inadequado)
        
        return None


class CentrifugaPoolItem:
    """Item de centrífuga para uso no pool."""
    
    def __init__(self, nome: str, velocidade_maxima: int):
        self.nome = nome
        self.velocidade_maxima = velocidade_maxima
        self.em_uso = False
        self.pesquisador_atual = ""
        self.tempo_uso_inicio = None
    
    def reservar(self, pesquisador: str) -> bool:
        """Reserva a centrífuga."""
        if not self.em_uso:
            self.em_uso = True
            self.pesquisador_atual = pesquisador
            self.tempo_uso_inicio = time.time()
            return True
        return False
    
    def liberar(self) -> None:
        """Libera a centrífuga."""
        self.em_uso = False
        self.pesquisador_atual = ""
        self.tempo_uso_inicio = None
    
    def centrifugar(self, amostra: str, velocidade: int) -> str:
        """Executa centrifugação."""
        if not self.em_uso:
            return "Centrífuga não está reservada"
        
        if velocidade > self.velocidade_maxima:
            return f"Velocidade {velocidade} rpm excede o máximo de {self.velocidade_maxima} rpm"
        
        tempo_uso = time.time() - self.tempo_uso_inicio if self.tempo_uso_inicio else 0
        return f"Centrifugando {amostra} a {velocidade} rpm (máx: {self.velocidade_maxima}) por {self.pesquisador_atual} (uso: {tempo_uso:.1f}s)"
    
    def __str__(self) -> str:
        status = f"Em uso por {self.pesquisador_atual}" if self.em_uso else "Disponível"
        return f"{self.nome} ({self.velocidade_maxima} rpm) - {status}"


class PoolManager:
    """Gerenciador centralizado de múltiplos pools."""
    
    def __init__(self):
        self.pools: Dict[str, ObjectPool] = {}
        self.lock = threading.Lock()
    
    def registrar_pool(self, nome: str, pool: ObjectPool) -> None:
        """Registra um pool com um nome."""
        with self.lock:
            self.pools[nome] = pool
    
    def obter_pool(self, nome: str) -> Optional[ObjectPool]:
        """Obtém um pool pelo nome."""
        return self.pools.get(nome)
    
    def listar_pools(self) -> List[str]:
        """Lista todos os pools registrados."""
        return list(self.pools.keys())
    
    def obter_stats_gerais(self) -> Dict[str, Dict[str, Any]]:
        """Obtém estatísticas de todos os pools."""
        stats = {}
        for nome, pool in self.pools.items():
            stats[nome] = pool.get_stats()
        return stats


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Pool de Equipamentos Gerais ===")
    
    # Criar equipamentos para o pool
    equipamentos = [
        EquipamentoLaboratorial("Microscopio_1", "Microscópio"),
        EquipamentoLaboratorial("Centrifuga_1", "Centrífuga"),
        EquipamentoLaboratorial("PCR_1", "Termociclador"),
        EquipamentoLaboratorial("Espectrofotometro_1", "Espectrofotômetro")
    ]
    
    # Criar pool
    pool_equipamentos = EquipamentoPool(equipamentos)
    
    print("Stats iniciais:", pool_equipamentos.get_stats())
    
    # Adquirir equipamentos
    microscopio = pool_equipamentos.acquire_equipamento("Microscópio", "Dr. Silva")
    termociclador = pool_equipamentos.acquire_equipamento("Termociclador", "Dra. Santos")
    
    print(f"\nEquipamentos obtidos:")
    print(f"  {microscopio}")
    print(f"  {termociclador}")
    
    print("\nStats durante uso:", pool_equipamentos.get_stats())
    
    # Tentar obter equipamento não disponível
    outro_microscopio = pool_equipamentos.acquire_equipamento("Microscópio", "Dr. Oliveira")
    print(f"Segundo microscópio: {outro_microscopio}")
    
    # Liberar equipamentos
    pool_equipamentos.release_equipamento(microscopio)
    pool_equipamentos.release_equipamento(termociclador)
    
    print("\nStats após liberação:", pool_equipamentos.get_stats())
    
    print("\n=== Exemplo 2: Pool de Centrífugas Especializado ===")
    
    # Criar pool de centrífugas
    pool_centrifugas = CentrifugaPool(4)
    
    print("Stats iniciais centrífugas:", pool_centrifugas.get_stats())
    
    # Adquirir centrífugas com diferentes requisitos
    centrifuga1 = pool_centrifugas.acquire_centrifuga(20000)  # Mínimo 20000 rpm
    centrifuga2 = pool_centrifugas.acquire_centrifuga(30000)  # Mínimo 30000 rpm
    centrifuga3 = pool_centrifugas.acquire_centrifuga(10000)  # Mínimo 10000 rpm
    
    print(f"\nCentrífugas obtidas:")
    if centrifuga1:
        centrifuga1.reservar("Dr. Silva")
        print(f"  {centrifuga1}")
        print(f"  Uso: {centrifuga1.centrifugar('Amostra A', 18000)}")
    
    if centrifuga2:
        centrifuga2.reservar("Dra. Santos")
        print(f"  {centrifuga2}")
        print(f"  Uso: {centrifuga2.centrifugar('Amostra B', 28000)}")
    
    if centrifuga3:
        centrifuga3.reservar("Dr. Oliveira")
        print(f"  {centrifuga3}")
        print(f"  Uso: {centrifuga3.centrifugar('Amostra C', 12000)}")
    
    print("\nStats durante uso:", pool_centrifugas.get_stats())
    
    # Liberar centrífugas
    pool_centrifugas.release(centrifuga1)
    pool_centrifugas.release(centrifuga2)
    pool_centrifugas.release(centrifuga3)
    
    print("\nStats após liberação:", pool_centrifugas.get_stats())
    
    print("\n=== Exemplo 3: Pool Manager Centralizado ===")
    
    # Criar gerenciador de pools
    manager = PoolManager()
    manager.registrar_pool("equipamentos", pool_equipamentos)
    manager.registrar_pool("centrifugas", pool_centrifugas)
    
    print("Pools registrados:", manager.listar_pools())
    
    # Obter stats gerais
    stats_gerais = manager.obter_stats_gerais()
    print("\nStats gerais dos pools:")
    for nome, stats in stats_gerais.items():
        print(f"  {nome}: {stats}")
    
    print("\n=== Exemplo 4: Teste de Concorrência ===")
    import threading
    import time
    
    def worker_pool(worker_id, pool):
        """Worker que usa o pool."""
        equipamento = pool.acquire_equipamento(pesquisador=f"Worker_{worker_id}")
        if equipamento:
            print(f"Worker {worker_id}: Obteve {equipamento.nome}")
            time.sleep(0.5)  # Simula uso
            pool.release_equipamento(equipamento)
            print(f"Worker {worker_id}: Liberou {equipamento.nome}")
        else:
            print(f"Worker {worker_id}: Não conseguiu obter equipamento")
    
    # Criar múltiplas threads
    threads = []
    for i in range(8):  # Mais threads que equipamentos
        t = threading.Thread(target=worker_pool, args=(i, pool_equipamentos))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("\nStats finais:", pool_equipamentos.get_stats())
    print("Teste de concorrência concluído!")
