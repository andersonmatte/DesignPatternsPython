from abc import ABC, abstractmethod
from typing import Dict, Any, List
from domain.analise import AnaliseBio


class AnaliseBioInterface(ABC):
    """Interface base para análises biológicas."""
    
    @abstractmethod
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa a análise."""
        pass


class AnaliseBasica(AnaliseBioInterface):
    """Implementação básica de análise."""
    
    def __init__(self, nome: str = "Análise Básica"):
        self.nome = nome
        self.custo_base = 100.0
        self.tempo_execucao = 30.0  # minutos
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa análise básica."""
        return {
            "tipo": "básica",
            "nome": self.nome,
            "status": "concluída",
            "dados_processados": len(str(dados)),
            "custo": self.custo_base,
            "tempo_execucao": self.tempo_execucao,
            "resultado": self._processar_dados(dados)
        }
    
    def _processar_dados(self, dados: Any) -> str:
        """Processamento básico dos dados."""
        return f"Dados básicos processados: {str(dados)[:50]}..."


class AnaliseDecorator(AnaliseBioInterface):
    """Classe base para decoradores de análise."""
    
    def __init__(self, analise: AnaliseBioInterface):
        self._analise = analise
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa a análise decorada."""
        return self._analise.executar(dados)


class AnaliseComValidacao(AnaliseDecorator):
    """Decorator que adiciona validação de dados."""
    
    def __init__(self, analise: AnaliseBioInterface, regras_validacao: List[str] = None):
        super().__init__(analise)
        self.regras_validacao = regras_validacao or ["tamanho_minimo", "formato_valido"]
        self.custo_validacao = 20.0
        self.tempo_validacao = 5.0
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa análise com validação."""
        # Realiza validação
        resultado_validacao = self._validar_dados(dados)
        
        if not resultado_validacao["valido"]:
            return {
                "tipo": "validacao_falhou",
                "status": "erro",
                "erros": resultado_validacao["erros"],
                "custo": self.custo_validacao,
                "tempo_execucao": self.tempo_validacao
            }
        
        # Executa análise original
        resultado = self._analise.executar(dados)
        
        # Adiciona informações de validação
        resultado["validacao"] = resultado_validacao
        resultado["custo"] += self.custo_validacao
        resultado["tempo_execucao"] += self.tempo_validacao
        resultado["tipo"] = f"{resultado['tipo']}_com_validacao"
        
        return resultado
    
    def _validar_dados(self, dados: Any) -> Dict[str, Any]:
        """Valida os dados de entrada."""
        erros = []
        dados_str = str(dados)
        
        if "tamanho_minimo" in self.regras_validacao and len(dados_str) < 10:
            erros.append("Dados muito curtos (mínimo 10 caracteres)")
        
        if "formato_valido" in self.regras_validacao:
            if not any(c.isalpha() or c.isdigit() for c in dados_str):
                erros.append("Formato inválido - deve conter caracteres alfanuméricos")
        
        if "sem_caracteres_especiais" in self.regras_validacao:
            caracteres_especiais = "!@#$%^&*()_+=[]{}|;:,.<>?"
            if any(c in caracteres_especiais for c in dados_str):
                erros.append("Dados contêm caracteres especiais não permitidos")
        
        return {
            "valido": len(erros) == 0,
            "erros": erros,
            "regras_aplicadas": self.regras_validacao
        }


