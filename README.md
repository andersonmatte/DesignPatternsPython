# Design Patterns em Python - Sistema de Bioinformática

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Patterns](https://img.shields.io/badge/Design_Patterns-23-blue.svg)
![Bioinformatics](https://img.shields.io/badge/Bioinformatics-Genomics-orange.svg)

Este projeto demonstra a implementação de padrões de projeto (Design Patterns) em Python, aplicados a um sistema de bioinformática para análise genômica e proteômica.

## Contexto do Sistema

O sistema simula um laboratório de bioinformática que realiza:

- **Sequenciamento de DNA/RNA** - Análise de material genético
- **Alinhamento de sequências** - Comparação com bases de dados de referência
- **Análise proteômica** - Estudo de proteínas e suas funções
- **Geração de relatórios** - Documentação dos resultados analíticos
- **Gerenciamento de equipamentos** - Controle de recursos laboratoriais

---

## Estrutura do Projeto

```
DesignPatternsPython/
├── patterns/                    # Implementações dos padrões
│   ├── criacionais/            # Padrões criacionais
│   │   ├── factory_method.py   # Factory Method
│   │   ├── abstract_factory.py # Abstract Factory
│   │   ├── builder.py          # Builder
│   │   ├── prototype.py        # Prototype
│   │   └── singleton.py        # Singleton
│   ├── estruturais/           # Padrões estruturais
│   │   ├── adapter.py          # Adapter
│   │   ├── bridge.py           # Bridge
│   │   ├── composite.py        # Composite
│   │   ├── decorator.py        # Decorator
│   │   ├── facade.py           # Facade
│   │   ├── flyweight.py        # Flyweight
│   │   └── proxy.py            # Proxy
│   ├── comportamentais/        # Padrões comportamentais
│   │   ├── chain_of_responsibility.py # Chain of Responsibility
│   │   ├── command.py          # Command
│   │   ├── iterator.py         # Iterator
│   │   ├── mediator.py         # Mediator
│   │   ├── memento.py          # Memento
│   │   ├── observer.py         # Observer
│   │   ├── state.py            # State
│   │   ├── strategy.py         # Strategy
│   │   ├── template_method.py  # Template Method
│   │   └── visitor.py          # Visitor
├── domain/                     # Classes de domínio
│   ├── __init__.py
│   ├── amostra_biologica.py  # Modelos de amostras biológicas
│   └── analise.py            # Modelos de análises
├── tests/                      # Testes unitários
│   ├── __init__.py
│   ├── test_factory_method.py  # 12 testes - Factory Method
│   ├── test_singleton.py        # 8 testes - Singleton
│   ├── test_observer.py         # 15 testes - Observer
│   ├── test_abstract_factory.py # 12 testes - Abstract Factory
│   ├── test_builder.py          # 15 testes - Builder
│   ├── test_prototype.py        # 18 testes - Prototype
│   ├── test_multiton.py         # 20 testes - Multiton
│   ├── test_object_pool.py      # 20 testes - Object Pool
│   ├── test_adapter.py          # 25 testes - Adapter
│   ├── test_command.py          # 25 testes - Command
│   ├── test_iterator.py         # 30 testes - Iterator
│   └── test_all_patterns.py     # Suite completa (200+ testes)
├── requirements.txt             # Dependências do projeto
└── README.md                  # Este arquivo
```

---

## Padrões Criacionais

### Factory Method

**Propósito:** Definir interface para criar objeto, mas deixar subclasses decidirem qual classe instanciar.

**Implementação:** Criação de analisadores especializados baseados no tipo de dado:

- **Analisador FASTA:** Especializado em formato FASTA
- **Analisador GenBank:** Especializado em formato GenBank
- **Factory Method:** Delegação para subclasses específicas

```python
# Exemplo: Criação baseada no tipo de formato
analisador = AnalisadorFactory().criar_analisador("FASTA")
resultado = analisador.analisar_sequencia("ATCGATCG")
```

### Abstract Factory

**Propósito:** Criar famílias de objetos relacionados sem especificar suas classes concretas.

**Implementação:** Sistema cria diferentes tipos de equipamentos laboratoriais:

- **Genética:** Equipamentos para análise de DNA/RNA
- **Bioquímica:** Equipamentos para análise química
- **Molecular:** Equipamentos para análise molecular

```python
# Exemplo: Factory cria equipamentos especializados
factory = EquipamentoLaboratorialFactory.get_factory("genetica")
centrifuga = factory.criar_centrifuga()
```

### Builder

**Propósito:** Separar a construção de objetos complexos de sua representação.

**Implementação:** Construção de protocolos experimentais com múltiplos parâmetros:

- Nome do pesquisador
- Volume da amostra
- Tipo de análise
- Metodologia utilizada

```python
# Exemplo: Construção incremental de protocolo
protocolo = (GeradorDeProtocolo()
               .com_nome_pesquisador("Dr. Ana Silva")
               .com_volume_amostra(15.5)
               .com_tipo_analise("Sequenciamento")
               .gerar())
```

### Prototype

**Propósito:** Criar novos objetos clonando objetos existentes.

**Implementação:** Clonagem de amostras biológicas para experimentos replicáveis:

- Preservação de dados genéticos
- Manutenção de marcadores
- Replicação de condições experimentais

```python
# Exemplo: Clonagem de amostra para múltiplos testes
amostra_original = AmostraBiologica("AMOSTRA_001")
amostra_clonada = amostra_original.clonar()
```

### Singleton

**Propósito:** Garantir que uma classe tenha apenas uma instância e fornecer ponto global de acesso.

**Implementação:** Gerenciador único de recursos laboratoriais:

- **Instância Única:** Apenas um gerenciador para todo o sistema
- **Acesso Global:** Ponto centralizado para obter recursos
- **Thread Safety:** Sincronização para ambientes concorrentes

```python
# Exemplo: Acesso único ao gerenciador de recursos
gerenciador = GerenciadorRecursos.get_instancia()
recurso = gerenciador.obter_recurso("Microscopio")
```

### Multiton

**Propósito:** Permitir múltiplas instâncias nomeadas com controle sobre sua criação.

**Implementação:** Pool de instâncias específicas de analisadores:

- **Instâncias Nomeadas:** Diferentes configurações por nome
- **Cache Controlado:** Gerenciamento do ciclo de vida
- **Reutilização:** Compartilhamento controlado de objetos

```python
# Exemplo: Instâncias nomeadas de analisadores
analisador1 = MultitonFactory.get_instancia("RAPIDO")
analisador2 = MultitonFactory.get_instancia("PRECISO")
```

### Object Pool

**Propósito:** Reutilizar objetos caros de criação, otimizando performance.

**Implementação:** Pool de equipamentos laboratoriais compartilhados:

- Centrífugas de alta velocidade
- Microscópios eletrônicos
- Sistema de alocação/liberação

```python
# Exemplo: Reutilização de equipamentos escassos
equipamento = pool.adquirir_equipamento()
# ... uso do equipamento ...
pool.liberar_equipamento(equipamento)
```

---

## Padrões Estruturais

### Adapter

**Propósito:** Permitir que interfaces incompatíveis trabalhem juntas.

**Implementação:** Adaptador unifica diferentes formatos de análise:

- **FASTA:** Formato padrão de sequências
- **GenBank:** Formato com metadados estruturados
- **Analisador Unificado:** Interface comum para todos os formatos

```python
# Exemplo: Adapter unificado para diferentes formatos
from patterns.estruturais.adapter import FabricaAdapters

factory = FabricaAdapters()
adapter = factory.criar_adapter("UNIFICADO")

# Detecta automaticamente o formato e analisa
resultado = adapter.analisar_sequencia(">seq1\nATCGATCGATCGATCG")
print(f"Formato detectado: {resultado['formato']}")
print(f"Sequência: {resultado['sequencia']}")
print(f"Comprimento: {resultado['comprimento']}")
```

### Bridge

**Propósito:** Desacoplar abstração da implementação, permitindo variação independente.

**Implementação:** Separação entre tipo de análise e algoritmo de processamento:

- **Análises Genômicas:** Sequenciamento, alinhamento, expressão
- **Algoritmos:** Needleman-Wunsch, BLAST, Smith-Waterman

```python
# Exemplo: Bridge separando análise e algoritmo
from patterns.estruturais.bridge import AnaliseSequenciamento, AlinhamentoGlobal

# Criar análise com algoritmo específico
analise = AnaliseSequenciamento(AlinhamentoGlobal())
resultado = analise.executar_analise("ATCGATCG", "referencia.fasta")

print(f"Tipo de análise: {resultado['tipo_analise']}")
print(f"Algoritmo usado: {resultado['algoritmo']}")
print(f"Score de alinhamento: {resultado['score']}")
```

### Composite

**Propósito:** Compor objetos em estruturas de árvore, tratando individuais e composições uniformemente.

**Implementação:** Estrutura hierárquica de sequências genéticas:

- **Genes:** Componentes complexos com múltiplos nucleotídeos
- **Nucleotídeos:** Componentes básicos individuais
- **Proteínas:** Componentes compostos

```python
# Exemplo: Composite para estrutura genômica
from patterns.estruturais.composite import Genoma, SequenciaNucleotidica, BaseNitrogenada

# Criar estrutura hierárquica
genoma = Genoma("Genoma Humano")
cromossomo1 = SequenciaNucleotidica("Cromossomo 1")
cromossomo1.adicionar_componente(BaseNitrogenada("A", 1000))
cromossomo1.adicionar_componente(BaseNitrogenada("T", 1001))
cromossomo1.adicionar_componente(BaseNitrogenada("C", 1002))
cromossomo1.adicionar_componente(BaseNitrogenada("G", 1003))

genoma.adicionar_componente(cromossomo1)

# Tratar uniformemente
print(f"Tamanho do genoma: {genoma.obter_tamanho()}")
print(f"Composição: {genoma.obter_composicao()}")
```

### Decorator

**Propósito:** Adicionar responsabilidades dinamicamente a objetos.

**Implementação:** Enriquecimento funcional de análises genômicas:

- **Análise Base:** Funcionalidade fundamental de análise
- **Com Validação:** Adição de verificação de dados
- **Com Relatório:** Adição de geração de relatórios
- **Composição:** Múltiplas camadas de funcionalidade

```python
# Exemplo: Decorator para enriquecer análise
from patterns.estruturais.decorator import (
    AnaliseBasica, AnaliseComValidacao, AnaliseComRelatorio, AnaliseComCache
)

# Criar análise base e adicionar decoradores
analise = AnaliseBasica("Análise Genômica")
analise = AnaliseComValidacao(analise)
analise = AnaliseComRelatorio(analise)
analise = AnaliseComCache(analise)

# Executar com todas as funcionalidades
resultado = analise.executar("dados_genomicos.fasta")
print(f"Resultado: {resultado['resultado']}")
print(f"Validado: {resultado['validado']}")
print(f"Relatório gerado: {resultado['relatorio']}")
print(f"Cache usado: {resultado['cache']}")
```

### Facade

**Propósito:** Fornecer interface simplificada para subsistemas complexos.

**Implementação:** Fachada unificada para análise genômica completa:

- **Sequenciamento:** Extração e preparação de amostras
- **Alinhamento:** Comparação com referências
- **Análise:** Processamento e interpretação
- **Relatório:** Geração de resultados

```python
# Exemplo: Facade simplificando sistema complexo
from patterns.estruturais.facade import SistemaBioinformaticaFacade

# Interface única para todo o processo
facade = SistemaBioinformaticaFacade()
resultado = facade.analisar_amostra_completa(
    amostra="sangue_paciente001",
    tipo_analise="genomica",
    referencia="hg38"
)

print(f"Status: {resultado['status']}")
print(f"Sequenciamento: {resultado['sequenciamento']['status']}")
print(f"Alinhamento: {resultado['alinhamento']['status']}")
print(f"Análise: {resultado['analise']['status']}")
print(f"Relatório: {resultado['relatorio']['arquivo']}")
```

### Flyweight

**Propósito:** Compartilhar estado intrínseco para otimizar uso de memória.

**Implementação:** Compartilhamento de dados genéticos entre múltiplas análises:

- **Dados Proteicos:** Sequências de aminoácidos compartilhadas
- **Estado Extrínseco:** Contexto específico de cada análise
- **Cache:** Reutilização eficiente de estruturas

```python
# Exemplo: Flyweight para otimizar memória
from patterns.estruturais.flyweight import (
    DadoGeneticoFlyweightFactory, AnaliseGenomicaComFlyweight
)

factory = DadoGeneticoFlyweightFactory()

# Reutilizar dados compartilhados
proteina1 = factory.obter_flyweight_proteico("Hemoglobina", "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNMIVIVLGHYKK")
proteina2 = factory.obter_flyweight_proteico("Hemoglobina", "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNMIVIVLGHYKK")

# Mesmo objeto compartilhado
print(f"Mesmo objeto: {proteina1 is proteina2}")

# Análise com contexto extrínseco
analise = AnaliseGenomicaComFlyweight()
resultado1 = analise.analisar_com_contexto(proteina1, {"paciente": "001", "data": "2023-01-01"})
resultado2 = analise.analisar_com_contexto(proteina2, {"paciente": "002", "data": "2023-01-02"})
```

### Front Controller

**Propósito:** Centralizar requisições e fornecer tratamento unificado.

**Implementação:** Controlador frontal para sistema de bioinformática:

- **Roteamento:** Direcionamento para módulos específicos
- **Validação:** Verificação de parâmetros e permissões
- **Tratamento:** Gerenciamento de erros e exceções

```python
# Exemplo: Front Controller centralizando requisições
from patterns.estruturais.front_controller import FrontController, Request

# Criar requisição
request = Request(
    method="POST",
    path="/analise/sequenciamento",
    headers={"Authorization": "Bearer token123"},
    body={"amostra": "paciente001", "plataforma": "illumina"}
)

# Processar através do controlador frontal
controller = FrontController()
response = controller.processar_requisicao(request)

print(f"Status: {response.status_code}")
print(f"Resultado: {response.body}")
print(f"Headers: {response.headers}")
```

### Proxy

**Propósito:** Controlar acesso a objetos, fornecendo interface intermediária.

**Implementação:** Proxy de segurança para banco de dados genéticos:

- **Controle de Acesso:** Validação de permissões de usuários
- **Cache:** Otimização de consultas frequentes
- **Logging:** Registro de operações de acesso

```python
# Exemplo: Proxy controlando acesso ao banco de dados
from patterns.estruturais.proxy import BancoDadosGeneticosProxy

# Criar proxy com controle de acesso
banco_proxy = BancoDadosGeneticosProxy()

# Tentar acesso sem permissão
try:
    resultado = banco_proxy.buscar_sequencia("BRCA1", "usuario_sem_permissao")
except PermissionError as e:
    print(f"Erro de acesso: {e}")

# Acesso com permissão
resultado = banco_proxy.buscar_sequencia("BRCA1", "pesquisador_autorizado")
print(f"Sequência encontrada: {resultado['sequencia'][:50]}...")
print(f"Cache usado: {resultado['cache']}")
print(f"Log registrado: {resultado['log_id']}")
```

**Propósito:** Fornecer interface simplificada para subsistemas complexos.

**Implementação:** Fachada unificada para análise genômica completa:

- **Sequenciamento:** Extração e preparação de amostras
- **Alinhamento:** Comparação com referências
- **Análise:** Processamento e interpretação
- **Relatório:** Geração de resultados

---

## Padrões Comportamentais

### Chain of Responsibility

**Propósito:** Passar requisições por uma corrente de handlers, onde cada um decide processar ou passar adiante.

**Implementação:** Pipeline de validação e processamento de sequências biológicas:

- **Validadores:** DNA, RNA e qualidade de sequências
- **Filtros:** Contaminação e complexidade
- **Processadores:** Análise final e geração de resultados

```python
# Exemplo: Chain of Responsibility para processamento de sequências
from patterns.comportamentais.chain_of_responsibility import SequenceAnalysisSystem

# Criar sistema com cadeia de handlers
sistema = SequenceAnalysisSystem()

# Analisar sequência através da cadeia
resultado = sistema.analyze_sequence("ATCGATCGATCG", "DNA")
if resultado.is_valid:
    print(f"Sequência válida: {resultado.processing_steps}")
else:
    print(f"Erros: {resultado.errors}")
```

### Command

**Propósito:** Encapsular requisições como objetos, permitindo parametrização, fila e operações.

**Implementação:** Sistema de comandos para operações laboratoriais:

- **Sequenciar:** Execução de sequenciamento de amostras
- **Alinhar:** Realização de alinhamentos genéticos
- **Analisar:** Processamento de dados proteômicos
- **Desfazer:** Reversão de operações executadas
- **Invocador:** Gerenciador de fila de comandos

```python
# Exemplo: Command para operações laboratoriais
from patterns.comportamentais.command import (
    SequenciarCommand, AlinharCommand, AnalisarCommand, InvocadorComandos
)

# Criar invocador de comandos
invocador = InvocadorComandos()

# Criar e executar comandos
cmd_sequenciar = SequenciarCommand("Amostra_001", "illumina")
cmd_alinhar = AlinharCommand("sequenciamento.fastq", "hg38")
cmd_analisar = AnalisarCommand("alinhado.bam", "variacao")

# Executar comandos
invocador.executar_comando(cmd_sequenciar)
invocador.executar_comando(cmd_alinhar)
invocador.executar_comando(cmd_analisar)

# Desfazer último comando
invocador.desfazer_ultimo_comando()

# Verificar histórico
historico = invocador.obter_historico()
print(f"Comandos executados: {len(historico)}")
```

### Iterator

**Propósito:** Acessar elementos de coleções sem expor estrutura interna.

**Implementação:** Iteração sobre resultados de análises genéticas:

- **Sequências:** Navegação por dados sequenciados
- **Proteínas:** Iteração sobre estruturas proteicas
- **Resultados:** Percorrer análises processadas
- **Abstração:** Interface unificada para diferentes coleções

```python
# Exemplo: Iterator para resultados de análises
from patterns.comportamentais.iterator import (
    ResultadosSequenciamento, ResultadosProteomicos, TipoDado
)

# Criar coleções de resultados
resultados_seq = ResultadosSequenciamento()
resultados_prot = ResultadosProteomicos()

# Adicionar resultados
resultados_seq.adicionar(ResultadoAnalise("SEQ001", TipoDado.SEQUENCIA, {"plataforma": "illumina"}))
resultados_prot.adicionar(ResultadoAnalise("PROT001", TipoDado.PROTEINA, {"proteina": "Hemoglobina"}))

# Iterar sobre sequenciamento
iterador_seq = resultados_seq.criar_iterador()
while iterador_seq.tem_proximo():
    resultado = iterador_seq.proximo()
    print(f"Sequência: {resultado.id_resultado}")

# Iterar com filtros
iterador_prot = resultados_prot.criar_iterador()
iterador_prot.definir_filtro_peso(15000, 17000)  # Filtrar por peso molecular
while iterador_prot.tem_proximo():
    resultado = iterador_prot.proximo()
    print(f"Proteína: {resultado.dados['proteina']}")
```

### Mediator

**Propósito:** Definir objeto que centraliza comunicação entre outros objetos.

**Implementação:** Coordenador de análises genômicas:

- **Sincronização:** Coordenação entre diferentes etapas
- **Comunicação:** Troca de dados entre módulos
- **Orquestração:** Gerenciamento do fluxo de trabalho
- **Desacoplamento:** Redução de dependências diretas

```python
# Exemplo: Mediator para coordenar componentes
from patterns.comportamentais.mediator import (
    CoordenadorAnalise, Sequenciador, Alinhador, Analisador
)

# Criar mediador
mediador = CoordenadorAnalise()

# Criar componentes
sequenciador = Sequenciador(mediador)
alinhador = Alinhador(mediador)
analisador = Analisador(mediador)

# Registrar componentes no mediador
mediador.registrar_componente("sequenciador", sequenciador)
mediador.registrar_componente("alinhador", alinhador)
mediador.registrar_componente("analisador", analisador)

# Iniciar processo coordenado
sequenciador.sequenciar_amostra("Amostra_001")
# O mediador coordena automaticamente o fluxo completo
```

### Memento

**Propósito:** Salvar e restaurar estado anterior de objetos sem expor detalhes de implementação.

**Implementação:** Sistema de checkpoint para experimentos genômicos:

- **Originator:** Experimentos que podem salvar/restaurar estados
- **Memento:** Snapshots do estado do experimento
- **Caretaker:** Gerenciador de histórico de estados

```python
# Exemplo: Memento para undo/redo em experimentos
from patterns.comportamentais.memento import ExperimentManager

# Criar gerenciador de experimentos
manager = ExperimentManager()
manager.create_experiment("EXP001", "ATCGATCG", "alignment")

# Modificar e executar análise
manager.modify_experiment(sequence="ATCGATCGATCGATCG")
manager.run_analysis()

# Desfazer alterações
manager.undo()  # Volta estado anterior
manager.redo()  # Refaz alteração

# Verificar histórico
historico = manager.get_history()
print(f"Estados salvos: {len(historico)}")
```

### Observer

**Propósito:** Definir dependência um-para-muitos, notificando mudanças automaticamente.

**Implementação:** Sistema de notificação de resultados experimentais:

- **Pesquisadores:** Observadores interessados em resultados
- **Análises:** Sujeitos que notificam conclusão
- **Eventos:** Mudanças de estado e conclusões
- **Notificação:** Atualização automática de múltiplos observadores

```python
# Exemplo: Observer para notificação de análises
from patterns.comportamentais.observer import (
    Pesquisador, SistemaAlerta, AnaliseGenomica, TipoEvento
)

# Criar observadores
pesquisador1 = Pesquisador("Dr. Silva", "silva@lab.com", "genomica")
pesquisador2 = Pesquisador("Dra. Santos", "santos@lab.com", "proteomica")
sistema_alerta = SistemaAlerta("Sistema de Alertas", "alto")

# Criar análise (sujeito)
analise = AnaliseGenomica("ANALISE_001", "Análise de BRCA1")

# Registrar observadores
analise.adicionar_observador(pesquisador1)
analise.adicionar_observador(pesquisador2)
analise.adicionar_observador(sistema_alerta)

# Definir interesses
pesquisador1.definir_interesses([TipoEvento.ANALISE_CONCLUIDA])
pesquisador2.definir_interesses([TipoEvento.ANALISE_FALHOU])

# Executar análise e notificar observadores
analise.iniciar_analise()
analise.concluir_analise({"variantes": 42, "qualidade": "alta"})
```

### Strategy

**Propósito:** Definir família de algoritmos intercambiáveis, permitindo variação independente.

**Implementação:** Diferentes algoritmos de alinhamento de sequências:

- **Needleman-Wunsch:** Alinhamento global exato
- **Smith-Waterman:** Alinhamento local exato
- **BLAST:** Alinhamento heurístico rápido
- **K-mer:** Alinhamento aproximado ultra-rápido

```python
# Exemplo: Strategy para diferentes algoritmos de alinhamento
from patterns.comportamentais.strategy import (
    SequenceAligner, NeedlemanWunschStrategy, SmithWatermanStrategy, BLASTStrategy
)

# Criar alinhador com estratégia inicial
aligner = SequenceAligner(NeedlemanWunschStrategy())

# Mudar estratégia dinamicamente
aligner.set_strategy(SmithWatermanStrategy())
result_local = aligner.align_sequences("ATCGATCG", "ATCGATCG")

# Comparar estratégias
benchmark = AlignmentBenchmark()
best_strategy = benchmark.get_best_strategy("ATCGATCG", "GCTAGCTA", "identity")
print(f"Melhor estratégia: {best_strategy[0]}")
```

### State

**Propósito:** Permitir que objeto mude comportamento quando estado interno muda.

**Implementação:** Estados de equipamentos laboratoriais:

- **Disponível:** Pronto para uso, operações básicas
- **Em Uso:** Ocupado em análise, operações limitadas
- **Manutenção:** Indisponível temporariamente, operações de manutenção
- **Comportamento:** Varia conforme estado atual

```python
# Exemplo: State para gerenciar estados de equipamento
from patterns.comportamentais.state import EquipamentoLaboratorial

# Criar equipamento
microscopio = EquipamentoLaboratorial("Microscopio_001", "Microscópio Eletrônico")

# Verificar estado inicial
status = microscopio.verificar_status()
print(f"Estado inicial: {status['estado_atual']}")

# Ligando equipamento
microscopio.ligar()

# Iniciar uso
microscopio.iniciar_uso("Dr. Silva")
print(f"Em uso por: {microscopio.usuario_atual}")

# Tentar usar por outro usuário (deve falhar)
resultado = microscopio.iniciar_uso("Dra. Santos")
print(f"Segunda tentativa: {resultado}")

# Finalizar uso
microscopio.finalizar_uso()

# Iniciar manutenção
microscopio.iniciar_manutencao("Técnico João")
print(f"Em manutenção com: {microscopio.tecnico_manutencao}")
```

### Template Method

**Propósito:** Definir esqueleto de algoritmo, delegando passos específicos para subclasses.

**Implementação:** Pipeline de análise biológica com estrutura fixa:

- **Estrutura Comum:** Preparação → Extração → Processamento → Finalização
- **Variações:** Passos específicos por tipo de análise
- **Extensibilidade:** Novos tipos de análise sem modificar estrutura
- **Controle:** Ordem fixa de execução garantida

```python
# Exemplo: Template Method para pipelines de análise
from patterns.comportamentais.template_method import (
    PipelineGenomica, PipelineProteomica, PipelineTranscriptomica
)

# Criar pipelines específicos
pipeline_genomica = PipelineGenomica("Análise BRCA1")
pipeline_proteomica = PipelineProteomica("Análise Proteômica")
pipeline_transcriptomica = PipelineTranscriptomica("Análise de Expressão")

# Executar pipelines com estrutura comum mas implementações diferentes
dados_teste = {"amostra": "Paciente_001", "tipo": "sangue"}

resultado_genomica = pipeline_genomica.executar_analise_completa(dados_teste)
print(f"Genômica: {resultado_genomica.obter_resumo()['status']}")

resultado_proteomica = pipeline_proteomica.executar_analise_completa(dados_teste)
print(f"Proteômica: {resultado_proteomica.obter_resumo()['status']}")

resultado_transcriptomica = pipeline_transcriptomica.executar_analise_completa(dados_teste)
print(f"Transcriptômica: {resultado_transcriptomica.obter_resumo()['status']}")
```

### Visitor

**Propósito:** Adicionar novas operações a estrutura de objetos sem modificá-los.

**Implementação:** Operações de análise sobre estruturas genéticas:

- **Genes de Proteína:** Análise de expressão gênica
- **Genes Reguladores:** Análise de função regulatória
- **Visitantes:** Novas análises sem alterar classes existentes
- **Double Dispatch:** Operação baseada em tipo de visitante e elemento

```python
# Exemplo: Visitor para análises moleculares
from patterns.comportamentais.visitor import (
    GeneProteina, GeneRegulador, GeneEstrutural, GeneHousekeeping,
    AnalisadorMolecular, OtimizadorTerapeutico
)

# Criar diferentes tipos de genes
gene_proteina = GeneProteina("BRCA1", "17", 43044295, "Proteína supressora de tumor")
gene_regulador = GeneRegulador("TP53", "17", 7579472, "ativador")
gene_estrutural = GeneEstrutural("ACTB", "7", 5524907, "Manutenção do citoesqueleto")
gene_housekeeping = GeneHousekeeping("GAPDH", "12", 6656342, "Glicólise")

# Configurar genes
gene_proteina.definir_sequencia("ATCGATCGATCGATCG")
gene_proteina.definir_expressao(2.5)
gene_proteina.adicionar_dominio("RING")
gene_proteina.adicionar_dominio("BRCT")

# Criar visitantes
analisador = AnalisadorMolecular()
otimizador = OtimizadorTerapeutico()

# Aplicar visitantes aos genes
genes = [gene_proteina, gene_regulador, gene_estrutural, gene_housekeeping]

for gene in genes:
    # Análise molecular
    resultado_analise = gene.aceitar(analisador)
    print(f"{gene.nome}: {resultado_analise['tipo']}")
    
    # Análise terapêutica
    resultado_terapeutico = gene.aceitar(otimizador)
    print(f"  Score terapêutico: {resultado_terapeutico.get('score', 0):.2f}")

# Obter alvos terapêuticos identificados
alvos = otimizador.obter_alvos_terapeuticos()
print(f"\nAlvos terapêuticos identificados: {len(alvos)}")
```

- **Disponível:** Pronto para uso, operações básicas
- **Em Uso:** Ocupado em análise, operações limitadas
- **Manutenção:** Indisponível temporariamente, operações de manutenção
- **Comportamento:** Varia conforme estado atual

### Template Method

**Propósito:** Definir esqueleto de algoritmo, delegando passos específicos para subclasses.

**Implementação:** Pipeline de análise biológica com estrutura fixa:

- **Estrutura Comum:** Preparação → Extração → Processamento → Finalização
- **Variações:** Passos específicos por tipo de análise
- **Extensibilidade:** Novos tipos de análise sem modificar estrutura
- **Controle:** Ordem fixa de execução garantida

### Visitor

**Propósito:** Adicionar novas operações a estrutura de objetos sem modificá-los.

**Implementação:** Operações de análise sobre estruturas genéticas:

- **Genes de Proteína:** Análise de expressão gênica
- **Genes Reguladores:** Análise de função regulatória
- **Visitantes:** Novas análises sem alterar classes existentes
- **Double Dispatch:** Operação baseada em tipo de visitante e elemento

---

## Benefícios dos Padrões no Contexto Bioinformático

1. **Flexibilidade:** Troca de algoritmos de alinhamento sem modificar análises
2. **Reusabilidade:** Equipamentos compartilhados entre experimentos
3. **Manutenibilidade:** Separação clara entre tipos de dados e processamento
4. **Escalabilidade:** Singleton e Flyweight para lidar com grande volume de dados
5. **Segurança:** Proxy controlando acesso a dados sensíveis
6. **Performance:** Flyweight otimizando memória em análises em massa

---

## Como Executar

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Executando os Exemplos

Cada padrão pode ser executado individualmente:

```bash
# Padrões Criacionais
python patterns/criacionais/factory_method.py
python patterns/criacionais/abstract_factory.py
python patterns/criacionais/builder.py
python patterns/criacionais/prototype.py
python patterns/criacionais/singleton.py
python patterns/criacionais/multiton.py
python patterns/criacionais/object_pool.py

# Padrões Estruturais
python patterns/estruturais/adapter.py
python patterns/estruturais/bridge.py
python patterns/estruturais/composite.py
python patterns/estruturais/decorator.py
python patterns/estruturais/facade.py
python patterns/estruturals/flyweight.py
python patterns/estruturais/front_controller.py
python patterns/estruturais/proxy.py

# Padrões Comportamentais
python patterns/comportamentais/command.py
python patterns/comportamentais/iterator.py
python patterns/comportamentais/mediator.py
python patterns/comportamentais/observer.py
python patterns/comportamentais/state.py
python patterns/comportamentais/template_method.py
python patterns/comportamentais/visitor.py
```

### Executando os Testes

O projeto inclui **200+ testes unitários** abrangendo todos os padrões implementados:

```bash
# Executar todos os testes
python tests/test_all_patterns.py

# Executar todos os testes via unittest
python -m unittest discover tests/

# Executar testes por categoria
python -m unittest tests.test_factory_method     # Factory Method (12 testes)
python -m unittest tests.test_singleton          # Singleton (8 testes)
python -m unittest tests.test_observer           # Observer (15 testes)
python -m unittest tests.test_abstract_factory   # Abstract Factory (12 testes)
python -m unittest tests.test_builder            # Builder (15 testes)
python -m unittest tests.test_prototype          # Prototype (18 testes)
python -m unittest tests.test_multiton           # Multiton (20 testes)
python -m unittest tests.test_object_pool        # Object Pool (20 testes)
python -m unittest tests.test_adapter            # Adapter (25 testes)
python -m unittest tests.test_command            # Command (25 testes)
python -m unittest tests.test_iterator           # Iterator (30 testes)

# Executar suite completa com relatório detalhado
python tests/test_all_patterns.py
```

**Cobertura de Testes:**
- ✅ **Padrões Criacionais**: Factory Method, Abstract Factory, Builder, Prototype, Singleton, Multiton, Object Pool
- ✅ **Padrões Estruturais**: Adapter (outros padrões estruturais podem ser adicionados)
- ✅ **Padrões Comportamentais**: Command, Iterator, Observer (outros padrões comportamentais podem ser adicionados)

---

## Fonte de Estudos

Baseado em [Refactoring.Guru](https://refactoring.guru/pt-br/design-patterns/python) com adaptações para o contexto de bioinformática.

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## Autor

**Anderson Matte** - [GitHub](https://github.com/andersonmatte)

---

## Agradecimentos

- A comunidade de desenvolvimento Python pelos excelentes recursos educacionais
- A equipe do Refactoring.Guru pelo conteúdo de alta qualidade sobre padrões de projeto
- A comunidade bioinformática pelos exemplos práticos e casos de uso reais
