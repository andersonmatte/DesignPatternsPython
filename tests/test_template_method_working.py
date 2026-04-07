"""
Testes para o padrão Template Method
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.template_method import (
    TipoAnalise, ResultadoPipeline
)


class TestTemplateMethod(unittest.TestCase):
    """Testes para o padrão Template Method."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.resultado_genomica = ResultadoPipeline(TipoAnalise.GENOMICA)
        self.resultado_proteomica = ResultadoPipeline(TipoAnalise.PROTEOMICA)
        self.resultado_transcriptomica = ResultadoPipeline(TipoAnalise.TRANSCRIPTOMICA)
    
    def test_tipo_analise_enum(self):
        """Testa enum TipoAnalise."""
        self.assertEqual(TipoAnalise.GENOMICA.value, "genomica")
        self.assertEqual(TipoAnalise.PROTEOMICA.value, "proteomica")
        self.assertEqual(TipoAnalise.TRANSCRIPTOMICA.value, "transcriptomica")
        self.assertEqual(TipoAnalise.METABOLOMICA.value, "metabolomica")
    
    def test_resultado_pipeline_creation(self):
        """Testa criação de ResultadoPipeline."""
        resultado = ResultadoPipeline(TipoAnalise.GENOMICA)
        
        self.assertIsInstance(resultado, ResultadoPipeline)
        self.assertEqual(resultado.tipo_analise, TipoAnalise.GENOMICA)
        self.assertEqual(len(resultado.etapas_concluidas), 0)
        self.assertEqual(len(resultado.resultados_etapas), 0)
    
    def test_resultado_pipeline_adicionar_etapa(self):
        """Testa adição de etapa ao resultado."""
        self.resultado_genomica.adicionar_etapa("preprocessamento", {"status": "concluido"})
        
        self.assertIn("preprocessamento", self.resultado_genomica.etapas_concluidas)
        self.assertIn("preprocessamento", self.resultado_genomica.resultados_etapas)
        self.assertEqual(len(self.resultado_genomica.etapas_concluidas), 1)
    
    def test_resultado_pipeline_obter_resumo(self):
        """Testa obtenção de resumo do resultado."""
        self.resultado_genomica.adicionar_etapa("preprocessamento", {"status": "concluido"})
        self.resultado_genomica.adicionar_etapa("alinhamento", {"status": "concluido"})
        
        resumo = self.resultado_genomica.obter_resumo()
        
        self.assertIsInstance(resumo, dict)
        self.assertIn('tipo_analise', resumo)
        self.assertIn('total_etapas', resumo)
        self.assertIn('etapas_concluidas', resumo)
        self.assertIn('taxa_conclusao', resumo)
        
        self.assertEqual(resumo['tipo_analise'], "genomica")
        self.assertEqual(resumo['total_etapas'], 2)
        self.assertEqual(resumo['taxa_conclusao'], 100.0)
    
    def test_resultado_pipeline_diferentes_tipos(self):
        """Testa resultados de diferentes tipos de análise."""
        resumo_genomica = self.resultado_genomica.obter_resumo()
        resumo_proteomica = self.resultado_proteomica.obter_resumo()
        resumo_transcriptomica = self.resultado_transcriptomica.obter_resumo()
        
        self.assertEqual(resumo_genomica['tipo_analise'], "genomica")
        self.assertEqual(resumo_proteomica['tipo_analise'], "proteomica")
        self.assertEqual(resumo_transcriptomica['tipo_analise'], "transcriptomica")
    
    def test_resultado_pipeline_taxa_conclusao(self):
        """Testa cálculo de taxa de conclusão."""
        # Adicionar etapas concluídas
        self.resultado_genomica.adicionar_etapa("etapa1", {"status": "concluido"})
        self.resultado_genomica.adicionar_etapa("etapa2", {"status": "concluido"})
        self.resultado_genomica.adicionar_etapa("etapa3", {"status": "erro"})
        
        resumo = self.resultado_genomica.obter_resumo()
        
        # 2 de 3 etapas concluídas = 66.67%
        self.assertAlmostEqual(resumo['taxa_conclusao'], 66.67, places=1)
    
    def test_resultado_pipeline_validacao(self):
        """Testa validação de resultado."""
        # Resultado sem etapas
        self.assertFalse(self.resultado_genomica.esta_valido())
        
        # Adicionar etapas
        self.resultado_genomica.adicionar_etapa("etapa1", {"status": "concluido"})
        self.resultado_genomica.adicionar_etapa("etapa2", {"status": "concluido"})
        
        self.assertTrue(self.resultado_genomica.esta_valido())
    
    def test_resultado_pipeline_tempo_execucao(self):
        """Testa registro de tempo de execução."""
        import time
        
        # Iniciar timer
        self.resultado_genomica.iniciar_timer()
        time.sleep(0.1)  # Pequena pausa
        self.resultado_genomica.finalizar_timer()
        
        resumo = self.resultado_genomica.obter_resumo()
        
        self.assertIn('tempo_execucao', resumo)
        self.assertGreater(resumo['tempo_execucao'], 0.1)
    
    def test_resultado_pipeline_erro_tratamento(self):
        """Testa tratamento de erros no resultado."""
        # Adicionar etapa com erro
        self.resultado_genomica.adicionar_etapa("etapa_com_erro", {"status": "erro", "mensagem": "Falha"})
        
        resumo = self.resultado_genomica.obter_resumo()
        
        self.assertIn('erros', resumo)
        self.assertEqual(len(resumo['erros']), 1)
        self.assertEqual(resumo['erros'][0]['etapa'], "etapa_com_erro")
        self.assertEqual(resumo['erros'][0]['mensagem'], "Falha")
    
    def test_resultado_pipeline_exportacao(self):
        """Testa exportação de resultados."""
        # Adicionar algumas etapas
        self.resultado_genomica.adicionar_etapa("preprocessamento", {"status": "concluido"})
        self.resultado_genomica.adicionar_etapa("alinhamento", {"status": "concluido"})
        
        # Exportar para dicionário
        exportado = self.resultado_genomica.exportar_dict()
        
        self.assertIsInstance(exportado, dict)
        self.assertIn('tipo_analise', exportado)
        self.assertIn('etapas', exportado)
        self.assertIn('resumo', exportado)
        self.assertEqual(len(exportado['etapas']), 2)
    
    def test_resultado_pipeline_comparacao(self):
        """Testa comparação entre resultados."""
        # Adicionar etapas diferentes
        self.resultado_genomica.adicionar_etapa("etapa1", {"status": "concluido"})
        self.resultado_proteomica.adicionar_etapa("etapa1", {"status": "concluido"})
        self.resultado_proteomica.adicionar_etapa("etapa2", {"status": "concluido"})
        
        resumo_genomica = self.resultado_genomica.obter_resumo()
        resumo_proteomica = self.resultado_proteomica.obter_resumo()
        
        # Proteômica deve ter mais etapas
        self.assertGreater(resumo_proteomica['total_etapas'], resumo_genomica['total_etapas'])
    
    def test_resultado_pipeline_estado_consistencia(self):
        """Testa consistência de estado do resultado."""
        resultado = ResultadoPipeline(TipoAnalise.GENOMICA)
        
        # Estado inicial
        self.assertEqual(len(resultado.etapas_concluidas), 0)
        self.assertEqual(len(resultado.resultados_etapas), 0)
        
        # Adicionar etapa
        resultado.adicionar_etapa("teste", {"status": "concluido"})
        
        # Estado após adição
        self.assertEqual(len(resultado.etapas_concluidas), 1)
        self.assertEqual(len(resultado.resultados_etapas), 1)
        self.assertEqual(resultado.etapas_concluidas[0], "teste")
        self.assertEqual(resultado.resultados_etapas["teste"]["status"], "concluido")
    
    def test_resultado_pipeline_polimorfismo(self):
        """Testa polimorfismo entre diferentes resultados."""
        resultados = [
            self.resultado_genomica,
            self.resultado_proteomica,
            self.resultado_transcriptomica
        ]
        
        for resultado in resultados:
            # Todos devem ter a mesma interface
            self.assertTrue(hasattr(resultado, 'adicionar_etapa'))
            self.assertTrue(hasattr(resultado, 'obter_resumo'))
            self.assertTrue(hasattr(resultado, 'esta_valido'))
            self.assertTrue(hasattr(resultado, 'exportar_dict'))
            
            # Todos devem retornar resumos consistentes
            resumo = resultado.obter_resumo()
            self.assertIsInstance(resumo, dict)
            self.assertIn('tipo_analise', resumo)
            self.assertIn('total_etapas', resumo)
    
    def test_resultado_pipeline_encapsulamento(self):
        """Testa encapsulamento dos dados do resultado."""
        resultado = ResultadoPipeline(TipoAnalise.GENOMICA)
        
        # Cliente não manipula estado diretamente
        resultado.adicionar_etapa("teste", {"status": "concluido"})
        
        # Acesso controlado através de métodos
        resumo = resultado.obter_resumo()
        self.assertIsInstance(resumo, dict)
        
        # Estado interno protegido
        self.assertIsInstance(resultado.etapas_concluidas, list)
        self.assertIsInstance(resultado.resultados_etapas, dict)
    
    def test_template_method_benefits(self):
        """Testa benefícios do padrão Template Method."""
        # 1. Estrutura comum
        resultado1 = ResultadoPipeline(TipoAnalise.GENOMICA)
        resultado2 = ResultadoPipeline(TipoAnalise.PROTEOMICA)
        
        # Ambos têm a mesma estrutura base
        self.assertTrue(hasattr(resultado1, 'adicionar_etapa'))
        self.assertTrue(hasattr(resultado2, 'adicionar_etapa'))
        
        # 2. Variação no comportamento
        resumo1 = resultado1.obter_resumo()
        resumo2 = resultado2.obter_resumo()
        
        self.assertNotEqual(resumo1['tipo_analise'], resumo2['tipo_analise'])
        
        # 3. Reutilização de código
        resultado1.adicionar_etapa("etapa1", {"status": "concluido"})
        resultado2.adicionar_etapa("etapa1", {"status": "concluido"})
        
        # Mesma lógica aplicada a tipos diferentes
        self.assertEqual(resultado1.obter_resumo()['total_etapas'], 1)
        self.assertEqual(resultado2.obter_resumo()['total_etapas'], 1)
        
        # 4. Extensibilidade
        # Pode adicionar novos tipos de análise sem mudar o código existente
        resultado_metabolomica = ResultadoPipeline(TipoAnalise.METABOLOMICA)
        resumo_metabolomica = resultado_metabolomica.obter_resumo()
        self.assertEqual(resumo_metabolomica['tipo_analise'], "metabolomica")


if __name__ == '__main__':
    unittest.main()
