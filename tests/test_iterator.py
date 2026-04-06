import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.comportamentais.iterator import (
    ResultadosSequenciamento, ResultadosProteomicos, ResultadosVariacao, ResultadosExpressao,
    IteradorMultiplasColecoes, TipoDado
)


class TestIterator(unittest.TestCase):
    """Testes para o padrão Iterator."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.resultados_seq = ResultadosSequenciamento()
        self.resultados_prot = ResultadosProteomicos()
        self.resultados_var = ResultadosVariacao()
        self.resultados_exp = ResultadosExpressao()
        
        # Adicionar alguns resultados de teste
        from patterns.comportamentais.iterator import ResultadoAnalise
        
        self.resultados_seq.adicionar(ResultadoAnalise("SEQ001", TipoDado.SEQUENCIA, {"plataforma": "illumina", "reads": 50000000}))
        self.resultados_seq.adicionar(ResultadoAnalise("SEQ002", TipoDado.SEQUENCIA, {"plataforma": "ont", "reads": 1000000}))
        self.resultados_seq.adicionar(ResultadoAnalise("SEQ003", TipoDado.SEQUENCIA, {"plataforma": "illumina", "reads": 45000000}))
        
        self.resultados_prot.adicionar(ResultadoAnalise("PROT001", TipoDado.PROTEINA, {"proteina": "Hemoglobina", "peso_molecular": 15867.0}))
        self.resultados_prot.adicionar(ResultadoAnalise("PROT002", TipoDado.PROTEINA, {"proteina": "Mioglobina", "peso_molecular": 16950.0}))
        self.resultados_prot.adicionar(ResultadoAnalise("PROT003", TipoDado.PROTEINA, {"proteina": "Albumina", "peso_molecular": 66437.0}))
        
        self.resultados_var.adicionar(ResultadoAnalise("VAR001", TipoDado.VARIAÇÃO, {"gene": "BRCA1", "impacto_clinico": "patogenico"}))
        self.resultados_var.adicionar(ResultadoAnalise("VAR002", TipoDado.VARIAÇÃO, {"gene": "TP53", "impacto_clinico": "benigno"}))
        self.resultados_var.adicionar(ResultadoAnalise("VAR003", TipoDado.VARIAÇÃO, {"gene": "EGFR", "impacto_clinico": "patogenico"}))
        
        self.resultados_exp.adicionar(ResultadoAnalise("EXP001", TipoDado.EXPRESSAO, {"gene": "BRCA1", "fold_change": 2.5}))
        self.resultados_exp.adicionar(ResultadoAnalise("EXP002", TipoDado.EXPRESSAO, {"gene": "TP53", "fold_change": -2.0}))
        self.resultados_exp.adicionar(ResultadoAnalise("EXP003", TipoDado.EXPRESSAO, {"gene": "EGFR", "fold_change": 5.0}))
    
    def test_criar_iterador_sequenciamento(self):
        """Testa criação de iterador de sequenciamento."""
        iterador = self.resultados_seq.criar_iterador()
        self.assertIsNotNone(iterador)
    
    def test_iterar_sequenciamento(self):
        """Testa iteração sobre resultados de sequenciamento."""
        iterador = self.resultados_seq.criar_iterador()
        resultados = []
        
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 3)
        self.assertEqual(resultados[0].id_resultado, "SEQ001")
        self.assertEqual(resultados[1].id_resultado, "SEQ002")
        self.assertEqual(resultados[2].id_resultado, "SEQ003")
    
    def test_iterar_sequenciamento_com_filtro_plataforma(self):
        """Testa iteração com filtro de plataforma."""
        iterador = self.resultados_seq.criar_iterador()
        iterador.definir_filtro_plataforma("illumina")
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 2)
        self.assertEqual(resultados[0].dados["plataforma"], "illumina")
        self.assertEqual(resultados[1].dados["plataforma"], "illumina")
    
    def test_iterar_proteomicos(self):
        """Testa iteração sobre resultados proteômicos."""
        iterador = self.resultados_prot.criar_iterador()
        resultados = []
        
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 3)
        self.assertEqual(resultados[0].id_resultado, "PROT001")
        self.assertEqual(resultados[1].id_resultado, "PROT002")
        self.assertEqual(resultados[2].id_resultado, "PROT003")
    
    def test_iterar_proteomicos_com_filtro_peso(self):
        """Testa iteração com filtro de peso molecular."""
        iterador = self.resultados_prot.criar_iterador()
        iterador.definir_filtro_peso(15000, 17000)
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 2)
        self.assertEqual(resultados[0].dados["proteina"], "Hemoglobina")
        self.assertEqual(resultados[1].dados["proteina"], "Mioglobina")
    
    def test_iterar_proteomicos_ordenado_por_peso(self):
        """Testa iteração ordenada por peso molecular."""
        iterador = self.resultados_prot.criar_iterador()
        iterador.definir_ordem_peso(crescente=True)
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 3)
        self.assertEqual(resultados[0].dados["proteina"], "Hemoglobina")  # 15867.0
        self.assertEqual(resultados[1].dados["proteina"], "Mioglobina")   # 16950.0
        self.assertEqual(resultados[2].dados["proteina"], "Albumina")      # 66437.0
    
    def test_iterar_variacao(self):
        """Testa iteração sobre resultados de variação."""
        iterador = self.resultados_var.criar_iterador()
        resultados = []
        
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 3)
        self.assertEqual(resultados[0].id_resultado, "VAR001")
        self.assertEqual(resultados[1].id_resultado, "VAR002")
        self.assertEqual(resultados[2].id_resultado, "VAR003")
    
    def test_iterar_variacao_com_filtro_impacto(self):
        """Testa iteração com filtro de impacto clínico."""
        iterador = self.resultados_var.criar_iterador()
        iterador.definir_filtro_impacto("patogenico")
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 2)
        self.assertEqual(resultados[0].dados["impacto_clinico"], "patogenico")
        self.assertEqual(resultados[1].dados["impacto_clinico"], "patogenico")
    
    def test_iterar_variacao_com_filtro_frequencia(self):
        """Testa iteração com filtro de frequência."""
        iterador = self.resultados_var.criar_iterador()
        iterador.definir_filtro_frequencia(0.01)
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        # Todos os resultados têm frequência < 0.01
        self.assertEqual(len(resultados), 3)
    
    def test_iterar_expressao(self):
        """Testa iteração sobre resultados de expressão."""
        iterador = self.resultados_exp.criar_iterador()
        resultados = []
        
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 3)
        self.assertEqual(resultados[0].id_resultado, "EXP001")
        self.assertEqual(resultados[1].id_resultado, "EXP002")
        self.assertEqual(resultados[2].id_resultado, "EXP003")
    
    def test_iterar_expressao_com_filtro_regulacao(self):
        """Testa iteração com filtro de regulação."""
        iterador = self.resultados_exp.criar_iterador()
        iterador.definir_filtro_regulacao("up")
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 2)
        self.assertGreater(resultados[0].dados["fold_change"], 0)
        self.assertGreater(resultados[1].dados["fold_change"], 0)
    
    def test_iterar_expressao_com_filtro_fold_change(self):
        """Testa iteração com filtro de fold change."""
        iterador = self.resultados_exp.criar_iterador()
        iterador.definir_filtro_fold_change(2.0)
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 2)
        self.assertGreaterEqual(abs(resultados[0].dados["fold_change"]), 2.0)
        self.assertGreaterEqual(abs(resultados[1].dados["fold_change"]), 2.0)
    
    def test_iterar_expressao_ordenado_por_fold_change(self):
        """Testa iteração ordenada por fold change."""
        iterador = self.resultados_exp.criar_iterador()
        iterador.definir_ordem_fold_change()
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 3)
        # Deve estar em ordem decrescente de fold change absoluto
        self.assertEqual(abs(resultados[0].dados["fold_change"]), 5.0)  # EGFR
        self.assertEqual(abs(resultados[1].dados["fold_change"]), 2.5)  # BRCA1
        self.assertEqual(abs(resultados[2].dados["fold_change"]), 2.0)  # TP53
    
    def test_iterador_multiplas_colecoes(self):
        """Testa iterador sobre múltiplas coleções."""
        colecoes = [self.resultados_seq, self.resultados_prot, self.resultados_var, self.resultados_exp]
        iterador_multiplas = IteradorMultiplasColecoes(colecoes)
        
        resultados = []
        while iterador_multiplas.tem_proximo():
            resultado = iterador_multiplas.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 12)  # 3 + 3 + 3 + 3
    
    def test_resetar_iterador(self):
        """Testa reset do iterador."""
        iterador = self.resultados_seq.criar_iterador()
        
        # Consumir alguns resultados
        iterador.proximo()
        iterador.proximo()
        
        # Resetar
        iterador.resetar()
        
        # Deve começar do início
        resultado = iterador.proximo()
        self.assertEqual(resultado.id_resultado, "SEQ001")
    
    def test_obter_total_resultados(self):
        """Testa obtenção do total de resultados."""
        self.assertEqual(self.resultados_seq.obter_total(), 3)
        self.assertEqual(self.resultados_prot.obter_total(), 3)
        self.assertEqual(self.resultados_var.obter_total(), 3)
        self.assertEqual(self.resultados_exp.obter_total(), 3)
    
    def test_adicionar_resultado_tipo_incorreto(self):
        """Testa adição de resultado com tipo incorreto."""
        from patterns.comportamentais.iterator import ResultadoAnalise
        
        with self.assertRaises(ValueError):
            self.resultados_seq.adicionar(ResultadoAnalise("PROT001", TipoDado.PROTEINA, {}))
        
        with self.assertRaises(ValueError):
            self.resultados_prot.adicionar(ResultadoAnalise("SEQ001", TipoDado.SEQUENCIA, {}))
    
    def test_filtro_sem_resultados(self):
        """Testa filtro que não retorna resultados."""
        iterador = self.resultados_seq.criar_iterador()
        iterador.definir_filtro_plataforma("plataforma_inexistente")
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 0)
    
    def test_colecao_vazia(self):
        """Testa iteração sobre coleção vazia."""
        colecao_vazia = ResultadosSequenciamento()
        iterador = colecao_vazia.criar_iterador()
        
        self.assertFalse(iterador.tem_proximo())
        self.assertIsNone(iterador.proximo())
    
    def test_iterador_multiplas_colecoes_vazias(self):
        """Testa iterador sobre coleções vazias."""
        colecoes_vazias = [ResultadosSequenciamento(), ResultadosProteomicos()]
        iterador = IteradorMultiplasColecoes(colecoes_vazias)
        
        self.assertFalse(iterador.tem_proximo())
        self.assertIsNone(iterador.proximo())
    
    def test_combinacao_filtros(self):
        """Testa combinação de múltiplos filtros."""
        iterador = self.resultados_prot.criar_iterador()
        iterador.definir_filtro_peso(15000, 17000)
        iterador.definir_ordem_peso(crescente=True)
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 2)
        # Deve estar ordenado por peso
        self.assertLessEqual(resultados[0].dados["peso_molecular"], resultados[1].dados["peso_molecular"])
        # Deve estar dentro do filtro
        self.assertTrue(15000 <= resultados[0].dados["peso_molecular"] <= 17000)
        self.assertTrue(15000 <= resultados[1].dados["peso_molecular"] <= 17000)
    
    def test_iterador_multiplas_colecoes_uma_vazia(self):
        """Testa iterador com uma coleção vazia."""
        colecoes = [self.resultados_seq, ResultadosProteomicos(), self.resultados_var]
        iterador = IteradorMultiplasColecoes(colecoes)
        
        resultados = []
        while iterador.tem_proximo():
            resultado = iterador.proximo()
            resultados.append(resultado)
        
        self.assertEqual(len(resultados), 6)  # 3 + 0 + 3
    
    def test_resetar_iterador_multiplas_colecoes(self):
        """Testa reset do iterador múltiplas coleções."""
        colecoes = [self.resultados_seq, self.resultados_prot]
        iterador = IteradorMultiplasColecoes(colecoes)
        
        # Consumir alguns resultados
        for _ in range(3):
            iterador.proximo()
        
        # Resetar
        iterador.resetar()
        
        # Deve começar do início
        resultado = iterador.proximo()
        self.assertEqual(resultado.id_resultado, "SEQ001")


if __name__ == "__main__":
    unittest.main()
