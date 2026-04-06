from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import time
import hashlib
from functools import wraps


class BancoDadosGeneticosInterface(ABC):
    """Interface para banco de dados genéticos."""
    
    @abstractmethod
    def buscar_sequencia(self, id_sequencia: str, usuario: str) -> Optional[Dict[str, Any]]:
        """Busca sequência por ID."""
        pass
    
    @abstractmethod
    def buscar_variantes(self, gene: str, usuario: str) -> List[Dict[str, Any]]:
        """Busca variantes de um gene."""
        pass
    
    @abstractmethod
    def salvar_analise(self, dados_analise: Dict[str, Any], usuario: str) -> bool:
        """Salva resultados de análise."""
        pass
    
    @abstractmethod
    def obter_estatisticas(self, usuario: str) -> Dict[str, Any]:
        """Obtém estatísticas do banco."""
        pass


class BancoDadosGeneticosReal(BancoDadosGeneticosInterface):
    """Implementação real do banco de dados genéticos."""
    
    def __init__(self):
        self.sequencias = {
            "SEQ001": {
                "id": "SEQ001",
                "sequencia": "ATCGATCGATCGATCGATCG",
                "gene": "BRCA1",
                "cromossomo": "17",
                "posicao": "43044295",
                "descricao": "Gene supressor de tumor BRCA1"
            },
            "SEQ002": {
                "id": "SEQ002", 
                "sequencia": "GCTAGCTAGCTAGCTAGCTA",
                "gene": "TP53",
                "cromossomo": "17",
                "posicao": "7579472",
                "descricao": "Gene supressor de tumor TP53"
            },
            "SEQ003": {
                "id": "SEQ003",
                "sequencia": "TTTTAAAATTTTAAAATTTT",
                "gene": "EGFR",
                "cromossomo": "7",
                "posicao": "55019017",
                "descricao": "Receptor de fator de crescimento epitelial"
            }
        }
        
        self.variantes = {
            "BRCA1": [
                {"id": "VAR001", "tipo": "SNP", "posicao": 123, "ref": "A", "alt": "G", "frequencia": 0.001},
                {"id": "VAR002", "tipo": "INDEL", "posicao": 456, "ref": "AT", "alt": "A", "frequencia": 0.0005}
            ],
            "TP53": [
                {"id": "VAR003", "tipo": "SNP", "posicao": 789, "ref": "C", "alt": "T", "frequencia": 0.002},
                {"id": "VAR004", "tipo": "SNP", "posicao": 1011, "ref": "G", "alt": "A", "frequencia": 0.0015}
            ],
            "EGFR": [
                {"id": "VAR005", "tipo": "SNP", "posicao": 555, "ref": "T", "alt": "C", "frequencia": 0.003}
            ]
        }
        
        self.analises_salvas = []
        self.acessos = []
    
    def buscar_sequencia(self, id_sequencia: str, usuario: str) -> Optional[Dict[str, Any]]:
        """Busca sequência no banco real."""
        print(f"[BANCO REAL] Buscando sequência {id_sequencia} para usuário {usuario}")
        
        # Simula tempo de acesso ao banco
        time.sleep(0.1)
        
        # Registra acesso
        self.acessos.append({
            "operacao": "buscar_sequencia",
            "usuario": usuario,
            "parametro": id_sequencia,
            "timestamp": time.time()
        })
        
        return self.sequencias.get(id_sequencia)
    
    def buscar_variantes(self, gene: str, usuario: str) -> List[Dict[str, Any]]:
        """Busca variantes de um gene."""
        print(f"[BANCO REAL] Buscando variantes do gene {gene} para usuário {usuario}")
        
        # Simula tempo de acesso
        time.sleep(0.15)
        
        # Registra acesso
        self.acessos.append({
            "operacao": "buscar_variantes",
            "usuario": usuario,
            "parametro": gene,
            "timestamp": time.time()
        })
        
        return self.variantes.get(gene, [])
    
    def salvar_analise(self, dados_analise: Dict[str, Any], usuario: str) -> bool:
        """Salva análise no banco."""
        print(f"[BANCO REAL] Salvando análise para usuário {usuario}")
        
        # Simula tempo de salvamento
        time.sleep(0.2)
        
        # Adiciona metadados
        dados_completos = {
            **dados_analise,
            "usuario": usuario,
            "timestamp": time.time(),
            "id": f"ANALISE_{len(self.analises_salvas) + 1:04d}"
        }
        
        self.analises_salvas.append(dados_completos)
        
        # Registra acesso
        self.acessos.append({
            "operacao": "salvar_analise",
            "usuario": usuario,
            "parametro": dados_analise.get("tipo", "desconhecido"),
            "timestamp": time.time()
        })
        
        return True
    
    def obter_estatisticas(self, usuario: str) -> Dict[str, Any]:
        """Obtém estatísticas do banco."""
        print(f"[BANCO REAL] Obtendo estatísticas para usuário {usuario}")
        
        # Simula tempo de processamento
        time.sleep(0.05)
        
        # Registra acesso
        self.acessos.append({
            "operacao": "obter_estatisticas",
            "usuario": usuario,
            "parametro": "estatisticas",
            "timestamp": time.time()
        })
        
        return {
            "total_sequencias": len(self.sequencias),
            "total_variantes": sum(len(var) for var in self.variantes.values()),
            "total_analises": len(self.analises_salvas),
            "total_acessos": len(self.acessos),
            "usuarios_unicos": len(set(a["usuario"] for a in self.acessos))
        }