class AnaliseComRelatorio(AnaliseDecorator):
    """Decorator que adiciona geração de relatórios."""
    
    def __init__(self, analise: AnaliseBioInterface, formato: str = "pdf"):
        super().__init__(analise)
        self.formato = formato
        self.custo_relatorio = 50.0
        self.tempo_relatorio = 10.0
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa análise com relatório."""
        # Executa análise original
        resultado = self._analise.executar(dados)
        
        # Gera relatório
        relatorio = self._gerar_relatorio(resultado)
        
        # Adiciona informações do relatório
        resultado["relatorio"] = relatorio
        resultado["custo"] += self.custo_relatorio
        resultado["tempo_execucao"] += self.tempo_relatorio
        resultado["tipo"] = f"{resultado['tipo']}_com_relatorio"
        
        return resultado
    
    def _gerar_relatorio(self, resultado_analise: Dict[str, Any]) -> Dict[str, Any]:
        """Gera relatório detalhado."""
        return {
            "formato": self.formato,
            "titulo": f"Relatório de {resultado_analise.get('nome', 'Análise')}",
            "data_geracao": self._obter_data_atual(),
            "resumo": self._criar_resumo(resultado_analise),
            "detalhes": self._criar_detalhes(resultado_analise),
            "conclusoes": self._criar_conclusoes(resultado_analise)
        }
    
    def _obter_data_atual(self) -> str:
        """Obtém data atual formatada."""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def _criar_resumo(self, resultado: Dict[str, Any]) -> str:
        """Cria resumo do relatório."""
        return f"""Análise do tipo {resultado.get('tipo', 'desconhecido')} 
        executada com status {resultado.get('status', 'desconhecido')}. 
        Custo total: R${resultado.get('custo', 0):.2f}"""
    
    def _criar_detalhes(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Cria seção de detalhes do relatório."""
        return {
            "dados_processados": resultado.get("dados_processados", 0),
            "tempo_execucao": resultado.get("tempo_execucao", 0),
            "resultado_principal": resultado.get("resultado", "N/A")
        }
    
    def _criar_conclusoes(self, resultado: Dict[str, Any]) -> List[str]:
        """Cria conclusões baseadas nos resultados."""
        conclusoes = []
        
        if resultado.get("status") == "concluída":
            conclusoes.append("Análise executada com sucesso")
        
        if resultado.get("custo", 0) > 200:
            conclusoes.append("Custo elevado - considere otimização")
        
        if resultado.get("tempo_execucao", 0) > 60:
            conclusoes.append("Tempo de execução acima do esperado")
        
        return conclusoes


class AnaliseComCache(AnaliseDecorator):
    """Decorator que adiciona cache de resultados."""
    
    def __init__(self, analise: AnaliseBioInterface, tamanho_cache: int = 100):
        super().__init__(analise)
        self.cache = {}
        self.tamanho_cache = tamanho_cache
        self.cache_hits = 0
        self.cache_misses = 0
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa análise com cache."""
        chave_cache = self._gerar_chave_cache(dados)
        
        # Verifica se resultado está em cache
        if chave_cache in self.cache:
            self.cache_hits += 1
            resultado_cache = self.cache[chave_cache].copy()
            resultado_cache["cache_info"] = {
                "hit": True,
                "chave": chave_cache,
                "taxa_hit": self._calcular_taxa_hit()
            }
            return resultado_cache
        
        # Executa análise original
        self.cache_misses += 1
        resultado = self._analise.executar(dados)
        
        # Armazena em cache
        self._armazenar_cache(chave_cache, resultado)
        
        # Adiciona informações do cache
        resultado["cache_info"] = {
            "hit": False,
            "chave": chave_cache,
            "taxa_hit": self._calcular_taxa_hit()
        }
        
        return resultado
    
    def _gerar_chave_cache(self, dados: Any) -> str:
        """Gera chave única para os dados."""
        import hashlib
        dados_str = str(dados)
        return hashlib.md5(dados_str.encode()).hexdigest()
    
    def _armazenar_cache(self, chave: str, resultado: Dict[str, Any]) -> None:
        """Armazena resultado em cache."""
        # Remove item mais antigo se cache estiver cheio
        if len(self.cache) >= self.tamanho_cache:
            chave_antiga = next(iter(self.cache))
            del self.cache[chave_antiga]
        
        # Armazena nova entrada
        self.cache[chave] = resultado.copy()
    
    def _calcular_taxa_hit(self) -> float:
        """Calcula taxa de cache hit."""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    def limpar_cache(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0


class AnaliseComLog(AnaliseDecorator):
    """Decorator que adiciona logging das operações."""
    
    def __init__(self, analise: AnaliseBioInterface, nivel_log: str = "INFO"):
        super().__init__(analise)
        self.nivel_log = nivel_log
        self.logs = []
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa análise com logging."""
        import time
        
        # Registra início
        inicio = time.time()
        self._registrar_log("INICIO", f"Iniciando análise com {len(str(dados))} caracteres")
        
        try:
            # Executa análise original
            resultado = self._analise.executar(dados)
            
            # Registra sucesso
            fim = time.time()
            tempo_exec = fim - inicio
            self._registrar_log("SUCESSO", 
                              f"Análise concluída em {tempo_exec:.2f}s. "
                              f"Status: {resultado.get('status', 'desconhecido')}")
            
            # Adiciona informações de log ao resultado
            resultado["log_info"] = {
                "nivel": self.nivel_log,
                "total_logs": len(self.logs),
                "logs_recentes": self.logs[-5:]  # Últimos 5 logs
            }
            
            return resultado
            
        except Exception as e:
            # Registra erro
            fim = time.time()
            tempo_exec = fim - inicio
            self._registrar_log("ERRO", f"Erro após {tempo_exec:.2f}s: {str(e)}")
            
            return {
                "tipo": "erro",
                "status": "falha",
                "erro": str(e),
                "tempo_execucao": tempo_exec,
                "log_info": {
                    "nivel": self.nivel_log,
                    "total_logs": len(self.logs),
                    "logs_recentes": self.logs[-5:]
                }
            }
    
    def _registrar_log(self, tipo: str, mensagem: str) -> None:
        """Registra uma entrada de log."""
        import datetime
        entrada_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "nivel": self.nivel_log,
            "tipo": tipo,
            "mensagem": mensagem
        }
        self.logs.append(entrada_log)
        
        # Mantém apenas últimos 1000 logs
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
    
    def obter_logs(self, limite: int = 50) -> List[Dict[str, Any]]:
        """Obtém logs registrados."""
        return self.logs[-limite:]


