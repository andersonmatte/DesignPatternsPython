import threading
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class AnalisadorSequenciasMultiton(ABC):
    """Classe base para analisadores com padrão Multiton."""
    
    _instancias: Dict[str, 'AnalisadorSequenciasMultiton'] = {}
    _lock = threading.Lock()
    
    def __new__(cls, nome_configuracao: str, *args, **kwargs):
        """Cria ou retorna uma instância nomeada existente."""
        if nome_configuracao not in cls._instancias:
            with cls._lock:
                if nome_configuracao not in cls._instancias:
                    instancia = super().__new__(cls)
                    cls._instancias[nome_configuracao] = instancia
        return cls._instancias[nome_configuracao]
    
    def __init__(self, nome_configuracao: str):
        if not hasattr(self, '_inicializado'):
            self.nome_configuracao = nome_configuracao
            self._inicializado = True
    
    @abstractmethod
    def analisar(self, dados: Any) -> Dict[str, Any]:
        """Método abstrato para análise."""
        pass
    
    @classmethod
    def get_instancia(cls, nome_configuracao: str) -> 'AnalisadorSequenciasMultiton':
        """Obtém uma instância específica pelo nome."""
        if nome_configuracao not in cls._instancias:
            cls(nome_configuracao)
        return cls._instancias[nome_configuracao]
    
    @classmethod
    def listar_instancias(cls) -> list:
        """Lista todas as instâncias criadas."""
        return list(cls._instancias.keys())
    
    @classmethod
    def remover_instancia(cls, nome_configuracao: str) -> bool:
        """Remove uma instância específica."""
        if nome_configuracao in cls._instancias:
            del cls._instancias[nome_configuracao]
            return True
        return False


class AnalisadorRapido(AnalisadorSequenciasMultiton):
    """Analisador rápido para processamento em alta velocidade."""
    
    def __init__(self, nome_configuracao: str):
        super().__init__(nome_configuracao)
        if not hasattr(self, 'configurado'):
            self.velocidade_processamento = 1000  # sequências/segundo
            self.precisao = 0.85
            self.memoria_maxima = "512MB"
            self.algoritmo = "QuickMatch"
            self.configurado = True
    
    def analisar(self, dados: Any) -> Dict[str, Any]:
        """Análise rápida com alta velocidade."""
        sequencia = str(dados)
        return {
            "configuracao": self.nome_configuracao,
            "algoritmo": self.algoritmo,
            "velocidade": self.velocidade_processamento,
            "precisao": self.precisao,
            "resultado": f"Análise rápida de {len(sequencia)} bases",
            "tempo_processamento": len(sequencia) / self.velocidade_processamento,
            "composicao": self._composicao_rapida(sequencia)
        }
    
    def _composicao_rapida(self, sequencia: str) -> Dict[str, int]:
        """Cálculo rápido de composição."""
        composicao = {"A": 0, "T": 0, "C": 0, "G": 0}
        for base in sequencia.upper()[:100]:  # Limita para velocidade
            if base in composicao:
                composicao[base] += 1
        return composicao


class AnalisadorPreciso(AnalisadorSequenciasMultiton):
    """Analisador preciso para resultados de alta qualidade."""
    
    def __init__(self, nome_configuracao: str):
        super().__init__(nome_configuracao)
        if not hasattr(self, 'configurado'):
            self.velocidade_processamento = 100  # sequências/segundo
            self.precisao = 0.99
            self.memoria_maxima = "2GB"
            self.algoritmo = "Smith-Waterman"
            self.configurado = True
    
    def analisar(self, dados: Any) -> Dict[str, Any]:
        """Análise precisa com alta qualidade."""
        sequencia = str(dados)
        return {
            "configuracao": self.nome_configuracao,
            "algoritmo": self.algoritmo,
            "velocidade": self.velocidade_processamento,
            "precisao": self.precisao,
            "resultado": f"Análise precisa de {len(sequencia)} bases",
            "tempo_processamento": len(sequencia) / self.velocidade_processamento,
            "composicao": self._composicao_completa(sequencia),
            "qualidade": self._calcular_qualidade(sequencia)
        }
    
    def _composicao_completa(self, sequencia: str) -> Dict[str, int]:
        """Cálculo completo de composição."""
        composicao = {"A": 0, "T": 0, "C": 0, "G": 0, "N": 0}
        for base in sequencia.upper():
            if base in composicao:
                composicao[base] += 1
        return composicao
    
    def _calcular_qualidade(self, sequencia: str) -> Dict[str, float]:
        """Cálculo detalhado de qualidade."""
        total = len(sequencia)
        if total == 0:
            return {"gc_content": 0.0, "complexidade": 0.0}
        
        gc_count = sequencia.upper().count('G') + sequencia.upper().count('C')
        gc_content = (gc_count / total) * 100
        
        # Cálculo simplificado de complexidade
        bases_unicas = len(set(sequencia.upper()))
        complexidade = (bases_unicas / min(4, total)) * 100
        
        return {
            "gc_content": gc_content,
            "complexidade": complexidade
        }


