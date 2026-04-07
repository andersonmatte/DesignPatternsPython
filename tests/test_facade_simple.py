"""
Testes para o padrão Facade
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.facade import (
    SistemaBioinformaticaFacade, ExtratorAmostras, PreparadorAmostras,
    Sequenciador, Alinhador, Analisador, GeradorRelatorios
)


class TestFacade(unittest.TestCase):
    """Testes para o padrão Facade."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.facade = SistemaBioinformaticaFacade()
        
        # Componentes individuais para testes específicos
        self.extrator = ExtratorAmostras()
        self.preparador = PreparadorAmostras()
        self.sequenciador = Sequenciador()
        self.alinhador = Alinhador()
        self.analisador = Analisador()
        self.gerador_relatorios = GeradorRelatorios()
    
    def test_facade_creation(self):
        """Testa criação da fachada."""
        facade = SistemaBioinformaticaFacade()
        
        self.assertIsInstance(facade, SistemaBioinformaticaFacade)
        self.assertIsInstance(facade.extrator, ExtratorAmostras)
        self.assertIsInstance(facade.preparador, PreparadorAmostras)
        self.assertIsInstance(facade.sequenciador, Sequenciador)
        self.assertIsInstance(facade.alinhador, Alinhador)
        self.assertIsInstance(facade.analisador, Analisador)
        self.assertIsInstance(facade.gerador_relatorios, GeradorRelatorios)
    
    def test_extrator_amostras_creation(self):
        """Testa criação do extrator de amostras."""
        extrator = ExtratorAmostras()
        
        self.assertIsInstance(extrator, ExtratorAmostras)
    
    def test_extrator_extrair_dna(self):
        """Testa extração de DNA."""
        resultado = self.extrator.extrair_dna("SAMPLE001")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo', resultado)
        self.assertIn('amostra_origem', resultado)
        self.assertIn('concentracao', resultado)
        self.assertIn('pureza', resultado)
        self.assertEqual(resultado['tipo'], "DNA")
        self.assertEqual(resultado['amostra_origem'], "SAMPLE001")
    
    def test_extrator_extrair_rna(self):
        """Testa extração de RNA."""
        resultado = self.extrator.extrair_rna("SAMPLE001")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo', resultado)
        self.assertIn('amostra_origem', resultado)
        self.assertEqual(resultado['tipo'], "RNA")
        self.assertEqual(resultado['amostra_origem'], "SAMPLE001")
    
    def test_preparador_amostras_creation(self):
        """Testa criação do preparador de amostras."""
        preparador = PreparadorAmostras()
        
        self.assertIsInstance(preparador, PreparadorAmostras)
    
    def test_preparador_quantificar_amostra(self):
        """Testa quantificação de amostra."""
        dados_amostra = {"amostra_origem": "SAMPLE001"}
        resultado = self.preparador.quantificar_amostra(dados_amostra)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('concentracao_final', resultado)
        self.assertIn('volume_total', resultado)
        self.assertIn('metodo_quantificacao', resultado)
    
    def test_preparador_verificar_qualidade(self):
        """Testa verificação de qualidade."""
        dados_amostra = {"amostra_origem": "SAMPLE001"}
        resultado = self.preparador.verificar_qualidade(dados_amostra)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('qualidade_geral', resultado)
        self.assertIn('rin', resultado)
        self.assertIn('integridade', resultado)
    
    def test_sequenciador_creation(self):
        """Testa criação do sequenciador."""
        sequenciador = Sequenciador()
        
        self.assertIsInstance(sequenciador, Sequenciador)
    
    def test_sequenciador_sequenciar_illumina(self):
        """Testa sequenciamento com Illumina."""
        dados_preparados = {"amostra_origem": "SAMPLE001"}
        resultado = self.sequenciador.sequenciar_illumina(dados_preparados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('plataforma', resultado)
        self.assertIn('tecnologia', resultado)
        self.assertIn('sequencias_geradas', resultado)
        self.assertEqual(resultado['plataforma'], "Illumina")
    
    def test_alinhador_creation(self):
        """Testa criação do alinhador."""
        alinhador = Alinhador()
        
        self.assertIsInstance(alinhador, Alinhador)
    
    def test_alinhador_alinhar_genoma(self):
        """Testa alinhamento de genoma."""
        dados_sequenciamento = {"sequencias_geradas": []}
        resultado = self.alinhador.alinhar_genoma(dados_sequenciamento)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('referencia', resultado)
        self.assertIn('taxa_alinhamento', resultado)
        self.assertIn('cobertura', resultado)
        self.assertEqual(resultado['referencia'], "hg38")
    
    def test_analisador_creation(self):
        """Testa criação do analisador."""
        analisador = Analisador()
        
        self.assertIsInstance(analisador, Analisador)
    
    def test_analisador_analisar_variacao(self):
        """Testa análise de variação."""
        dados_alinhamento = {"taxa_alinhamento": 95.0}
        resultado = self.analisador.analisar_variacao(dados_alinhamento)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_analise', resultado)
        self.assertIn('variantes_encontradas', resultado)
        self.assertIn('qualidade_analise', resultado)
        self.assertEqual(resultado['tipo_analise'], "variacao_genetica")
    
    def test_gerador_relatorios_creation(self):
        """Testa criação do gerador de relatórios."""
        gerador = GeradorRelatorios()
        
        self.assertIsInstance(gerador, GeradorRelatorios)
    
    def test_gerador_relatorios_gerar_relatorio_variacao(self):
        """Testa geração de relatório de variação."""
        dados_analise = {"variantes_encontradas": 10}
        resultado = self.gerador_relatorios.gerar_relatorio_variacao(dados_analise)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('titulo', resultado)
        self.assertIn('resumo', resultado)
        self.assertIn('formato', resultado)
        self.assertIn('arquivo_saida', resultado)
        self.assertEqual(resultado['titulo'], "Relatório de Variação Genética")
    
    def test_facade_executar_analise_genomica_completa(self):
        """Testa execução completa de análise genômica via fachada."""
        resultado = self.facade.executar_analise_genomica_completa("SAMPLE001", "illumina")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('etapas', resultado)
        self.assertIn('resultado_final', resultado)
        self.assertIn('tempo_total', resultado)
        self.assertEqual(resultado['status'], "concluida")
    
    def test_facade_simplificacao_interface(self):
        """Testa simplificação da interface pela fachada."""
        # Cliente não precisa conhecer todos os subsistemas
        resultado = self.facade.executar_analise_genomica_completa("SAMPLE001")
        
        # A fachada coordena tudo internamente
        self.assertIsInstance(resultado, dict)
        self.assertIn('resultado_final', resultado)
    
    def test_facade_acesso_direto_vs_indireto(self):
        """Testa acesso direto vs indireto via fachada."""
        # Acesso direto (complexo)
        dados_extraidos = self.extrator.extrair_dna("SAMPLE001")
        dados_quantificados = self.preparador.quantificar_amostra(dados_extraidos)
        dados_sequenciados = self.sequenciador.sequenciar_illumina(dados_quantificados)
        
        # Acesso via fachada (simples)
        resultado_facade = self.facade.executar_analise_genomica_completa("SAMPLE001")
        
        # Ambos devem funcionar, mas fachada é mais simples
        self.assertIsInstance(dados_sequenciados, dict)
        self.assertIsInstance(resultado_facade, dict)
    
    def test_facade_desacoplamento(self):
        """Testa desacoplamento proporcionado pela fachada."""
        # Cliente só conhece a fachada, não os subsistemas
        facade = SistemaBioinformaticaFacade()
        
        # Interface unificada e simplificada
        self.assertTrue(hasattr(facade, 'executar_analise_genomica_completa'))
        
        # Mas internamente tem todos os subsistemas
        self.assertIsInstance(facade.extrator, ExtratorAmostras)
        self.assertIsInstance(facade.preparador, PreparadorAmostras)
    
    def test_facade_organizacao_subsistemas(self):
        """Testa organização dos subsistemas pela fachada."""
        # Fachada organiza e coordena os subsistemas
        resultado = self.facade.executar_analise_genomica_completa("SAMPLE001")
        
        # Deve conter resultados de múltiplos subsistemas
        self.assertIn('etapas', resultado)
        etapas = resultado['etapas']
        
        # Verificar se etapas principais foram executadas
        self.assertIsInstance(etapas, dict)
        self.assertGreater(len(etapas), 0)
    
    def test_facade_facilitacao_uso(self):
        """Testa facilitação do uso pela fachada."""
        # Interface simples para operação complexa
        resultado = self.facade.executar_analise_genomica_completa("SAMPLE001")
        
        # Cliente não precisa saber sobre:
        # - Extração, preparação, sequenciamento, alinhamento, análise
        # - Parâmetros específicos de cada subsistema
        # - Ordem correta das operações
        # - Tratamento de erros entre subsistemas
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('resultado_final', resultado)
    
    def test_facade_benefits(self):
        """Testa benefícios do padrão Facade."""
        # 1. Interface simplificada
        self.assertTrue(hasattr(self.facade, 'executar_analise_genomica_completa'))
        
        # 2. Desacoplamento
        # Cliente não conhece os subsistemas diretamente
        
        # 3. Organização
        # Fachada organiza os subsistemas de forma lógica
        
        # 4. Flexibilidade
        # Pode mudar implementação interna sem afetar cliente
        
        # Verificar se todos os subsistemas estão presentes
        self.assertIsNotNone(self.facade.extrator)
        self.assertIsNotNone(self.facade.preparador)
        self.assertIsNotNone(self.facade.sequenciador)
        self.assertIsNotNone(self.facade.alinhador)
        self.assertIsNotNone(self.facade.analisador)
        self.assertIsNotNone(self.facade.gerador_relatorios)


if __name__ == '__main__':
    unittest.main()