class AnaliseComNotificacao(AnaliseDecorator):
    """Decorator que adiciona sistema de notificações."""
    
    def __init__(self, analise: AnaliseBioInterface, emails: List[str] = None):
        super().__init__(analise)
        self.emails = emails or []
        self.notificacoes_enviadas = []
    
    def executar(self, dados: Any) -> Dict[str, Any]:
        """Executa análise com notificações."""
        # Executa análise original
        resultado = self._analise.executar(dados)
        
        # Envia notificações baseadas no resultado
        notificacoes = self._processar_notificacoes(resultado)
        
        # Adiciona informações de notificação
        resultado["notificacoes"] = {
            "emails_configurados": len(self.emails),
            "notificacoes_enviadas": len(notificacoes),
            "detalhes": notificacoes
        }
        
        return resultado
    
    def _processar_notificacoes(self, resultado: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processa e envia notificações."""
        notificacoes = []
        
        # Notificação de conclusão
        if resultado.get("status") == "concluída":
            notificacao = {
                "tipo": "conclusao",
                "mensagem": f"Análise {resultado.get('nome', 'desconhecida')} concluída com sucesso",
                "destinatarios": self.emails,
                "enviada": True
            }
            notificacoes.append(notificacao)
            self.notificacoes_enviadas.append(notificacao)
        
        # Notificação de erro
        if resultado.get("status") == "erro":
            notificacao = {
                "tipo": "erro",
                "mensagem": f"Erro na análise: {resultado.get('erro', 'Erro desconhecido')}",
                "destinatarios": self.emails,
                "enviada": True
            }
            notificacoes.append(notificacao)
            self.notificacoes_enviadas.append(notificacao)
        
        # Notificação de custo elevado
        if resultado.get("custo", 0) > 300:
            notificacao = {
                "tipo": "alerta_custo",
                "mensagem": f"Custo elevado detectado: R${resultado.get('custo', 0):.2f}",
                "destinatarios": self.emails,
                "enviada": True
            }
            notificacoes.append(notificacao)
            self.notificacoes_enviadas.append(notificacao)
        
        return notificacoes


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Análise Básica ===")
    
    # Análise básica
    analise_base = AnaliseBasica("Análise de DNA")
    dados_teste = "ATCGATCGATCGATCGATCGATCGATCG"
    
    resultado_base = analise_base.executar(dados_teste)
    print("Resultado análise básica:")
    for chave, valor in resultado_base.items():
        print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 2: Análise com Validação ===")
    
    # Adicionando validação
    analise_validada = AnaliseComValidacao(analise_base)
    resultado_validado = analise_validada.executar(dados_teste)
    
    print("Resultado análise validada:")
    for chave, valor in resultado_validado.items():
        if chave != "validacao":
            print(f"  {chave}: {valor}")
    print(f"  Validação: {resultado_validado['validacao']}")
    
    # Teste com dados inválidos
    dados_invalidos = "ABC"
    resultado_invalido = analise_validada.executar(dados_invalidos)
    print(f"\nResultado com dados inválidos: {resultado_invalido['status']}")
    print(f"Erros: {resultado_invalido['erros']}")
    
    print("\n=== Exemplo 3: Composição Múltipla de Decorators ===")
    
    # Análise com múltiplas camadas
    analise_completa = AnaliseComRelatorio(
        AnaliseComValidacao(
            AnaliseComLog(
                AnaliseBasica("Análise Completa")
            )
        )
    )
    
    resultado_completo = analise_completa.executar(dados_teste)
    print("Resultado análise completa:")
    print(f"  Tipo: {resultado_completo['tipo']}")
    print(f"  Custo: R${resultado_completo['custo']:.2f}")
    print(f"  Tempo: {resultado_completo['tempo_execucao']:.1f} min")
    print(f"  Tem relatório: {'relatorio' in resultado_completo}")
    print(f"  Tem validação: {'validacao' in resultado_completo}")
    print(f"  Tem log: {'log_info' in resultado_completo}")
    
    print("\n=== Exemplo 4: Análise com Cache ===")
    
    # Análise com cache
    analise_cache = AnaliseComCache(AnaliseBasica("Análise Cache"))
    
    # Primeira execução (cache miss)
    resultado1 = analise_cache.executar(dados_teste)
    print(f"Primeira execução - Cache hit: {resultado1['cache_info']['hit']}")
    print(f"Taxa de hit: {resultado1['cache_info']['taxa_hit']:.1f}%")
    
    # Segunda execução (cache hit)
    resultado2 = analise_cache.executar(dados_teste)
    print(f"Segunda execução - Cache hit: {resultado2['cache_info']['hit']}")
    print(f"Taxa de hit: {resultado2['cache_info']['taxa_hit']:.1f}%")
    
    # Terceira execução com dados diferentes
    resultado3 = analise_cache.executar("GCTAGCTAGCTAGCTAGCTA")
    print(f"Terceira execução - Cache hit: {resultado3['cache_info']['hit']}")
    print(f"Taxa de hit: {resultado3['cache_info']['taxa_hit']:.1f}%")
    
    print("\n=== Exemplo 5: Análise com Notificações ===")
    
    # Análise com notificações
    analise_notificacao = AnaliseComNotificacao(
        AnaliseBasica("Análise Crítica"),
        emails=["pesquisador@lab.com", "supervisor@lab.com"]
    )
    
    resultado_notificacao = analise_notificacao.executar(dados_teste)
    print("Resultado com notificações:")
    print(f"  Notificações enviadas: {resultado_notificacao['notificacoes']['notificacoes_enviadas']}")
    for notif in resultado_notificacao['notificacoes']['detalhes']:
        print(f"    - {notif['tipo']}: {notif['mensagem']}")
    
    print("\n=== Exemplo 6: Pipeline Completo de Análise ===")
    
    # Pipeline completo com todos os decorators
    pipeline_analise = AnaliseComNotificacao(
        AnaliseComRelatorio(
            AnaliseComCache(
                AnaliseComValidacao(
                    AnaliseComLog(
                        AnaliseBasica("Pipeline Bioinformática")
                    )
                ),
                tamanho_cache=50
            ),
            formato="html"
        ),
        emails=["bioinfo@lab.com"]
    )
    
    resultado_pipeline = pipeline_analise.executar(dados_teste)
    
    print("Pipeline completo:")
    print(f"  Tipo final: {resultado_pipeline['tipo']}")
    print(f"  Custo total: R${resultado_pipeline['custo']:.2f}")
    print(f"  Tempo total: {resultado_pipeline['tempo_execucao']:.1f} min")
    print(f"  Features: Validação ✓ Cache ✓ Log ✓ Relatório ✓ Notificação ✓")
    
    print("\nDecorator pattern implementado com sucesso!")
