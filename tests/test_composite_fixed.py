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
        self.folha1 = FolhaGenomica("SEQ001", "Análise de Sequência", "sequenciamento")
        self.folha2 = FolhaGenomica("ALN001", "Análise de Alinhamento", "alinhamento")
        self.folha3 = FolhaGenomica("ANN001", "Análise de Anotação", "anotação")
        
        self.composto = CompostoGenomico("PIPE001", "Pipeline Genômico")
        self.pipeline = PipelineGenomico()
    
    def test_folha_genomica_creation(self):
        """Testa criação de folha genômica."""
        folha = FolhaGenomica("TEST001", "Test Analysis", "test")
        
        self.assertIsInstance(folha, ComponenteGenomico)
        self.assertEqual(folha.nome, "TEST001")
        self.assertEqual(folha.descricao, "Test Analysis")
        self.assertEqual(folha.tipo, "test")
    
    def test_composto_genomico_creation(self):
        """Testa criação de composto genômico."""
        composto = CompostoGenomico("COMP001", "Composite Analysis")
        
        self.assertIsInstance(composto, ComponenteGenomico)
        self.assertEqual(composto.nome, "COMP001")
        self.assertEqual(composto.descricao, "Composite Analysis")
        self.assertEqual(len(composto.filhos), 0)
    
    def test_folha_genomica_executar(self):
        """Testa execução de folha genômica."""
        resultado = self.folha1.executar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('nome', resultado)
        self.assertIn('tipo', resultado)
        self.assertIn('status', resultado)
        self.assertIn('resultado', resultado)
        self.assertEqual(resultado['nome'], "SEQ001")
        self.assertEqual(resultado['status'], "Concluída")
    
    def test_composto_genomico_adicionar(self):
        """Testa adição de filho ao composto genômico."""
        self.composto.adicionar(self.folha1)
        
        self.assertEqual(len(self.composto.filhos), 1)
        self.assertIn(self.folha1, self.composto.filhos)
    
    def test_composto_genomico_remover(self):
        """Testa remoção de filho do composto genômico."""
        self.composto.adicionar(self.folha1)
        self.composto.adicionar(self.folha2)
        
        self.assertEqual(len(self.composto.filhos), 2)
        
        self.composto.remover(self.folha1)
        
        self.assertEqual(len(self.composto.filhos), 1)
        self.assertNotIn(self.folha1, self.composto.filhos)
        self.assertIn(self.folha2, self.composto.filhos)
    
    def test_composto_genomico_executar(self):
        """Testa execução de composto genômico."""
        self.composto.adicionar(self.folha1)
        self.composto.adicionar(self.folha2)
        
        resultado = self.composto.executar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('nome', resultado)
        self.assertIn('tipo', resultado)
        self.assertIn('status', resultado)
        self.assertIn('resultados_filhos', resultado)
        self.assertEqual(resultado['tipo'], "composto")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(len(resultado['resultados_filhos']), 2)
    
    def test_composto_genomico_executar_vazio(self):
        """Testa execução de composto genômico vazio."""
        resultado = self.composto.executar()
        
        self.assertEqual(resultado['status'], "Sem filhos para executar")
        self.assertEqual(len(resultado['resultados_filhos']), 0)
    
    def test_folha_genomica_get_info(self):
        """Testa obtenção de informações de folha genômica."""
        info = self.folha1.get_info()
        
        self.assertIsInstance(info, str)
        self.assertIn("SEQ001", info)
        self.assertIn("Análise de Sequência", info)
        self.assertIn("sequenciamento", info)
        self.assertIn("Folha", info)
    
    def test_composto_genomico_get_info(self):
        """Testa obtenção de informações de composto genômico."""
        self.composto.adicionar(self.folha1)
        self.composto.adicionar(self.folha2)
        
        info = self.composto.get_info()
        
        self.assertIsInstance(info, str)
        self.assertIn("PIPE001", info)
        self.assertIn("Pipeline Genômico", info)
        self.assertIn("Composto", info)
        self.assertIn("2 filhos", info)
    
    def test_pipeline_genomico_creation(self):
        """Testa criação de pipeline genômico."""
        self.assertIsInstance(self.pipeline, CompostoGenomico)
        self.assertEqual(self.pipeline.nome, "PIPELINE_MASTER")
        self.assertEqual(self.pipeline.descricao, "Pipeline Principal")
    
    def test_pipeline_adicionar_analise(self):
        """Testa adição de análise ao pipeline."""
        self.pipeline.adicionar_analise(self.folha1)
        
        self.assertEqual(len(self.pipeline.filhos), 1)
        self.assertIn(self.folha1, self.pipeline.filhos)
    
    def test_pipeline_remover_analise(self):
        """Testa remoção de análise do pipeline."""
        self.pipeline.adicionar_analise(self.folha1)
        self.pipeline.adicionar_analise(self.folha2)
        
        self.assertEqual(len(self.pipeline.filhos), 2)
        
        self.pipeline.remover_analise("SEQ001")
        
        self.assertEqual(len(self.pipeline.filhos), 1)
        self.assertNotIn(self.folha1, self.pipeline.filhos)
    
    def test_pipeline_executar_todas(self):
        """Testa execução de todas as análises do pipeline."""
        self.pipeline.adicionar_analise(self.folha1)
        self.pipeline.adicionar_analise(self.folha2)
        self.pipeline.adicionar_analise(self.folha3)
        
        resultado = self.pipeline.executar_todas()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('pipeline', resultado)
        self.assertIn('total_analises', resultado)
        self.assertIn('resultados', resultado)
        self.assertEqual(resultado['total_analises'], 3)
        self.assertEqual(len(resultado['resultados']), 3)
    
    def test_pipeline_executar_todas_vazio(self):
        """Testa execução de pipeline vazio."""
        resultado = self.pipeline.executar_todas()
        
        self.assertEqual(resultado['total_analises'], 0)
        self.assertEqual(len(resultado['resultados']), 0)
    
    def test_pipeline_buscar_analise_por_id(self):
        """Testa busca de análise por ID no pipeline."""
        self.pipeline.adicionar_analise(self.folha1)
        self.pipeline.adicionar_analise(self.folha2)
        
        found = self.pipeline.buscar_analise_por_id("SEQ001")
        not_found = self.pipeline.buscar_analise_por_id("INVALID")
        
        self.assertEqual(found, self.folha1)
        self.assertIsNone(not_found)
    
    def test_nested_composite(self):
        """Testa composição aninhada (composite dentro de composite)."""
        sub_pipeline = CompostoGenomico("SUB001", "Sub-Pipeline")
        sub_pipeline.adicionar(self.folha1)
        sub_pipeline.adicionar(self.folha2)
        
        self.composto.adicionar(sub_pipeline)
        self.composto.adicionar(self.folha3)
        
        resultado = self.composto.executar()
        
        self.assertEqual(len(resultado['resultados_filhos']), 2)
        
        # Verifica se o sub-pipeline executou seus filhos
        sub_result = resultado['resultados_filhos'][0]
        self.assertEqual(sub_result['nome'], "SUB001")
        self.assertEqual(len(sub_result['resultados_filhos']), 2)
    
    def test_composite_tree_structure(self):
        """Testa estrutura em árvore do composite."""
        # Nível 1: Pipeline principal
        main_pipeline = CompostoGenomico("MAIN001", "Main Pipeline")
        
        # Nível 2: Sub-pipelines
        seq_pipeline = CompostoGenomico("SEQ001", "Sequencing Pipeline")
        ann_pipeline = CompostoGenomico("ANN001", "Annotation Pipeline")
        
        # Nível 3: Análises atômicas
        seq_pipeline.adicionar(FolhaGenomica("SEQ001", "DNA Sequencing", "dna_seq"))
        seq_pipeline.adicionar(FolhaGenomica("SEQ002", "RNA Sequencing", "rna_seq"))
        
        ann_pipeline.adicionar(FolhaGenomica("ANN001", "Gene Annotation", "gene_ann"))
        ann_pipeline.adicionar(FolhaGenomica("ANN002", "Protein Annotation", "prot_ann"))
        
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
            self.folha1,
            self.composto,
            self.pipeline
        ]
        
        for componente in componentes:
            # Todos devem ter os mesmos métodos
            self.assertTrue(hasattr(componente, 'executar'))
            self.assertTrue(hasattr(componente, 'get_info'))
            
            # Todos devem retornar resultados com estrutura similar
            resultado = componente.executar()
            self.assertIsInstance(resultado, dict)
            self.assertIn('nome', resultado)
    
    def test_composite_error_handling(self):
        """Testa tratamento de erros no composite."""
        # Mock que lança exceção
        mock_analise = Mock(spec=FolhaGenomica)
        mock_analise.executar.side_effect = Exception("Test error")
        mock_analise.nome = "ERROR001"
        
        self.composto.adicionar(mock_analise)
        
        resultado = self.composto.executar()
        
        # Deve continuar mesmo com erro em um filho
        self.assertEqual(len(resultado['resultados_filhos']), 1)
        self.assertIn('erro', resultado['resultados_filhos'][0])


if __name__ == '__main__':
    unittest.main()