class GerenciadorPermissoes:
    """Gerenciador de permissões de usuários."""
    
    def __init__(self):
        self.permissoes = {
            "admin": ["buscar_sequencia", "buscar_variantes", "salvar_analise", "obter_estatisticas", "deletar"],
            "pesquisador": ["buscar_sequencia", "buscar_variantes", "salvar_analise", "obter_estatisticas"],
            "estudante": ["buscar_sequencia", "buscar_variantes"],
            "visitante": ["buscar_sequencia"]
        }
        
        self.usuarios = {
            "joao.silva": "admin",
            "maria.santos": "pesquisador", 
            "pedro.oliveira": "estudante",
            "convidado": "visitante"
        }
    
    def verificar_permissao(self, usuario: str, operacao: str) -> bool:
        """Verifica se usuário tem permissão para operação."""
        nivel_usuario = self.usuarios.get(usuario)
        if not nivel_usuario:
            return False
        
        permissoes_usuario = self.permissoes.get(nivel_usuario, [])
        return operacao in permissoes_usuario
    
    def obter_nivel_usuario(self, usuario: str) -> str:
        """Obtém nível de permissão do usuário."""
        return self.usuarios.get(usuario, "desconhecido")


class CacheProxy:
    """Proxy com cache para otimizar consultas frequentes."""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def gerar_chave(self, operacao: str, **kwargs) -> str:
        """Gera chave única para cache."""
        chave_str = f"{operacao}:{sorted(kwargs.items())}"
        return hashlib.md5(chave_str.encode()).hexdigest()
    
    def obter(self, chave: str) -> Optional[Any]:
        """Obtém item do cache."""
        if chave in self.cache:
            item = self.cache[chave]
            if time.time() - item["timestamp"] < self.ttl:
                print(f"[CACHE HIT] Chave {chave}")
                return item["dados"]
            else:
                # Item expirado
                del self.cache[chave]
                print(f"[CACHE EXPIRADO] Chave {chave}")
        
        print(f"[CACHE MISS] Chave {chave}")
        return None
    
    def armazenar(self, chave: str, dados: Any) -> None:
        """Armazena item no cache."""
        self.cache[chave] = {
            "dados": dados,
            "timestamp": time.time()
        }
    
    def limpar(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
        print("[CACHE] Cache limpo")
    
    def obter_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do cache."""
        return {
            "itens_cache": len(self.cache),
            "ttl_seconds": self.ttl
        }


class BancoDadosGeneticosProxy(BancoDadosGeneticosInterface):
    """Proxy para banco de dados genéticos com segurança, cache e logging."""
    
    def __init__(self, banco_real: BancoDadosGeneticosReal):
        self.banco_real = banco_real
        self.gerenciador_permissoes = GerenciadorPermissoes()
        self.cache = CacheProxy(ttl_seconds=60)
        self.logs = []
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "acessos_negados": 0,
            "operacoes": {}
        }
    
    def _registrar_log(self, operacao: str, usuario: str, parametro: str, 
                      sucesso: bool, mensagem: str = "") -> None:
        """Registra log da operação."""
        log_entry = {
            "timestamp": time.time(),
            "operacao": operacao,
            "usuario": usuario,
            "parametro": parametro,
            "sucesso": sucesso,
            "mensagem": mensagem
        }
        self.logs.append(log_entry)
        
        # Mantém apenas últimos 1000 logs
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    def _verificar_permissao(self, usuario: str, operacao: str) -> bool:
        """Verifica permissão do usuário."""
        if not self.gerenciador_permissoes.verificar_permissao(usuario, operacao):
            self.stats["acessos_negados"] += 1
            nivel_usuario = self.gerenciador_permissoes.obter_nivel_usuario(usuario)
            self._registrar_log(operacao, usuario, "", False, 
                              f"Acesso negado. Usuário nível: {nivel_usuario}")
            return False
        return True
    
    def _atualizar_stats(self, operacao: str) -> None:
        """Atualiza estatísticas."""
        self.stats["total_requests"] += 1
        self.stats["operacoes"][operacao] = self.stats["operacoes"].get(operacao, 0) + 1
    
    def buscar_sequencia(self, id_sequencia: str, usuario: str) -> Optional[Dict[str, Any]]:
        """Busca sequência com proxy."""
        operacao = "buscar_sequencia"
        self._atualizar_stats(operacao)
        
        # Verifica permissão
        if not self._verificar_permissao(usuario, operacao):
            return None
        
        # Verifica cache
        chave_cache = self.cache.gerar_chave(operacao, id_sequencia=id_sequencia, usuario=usuario)
        resultado_cache = self.cache.obter(chave_cache)
        
        if resultado_cache:
            self.stats["cache_hits"] += 1
            self._registrar_log(operacao, usuario, id_sequencia, True, "Cache hit")
            return resultado_cache
        
        self.stats["cache_misses"] += 1
        
        # Acessa banco real
        try:
            resultado = self.banco_real.buscar_sequencia(id_sequencia, usuario)
            
            # Armazena no cache
            if resultado:
                self.cache.armazenar(chave_cache, resultado)
            
            self._registrar_log(operacao, usuario, id_sequencia, True, 
                              f"Sequência encontrada: {resultado is not None}")
            return resultado
            
        except Exception as e:
            self._registrar_log(operacao, usuario, id_sequencia, False, f"Erro: {str(e)}")
            return None
    
    def buscar_variantes(self, gene: str, usuario: str) -> List[Dict[str, Any]]:
        """Busca variantes com proxy."""
        operacao = "buscar_variantes"
        self._atualizar_stats(operacao)
        
        # Verifica permissão
        if not self._verificar_permissao(usuario, operacao):
            return []
        
        # Verifica cache
        chave_cache = self.cache.gerar_chave(operacao, gene=gene, usuario=usuario)
        resultado_cache = self.cache.obter(chave_cache)
        
        if resultado_cache:
            self.stats["cache_hits"] += 1
            self._registrar_log(operacao, usuario, gene, True, "Cache hit")
            return resultado_cache
        
        self.stats["cache_misses"] += 1
        
        # Acessa banco real
        try:
            resultado = self.banco_real.buscar_variantes(gene, usuario)
            
            # Armazena no cache
            self.cache.armazenar(chave_cache, resultado)
            
            self._registrar_log(operacao, usuario, gene, True, 
                              f"Variantes encontradas: {len(resultado)}")
            return resultado
            
        except Exception as e:
            self._registrar_log(operacao, usuario, gene, False, f"Erro: {str(e)}")
            return []
    
    def salvar_analise(self, dados_analise: Dict[str, Any], usuario: str) -> bool:
        """Salva análise com proxy."""
        operacao = "salvar_analise"
        self._atualizar_stats(operacao)
        
        # Verifica permissão
        if not self._verificar_permissao(usuario, operacao):
            return False
        
        # Operações de escrita não usam cache
        try:
            resultado = self.banco_real.salvar_analise(dados_analise, usuario)
            
            # Limpa cache relacionado após escrita
            self.cache.limpar()
            
            self._registrar_log(operacao, usuario, dados_analise.get("tipo", "desconhecido"), 
                              True, f"Análise salva: {resultado}")
            return resultado
            
        except Exception as e:
            self._registrar_log(operacao, usuario, dados_analise.get("tipo", "desconhecido"), 
                              False, f"Erro: {str(e)}")
            return False
    
    def obter_estatisticas(self, usuario: str) -> Dict[str, Any]:
        """Obtém estatísticas com proxy."""
        operacao = "obter_estatisticas"
        self._atualizar_stats(operacao)
        
        # Verifica permissão
        if not self._verificar_permissao(usuario, operacao):
            return {}
        
        # Verifica cache (estatísticas mudam com frequência, TTL curto)
        chave_cache = self.cache.gerar_chave(operacao, usuario=usuario)
        resultado_cache = self.cache.obter(chave_cache)
        
        if resultado_cache:
            self.stats["cache_hits"] += 1
            self._registrar_log(operacao, usuario, "estatisticas", True, "Cache hit")
            return resultado_cache
        
        self.stats["cache_misses"] += 1
        
        # Acessa banco real
        try:
            resultado = self.banco_real.obter_estatisticas(usuario)
            
            # Armazena no cache por pouco tempo
            self.cache.armazenar(chave_cache, resultado)
            
            self._registrar_log(operacao, usuario, "estatisticas", True, "Estatísticas obtidas")
            return resultado
            
        except Exception as e:
            self._registrar_log(operacao, usuario, "estatisticas", False, f"Erro: {str(e)}")
            return {}
    
    def obter_logs_proxy(self, limite: int = 50) -> List[Dict[str, Any]]:
        """Obtém logs do proxy."""
        return self.logs[-limite:]
    
    def obter_stats_proxy(self) -> Dict[str, Any]:
        """Obtém estatísticas do proxy."""
        cache_stats = self.cache.obter_stats()
        
        return {
            **self.stats,
            "cache_stats": cache_stats,
            "taxa_cache_hit": (self.stats["cache_hits"] / 
                              max(1, self.stats["cache_hits"] + self.stats["cache_misses"])) * 100
        }
    
    def limpar_cache_proxy(self) -> None:
        """Limpa cache do proxy."""
        self.cache.limpar()


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Configuração do Proxy ===")
    
    # Criar banco real e proxy
    banco_real = BancoDadosGeneticosReal()
    banco_proxy = BancoDadosGeneticosProxy(banco_real)
    
    print("Banco de dados com proxy configurado!")
    
    print("\n=== Exemplo 2: Teste de Permissões ===")
    
    # Testar diferentes usuários
    usuarios_teste = [
        ("joao.silva", "Admin"),
        ("maria.santos", "Pesquisador"),
        ("pedro.oliveira", "Estudante"),
        ("convidado", "Visitante"),
        ("usuario.inexistente", "Não cadastrado")
    ]
    
    for usuario, descricao in usuarios_teste:
        print(f"\nTestando usuário: {usuario} ({descricao})")
        
        # Tentar buscar sequência
        resultado = banco_proxy.buscar_sequencia("SEQ001", usuario)
        print(f"  Buscar sequência: {'Sucesso' if resultado else 'Falha'}")
        
        # Tentar buscar variantes
        variantes = banco_proxy.buscar_variantes("BRCA1", usuario)
        print(f"  Buscar variantes: {'Sucesso' if variantes else 'Falha'} ({len(variantes)} encontradas)")
        
        # Tentar salvar análise
        analise_teste = {"tipo": "teste", "resultado": "OK"}
        salvo = banco_proxy.salvar_analise(analise_teste, usuario)
        print(f"  Salvar análise: {'Sucesso' if salvo else 'Falha'}")
    
    print("\n=== Exemplo 3: Teste de Cache ===")
    
    print("\nPrimeira busca (cache miss):")
    resultado1 = banco_proxy.buscar_sequencia("SEQ001", "maria.santos")
    print(f"Resultado: {resultado1['gene'] if resultado1 else 'None'}")
    
    print("\nSegunda busca mesma sequência (cache hit):")
    resultado2 = banco_proxy.buscar_sequencia("SEQ001", "maria.santos")
    print(f"Resultado: {resultado2['gene'] if resultado2 else 'None'}")
    
    print("\nTerceira busca sequência diferente (cache miss):")
    resultado3 = banco_proxy.buscar_sequencia("SEQ002", "maria.santos")
    print(f"Resultado: {resultado3['gene'] if resultado3 else 'None'}")
    
    print("\nQuarta busca primeira sequência (cache hit):")
    resultado4 = banco_proxy.buscar_sequencia("SEQ001", "maria.santos")
    print(f"Resultado: {resultado4['gene'] if resultado4 else 'None'}")
    
    print("\n=== Exemplo 4: Operações com Diferentes Usuários ===")
    
    # Pesquisador faz várias operações
    print("\nOperações do pesquisador maria.santos:")
    
    variantes_brca = banco_proxy.buscar_variantes("BRCA1", "maria.santos")
    print(f"Variantes BRCA1: {len(variantes_brca)} encontradas")
    
    variantes_tp53 = banco_proxy.buscar_variantes("TP53", "maria.santos")
    print(f"Variantes TP53: {len(variantes_tp53)} encontradas")
    
    # Salvar análise
    analise_completa = {
        "tipo": "variacao_genetica",
        "genes_analisados": ["BRCA1", "TP53"],
        "variantes_encontradas": len(variantes_brca) + len(variantes_tp53),
        "conclusao": "Análise concluída com sucesso"
    }
    
    salvo = banco_proxy.salvar_analise(analise_completa, "maria.santos")
    print(f"Análise salva: {salvo}")
    
    # Estatísticas
    stats = banco_proxy.obter_estatisticas("maria.santos")
    print(f"Estatísticas: {stats}")
    
    print("\n=== Exemplo 5: Logs e Estatísticas do Proxy ===")
    
    # Obter logs recentes
    logs_recentes = banco_proxy.obter_logs_proxy(10)
    print(f"\nLogs recentes ({len(logs_recentes)}):")
    for log in logs_recentes[-5:]:  # Últimos 5 logs
        status = "✓" if log["sucesso"] else "✗"
        print(f"  {status} {log['operacao']} - {log['usuario']} - {log['mensagem']}")
    
    # Estatísticas do proxy
    stats_proxy = banco_proxy.obter_stats_proxy()
    print(f"\nEstatísticas do Proxy:")
    for chave, valor in stats_proxy.items():
        if isinstance(valor, float):
            print(f"  {chave}: {valor:.2f}")
        elif isinstance(valor, dict):
            print(f"  {chave}:")
            for sub_chave, sub_valor in valor.items():
                print(f"    {sub_chave}: {sub_valor}")
        else:
            print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 6: Limpeza de Cache ===")
    
    print("Limpando cache...")
    banco_proxy.limpar_cache_proxy()
    
    print("\nBusca após limpar cache (deve ser cache miss):")
    resultado_pos_limpeza = banco_proxy.buscar_sequencia("SEQ001", "maria.santos")
    print(f"Resultado: {resultado_pos_limpeza['gene'] if resultado_pos_limpeza else 'None'}")
    
    print("\n=== Exemplo 7: Comparação de Desempenho ===")
    
    # Simular múltiplas operações
    import time
    
    print("\nTestando desempenho com 20 operações...")
    
    usuarios = ["maria.santos", "pedro.oliveira", "joao.silva"]
    sequencias = ["SEQ001", "SEQ002", "SEQ003"]
    
    inicio = time.time()
    
    for i in range(20):
        usuario = usuarios[i % len(usuarios)]
        sequencia = sequencias[i % len(sequencias)]
        banco_proxy.buscar_sequencia(sequencia, usuario)
    
    fim = time.time()
    
    stats_finais = banco_proxy.obter_stats_proxy()
    
    print(f"\nTempo total: {fim - inicio:.3f} segundos")
    print(f"Taxa de cache hit: {stats_finais['taxa_cache_hit']:.1f}%")
    print(f"Total de requests: {stats_finais['total_requests']}")
    print(f"Cache hits: {stats_finais['cache_hits']}")
    print(f"Cache misses: {stats_finais['cache_misses']}")
    print(f"Acessos negados: {stats_finais['acessos_negados']}")
    
    print("\nProxy pattern implementado com sucesso!")
