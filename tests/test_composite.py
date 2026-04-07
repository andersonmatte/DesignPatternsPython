"""
Testes para o padrão Composite
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.composite import (
    ComponenteGenomico, FolhaGenomica, CompostoGenomico, PipelineGenomico
)


class TestComposite(unittest.TestCase):
    """Testes para o padrão Composite."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.analise_simples1 = AnaliseAtomica("SEQ001", "Análise de Sequência", "sequenciamento")
        self.analise_simples2 = AnaliseAtomica("ALN001", "Análise de Alinhamento", "alinhamento")
        self.analise_simples3 = AnaliseAtomica("ANN001", "Análise de Anotação", "anotação")
        
        self.analise_composta = AnaliseComposta("PIPE001", "Pipeline Genômico")
        self.pipeline = PipelineAnalise()
    
    def test_analise_atomica_creation(self):
        """Testa criação de análise atômica."""
        analise = AnaliseAtomica("TEST001", "Test Analysis", "test")
        
        self.assertIsInstance(analise, ComponenteAnalise)
        self.assertEqual(analise.id_analise, "TEST001")
        self.assertEqual(analise.nome, "Test Analysis")
        self.assertEqual(analise.tipo, "test")
        self.assertFalse(analise.composta)
    
    def test_analise_composta_creation(self):
        """Testa criação de análise composta."""
        analise = AnaliseComposta("COMP001", "Composite Analysis")
        
        self.assertIsInstance(analise, ComponenteAnalise)
        self.assertEqual(analise.id_analise, "COMP001")
        self.assertEqual(analise.nome, "Composite Analysis")
        self.assertTrue(analise.composta)
        self.assertEqual(len(analise.filhos), 0)
    
    def test_analise_atomica_execute(self):
        """Testa execução de análise atômica."""
        resultado = self.analise_simples1.executar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('id_analise', resultado)
        self.assertIn('nome', resultado)
        self.assertIn('tipo', resultado)
        self.assertIn('status', resultado)
        self.assertIn('resultado', resultado)
        self.assertEqual(resultado['id_analise'], "SEQ001")
        self.assertEqual(resultado['status'], "Concluída")
    
    def test_analise_composta_add_child(self):
        """Testa adição de filho à análise composta."""
        self.analise_composta.adicionar(self.analise_simples1)
        
        self.assertEqual(len(self.analise_composta.filhos), 1)
        self.assertIn(self.analise_simples1, self.analise_composta.filhos)
    
    def test_analise_composta_remove_child(self):
        """Testa remoção de filho da análise composta."""
        self.analise_composta.adicionar(self.analise_simples1)
        self.analise_composta.adicionar(self.analise_simples2)
        
        self.assertEqual(len(self.analise_composta.filhos), 2)
        
        self.analise_composta.remover(self.analise_simples1)
        
        self.assertEqual(len(self.analise_composta.filhos), 1)
        self.assertNotIn(self.analise_simples1, self.analise_composta.filhos)
        self.assertIn(self.analise_simples2, self.analise_composta.filhos)
    
    def test_analise_composta_execute(self):
        """Testa execução de análise composta."""
        self.analise_composta.adicionar(self.analise_simples1)
        self.analise_composta.adicionar(self.analise_simples2)
        
        resultado = self.analise_composta.executar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('id_analise', resultado)
        self.assertIn('nome', resultado)
        self.assertIn('tipo', resultado)
        self.assertIn('status', resultado)
        self.assertIn('resultados_filhos', resultado)
        self.assertEqual(resultado['tipo'], "composta")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(len(resultado['resultados_filhos']), 2)
    
    def test_analise_composta_execute_empty(self):
        """Testa execução de análise composta vazia."""
        resultado = self.analise_composta.executar()
        
        self.assertEqual(resultado['status'], "Sem filhos para executar")
        self.assertEqual(len(resultado['resultados_filhos']), 0)
    
    def test_analise_atomica_get_info(self):
        """Testa obtenção de informações de análise atômica."""
        info = self.analise_simples1.get_info()
        
        self.assertIsInstance(info, str)
        self.assertIn("SEQ001", info)
        self.assertIn("Análise de Sequência", info)
        self.assertIn("sequenciamento", info)
        self.assertIn("Atômica", info)
    
    def test_analise_composta_get_info(self):
        """Testa obtenção de informações de análise composta."""
        self.analise_composta.adicionar(self.analise_simples1)
        self.analise_composta.adicionar(self.analise_simples2)
        
        info = self.analise_composta.get_info()
        
        self.assertIsInstance(info, str)
        self.assertIn("PIPE001", info)
        self.assertIn("Pipeline Genômico", info)
        self.assertIn("Composta", info)
        self.assertIn("2 filhos", info)
    
    def test_pipeline_analise_creation(self):
        """Testa criação de pipeline de análise."""
        self.assertIsInstance(self.pipeline, AnaliseComposta)
        self.assertEqual(self.pipeline.id_analise, "PIPELINE_MASTER")
        self.assertEqual(self.pipeline.nome, "Pipeline Principal")
    
    def test_pipeline_add_analysis(self):
        """Testa adição de análise ao pipeline."""
        self.pipeline.adicionar_analise(self.analise_simples1)
        
        self.assertEqual(len(self.pipeline.filhos), 1)
        self.assertIn(self.analise_simples1, self.pipeline.filhos)
    
    def test_pipeline_remove_analysis(self):
        """Testa remoção de análise do pipeline."""
        self.pipeline.adicionar_analise(self.analise_simples1)
        self.pipeline.adicionar_analise(self.analise_simples2)
        
        self.assertEqual(len(self.pipeline.filhos), 2)
        
        self.pipeline.remover_analise("SEQ001")
        
        self.assertEqual(len(self.pipeline.filhos), 1)
        self.assertNotIn(self.analise_simples1, self.pipeline.filhos)
    
    def test_pipeline_execute_all(self):
        """Testa execução de todas as análises do pipeline."""
        self.pipeline.adicionar_analise(self.analise_simples1)
        self.pipeline.adicionar_analise(self.analise_simples2)
        self.pipeline.adicionar_analise(self.analise_simples3)
        
        resultado = self.pipeline.executar_todas()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('pipeline', resultado)
        self.assertIn('total_analises', resultado)
        self.assertIn('resultados', resultado)
        self.assertEqual(resultado['total_analises'], 3)
        self.assertEqual(len(resultado['resultados']), 3)
    
    def test_pipeline_execute_all_empty(self):
        """Testa execução de pipeline vazio."""
        resultado = self.pipeline.executar_todas()
        
        self.assertEqual(resultado['total_analises'], 0)
        self.assertEqual(len(resultado['resultados']), 0)
    
    def test_pipeline_get_analysis_by_id(self):
        """Testa busca de análise por ID no pipeline."""
        self.pipeline.adicionar_analise(self.analise_simples1)
        self.pipeline.adicionar_analise(self.analise_simples2)
        
        found = self.pipeline.buscar_analise_por_id("SEQ001")
        not_found = self.pipeline.buscar_analise_por_id("INVALID")
        
        self.assertEqual(found, self.analise_simples1)
        self.assertIsNone(not_found)
    
    def test_nested_composite(self):
        """Testa composição aninhada (composite dentro de composite)."""
        sub_pipeline = AnaliseComposta("SUB001", "Sub-Pipeline")
        sub_pipeline.adicionar(self.analise_simples1)
        sub_pipeline.adicionar(self.analise_simples2)
        
        self.analise_composta.adicionar(sub_pipeline)
        self.analise_composta.adicionar(self.analise_simples3)
        
        resultado = self.analise_composta.executar()
        
        self.assertEqual(len(resultado['resultados_filhos']), 2)
        
        # Verifica se o sub-pipeline executou seus filhos
        sub_result = resultado['resultados_filhos'][0]
        self.assertEqual(sub_result['id_analise'], "SUB001")
        self.assertEqual(len(sub_result['resultados_filhos']), 2)
    
    def test_composite_tree_structure(self):
        """Testa estrutura em árvore do composite."""
        # Nível 1: Pipeline principal
        main_pipeline = AnaliseComposta("MAIN001", "Main Pipeline")
        
        # Nível 2: Sub-pipelines
        seq_pipeline = AnaliseComposta("SEQ001", "Sequencing Pipeline")
        ann_pipeline = AnaliseComposta("ANN001", "Annotation Pipeline")
        
        # Nível 3: Análises atômicas
        seq_pipeline.adicionar(AnaliseAtomica("SEQ001", "DNA Sequencing", "dna_seq"))
        seq_pipeline.adicionar(AnaliseAtomica("SEQ002", "RNA Sequencing", "rna_seq"))
        
        ann_pipeline.adicionar(AnaliseAtomica("ANN001", "Gene Annotation", "gene_ann"))
        ann_pipeline.adicionar(AnaliseAtomica("ANN002", "Protein Annotation", "prot_ann"))
        
        # Montar árvore
        main_pipeline.adicionar(seq_pipeline)
        main_pipeline.adicionar(ann_pipeline)
        
        resultado = main_pipeline.executar()
        
        # Verifica estrutura
        self.assertEqual(len(resultado['resultados_filhos']), 2)
        
        seq_result = resultado['resultados_filhos'][0]
        ann_result = resultado['resultados_filhos'][1]
        
        self.assertEqual(len(seq_result['resultados_filhos']), 2)
        self.assertEqual(len(ann_result['resultados_filhos']), 2)
    
    def test_composite_uniform_interface(self):
        """Testa interface uniforme entre componentes."""
        componentes = [
            self.analise_simples1,
            self.analise_composta,
            self.pipeline
        ]
        
        for componente in componentes:
            # Todos devem ter os mesmos métodos
            self.assertTrue(hasattr(componente, 'executar'))
            self.assertTrue(hasattr(componente, 'get_info'))
            
            # Todos devem retornar resultados com estrutura similar
            resultado = componente.executar()
            self.assertIsInstance(resultado, dict)
            self.assertIn('id_analise', resultado)
            self.assertIn('nome', resultado)
    
    def test_composite_error_handling(self):
        """Testa tratamento de erros no composite."""
        # Mock que lança exceção
        mock_analise = Mock(spec=AnaliseAtomica)
        mock_analise.executar.side_effect = Exception("Test error")
        mock_analise.id_analise = "ERROR001"
        mock_analise.nome = "Error Analysis"
        
        self.analise_composta.adicionar(mock_analise)
        
        resultado = self.analise_composta.executar()
        
        # Deve continuar mesmo com erro em um filho
        self.assertEqual(len(resultado['resultados_filhos']), 1)
        self.assertIn('erro', resultado['resultados_filhos'][0])
    
    def test_composite_deep_copy_independence(self):
        """Testa independência entre componentes."""
        self.analise_composta.adicionar(self.analise_simples1)
        
        # Executar não deve modificar o estado original
        resultado1 = self.analise_composta.executar()
        resultado2 = self.analise_composta.executar()
        
        # Resultados devem ser consistentes
        self.assertEqual(resultado1['id_analise'], resultado2['id_analise'])
        self.assertEqual(len(resultado1['resultados_filhos']), len(resultado2['resultados_filhos']))
    
    def test_composite_performance_large_tree(self):
        """Testa performance com árvore grande."""
        # Criar árvore grande
        root = AnaliseComposta("ROOT", "Root")
        
        for i in range(10):
            child = AnaliseComposta(f"CHILD_{i}", f"Child {i}")
            for j in range(5):
                leaf = AnaliseAtomica(f"LEAF_{i}_{j}", f"Leaf {i}-{j}", "test")
                child.adicionar(leaf)
            root.adicionar(child)
        
        # Executar e medir tempo
        import time
        start_time = time.time()
        resultado = root.executar()
        end_time = time.time()
        
        # Verifica se executou corretamente
        self.assertEqual(len(resultado['resultados_filhos']), 10)
        
        # Verifica performance (não deve demorar muito)
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)  # Menos de 1 segundo
    
    def test_composite_client_code_transparency(self):
        """Testa transparência para código cliente."""
        # O código cliente não precisa saber se está tratando com folha ou composto
        componentes = [self.analise_simples1, self.analise_composta]
        
        resultados = []
        for componente in componentes:
            resultado = componente.executar()
            resultados.append(resultado)
            
            # Interface é a mesma para ambos
            self.assertIn('id_analise', resultado)
            self.assertIn('status', resultado)
        
        self.assertEqual(len(resultados), 2)
    
    def test_composite_remove_nonexistent_child(self):
        """Testa remoção de filho inexistente."""
        self.analise_composta.adicionar(self.analise_simples1)
        
        # Tentar remover filho que não existe
        initial_count = len(self.analise_composta.filhos)
        self.analise_composta.remover(self.analise_simples2)
        
        # Não deve alterar
        self.assertEqual(len(self.analise_composta.filhos), initial_count)
    
    def test_composite_get_statistics(self):
        """Testa obtenção de estatísticas do composite."""
        self.analise_composta.adicionar(self.analise_simples1)
        self.analise_composta.adicionar(self.analise_simples2)
        
        stats = self.analise_composta.get_estatisticas()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_filhos', stats)
        self.assertIn('total_atomicas', stats)
        self.assertIn('total_compostas', stats)
        self.assertEqual(stats['total_filhos'], 2)
        self.assertEqual(stats['total_atomicas'], 2)
        self.assertEqual(stats['total_compostas'], 0)


if __name__ == '__main__':
    unittest.main()