class AnalisadorEspecializado(AnalisadorSequenciasMultiton):
    """Analisador especializado para tipos específicos de análise."""
    
    def __init__(self, nome_configuracao: str, especialidade: str = "geral"):
        super().__init__(nome_configuracao)
        if not hasattr(self, 'configurado'):
            self.especialidade = especialidade
            self.velocidade_processamento = 500
            self.precisao = 0.95
            self.memoria_maxima = "1GB"
            self.algoritmo = "Needleman-Wunsch"
            self.parametros_especializados = self._configurar_parametros(especialidade)
            self.configurado = True
    
    def _configurar_parametros(self, especialidade: str) -> Dict[str, Any]:
        """Configura parâmetros baseados na especialidade."""
        parametros = {
            "geral": {"match": 2, "mismatch": -1, "gap": -1},
            "dna": {"match": 2, "mismatch": -2, "gap": -2},
            "rna": {"match": 2, "mismatch": -1, "gap": -1.5},
            "proteina": {"match": 5, "mismatch": -3, "gap": -4}
        }
        return parametros.get(especialidade, parametros["geral"])
    
    def analisar(self, dados: Any) -> Dict[str, Any]:
        """Análise especializada baseada na configuração."""
        sequencia = str(dados)
        return {
            "configuracao": self.nome_configuracao,
            "especialidade": self.especialidade,
            "algoritmo": self.algoritmo,
            "velocidade": self.velocidade_processamento,
            "precisao": self.precisao,
            "resultado": f"Análise especializada ({self.especialidade}) de {len(sequencia)} bases",
            "parametros": self.parametros_especializados,
            "tempo_processamento": len(sequencia) / self.velocidade_processamento
        }


class MultitonFactory:
    """Factory para gerenciar instâncias Multiton de diferentes tipos."""
    
    @staticmethod
    def get_instancia_rapido(nome_configuracao: str) -> AnalisadorRapido:
        """Obtém instância rápida nomeada."""
        return AnalisadorRapido.get_instancia(nome_configuracao)
    
    @staticmethod
    def get_instancia_preciso(nome_configuracao: str) -> AnalisadorPreciso:
        """Obtém instância precisa nomeada."""
        return AnalisadorPreciso.get_instancia(nome_configuracao)
    
    @staticmethod
    def get_instancia_especializado(nome_configuracao: str, especialidade: str = "geral") -> AnalisadorEspecializado:
        """Obtém instância especializada nomeada."""
        return AnalisadorEspecializado(nome_configuracao, especialidade)
    
    @staticmethod
    def listar_todas_instancias() -> Dict[str, list]:
        """Lista todas as instâncias de todos os tipos."""
        return {
            "rapido": AnalisadorRapido.listar_instancias(),
            "preciso": AnalisadorPreciso.listar_instancias(),
            "especializado": AnalisadorEspecializado.listar_instancias()
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Instâncias Nomeadas de Analisadores ===")
    
    # Criar instâncias nomeadas
    analisador_rapido_1 = MultitonFactory.get_instancia_rapido("RAPIDO_001")
    analisador_rapido_2 = MultitonFactory.get_instancia_rapido("RAPIDO_001")  # Mesma instância
    analisador_rapido_3 = MultitonFactory.get_instancia_rapido("RAPIDO_002")  # Nova instância
    
    analisador_preciso_1 = MultitonFactory.get_instancia_preciso("PRECISO_001")
    analisador_preciso_2 = MultitonFactory.get_instancia_preciso("PRECISO_001")  # Mesma instância
    
    print(f"RAPIDO_001 é a mesma instância? {analisador_rapido_1 is analisador_rapido_2}")
    print(f"RAPIDO_001 é diferente de RAPIDO_002? {analisador_rapido_1 is analisador_rapido_3}")
    print(f"PRECISO_001 é a mesma instância? {analisador_preciso_1 is analisador_preciso_2}")
    
    # Realizar análises
    sequencia_teste = "ATCGATCGATCGATCGATCG"
    
    resultado_rapido = analisador_rapido_1.analisar(sequencia_teste)
    print(f"\nResultado análise rápida:")
    for chave, valor in resultado_rapido.items():
        print(f"  {chave}: {valor}")
    
    resultado_preciso = analisador_preciso_1.analisar(sequencia_teste)
    print(f"\nResultado análise precisa:")
    for chave, valor in resultado_preciso.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 2: Analisadores Especializados ===")
    
    analisador_dna = MultitonFactory.get_instancia_especializado("DNA_ANALISER", "dna")
    analisador_rna = MultitonFactory.get_instancia_especializado("RNA_ANALISER", "rna")
    analisador_proteina = MultitonFactory.get_instancia_especializado("PROTEIN_ANALISER", "proteina")
    
    resultado_dna = analisador_dna.analisar("ATCGATCG")
    resultado_rna = analisador_rna.analisar("AUCGAUCG")
    resultado_proteina = analisador_proteina.analisar("MKTLLILAV")
    
    print("Análise DNA:", resultado_dna["resultado"])
    print("Análise RNA:", resultado_rna["resultado"])
    print("Análise Proteína:", resultado_proteina["resultado"])
    
    print("\n=== Exemplo 3: Listar Todas as Instâncias ===")
    
    todas_instancias = MultitonFactory.listar_todas_instancias()
    print("Instâncias criadas:")
    for tipo, instancias in todas_instancias.items():
        print(f"  {tipo}: {instancias}")
    
    print("\n=== Exemplo 4: Cache Controlado ===")
    
    # Obter mesma instância múltiplas vezes
    for i in range(3):
        instancia = MultitonFactory.get_instancia_rapido("CACHE_TEST")
        print(f"Obtenção {i+1}: ID da instância = {id(instancia)}")
    
    # Remover instância
    print(f"\nRemovendo instância 'CACHE_TEST': {AnalisadorRapido.remover_instancia('CACHE_TEST')}")
    print(f"Instâncias rápidas restantes: {AnalisadorRapido.listar_instancias()}")
    
    print("\n=== Exemplo 5: Thread Safety Test ===")
    import time
    import threading
    
    def worker_multiton(worker_id):
        try:
            instancia = MultitonFactory.get_instancia_rapido("THREAD_TEST")
            print(f"Worker {worker_id}: ID = {id(instancia)}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Worker {worker_id}: Erro = {e}")
    
    # Criar múltiplas threads
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_multiton, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("Thread safety test concluído!")
