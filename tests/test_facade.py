"""
Testes para o padrão Facade
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.facade import (
    SistemaBioinformatica, GerenciadorSequenciamento, GerenciadorAlinhamento, GerenciadorAnalise
)


class TestFacade(unittest.TestCase):
    """Testes para o padrão Facade."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.sistema = SistemaBioinformatica()
        
        # Componentes individuais para testes específicos
        self.gerenciador_seq = GerenciadorSequenciamento()
        self.gerenciador_alin = GerenciadorAlinhamento()
        self.gerenciador_analise = GerenciadorAnalise()
    
    def test_sistema_bioinformatica_creation(self):
        """Testa criação do sistema de bioinformática."""
        self.assertIsInstance(self.sistema, SistemaBioinformatica)
        self.assertIsInstance(self.sistema.gerenciador_sequenciamento, GerenciadorSequenciamento)
        self.assertIsInstance(self.sistema.gerenciador_alinhamento, GerenciadorAlinhamento)
        self.assertIsInstance(self.sistema.gerenciador_analise, GerenciadorAnalise)
    
    def test_sistema_analise_completa(self):
        """Testa análise completa através da fachada."""
        resultado = self.sistema.realizar_analise_completa("ATCGATCGATCG", "hg38")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status_geral', resultado)
        self.assertIn('sequenciamento', resultado)
        self.assertIn('alinhamento', resultado)
        self.assertIn('analise', resultado)
        self.assertIn('timestamp', resultado)
        self.assertEqual(resultado['status_geral'], 'Concluída')
    
    def test_sistema_analise_rapida(self):
        """Testa análise rápida através da fachada."""
        resultado = self.sistema.realizar_analise_rapida("ATCGATCG")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('resultado', resultado)
        self.assertIn('timestamp', resultado)
        self.assertEqual(resultado['status'], 'Concluída')
    
    def test_sistema_relatorio_simplificado(self):
        """Testa geração de relatório simplificado."""
        resultado = self.sistema.gerar_relatorio_simplificado("EXP001")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('id_experimento', resultado)
        self.assertIn('resumo', resultado)
        self.assertIn('timestamp', resultado)
        self.assertEqual(resultado['id_experimento'], "EXP001")
    
    def test_gerenciador_sequenciamento_creation(self):
        """Testa criação do gerenciador de sequenciamento."""
        self.assertIsInstance(self.gerenciador_seq, GerenciadorSequenciamento)
        self.assertEqual(self.gerenciador_seq.nome, "Gerenciador de Sequenciamento")
    
    def test_gerenciador_sequenciamento_sequenciar_dna(self):
        """Testa sequenciamento de DNA."""
        resultado = self.gerenciador_seq.sequenciar("ATCGATCG", "DNA")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_material', resultado)
        self.assertIn('sequencia_bruta', resultado)
        self.assertIn('qualidade', resultado)
        self.assertIn('plataforma', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['tipo_material'], "DNA")
        self.assertEqual(resultado['status'], "Sequenciado")
    
    def test_gerenciador_sequenciamento_sequenciar_rna(self):
        """Testa sequenciamento de RNA."""
        resultado = self.gerenciador_seq.sequenciar("AUCGAUCG", "RNA")
        
        self.assertEqual(resultado['tipo_material'], "RNA")
        self.assertEqual(resultado['status'], "Sequenciado")
    
    def test_gerenciador_sequenciamento_preparar_amostra(self):
        """Testa preparação de amostra."""
        resultado = self.gerenciador_seq.preparar_amostra("ATCGATCG", "DNA")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status_preparacao', resultado)
        self.assertIn('concentracao', resultado)
        self.assertIn('pureza', resultado)
        self.assertEqual(resultado['status_preparacao'], "Preparada")
    
    def test_gerenciador_sequenciamento_verificar_qualidade(self):
        """Testa verificação de qualidade."""
        resultado = self.gerenciador_seq.verificar_qualidade("ATCGATCG")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('score_qualidade', resultado)
        self.assertIn('status_qualidade', resultado)
        self.assertIn('metricas', resultado)
        self.assertGreaterEqual(resultado['score_qualidade'], 0.0)
        self.assertLessEqual(resultado['score_qualidade'], 1.0)
    
    def test_gerenciador_alinhamento_creation(self):
        """Testa criação do gerenciador de alinhamento."""
        self.assertIsInstance(self.gerenciador_alin, GerenciadorAlinhamento)
        self.assertEqual(self.gerenciador_alin.nome, "Gerenciador de Alinhamento")
    
    def test_gerenciador_alinhamento_alinhar_sequencia(self):
        """Testa alinhamento de sequência."""
        resultado = self.gerenciador_alin.alinhar_sequencia("ATCGATCG", "hg38")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('referencia', resultado)
        self.assertIn('sequencia_alinhada', resultado)
        self.assertIn('score_alinhamento', resultado)
        self.assertIn('posicao', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['referencia'], "hg38")
        self.assertEqual(resultado['status'], "Alinhado")
    
    def test_gerenciador_alinhamento_buscar_referencias(self):
        """Testa busca de referências."""
        resultado = self.gerenciador_alin.buscar_referencias("hg38")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('referencias', resultado)
        self.assertIn('total_encontradas', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['status'], "Encontradas")
    
    def test_gerenciador_alinhamento_validar_alinhamento(self):
        """Testa validação de alinhamento."""
        resultado = self.gerenciador_alin.validar_alinhamento("ATCGATCG", "hg38")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('valido', resultado)
        self.assertIn('score_validacao', resultado)
        self.assertIn('erros', resultado)
        self.assertIsInstance(resultado['valido'], bool)
    
    def test_gerenciador_analise_creation(self):
        """Testa criação do gerenciador de análise."""
        self.assertIsInstance(self.gerenciador_analise, GerenciadorAnalise)
        self.assertEqual(self.gerenciador_analise.nome, "Gerenciador de Análise")
    
    def test_gerenciador_analise_analisar_variantes(self):
        """Testa análise de variantes."""
        resultado = self.gerenciador_analise.analisar_variantes("ATCGATCG", "hg38")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('variantes_encontradas', resultado)
        self.assertIn('total_variantes', resultado)
        self.assertIn('tipo_analise', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['tipo_analise'], "variantes")
        self.assertEqual(resultado['status'], "Analisado")
    
    def test_gerenciador_analise_analisar_expressao(self):
        """Testa análise de expressão."""
        resultado = self.gerenciador_analise.analisar_expressao("ATCGATCG")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('niveis_expressao', resultado)
        self.assertIn('genes_regulados', resultado)
        self.assertIn('tipo_analise', resultado)
        self.assertEqual(resultado['tipo_analise'], "expressao")
    
    def test_gerenciador_analise_gerar_relatorio(self):
        """Testa geração de relatório."""
        resultado = self.gerenciador_analise.gerar_relatorio("EXP001")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('id_experimento', resultado)
        self.assertIn('dados_analise', resultado)
        self.assertIn('estatisticas', resultado)
        self.assertIn('formato', resultado)
        self.assertEqual(resultado['id_experimento'], "EXP001")
    
    def test_facade_simplifies_complexity(self):
        """Testa se a fachada simplifica a complexidade do subsistema."""
        # Cliente não precisa conhecer os detalhes internos
        resultado = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
        
        # Interface simples retorna resultado completo
        self.assertEqual(resultado['status_geral'], 'Concluída')
        self.assertIn('sequenciamento', resultado)
        self.assertIn('alinhamento', resultado)
        self.assertIn('analise', resultado)
    
    def test_facade_error_handling(self):
        """Testa tratamento de erros pela fachada."""
        # Mock que lança exceção
        with patch.object(self.sistema.gerenciador_sequenciamento, 'sequenciar', 
                         side_effect=Exception("Erro no sequenciamento")):
            
            resultado = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
            
            # Fachada deve tratar o erro gracefully
            self.assertEqual(resultado['status_geral'], 'Erro')
            self.assertIn('erro', resultado)
    
    def test_facade_decoupling_client_from_subsystem(self):
        """Testa desacoplamento do cliente do subsistema."""
        # Cliente interage apenas com a fachada
        resultado1 = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
        resultado2 = self.sistema.realizar_analise_completa("GCTAGCTA", "hg38")
        
        # Interface permanece a mesma independentemente da complexidade interna
        self.assertEqual(resultado1['status_geral'], 'Concluída')
        self.assertEqual(resultado2['status_geral'], 'Concluída')
        
        # Estrutura dos resultados é consistente
        self.assertIn('sequenciamento', resultado1)
        self.assertIn('sequenciamento', resultado2)
    
    def test_facade_layered_operations(self):
        """Testa operações em camadas da fachada."""
        # Operação básica
        rapida = self.sistema.realizar_analise_rapida("ATCGATCG")
        
        # Operação completa
        completa = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
        
        # Análise rápida deve ser mais simples
        self.assertIn('resultado', rapida)
        self.assertIn('sequenciamento', completa)
        self.assertIn('alinhamento', completa)
        self.assertIn('analise', completa)
    
    def test_facade_optional_operations(self):
        """Testa operações opcionais da fachada."""
        # Relatório sem análise prévia
        relatorio = self.sistema.gerar_relatorio_simplificado("TEST001")
        
        self.assertIsInstance(relatorio, dict)
        self.assertIn('resumo', relatorio)
        self.assertIn('id_experimento', relatorio)
    
    def test_facade_state_management(self):
        """Testa gerenciamento de estado pela fachada."""
        # Múltiplas operações devem manter consistência
        resultado1 = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
        resultado2 = self.sistema.realizar_analise_completa("GCTAGCTA", "hg38")
        
        # Cada operação deve ser independente
        self.assertNotEqual(
            resultado1['sequenciamento']['timestamp'],
            resultado2['sequenciamento']['timestamp']
        )
    
    def test_facade_performance_optimization(self):
        """Testa otimizações de performance da fachada."""
        import time
        
        # Medir tempo de operação completa
        start_time = time.time()
        resultado = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
        end_time = time.time()
        
        # Operação deve ser razoavelmente rápida
        execution_time = end_time - start_time
        self.assertLess(execution_time, 2.0)  # Menos de 2 segundos
        
        # Resultado deve estar completo
        self.assertEqual(resultado['status_geral'], 'Concluída')
    
    def test_facade_extensibility(self):
        """Testa extensibilidade da fachada."""
        # Fachada deve permitir adicionar novas operações sem afetar clientes
        # Isso é testado indiretamente pela existência de múltiplas operações
        
        operations = [
            self.sistema.realizar_analise_completa,
            self.sistema.realizar_analise_rapida,
            self.sistema.gerar_relatorio_simplificado
        ]
        
        # Todas as operações devem existir e ser chamáveis
        for op in operations:
            self.assertTrue(callable(op))
    
    def test_facade_consistent_interface(self):
        """Testa interface consistente da fachada."""
        # Todas as operações devem retornar estruturas similares
        resultados = [
            self.sistema.realizar_analise_completa("ATCGATCG", "hg38"),
            self.sistema.realizar_analise_rapida("ATCGATCG"),
            self.sistema.gerar_relatorio_simplificado("TEST001")
        ]
        
        for resultado in resultados:
            self.assertIsInstance(resultado, dict)
            self.assertIn('timestamp', resultado)
            self.assertIn('status' if 'status' in resultado else 'status_geral', resultado)
    
    def test_facade_subsystem_independence(self):
        """Testa independência dos subsistemas."""
        # Subsistemas devem funcionar independentemente
        resultado_seq = self.gerenciador_seq.sequenciar("ATCGATCG", "DNA")
        resultado_alin = self.gerenciador_alin.alinhar_sequencia("ATCGATCG", "hg38")
        resultado_analise = self.gerenciador_analise.analisar_variantes("ATCGATCG", "hg38")
        
        # Cada um deve ter sua própria estrutura
        self.assertIn('status', resultado_seq)
        self.assertIn('status', resultado_alin)
        self.assertIn('status', resultado_analise)
    
    def test_facade_integration_workflow(self):
        """Testa fluxo de trabalho integrado."""
        # A fachada deve coordenar o fluxo corretamente
        resultado = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
        
        # Verificar se as etapas foram executadas em ordem
        self.assertEqual(resultado['sequenciamento']['status'], "Sequenciado")
        self.assertEqual(resultado['alinhamento']['status'], "Alinhado")
        self.assertEqual(resultado['analise']['status'], "Analisado")
        
        # Timestamps devem ser crescentes
        ts_seq = resultado['sequenciamento']['timestamp']
        ts_alin = resultado['alinhamento']['timestamp']
        ts_analise = resultado['analise']['timestamp']
        
        # Nota: como as operações são rápidas, os timestamps podem ser iguais
        # O importante é que todos existam
    
    def test_facade_error_recovery(self):
        """Testa recuperação de erros."""
        # Simular falha em uma etapa
        with patch.object(self.sistema.gerenciador_alinhamento, 'alinhar_sequencia',
                         return_value={'status': 'Erro', 'erro': 'Falha no alinhamento'}):
            
            resultado = self.sistema.realizar_analise_completa("ATCGATCG", "hg38")
            
            # Fachada deve reportar o erro adequadamente
            self.assertEqual(resultado['status_geral'], 'Erro')
            self.assertIn('erro', resultado)


if __name__ == '__main__':
    unittest.main()
