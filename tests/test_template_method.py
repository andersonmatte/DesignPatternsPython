"""
Testes para o padrão Template Method
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.template_method import (
    PipelineAnalise, PipelineGenomica, PipelineProteomica, PipelineTranscriptomica
)


class TestTemplateMethod(unittest.TestCase):
    """Testes para o padrão Template Method."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.pipeline_genomica = PipelineGenomica()
        self.pipeline_proteomica = PipelineProteomica()
        self.pipeline_transcriptomica = PipelineTranscriptomica()
        
        # Dados de teste
        self.dados_teste = {
            'amostra': 'SAMPLE001',
            'sequencia': 'ATCGATCGATCG',
            'qualidade': 0.95,
            'parametros': {'metodo': 'padrao'}
        }
    
    def test_pipeline_genomica_creation(self):
        """Testa criação do pipeline genômico."""
        self.assertIsInstance(self.pipeline_genomica, PipelineGenomica)
        self.assertIsInstance(self.pipeline_genomica, PipelineAnalise)
        self.assertEqual(self.pipeline_genomica.nome, "Pipeline Genômico")
        self.assertEqual(self.pipeline_genomica.tipo_analise, "genomica")
    
    def test_pipeline_proteomica_creation(self):
        """Testa criação do pipeline proteômico."""
        self.assertIsInstance(self.pipeline_proteomica, PipelineProteomica)
        self.assertIsInstance(self.pipeline_proteomica, PipelineAnalise)
        self.assertEqual(self.pipeline_proteomica.nome, "Pipeline Proteômico")
        self.assertEqual(self.pipeline_proteomica.tipo_analise, "proteomica")
    
    def test_pipeline_transcriptomica_creation(self):
        """Testa criação do pipeline transcriptômico."""
        self.assertIsInstance(self.pipeline_transcriptomica, PipelineTranscriptomica)
        self.assertIsInstance(self.pipeline_transcriptomica, PipelineAnalise)
        self.assertEqual(self.pipeline_transcriptomica.nome, "Pipeline Transcriptômico")
        self.assertEqual(self.pipeline_transcriptomica.tipo_analise, "transcriptomica")
    
    def test_pipeline_base_creation(self):
        """Testa criação da classe base abstrata."""
        # Não deve ser possível instanciar a classe abstrata diretamente
        with self.assertRaises(TypeError):
            PipelineAnalise()
    
    def test_template_method_executar_analise_completa(self):
        """Testa método template executar_analise_completa."""
        resultado = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('pipeline', resultado)
        self.assertIn('tipo_analise', resultado)
        self.assertIn('status', resultado)
        self.assertIn('etapas', resultado)
        self.assertIn('resultado_final', resultado)
        self.assertIn('timestamp', resultado)
        
        self.assertEqual(resultado['pipeline'], "Pipeline Genômico")
        self.assertEqual(resultado['tipo_analise'], "genomica")
        self.assertEqual(resultado['status'], "Concluída")
    
    def test_template_method_estrutura_fixa(self):
        """Testa se a estrutura fixa do template method é seguida."""
        resultado = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
        
        etapas = resultado['etapas']
        
        # Verificar se todas as etapas foram executadas
        self.assertIn('preparacao', etapas)
        self.assertIn('processamento', etapas)
        self.assertIn('validacao', etapas)
        self.assertIn('finalizacao', etapas)
        
        # Verificar ordem das etapas
        self.assertEqual(len(etapas), 4)
    
    def test_preparacao_genomica(self):
        """Testa etapa de preparação genômica."""
        resultado = self.pipeline_genomica.preparar_dados(self.dados_teste)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('etapa', resultado)
        self.assertIn('status', resultado)
        self.assertIn('dados_preparados', resultado)
        self.assertIn('metodo_preparacao', resultado)
        
        self.assertEqual(resultado['etapa'], "preparacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_preparacao'], "extração_dna")
    
    def test_preparacao_proteomica(self):
        """Testa etapa de preparação proteômica."""
        resultado = self.pipeline_proteomica.preparar_dados(self.dados_teste)
        
        self.assertEqual(resultado['etapa'], "preparacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_preparacao'], "purificacao_proteinas")
    
    def test_preparacao_transcriptomica(self):
        """Testa etapa de preparação transcriptômica."""
        resultado = self.pipeline_transcriptomica.preparar_dados(self.dados_teste)
        
        self.assertEqual(resultado['etapa'], "preparacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_preparacao'], "isolamento_rna")
    
    def test_processamento_genomico(self):
        """Testa etapa de processamento genômico."""
        dados_preparados = self.pipeline_genomica.preparar_dados(self.dados_teste)
        resultado = self.pipeline_genomica.processar_dados(dados_preparados['dados_preparados'])
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('etapa', resultado)
        self.assertIn('status', resultado)
        self.assertIn('dados_processados', resultado)
        self.assertIn('metodo_processamento', resultado)
        
        self.assertEqual(resultado['etapa'], "processamento")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_processamento'], "sequenciamento")
    
    def test_processamento_proteomico(self):
        """Testa etapa de processamento proteômico."""
        dados_preparados = self.pipeline_proteomica.preparar_dados(self.dados_teste)
        resultado = self.pipeline_proteomica.processar_dados(dados_preparados['dados_preparados'])
        
        self.assertEqual(resultado['etapa'], "processamento")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_processamento'], "espectrometria")
    
    def test_processamento_transcriptomico(self):
        """Testa etapa de processamento transcriptômico."""
        dados_preparados = self.pipeline_transcriptomica.preparar_dados(self.dados_teste)
        resultado = self.pipeline_transcriptomica.processar_dados(dados_preparados['dados_preparados'])
        
        self.assertEqual(resultado['etapa'], "processamento")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_processamento'], "sequenciamento_rna")
    
    def test_validacao_genomica(self):
        """Testa etapa de validação genômica."""
        dados_processados = {'sequencia': 'ATCGATCG', 'qualidade': 0.95}
        resultado = self.pipeline_genomica.validar_resultados(dados_processados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('etapa', resultado)
        self.assertIn('status', resultado)
        self.assertIn('dados_validados', resultado)
        self.assertIn('metricas_validacao', resultado)
        
        self.assertEqual(resultado['etapa'], "validacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertTrue(resultado['dados_validados']['valido'])
    
    def test_validacao_proteomica(self):
        """Testa etapa de validação proteômica."""
        dados_processados = {'proteinas': ['P1', 'P2'], 'qualidade': 0.90}
        resultado = self.pipeline_proteomica.validar_resultados(dados_processados)
        
        self.assertEqual(resultado['etapa'], "validacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertTrue(resultado['dados_validados']['valido'])
    
    def test_validacao_transcriptomica(self):
        """Testa etapa de validação transcriptômica."""
        dados_processados = {'genes': ['G1', 'G2'], 'qualidade': 0.88}
        resultado = self.pipeline_transcriptomica.validar_resultados(dados_processados)
        
        self.assertEqual(resultado['etapa'], "validacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertTrue(resultado['dados_validados']['valido'])
    
    def test_finalizacao_genomica(self):
        """Testa etapa de finalização genômica."""
        dados_validados = {'sequencia': 'ATCGATCG', 'valido': True}
        resultado = self.pipeline_genomica.finalizar_analise(dados_validados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('etapa', resultado)
        self.assertIn('status', resultado)
        self.assertIn('resultado_final', resultado)
        self.assertIn('metodo_finalizacao', resultado)
        
        self.assertEqual(resultado['etapa'], "finalizacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_finalizacao'], "anotacao_genomica")
    
    def test_finalizacao_proteomica(self):
        """Testa etapa de finalização proteômica."""
        dados_validados = {'proteinas': ['P1', 'P2'], 'valido': True}
        resultado = self.pipeline_proteomica.finalizar_analise(dados_validados)
        
        self.assertEqual(resultado['etapa'], "finalizacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_finalizacao'], "identificacao_proteinas")
    
    def test_finalizacao_transcriptomica(self):
        """Testa etapa de finalização transcriptômica."""
        dados_validados = {'genes': ['G1', 'G2'], 'valido': True}
        resultado = self.pipeline_transcriptomica.finalizar_analise(dados_validados)
        
        self.assertEqual(resultado['etapa'], "finalizacao")
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(resultado['metodo_finalizacao'], "analise_expressao")
    
    def test_hook_methods(self):
        """Testa métodos hook (opcional)."""
        # Verificar se os métodos hook existem
        self.assertTrue(hasattr(self.pipeline_genomica, 'verificar_qualidade_minima'))
        self.assertTrue(hasattr(self.pipeline_proteomica, 'verificar_qualidade_minima'))
        self.assertTrue(hasattr(self.pipeline_transcriptomica, 'verificar_qualidade_minima'))
        
        # Testar hook com qualidade boa
        resultado_hook = self.pipeline_genomica.verificar_qualidade_minima(0.95)
        self.assertTrue(resultado_hook)
        
        # Testar hook com qualidade ruim
        resultado_hook = self.pipeline_genomica.verificar_qualidade_minima(0.3)
        self.assertFalse(resultado_hook)
    
    def test_diferentes_implementacoes_subclasses(self):
        """Testa diferentes implementações nas subclasses."""
        resultado_genomica = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
        resultado_proteomica = self.pipeline_proteomica.executar_analise_completa(self.dados_teste)
        resultado_transcriptomica = self.pipeline_transcriptomica.executar_analise_completa(self.dados_teste)
        
        # Estrutura deve ser a mesma
        for resultado in [resultado_genomica, resultado_proteomica, resultado_transcriptomica]:
            self.assertIn('etapas', resultado)
            self.assertEqual(len(resultado['etapas']), 4)
            self.assertEqual(resultado['status'], "Concluída")
        
        # Implementações devem ser diferentes
        self.assertNotEqual(
            resultado_genomica['resultado_final']['metodo'],
            resultado_proteomica['resultado_final']['metodo']
        )
        
        self.assertNotEqual(
            resultado_proteomica['resultado_final']['metodo'],
            resultado_transcriptomica['resultado_final']['metodo']
        )
    
    def test_template_method_invariabilidade(self):
        """Testa invariabilidade do algoritmo do template method."""
        # O algoritmo não deve poder ser alterado pelas subclasses
        resultado1 = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
        resultado2 = self.pipeline_proteomica.executar_analise_completa(self.dados_teste)
        
        # A ordem das etapas deve ser a mesma
        etapas1 = list(resultado1['etapas'].keys())
        etapas2 = list(resultado2['etapas'].keys())
        
        self.assertEqual(etapas1, etapas2)
        self.assertEqual(etapas1, ['preparacao', 'processamento', 'validacao', 'finalizacao'])
    
    def test_erro_em_etapa(self):
        """Testa tratamento de erro em uma etapa."""
        # Mock que lança exceção na preparação
        with patch.object(self.pipeline_genomica, 'preparar_dados', 
                         side_effect=Exception("Erro na preparação")):
            
            resultado = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
            
            # Deve reportar erro adequadamente
            self.assertEqual(resultado['status'], "Erro")
            self.assertIn('erro', resultado)
    
    def test_validacao_falha(self):
        """Testa falha na etapa de validação."""
        # Mock que retorna validação falha
        with patch.object(self.pipeline_genomica, 'validar_resultados') as mock_validar:
            mock_validar.return_value = {
                'etapa': 'validacao',
                'status': 'Falha',
                'dados_validados': {'valido': False},
                'erro': 'Qualidade insuficiente'
            }
            
            resultado = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
            
            # Deve parar na validação
            self.assertEqual(resultado['status'], "Falha")
            self.assertIn('erro', resultado)
    
    def test_extensao_template_method(self):
        """Testa extensão do template method."""
        # Criar nova subclass para testar extensibilidade
        class PipelineCustom(PipelineAnalise):
            def __init__(self):
                super().__init__("Pipeline Custom", "custom")
            
            def preparar_dados(self, dados):
                return {
                    'etapa': 'preparacao',
                    'status': 'Concluída',
                    'dados_preparados': dados,
                    'metodo_preparacao': 'custom_preparacao'
                }
            
            def processar_dados(self, dados):
                return {
                    'etapa': 'processamento',
                    'status': 'Concluída',
                    'dados_processados': dados,
                    'metodo_processamento': 'custom_processamento'
                }
            
            def validar_resultados(self, dados):
                return {
                    'etapa': 'validacao',
                    'status': 'Concluída',
                    'dados_validados': {'valido': True, 'dados': dados},
                    'metricas_validacao': {'score': 1.0}
                }
            
            def finalizar_analise(self, dados):
                return {
                    'etapa': 'finalizacao',
                    'status': 'Concluída',
                    'resultado_final': {'resultado': dados},
                    'metodo_finalizacao': 'custom_finalizacao'
                }
        
        pipeline_custom = PipelineCustom()
        resultado = pipeline_custom.executar_analise_completa(self.dados_teste)
        
        # Deve seguir a mesma estrutura
        self.assertEqual(resultado['status'], "Concluída")
        self.assertEqual(len(resultado['etapas']), 4)
        
        # Mas com implementações customizadas
        self.assertEqual(resultado['etapas']['preparacao']['metodo_preparacao'], 'custom_preparacao')
        self.assertEqual(resultado['etapas']['processamento']['metodo_processamento'], 'custom_processamento')
    
    def test_performance_template_method(self):
        """Testa performance do template method."""
        import time
        
        start_time = time.time()
        for i in range(10):
            self.pipeline_genomica.executar_analise_completa({
                'amostra': f'SAMPLE{i}',
                'sequencia': 'ATCGATCG',
                'qualidade': 0.9
            })
        end_time = time.time()
        
        # Deve ser razoavelmente rápido
        execution_time = end_time - start_time
        self.assertLess(execution_time, 2.0)  # Menos de 2 segundos
    
    def test_template_method_reutilizacao_codigo(self):
        """Testa reutilização de código do template method."""
        # O código do algoritmo é reutilizado em todas as subclasses
        # Apenas os passos específicos são implementados nas subclasses
        
        metodos_genomica = [method for method in dir(self.pipeline_genomica) 
                           if not method.startswith('_') and callable(getattr(self.pipeline_genomica, method))]
        
        metodos_proteomica = [method for method in dir(self.pipeline_proteomica) 
                             if not method.startswith('_') and callable(getattr(self.pipeline_proteomica, method))]
        
        # Métodos do template method devem ser os mesmos
        metodos_template = ['executar_analise_completa', 'preparar_dados', 'processar_dados', 
                           'validar_resultados', 'finalizar_analise', 'verificar_qualidade_minima']
        
        for metodo in metodos_template:
            self.assertIn(metodo, metodos_genomica)
            self.assertIn(metodo, metodos_proteomica)
    
    def test_template_method_controle_inversao(self):
        """Testa inversão de controle do template method."""
        # A classe base controla o fluxo, as subclasses implementam os passos
        resultado = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
        
        # Verificar se o fluxo foi controlado pela classe base
        etapas = list(resultado['etapas'].keys())
        self.assertEqual(etapas[0], 'preparacao')
        self.assertEqual(etapas[1], 'processamento')
        self.assertEqual(etapas[2], 'validacao')
        self.assertEqual(etapas[3], 'finalizacao')
    
    def test_template_method_polimorfismo(self):
        """Testa polimorfismo no template method."""
        pipelines = [
            self.pipeline_genomica,
            self.pipeline_proteomica,
            self.pipeline_transcriptomica
        ]
        
        resultados = []
        for pipeline in pipelines:
            resultado = pipeline.executar_analise_completa(self.dados_teste)
            resultados.append(resultado)
        
        # Todos devem ter a mesma estrutura
        for resultado in resultados:
            self.assertIn('etapas', resultado)
            self.assertIn('resultado_final', resultado)
            self.assertEqual(resultado['status'], "Concluída")
        
        # Mas com resultados diferentes
        self.assertNotEqual(
            resultados[0]['resultado_final']['metodo'],
            resultados[1]['resultado_final']['metodo']
        )
    
    def test_template_method_beneficios(self):
        """Testa benefícios do padrão Template Method."""
        # 1. Reutilização de código
        # O algoritmo é definido uma vez na classe base
        
        # 2. Controle do fluxo
        # A classe base controla a ordem das etapas
        
        # 3. Extensibilidade
        # Novas subclasses podem ser adicionadas facilmente
        
        # 4. Manutenibilidade
        # Mudanças no algoritmo afetam todas as subclasses
        
        # Verificar estrutura consistente
        resultado = self.pipeline_genomica.executar_analise_completa(self.dados_teste)
        self.assertIsInstance(resultado, dict)
        self.assertIn('etapas', resultado)
        self.assertEqual(len(resultado['etapas']), 4)


if __name__ == '__main__':
    unittest.main()
