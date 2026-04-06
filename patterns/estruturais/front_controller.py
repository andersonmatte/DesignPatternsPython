from typing import Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
import time
import logging
from functools import wraps


# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Request:
    """Representa uma requisição ao sistema."""
    
    def __init__(self, path: str, method: str = "GET", params: Dict[str, Any] = None, 
                 headers: Dict[str, str] = None, body: str = ""):
        self.path = path
        self.method = method.upper()
        self.params = params or {}
        self.headers = headers or {}
        self.body = body
        self.timestamp = time.time()
        self.session_id = self._gerar_session_id()
    
    def _gerar_session_id(self) -> str:
        """Gera ID de sessão único."""
        import uuid
        return str(uuid.uuid4())
    
    def __str__(self) -> str:
        return f"Request({self.method} {self.path}, params={self.params})"


class Response:
    """Representa uma resposta do sistema."""
    
    def __init__(self, status_code: int = 200, content: str = "", 
                 headers: Dict[str, str] = None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {}
        self.timestamp = time.time()
    
    def set_json(self, data: Dict[str, Any]) -> None:
        """Define conteúdo como JSON."""
        import json
        self.content = json.dumps(data, indent=2)
        self.headers["Content-Type"] = "application/json"
    
    def set_error(self, message: str, status_code: int = 500) -> None:
        """Define resposta de erro."""
        self.status_code = status_code
        self.content = f"{{\"error\": \"{message}\"}}"
        self.headers["Content-Type"] = "application/json"
    
    def __str__(self) -> str:
        return f"Response({self.status_code}, content_length={len(self.content)})"


class Command(ABC):
    """Interface base para comandos do sistema."""
    
    @abstractmethod
    def execute(self, request: Request) -> Response:
        """Executa o comando."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome do comando."""
        pass


class SequenciamentoCommand(Command):
    """Comando para operações de sequenciamento."""
    
    def execute(self, request: Request) -> Response:
        """Executa operação de sequenciamento."""
        response = Response()
        
        try:
            # Validação de parâmetros
            amostra = request.params.get("amostra")
            plataforma = request.params.get("plataforma", "illumina")
            
            if not amostra:
                response.set_error("Parâmetro 'amostra' é obrigatório", 400)
                return response
            
            # Simulação de processamento
            logger.info(f"Iniciando sequenciamento da amostra {amostra} com {plataforma}")
            
            # Processamento simulado
            resultado = self._processar_sequenciamento(amostra, plataforma)
            
            response.set_json({
                "status": "sucesso",
                "operacao": "sequenciamento",
                "amostra": amostra,
                "plataforma": plataforma,
                "resultado": resultado,
                "timestamp": time.time()
            })
            
            logger.info(f"Sequenciamento concluído para amostra {amostra}")
            
        except Exception as e:
            logger.error(f"Erro no sequenciamento: {str(e)}")
            response.set_error(f"Erro no sequenciamento: {str(e)}", 500)
        
        return response
    
    def get_name(self) -> str:
        return "sequenciamento"
    
    def _processar_sequenciamento(self, amostra: str, plataforma: str) -> Dict[str, Any]:
        """Processa o sequenciamento (simulado)."""
        time.sleep(0.1)  # Simula tempo de processamento
        
        return {
            "reads_gerados": 50000000 if plataforma == "illumina" else 1000000,
            "qualidade": "Q30" if plataforma == "illumina" else "Q15",
            "tempo_estimado": "12 horas" if plataforma == "illumina" else "24 horas",
            "arquivo_saida": f"sequenciamento_{amostra}_{plataforma}.fastq"
        }


class AlinhamentoCommand(Command):
    """Comando para operações de alinhamento."""
    
    def execute(self, request: Request) -> Response:
        """Executa operação de alinhamento."""
        response = Response()
        
        try:
            # Validação
            arquivo_fastq = request.params.get("arquivo_fastq")
            referencia = request.params.get("referencia", "hg38")
            
            if not arquivo_fastq:
                response.set_error("Parâmetro 'arquivo_fastq' é obrigatório", 400)
                return response
            
            logger.info(f"Iniciando alinhamento de {arquivo_fastq} contra {referencia}")
            
            # Processamento simulado
            resultado = self._processar_alinhamento(arquivo_fastq, referencia)
            
            response.set_json({
                "status": "sucesso",
                "operacao": "alinhamento",
                "arquivo_fastq": arquivo_fastq,
                "referencia": referencia,
                "resultado": resultado,
                "timestamp": time.time()
            })
            
            logger.info(f"Alinhamento concluído para {arquivo_fastq}")
            
        except Exception as e:
            logger.error(f"Erro no alinhamento: {str(e)}")
            response.set_error(f"Erro no alinhamento: {str(e)}", 500)
        
        return response
    
    def get_name(self) -> str:
        return "alinhamento"
    
    def _processar_alinhamento(self, arquivo: str, referencia: str) -> Dict[str, Any]:
        """Processa o alinhamento (simulado)."""
        time.sleep(0.15)  # Simula tempo de processamento
        
        return {
            "taxa_alinhamento": 98.5,
            "cobertura": 95.2,
            "arquivo_bam": f"alinhado_{arquivo.replace('.fastq', '.bam')}",
            "arquivo_indice": f"alinhado_{arquivo.replace('.fastq', '.bai')}",
            "tempo_processamento": "3 horas"
        }


class AnaliseVariacaoCommand(Command):
    """Comando para análise de variação genética."""
    
    def execute(self, request: Request) -> Response:
        """Executa análise de variação."""
        response = Response()
        
        try:
            arquivo_bam = request.params.get("arquivo_bam")
            tipo_analise = request.params.get("tipo", "padrao")
            
            if not arquivo_bam:
                response.set_error("Parâmetro 'arquivo_bam' é obrigatório", 400)
                return response
            
            logger.info(f"Iniciando análise de variação em {arquivo_bam}")
            
            resultado = self._processar_variacao(arquivo_bam, tipo_analise)
            
            response.set_json({
                "status": "sucesso",
                "operacao": "analise_variacao",
                "arquivo_bam": arquivo_bam,
                "tipo_analise": tipo_analise,
                "resultado": resultado,
                "timestamp": time.time()
            })
            
            logger.info(f"Análise de variação concluída para {arquivo_bam}")
            
        except Exception as e:
            logger.error(f"Erro na análise de variação: {str(e)}")
            response.set_error(f"Erro na análise de variação: {str(e)}", 500)
        
        return response
    
    def get_name(self) -> str:
        return "analise_variacao"
    
    def _processar_variacao(self, arquivo: str, tipo: str) -> Dict[str, Any]:
        """Processa análise de variação (simulado)."""
        time.sleep(0.2)  # Simula tempo de processamento
        
        return {
            "variantes_encontradas": 4500 if tipo == "padrao" else 8000,
            "snp_count": 4200 if tipo == "padrao" else 7500,
            "indel_count": 300 if tipo == "padrao" else 500,
            "variantes_raras": 150 if tipo == "padrao" else 300,
            "arquivo_vcf": f"variantes_{arquivo.replace('.bam', '.vcf')}",
            "tempo_processamento": "2 horas"
        }


class RelatorioCommand(Command):
    """Comando para geração de relatórios."""
    
    def execute(self, request: Request) -> Response:
        """Executa geração de relatório."""
        response = Response()
        
        try:
            tipo_relatorio = request.params.get("tipo", "variacao")
            dados_analise = request.params.get("dados_analise")
            formato = request.params.get("formato", "pdf")
            
            logger.info(f"Gerando relatório do tipo {tipo_relatorio} em formato {formato}")
            
            resultado = self._gerar_relatorio(tipo_relatorio, dados_analise, formato)
            
            response.set_json({
                "status": "sucesso",
                "operacao": "relatorio",
                "tipo_relatorio": tipo_relatorio,
                "formato": formato,
                "resultado": resultado,
                "timestamp": time.time()
            })
            
            logger.info(f"Relatório gerado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro na geração de relatório: {str(e)}")
            response.set_error(f"Erro na geração de relatório: {str(e)}", 500)
        
        return response
    
    def get_name(self) -> str:
        return "relatorio"
    
    def _gerar_relatorio(self, tipo: str, dados: Any, formato: str) -> Dict[str, Any]:
        """Gera relatório (simulado)."""
        time.sleep(0.05)  # Simula tempo de processamento
        
        return {
            "titulo": f"Relatório de {tipo.replace('_', ' ').title()}",
            "formato": formato.upper(),
            "paginas": 15 if formato == "pdf" else 10,
            "arquivo_saida": f"relatorio_{tipo}_{int(time.time())}.{formato}",
            "resumo": f"Relatório gerado com base na análise de {tipo}"
        }


class Dispatcher:
    """Dispatcher para rotear requisições para comandos apropriados."""
    
    def __init__(self):
        self.commands: Dict[str, Command] = {}
        self.middleware_stack = []
    
    def register_command(self, path: str, command: Command) -> None:
        """Registra um comando para um path específico."""
        self.commands[path] = command
        logger.info(f"Comando '{command.get_name()}' registrado para path '{path}'")
    
    def add_middleware(self, middleware_func: Callable) -> None:
        """Adiciona middleware ao stack."""
        self.middleware_stack.append(middleware_func)
    
    def dispatch(self, request: Request) -> Response:
        """Despacha requisição para comando apropriado."""
        logger.info(f"Despachando requisição: {request.method} {request.path}")
        
        # Aplica middleware antes do processamento
        for middleware in self.middleware_stack:
            result = middleware(request)
            if isinstance(result, Response):
                return result  # Middleware pode retornar resposta diretamente
        
        # Encontra comando apropriado
        command = self._find_command(request.path)
        
        if not command:
            response = Response(404)
            response.set_error(f"Path não encontrado: {request.path}", 404)
            return response
        
        # Executa comando
        try:
            response = command.execute(request)
            logger.info(f"Comando '{command.get_name()}' executado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao executar comando '{command.get_name()}': {str(e)}")
            response = Response(500)
            response.set_error(f"Erro interno: {str(e)}", 500)
        
        return response
    
    def _find_command(self, path: str) -> Optional[Command]:
        """Encontra comando para o path."""
        # Match exato
        if path in self.commands:
            return self.commands[path]
        
        # Match por padrão
        for registered_path, command in self.commands.items():
            if self._path_matches(path, registered_path):
                return command
        
        return None
    
    def _path_matches(self, request_path: str, pattern: str) -> bool:
        """Verifica se path corresponde ao padrão."""
        # Simplificação - apenas prefix matching
        return request_path.startswith(pattern.rstrip('/'))


class FrontController:
    """Controlador frontal centralizado."""
    
    def __init__(self):
        self.dispatcher = Dispatcher()
        self.setup_commands()
        self.setup_middleware()
        self.request_stats = {
            "total_requests": 0,
            "requests_by_path": {},
            "errors": 0,
            "avg_response_time": 0.0
        }
    
    def setup_commands(self) -> None:
        """Configura os comandos disponíveis."""
        self.dispatcher.register_command("/sequenciamento/executar", SequenciamentoCommand())
        self.dispatcher.register_command("/alinhamento/executar", AlinhamentoCommand())
        self.dispatcher.register_command("/analise/variacao", AnaliseVariacaoCommand())
        self.dispatcher.register_command("/relatorio/gerar", RelatorioCommand())
        
        # Padrões
        self.dispatcher.register_command("/sequenciamento", SequenciamentoCommand())
        self.dispatcher.register_command("/alinhamento", AlinhamentoCommand())
        self.dispatcher.register_command("/analise", AnaliseVariacaoCommand())
        self.dispatcher.register_command("/relatorio", RelatorioCommand())
    
    def setup_middleware(self) -> None:
        """Configura middleware."""
        self.dispatcher.add_middleware(self._auth_middleware)
        self.dispatcher.add_middleware(self._logging_middleware)
        self.dispatcher.add_middleware(self._rate_limit_middleware)
        self.dispatcher.add_middleware(self._validation_middleware)
    
    def processar_requisicao(self, path: str, method: str = "GET", 
                             params: Dict[str, Any] = None) -> Response:
        """Processa requisição através do front controller."""
        start_time = time.time()
        
        # Cria requisição
        request = Request(path, method, params)
        
        # Atualiza estatísticas
        self.request_stats["total_requests"] += 1
        path_key = path.split('/')[1] if '/' in path else path
        self.request_stats["requests_by_path"][path_key] = \
            self.request_stats["requests_by_path"].get(path_key, 0) + 1
        
        # Processa requisição
        response = self.dispatcher.dispatch(request)
        
        # Atualiza estatísticas de erro
        if response.status_code >= 400:
            self.request_stats["errors"] += 1
        
        # Atualiza tempo médio de resposta
        response_time = time.time() - start_time
        total_requests = self.request_stats["total_requests"]
        current_avg = self.request_stats["avg_response_time"]
        self.request_stats["avg_response_time"] = \
            (current_avg * (total_requests - 1) + response_time) / total_requests
        
        logger.info(f"Requisição processada em {response_time:.3f}s")
        
        return response
    
    def _auth_middleware(self, request: Request) -> Optional[Response]:
        """Middleware de autenticação."""
        # Simulação de autenticação
        api_key = request.headers.get("API-Key")
        
        if not api_key:
            response = Response(401)
            response.set_error("API-Key é obrigatória", 401)
            return response
        
        if api_key != "bioinfo-api-key-123":
            response = Response(403)
            response.set_error("API-Key inválida", 403)
            return response
        
        return None
    
    def _logging_middleware(self, request: Request) -> Optional[Response]:
        """Middleware de logging."""
        logger.info(f"[{request.session_id}] {request.method} {request.path}")
        logger.debug(f"Params: {request.params}")
        return None
    
    def _rate_limit_middleware(self, request: Request) -> Optional[Response]:
        """Middleware de rate limiting."""
        # Simulação simples de rate limiting
        # Em um sistema real, usaria Redis ou similar
        return None
    
    def _validation_middleware(self, request: Request) -> Optional[Response]:
        """Middleware de validação."""
        # Validações básicas
        if not request.path or not request.path.startswith('/'):
            response = Response(400)
            response.set_error("Path inválido", 400)
            return response
        
        return None
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema."""
        return self.request_stats.copy()
    
    def listar_endpoints(self) -> Dict[str, str]:
        """Lista todos os endpoints disponíveis."""
        return {
            path: command.get_name() 
            for path, command in self.dispatcher.commands.items()
        }


# Exemplo de uso
if __name__ == "__main__":
    print("=== Exemplo 1: Uso Básico do Front Controller ===")
    
    # Criar front controller
    front_controller = FrontController()
    
    print("Endpoints disponíveis:")
    for path, command in front_controller.listar_endpoints().items():
        print(f"  {path} -> {command}")
    
    print("\n=== Exemplo 2: Processando Requisições ===")
    
    # Requisição de sequenciamento
    print("\n1. Requisição de sequenciamento:")
    response1 = front_controller.processar_requisicao(
        "/sequenciamento/executar",
        "POST",
        {
            "amostra": "Paciente_001",
            "plataforma": "illumina"
        },
        headers={"API-Key": "bioinfo-api-key-123"}
    )
    
    print(f"Status: {response1.status_code}")
    print(f"Conteúdo: {response1.content[:200]}...")
    
    # Requisição de alinhamento
    print("\n2. Requisição de alinhamento:")
    response2 = front_controller.processar_requisicao(
        "/alinhamento/executar",
        "POST",
        {
            "arquivo_fastq": "sequenciamento_Paciente_001.fastq",
            "referencia": "hg38"
        },
        headers={"API-Key": "bioinfo-api-key-123"}
    )
    
    print(f"Status: {response2.status_code}")
    print(f"Conteúdo: {response2.content[:200]}...")
    
    # Requisição de análise
    print("\n3. Requisição de análise de variação:")
    response3 = front_controller.processar_requisicao(
        "/analise/variacao",
        "POST",
        {
            "arquivo_bam": "alinhado_sequenciamento_Paciente_001.bam",
            "tipo": "padrao"
        },
        headers={"API-Key": "bioinfo-api-key-123"}
    )
    
    print(f"Status: {response3.status_code}")
    print(f"Conteúdo: {response3.content[:200]}...")
    
    # Requisição de relatório
    print("\n4. Requisição de relatório:")
    response4 = front_controller.processar_requisicao(
        "/relatorio/gerar",
        "POST",
        {
            "tipo_relatorio": "variacao",
            "formato": "pdf"
        },
        headers={"API-Key": "bioinfo-api-key-123"}
    )
    
    print(f"Status: {response4.status_code}")
    print(f"Conteúdo: {response4.content[:200]}...")
    
    print("\n=== Exemplo 3: Tratamento de Erros ===")
    
    # Requisição sem API-Key
    print("\n1. Requisição sem autenticação:")
    response_erro1 = front_controller.processar_requisicao(
        "/sequenciamento/executar",
        "POST",
        {"amostra": "Teste"}
    )
    
    print(f"Status: {response_erro1.status_code}")
    print(f"Erro: {response_erro1.content}")
    
    # Requisição com API-Key inválida
    print("\n2. Requisição com API-Key inválida:")
    response_erro2 = front_controller.processar_requisicao(
        "/sequenciamento/executar",
        "POST",
        {"amostra": "Teste"},
        headers={"API-Key": "chave-invalida"}
    )
    
    print(f"Status: {response_erro2.status_code}")
    print(f"Erro: {response_erro2.content}")
    
    # Requisição para path inexistente
    print("\n3. Requisição para path inexistente:")
    response_erro3 = front_controller.processar_requisicao(
        "/endpoint/inexistente",
        "GET",
        {},
        headers={"API-Key": "bioinfo-api-key-123"}
    )
    
    print(f"Status: {response_erro3.status_code}")
    print(f"Erro: {response_erro3.content}")
    
    # Requisição com parâmetros inválidos
    print("\n4. Requisição com parâmetros inválidos:")
    response_erro4 = front_controller.processar_requisicao(
        "/sequenciamento/executar",
        "POST",
        {},  # Sem parâmetro obrigatório
        headers={"API-Key": "bioinfo-api-key-123"}
    )
    
    print(f"Status: {response_erro4.status_code}")
    print(f"Erro: {response_erro4.content}")
    
    print("\n=== Exemplo 4: Estatísticas do Sistema ===")
    
    # Processar mais algumas requisições para gerar estatísticas
    for i in range(5):
        front_controller.processar_requisicao(
            "/sequenciamento",
            "POST",
            {"amostra": f"Teste_{i}"},
            headers={"API-Key": "bioinfo-api-key-123"}
        )
    
    stats = front_controller.obter_estatisticas()
    print("Estatísticas do sistema:")
    for chave, valor in stats.items():
        if isinstance(valor, float):
            print(f"  {chave}: {valor:.3f}")
        else:
            print(f"  {chave}: {valor}")
    
    print("\n=== Exemplo 5: Pipeline Completo ===")
    
    print("\nExecutando pipeline completo de análise bioinformática:")
    
    # Pipeline: Sequenciamento -> Alinhamento -> Análise -> Relatório
    pipeline_steps = [
        ("/sequenciamento/executar", {"amostra": "Pipeline_Test", "plataforma": "illumina"}),
        ("/alinhamento/executar", {"arquivo_fastq": "sequenciamento_Pipeline_Test.fastq", "referencia": "hg38"}),
        ("/analise/variacao", {"arquivo_bam": "alinhado_sequenciamento_Pipeline_Test.bam", "tipo": "completo"}),
        ("/relatorio/gerar", {"tipo_relatorio": "variacao", "formato": "html"})
    ]
    
    results = []
    for step, params in pipeline_steps:
        print(f"\nExecutando: {step}")
        response = front_controller.processar_requisicao(
            step, "POST", params, headers={"API-Key": "bioinfo-api-key-123"}
        )
        print(f"  Status: {response.status_code}")
        results.append(response)
    
    print(f"\nPipeline concluído! {len(results)} etapas processadas.")
    
    print("\nFront Controller pattern implementado com sucesso!")
