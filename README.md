# Design Patterns em Python - Sistema de Bioinformática

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Patterns](https://img.shields.io/badge/Design_Patterns-23-green.svg)
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
│   │   ├── singleton.py        # Singleton
│   │   ├── multiton.py         # Multiton
│   │   └── object_pool.py      # Object Pool
│   ├── estruturais/           # Padrões estruturais
│   │   ├── adapter.py          # Adapter
│   │   ├── bridge.py           # Bridge
│   │   ├── composite.py        # Composite
│   │   ├── decorator.py        # Decorator
│   │   ├── facade.py           # Facade
│   │   ├── flyweight.py        # Flyweight
│   │   ├── front_controller.py # Front Controller
│   │   └── proxy.py            # Proxy
│   └── comportamentais/        # Padrões comportamentais
│       ├── command.py          # Command
│       ├── iterator.py         # Iterator
│       ├── mediator.py         # Mediator
│       ├── observer.py         # Observer
│       ├── state.py            # State
│       ├── template_method.py  # Template Method
│       └── visitor.py          # Visitor
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

### Bridge

**Propósito:** Desacoplar abstração da implementação, permitindo variação independente.

**Implementação:** Separação entre tipo de análise e algoritmo de processamento:

- **Análises Genômicas:** Sequenciamento, alinhamento, expressão
- **Algoritmos:** Needleman-Wunsch, BLAST, Smith-Waterman

### Composite

**Propósito:** Compor objetos em estruturas de árvore, tratando individuais e composições uniformemente.

**Implementação:** Estrutura hierárquica de sequências genéticas:

- **Genes:** Componentes complexos com múltiplos nucleotídeos
- **Nucleotídeos:** Componentes básicos individuais
- **Proteínas:** Componentes compostos

### Decorator

**Propósito:** Adicionar responsabilidades dinamicamente a objetos.

**Implementação:** Enriquecimento funcional de análises genômicas:

- **Análise Base:** Funcionalidade fundamental de análise
- **Com Validação:** Adição de verificação de dados
- **Com Relatório:** Adição de geração de relatórios
- **Composição:** Múltiplas camadas de funcionalidade

### Facade

**Propósito:** Fornecer interface simplificada para subsistemas complexos.

**Implementação:** Fachada unificada para análise genômica completa:

- **Sequenciamento:** Extração e preparação de amostras
- **Alinhamento:** Comparação com referências
- **Análise:** Processamento e interpretação
- **Relatório:** Geração de resultados

### Flyweight

**Propósito:** Compartilhar estado intrínseco para otimizar uso de memória.

**Implementação:** Compartilhamento de dados genéticos entre múltiplas análises:

- **Dados Proteicos:** Sequências de aminoácidos compartilhadas
- **Estado Extrínseco:** Contexto específico de cada análise
- **Cache:** Reutilização eficiente de estruturas

### Front Controller

**Propósito:** Centralizar requisições e fornecer tratamento unificado.

**Implementação:** Controlador frontal para sistema de bioinformática:

- **Roteamento:** Direcionamento para módulos específicos
- **Validação:** Verificação de parâmetros e permissões
- **Tratamento:** Gerenciamento de erros e exceções

### Proxy

**Propósito:** Controlar acesso a objetos, fornecendo interface intermediária.

**Implementação:** Proxy de segurança para banco de dados genéticos:

- **Controle de Acesso:** Validação de permissões de usuários
- **Cache:** Otimização de consultas frequentes
- **Logging:** Registro de operações de acesso

---

## Padrões Comportamentais

### Command

**Propósito:** Encapsular requisições como objetos, permitindo parametrização, fila e operações.

**Implementação:** Sistema de comandos para operações laboratoriais:

- **Sequenciar:** Execução de sequenciamento de amostras
- **Alinhar:** Realização de alinhamentos genéticos
- **Analisar:** Processamento de dados proteômicos
- **Desfazer:** Reversão de operações executadas
- **Invocador:** Gerenciador de fila de comandos

### Iterator

**Propósito:** Acessar elementos de coleções sem expor estrutura interna.

**Implementação:** Iteração sobre resultados de análises genéticas:

- **Sequências:** Navegação por dados sequenciados
- **Proteínas:** Iteração sobre estruturas proteicas
- **Resultados:** Percorrer análises processadas
- **Abstração:** Interface unificada para diferentes coleções

### Mediator

**Propósito:** Definir objeto que centraliza comunicação entre outros objetos.

**Implementação:** Coordenador de análises genômicas:

- **Sincronização:** Coordenação entre diferentes etapas
- **Comunicação:** Troca de dados entre módulos
- **Orquestração:** Gerenciamento do fluxo de trabalho
- **Desacoplamento:** Redução de dependências diretas

### Observer

**Propósito:** Definir dependência um-para-muitos, notificando mudanças automaticamente.

**Implementação:** Sistema de notificação de resultados experimentais:

- **Pesquisadores:** Observadores interessados em resultados
- **Análises:** Sujeitos que notificam conclusão
- **Eventos:** Mudanças de estado e conclusões
- **Notificação:** Atualização automática de múltiplos observadores

### State

**Propósito:** Permitir que objeto mude comportamento quando estado interno muda.

**Implementação:** Estados de equipamentos laboratoriais:

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
4. **Escalabilidade:** Pools de objetos para lidar com grande volume de dados
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
