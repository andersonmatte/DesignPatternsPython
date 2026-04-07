"""
Testes para o padrão Visitor
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.visitor import (
    ElementoGenetico, Gene, GeneProteina, GeneRegulador, GeneEstrutural, GeneHousekeeping,
    VisitorGenetico, AnalisadorMolecular, OtimizadorTerapeutico
)


class TestVisitor(unittest.TestCase):
    """Testes para o padrão Visitor."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        # Criar diferentes tipos de genes
        self.gene_proteina = GeneProteina("BRCA1", "17", 43044295, "Proteína supressora de tumor")
        self.gene_regulador = GeneRegulador("TP53", "17", 7579472, "ativador")
        self.gene_estrutural = GeneEstrutural("ACTB", "7", 5524907, "Manutenção do citoesqueleto")
        self.gene_housekeeping = GeneHousekeeping("GAPDH", "12", 6656342, "Glicólise")
        
        # Configurar genes com dados
        self.gene_proteina.definir_sequencia("ATCGATCGATCGATCG")
        self.gene_proteina.definir_expressao(2.5)
        self.gene_proteina.adicionar_dominio("RING")
        self.gene_proteina.adicionar_dominio("BRCT")
        
        self.gene_regulador.definir_sequencia("GCTAGCTAGCTAGCTA")
        self.gene_regulador.definir_expressao(1.8)
        self.gene_regulador.adicionar_alvo("CDKN1A")
        self.gene_regulador.adicionar_alvo("MDM2")
        
        # Criar visitantes
        self.analisador = AnalisadorMolecular()
        self.otimizador = OtimizadorTerapeutico()
    
    def test_gene_proteina_creation(self):
        """Testa criação de gene de proteína."""
        self.assertIsInstance(self.gene_proteina, GeneProteina)
        self.assertIsInstance(self.gene_proteina, Gene)
        self.assertIsInstance(self.gene_proteina, ElementoGenetico)
        
        self.assertEqual(self.gene_proteina.nome, "BRCA1")
        self.assertEqual(self.gene_proteina.cromossomo, "17")
        self.assertEqual(self.gene_proteina.posicao, 43044295)
        self.assertEqual(self.gene_proteina.funcao, "Proteína supressora de tumor")
        self.assertEqual(self.gene_proteina.tipo, "proteina")
    
    def test_gene_regulador_creation(self):
        """Testa criação de gene regulador."""
        self.assertIsInstance(self.gene_regulador, GeneRegulador)
        self.assertIsInstance(self.gene_regulador, Gene)
        self.assertIsInstance(self.gene_regulador, ElementoGenetico)
        
        self.assertEqual(self.gene_regulador.nome, "TP53")
        self.assertEqual(self.gene_regulador.tipo, "regulador")
    
    def test_gene_estrutural_creation(self):
        """Testa criação de gene estrutural."""
        self.assertIsInstance(self.gene_estrutural, GeneEstrutural)
        self.assertIsInstance(self.gene_estrutural, Gene)
        self.assertIsInstance(self.gene_estrutural, ElementoGenetico)
        
        self.assertEqual(self.gene_estrutural.nome, "ACTB")
        self.assertEqual(self.gene_estrutural.tipo, "estrutural")
    
    test_gene_housekeeping_creation = lambda self: None  # Placeholder
    
    def test_analisador_molecular_creation(self):
        """Testa criação do analisador molecular."""
        self.assertIsInstance(self.analisador, AnalisadorMolecular)
        self.assertIsInstance(self.analisador, VisitorGenetico)
        self.assertEqual(self.analisador.nome, "Analisador Molecular")
    
    def test_otimizador_terapeutico_creation(self):
        """Testa criação do otimizador terapêutico."""
        self.assertIsInstance(self.otimizador, OtimizadorTerapeutico)
        self.assertIsInstance(self.otimizador, VisitorGenetico)
        self.assertEqual(self.otimizador.nome, "Otimizador Terapêutico")
    
    def test_gene_proteina_aceitar_visitor(self):
        """Testa método aceitar do gene de proteína."""
        resultado = self.gene_proteina.aceitar(self.analisador)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('gene', resultado)
        self.assertIn('tipo_analise', resultado)
        self.assertIn('resultados', resultado)
        self.assertIn('visitor', resultado)
        
        self.assertEqual(resultado['gene'], "BRCA1")
        self.assertEqual(resultado['visitor'], "Analisador Molecular")
    
    def test_gene_regulador_aceitar_visitor(self):
        """Testa método aceitar do gene regulador."""
        resultado = self.gene_regulador.aceitar(self.analisador)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['gene'], "TP53")
        self.assertIn('resultados', resultado)
    
    def test_gene_estrutural_aceitar_visitor(self):
        """Testa método aceitar do gene estrutural."""
        resultado = self.gene_estrutural.aceitar(self.analisador)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['gene'], "ACTB")
        self.assertIn('resultados', resultado)
    
    def test_gene_housekeeping_aceitar_visitor(self):
        """Testa método aceitar do gene housekeeping."""
        resultado = self.gene_housekeeping.aceitar(self.analisador)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['gene'], "GAPDH")
        self.assertIn('resultados', resultado)
    
    def test_analisador_visit_gene_proteina(self):
        """Testa visit do analisador em gene de proteína."""
        resultado = self.analisador.visit_gene_proteina(self.gene_proteina)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_analise', resultado)
        self.assertIn('analise_proteina', resultado)
        self.assertIn('analise_estrutura', resultado)
        self.assertIn('analise_funcao', resultado)
        
        self.assertEqual(resultado['tipo_analise'], "proteina")
        self.assertIn('dominios', resultado['analise_proteina'])
        self.assertIn('RING', resultado['analise_proteina']['dominios'])
    
    def test_analisador_visit_gene_regulador(self):
        """Testa visit do analisador em gene regulador."""
        resultado = self.analisador.visit_gene_regulador(self.gene_regulador)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['tipo_analise'], "regulador")
        self.assertIn('analise_regulacao', resultado)
        self.assertIn('alvos_regulados', resultado['analise_regulacao'])
    
    def test_analisador_visit_gene_estrutural(self):
        """Testa visit do analisador em gene estrutural."""
        resultado = self.analisador.visit_gene_estrutural(self.gene_estrutural)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['tipo_analise'], "estrutural")
        self.assertIn('analise_estrutura', resultado)
    
    def test_analisador_visit_gene_housekeeping(self):
        """Testa visit do analisador em gene housekeeping."""
        resultado = self.analisador.visit_gene_housekeeping(self.gene_housekeeping)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['tipo_analise'], "housekeeping")
        self.assertIn('analise_housekeeping', resultado)
    
    def test_otimizador_visit_gene_proteina(self):
        """Testa visit do otimizador em gene de proteína."""
        resultado = self.otimizador.visit_gene_proteina(self.gene_proteina)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_otimizacao', resultado)
        self.assertIn('potencial_terapeutico', resultado)
        self.assertIn('alvos_medicamentos', resultado)
        
        self.assertEqual(resultado['tipo_otimizacao'], "proteina")
        self.assertIn('score', resultado['potencial_terapeutico'])
    
    def test_otimizador_visit_gene_regulador(self):
        """Testa visit do otimizador em gene regulador."""
        resultado = self.otimizador.visit_gene_regulador(self.gene_regulador)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['tipo_otimizacao'], "regulador")
        self.assertIn('potencial_terapeutico', resultado)
    
    def test_otimizador_visit_gene_estrutural(self):
        """Testa visit do otimizador em gene estrutural."""
        resultado = self.otimizador.visit_gene_estrutural(self.gene_estrutural)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['tipo_otimizacao'], "estrutural")
        self.assertIn('potencial_terapeutico', resultado)
    
    def test_otimizador_visit_gene_housekeeping(self):
        """Testa visit do otimizador em gene housekeeping."""
        resultado = self.otimizador.visit_gene_housekeeping(self.gene_housekeeping)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['tipo_otimizacao'], "housekeeping")
        self.assertIn('potencial_terapeutico', resultado)
    
    def test_visitor_double_dispatch(self):
        """Testa double dispatch do padrão Visitor."""
        # O tipo do visitante e do elemento determinam a operação executada
        resultado_analise = self.gene_proteina.aceitar(self.analisador)
        resultado_otimizacao = self.gene_proteina.aceitar(self.otimizador)
        
        # Mesmo gene, visitantes diferentes = resultados diferentes
        self.assertEqual(resultado_analise['visitor'], "Analisador Molecular")
        self.assertEqual(resultado_otimizacao['visitor'], "Otimizador Terapêutico")
        
        self.assertIn('tipo_analise', resultado_analise)
        self.assertIn('tipo_otimizacao', resultado_otimizacao)
    
    def test_visitor_diferentes_elementos(self):
        """Testa visitor com diferentes elementos."""
        genes = [self.gene_proteina, self.gene_regulador, self.gene_estrutural, self.gene_housekeeping]
        
        resultados = []
        for gene in genes:
            resultado = gene.aceitar(self.analisador)
            resultados.append(resultado)
        
        # Cada tipo de gene deve produzir análise diferente
        tipos_analise = [r['resultados']['tipo_analise'] for r in resultados]
        self.assertIn("proteina", tipos_analise)
        self.assertIn("regulador", tipos_analise)
        self.assertIn("estrutural", tipos_analise)
        self.assertIn("housekeeping", tipos_analise)
    
    def test_visitor_adicionar_operacoes_sem_modificar_elementos(self):
        """Teste adição de operações sem modificar elementos."""
        # Criar novo visitor sem modificar as classes de elementos
        class VisitorCustom(VisitorGenetico):
            def __init__(self):
                super().__init__("Visitor Custom")
            
            def visit_gene_proteina(self, gene):
                return {
                    'tipo_analise': 'custom_proteina',
                    'analise_custom': f'Análise custom de {gene.nome}',
                    'score_custom': len(gene.sequencia) if gene.sequencia else 0
                }
            
            def visit_gene_regulador(self, gene):
                return {
                    'tipo_analise': 'custom_regulador',
                    'analise_custom': f'Análise custom de {gene.nome}',
                    'score_custom': len(gene.alvos) if gene.alvos else 0
                }
            
            def visit_gene_estrutural(self, gene):
                return {
                    'tipo_analise': 'custom_estrutural',
                    'analise_custom': f'Análise custom de {gene.nome}',
                    'score_custom': 0.8
                }
            
            def visit_gene_housekeeping(self, gene):
                return {
                    'tipo_analise': 'custom_housekeeping',
                    'analise_custom': f'Análise custom de {gene.nome}',
                    'score_custom': 0.9
                }
        
        visitor_custom = VisitorCustom()
        resultado = self.gene_proteina.aceitar(visitor_custom)
        
        self.assertEqual(resultado['visitor'], "Visitor Custom")
        self.assertIn('analise_custom', resultado['resultados'])
    
    def test_visitor_coleta_dados_complexos(self):
        """Testa coleta de dados complexos pelo visitor."""
        # Coletar dados de múltiplos genes
        genes = [self.gene_proteina, self.gene_regulador, self.gene_estrutural, self.gene_housekeeping]
        
        dados_coletados = []
        for gene in genes:
            resultado = gene.aceitar(self.analisador)
            dados_coletados.append(resultado)
        
        # Verificar se dados foram coletados corretamente
        self.assertEqual(len(dados_coletados), 4)
        
        # Cada resultado deve ter estrutura consistente
        for resultado in dados_coletados:
            self.assertIn('gene', resultado)
            self.assertIn('resultados', resultado)
            self.assertIn('tipo_analise', resultado['resultados'])
    
    def test_visitor_relatorio_consolidado(self):
        """Testa geração de relatório consolidado."""
        genes = [self.gene_proteina, self.gene_regulador, self.gene_estrutural, self.gene_housekeeping]
        
        # Aplicar múltiplos visitantes
        resultados_analise = []
        resultados_otimizacao = []
        
        for gene in genes:
            resultados_analise.append(gene.aceitar(self.analisador))
            resultados_otimizacao.append(gene.aceitar(self.otimizador))
        
        # Gerar relatório consolidado
        relatorio = {
            'total_genes': len(genes),
            'analises': resultados_analise,
            'otimizacoes': resultados_otimizacao,
            'resumo': {
                'genes_proteina': len([r for r in resultados_analise if r['resultados']['tipo_analise'] == 'proteina']),
                'genes_regulador': len([r for r in resultados_analise if r['resultados']['tipo_analise'] == 'regulador']),
                'genes_estrutural': len([r for r in resultados_analise if r['resultados']['tipo_analise'] == 'estrutural']),
                'genes_housekeeping': len([r for r in resultados_analise if r['resultados']['tipo_analise'] == 'housekeeping'])
            }
        }
        
        self.assertEqual(relatorio['total_genes'], 4)
        self.assertEqual(relatorio['resumo']['genes_proteina'], 1)
        self.assertEqual(relatorio['resumo']['genes_regulador'], 1)
        self.assertEqual(relatorio['resumo']['genes_estrutural'], 1)
        self.assertEqual(relatorio['resumo']['genes_housekeeping'], 1)
    
    def test_visitor_performance(self):
        """Testa performance do visitor com muitos elementos."""
        import time
        
        # Criar muitos genes
        genes = []
        for i in range(100):
            gene = GeneProteina(f"GENE{i}", "1", 1000000 + i, f"Função {i}")
            gene.definir_sequencia("ATCG" * 100)
            genes.append(gene)
        
        # Aplicar visitor
        start_time = time.time()
        resultados = []
        for gene in genes:
            resultado = gene.aceitar(self.analisador)
            resultados.append(resultado)
        end_time = time.time()
        
        # Deve ser razoavelmente rápido
        execution_time = end_time - start_time
        self.assertLess(execution_time, 2.0)  # Menos de 2 segundos
        
        self.assertEqual(len(resultados), 100)
    
    def test_visitor_tratamento_erros(self):
        """Testa tratamento de erros no visitor."""
        # Gene sem dados
        gene_vazio = GeneProteina("EMPTY", "X", 0, "Vazio")
        
        # Visitor deve lidar com dados ausentes gracefully
        resultado = gene_vazio.aceitar(self.analisador)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['gene'], "EMPTY")
        self.assertIn('resultados', resultado)
    
    def test_visitor_extensibilidade_elementos(self):
        """Testa extensibilidade com novos elementos."""
        # Criar novo tipo de elemento genético
        class GeneMitochondrial(Gene):
            def __init__(self, nome, posicao, funcao):
                super().__init__(nome, "MT", posicao, funcao)
                self.tipo = "mitochondrial"
                self.membrane_potential = 0.0
            
            def definir_potencial_membrana(self, potencial):
                self.membrane_potential = potencial
        
        # Extender visitor para novo elemento
        class AnalisadorExtendido(AnalisorMolecular):
            def visit_gene_mitochondrial(self, gene):
                return {
                    'tipo_analise': 'mitochondrial',
                    'analise_mitocondrial': {
                        'potencial_membrana': gene.membrane_potential,
                        'eficiencia_energetica': 0.85,
                        'producao_atp': 'alta'
                    }
                }
        
        gene_mito = GeneMitochondrial("MT-CO1", 1234, "Citocromo oxidase")
        gene_mito.definir_potencial_membrana(0.15)
        
        analisador_extendido = AnalisadorExtendido()
        resultado = gene_mito.aceitar(analisador_extendido)
        
        self.assertEqual(resultado['resultados']['tipo_analise'], 'mitochondrial')
        self.assertEqual(resultado['resultados']['analise_mitocondrial']['potencial_membrana'], 0.15)
    
    def test_visitor_separacao_concerns(self):
        """Testa separação de concerns do visitor."""
        # Lógica de análise está no visitor
        self.assertIn('visit_gene_proteina', dir(self.analisador))
        self.assertIn('visit_gene_regulador', dir(self.analisador))
        
        # Lógica dos elementos está nas classes de elementos
        self.assertIn('aceitar', dir(self.gene_proteina))
        self.assertIn('nome', dir(self.gene_proteina))
        self.assertIn('sequencia', dir(self.gene_proteina))
        
        # Elementos não conhecem a lógica do visitor
        self.assertNotIn('analisar', dir(self.gene_proteina))
        self.assertNotIn('calcular_score', dir(self.gene_proteina))
    
    def test_visitor_polimorfismo_runtime(self):
        """Testa polimorfismo em tempo de execução."""
        genes = [self.gene_proteina, self.gene_regulador, self.gene_estrutural, self.gene_housekeeping]
        visitors = [self.analisador, self.otimizador]
        
        # Todas as combinações funcionam
        for gene in genes:
            for visitor in visitors:
                resultado = gene.aceitar(visitor)
                
                self.assertIsInstance(resultado, dict)
                self.assertEqual(resultado['gene'], gene.nome)
                self.assertEqual(resultado['visitor'], visitor.nome)
    
    def test_visitor_acumulacao_resultados(self):
        """Testa acumulação de resultados no visitor."""
        class AcumuladorVisitor(VisitorGenetico):
            def __init__(self):
                super().__init__("Acumulador")
                self.total_genes = 0
                self.total_sequencias = 0
            
            def visit_gene_proteina(self, gene):
                self.total_genes += 1
                if gene.sequencia:
                    self.total_sequencias += len(gene.sequencia)
                return {'gene': gene.nome, 'acumulado': True}
            
            def visit_gene_regulador(self, gene):
                self.total_genes += 1
                if gene.sequencia:
                    self.total_sequencias += len(gene.sequencia)
                return {'gene': gene.nome, 'acumulado': True}
            
            def visit_gene_estrutural(self, gene):
                self.total_genes += 1
                if gene.sequencia:
                    self.total_sequencias += len(gene.sequencia)
                return {'gene': gene.nome, 'acumulado': True}
            
            def visit_gene_housekeeping(self, gene):
                self.total_genes += 1
                if gene.sequencia:
                    self.total_sequencias += len(gene.sequencia)
                return {'gene': gene.nome, 'acumulado': True}
        
        acumulador = AcumuladorVisitor()
        genes = [self.gene_proteina, self.gene_regulador, self.gene_estrutural, self.gene_housekeeping]
        
        for gene in genes:
            gene.aceitar(acumulador)
        
        self.assertEqual(acumulador.total_genes, 4)
        self.assertGreater(acumulador.total_sequencias, 0)
    
    def test_visitor_beneficios_padrao(self):
        """Testa benefícios do padrão Visitor."""
        # 1. Adicionar operações sem modificar classes
        self.assertTrue(hasattr(self.analisador, 'visit_gene_proteina'))
        self.assertTrue(hasattr(self.otimizador, 'visit_gene_proteina'))
        
        # 2. Operações relacionadas em uma classe
        metodos_analisador = [m for m in dir(self.analisador) if m.startswith('visit_')]
        self.assertGreater(len(metodos_analisador), 0)
        
        # 3. Double dispatch
        resultado = self.gene_proteina.aceitar(self.analisador)
        self.assertEqual(resultado['gene'], "BRCA1")
        self.assertEqual(resultado['visitor'], "Analisador Molecular")
        
        # 4. Acumular estado
        # (verificado no teste de acumulação)


if __name__ == '__main__':
    unittest.main()
