import unittest
import sys
import os
import time

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.comportamentais.command import (
    SequenciarCommand, AlinharCommand, AnalisarCommand, MacroCommand, InvocadorComandos
)


class TestCommand(unittest.TestCase):
    """Testes para o padrão Command."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.invocador = InvocadorComandos()
    
    def test_criar_comando_sequenciamento(self):
        """Testa criação de comando de sequenciamento."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        
        self.assertEqual(comando.nome, "Sequenciar Amostra_001")
        self.assertEqual(comando.amostra, "Amostra_001")
        self.assertEqual(comando.plataforma, "illumina")
        self.assertEqual(comando.status.value, "pendente")
    
    def test_criar_comando_alinhamento(self):
        """Testa criação de comando de alinhamento."""
        comando = AlinharCommand("arquivo.fastq", "hg38")
        
        self.assertEqual(comando.nome, "Alinhar arquivo.fastq")
        self.assertEqual(comando.arquivo_fastq, "arquivo.fastq")
        self.assertEqual(comando.referencia, "hg38")
        self.assertEqual(comando.status.value, "pendente")
    
    def test_criar_comando_analise(self):
        """Testa criação de comando de análise."""
        comando = AnalisarCommand("arquivo.bam", "variacao")
        
        self.assertEqual(comando.nome, "Analisar arquivo.bam")
        self.assertEqual(comando.arquivo_bam, "arquivo.bam")
        self.assertEqual(comando.tipo_analise, "variacao")
        self.assertEqual(comando.status.value, "pendente")
    
    def test_executar_comando_sequenciamento(self):
        """Testa execução de comando de sequenciamento."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        resultado = comando.executar()
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["operacao"], "sequenciamento")
        self.assertEqual(resultado["amostra"], "Amostra_001")
        self.assertEqual(resultado["plataforma"], "illumina")
        self.assertIn("resultado", resultado)
        self.assertEqual(comando.status.value, "concluido")
    
    def test_executar_comando_alinhamento(self):
        """Testa execução de comando de alinhamento."""
        comando = AlinharCommand("sequenciamento.fastq", "hg38")
        resultado = comando.executar()
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["operacao"], "alinhamento")
        self.assertEqual(resultado["arquivo_fastq"], "sequenciamento.fastq")
        self.assertEqual(resultado["referencia"], "hg38")
        self.assertIn("resultado", resultado)
        self.assertEqual(comando.status.value, "concluido")
    
    def test_executar_comando_analise(self):
        """Testa execução de comando de análise."""
        comando = AnalisarCommand("alinhado.bam", "padrao")
        resultado = comando.executar()
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["operacao"], "analise_variacao")
        self.assertEqual(resultado["arquivo_bam"], "alinhado.bam")
        self.assertEqual(resultado["tipo_analise"], "padrao")
        self.assertIn("resultado", resultado)
        self.assertEqual(comando.status.value, "concluido")
    
    def test_comando_sequenciamento_parametros_invalidos(self):
        """Testa comando de sequenciamento com parâmetros inválidos."""
        comando = SequenciarCommand("", "illumina")  # Amostra vazia
        
        with self.assertRaises(Exception):
            comando.executar()
        
        self.assertEqual(comando.status.value, "falhou")
    
    def test_comando_alinhamento_parametros_invalidos(self):
        """Testa comando de alinhamento com parâmetros inválidos."""
        comando = AlinharCommand("", "hg38")  # Arquivo vazio
        
        with self.assertRaises(Exception):
            comando.executar()
        
        self.assertEqual(comando.status.value, "falhou")
    
    def test_comando_analise_parametros_invalidos(self):
        """Testa comando de análise com parâmetros inválidos."""
        comando = AnalisarCommand("", "padrao")  # Arquivo vazio
        
        with self.assertRaises(Exception):
            comando.executar()
        
        self.assertEqual(comando.status.value, "falhou")
    
    def test_desfazer_comando_sequenciamento(self):
        """Testa desfazer comando de sequenciamento."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        comando.executar()
        
        resultado_desfazer = comando.desfazer()
        self.assertTrue(resultado_desfazer)
        self.assertEqual(comando.status.value, "desfeito")
        self.assertEqual(len(comando.arquivos_gerados), 0)
    
    def test_desfazer_comando_nao_executado(self):
        """Testa desfazer comando não executado."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        
        resultado_desfazer = comando.desfazer()
        self.assertFalse(resultado_desfazer)
    
    def test_criar_macro_comando(self):
        """Testa criação de macro comando."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            AlinharCommand("sequenciamento.fastq", "hg38"),
            AnalisarCommand("alinhado.bam", "variacao")
        ]
        
        macro = MacroCommand("Pipeline Completo", comandos)
        
        self.assertEqual(macro.nome, "Pipeline Completo")
        self.assertEqual(len(macro.comandos), 3)
        self.assertEqual(macro.status.value, "pendente")
    
    def test_executar_macro_comando(self):
        """Testa execução de macro comando."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            AlinharCommand("sequenciamento.fastq", "hg38")
        ]
        
        macro = MacroCommand("Pipeline Teste", comandos)
        resultado = macro.executar()
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["nome_macro"], "Pipeline Teste")
        self.assertEqual(resultado["total_comandos"], 2)
        self.assertEqual(resultado["comandos_sucesso"], 2)
        self.assertEqual(resultado["comandos_falha"], 0)
        self.assertEqual(len(resultado["resultados"]), 2)
        self.assertEqual(macro.status.value, "concluido")
    
    def test_executar_macro_comando_com_falha(self):
        """Testa execução de macro comando com falha."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            SequenciarCommand("", "illumina"),  # Vai falhar
            AlinharCommand("sequenciamento.fastq", "hg38")
        ]
        
        macro = MacroCommand("Pipeline com Falha", comandos)
        resultado = macro.executar()
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["total_comandos"], 3)
        self.assertEqual(resultado["comandos_sucesso"], 2)
        self.assertEqual(resultado["comandos_falha"], 1)
    
    def test_desfazer_macro_comando(self):
        """Testa desfazer macro comando."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            AlinharCommand("sequenciamento.fastq", "hg38")
        ]
        
        macro = MacroCommand("Pipeline Teste", comandos)
        macro.executar()
        
        resultado_desfazer = macro.desfazer()
        self.assertTrue(resultado_desfazer)
        self.assertEqual(macro.status.value, "desfeito")
    
    def test_desfazer_macro_comando_parcial(self):
        """Testa desfazer macro comando com comandos não concluídos."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            SequenciarCommand("", "illumina")  # Vai falhar
        ]
        
        macro = MacroCommand("Pipeline Parcial", comandos)
        macro.executar()
        
        resultado_desfazer = macro.desfazer()
        self.assertTrue(resultado_desfazer)  # Ainda deve desfazer os que concluíram
    
    def test_invocador_executar_comando(self):
        """Testa invocador executando comando."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        resultado = self.invocador.executar_comando(comando)
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(len(self.invocador.historico_comandos), 1)
        self.assertEqual(len(self.invocador.pilha_desfazer), 1)
    
    def test_invocador_desfazer_ultimo(self):
        """Testa invocador desfazendo último comando."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        self.invocador.executar_comando(comando)
        
        resultado_desfazer = self.invocador.desfazer_ultimo_comando()
        self.assertTrue(resultado_desfazer)
        self.assertEqual(len(self.invocador.pilha_desfazer), 0)
    
    def test_invocador_desfazer_sem_comandos(self):
        """Testa invocador desfazer sem comandos na pilha."""
        resultado_desfazer = self.invocador.desfazer_ultimo_comando()
        self.assertFalse(resultado_desfazer)
    
    def test_invocador_desfazer_todos(self):
        """Testa invocador desfazendo todos os comandos."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            AlinharCommand("sequenciamento.fastq", "hg38"),
            AnalisarCommand("alinhado.bam", "variacao")
        ]
        
        for comando in comandos:
            self.invocador.executar_comando(comando)
        
        self.assertEqual(len(self.invocador.pilha_desfazer), 3)
        
        resultado_desfazer = self.invocador.desfazer_todos()
        self.assertTrue(resultado_desfazer)
        self.assertEqual(len(self.invocador.pilha_desfazer), 0)
    
    def test_invocador_obter_historico(self):
        """Testa invocador obtendo histórico."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            AlinharCommand("sequenciamento.fastq", "hg38")
        ]
        
        for comando in comandos:
            self.invocador.executar_comando(comando)
        
        historico = self.invocador.obter_historico()
        self.assertEqual(len(historico), 2)
        self.assertEqual(historico[0]["nome"], "Sequenciar Amostra_001")
        self.assertEqual(historico[1]["nome"], "Alinhar sequenciamento.fastq")
    
    def test_invocador_obter_estatisticas(self):
        """Testa invocador obtendo estatísticas."""
        comandos = [
            SequenciarCommand("Amostra_001", "illumina"),
            AlinharCommand("sequenciamento.fastq", "hg38"),
            AnalisarCommand("alinhado.bam", "variacao")
        ]
        
        for comando in comandos:
            self.invocador.executar_comando(comando)
        
        stats = self.invocador.obter_estatisticas()
        
        self.assertEqual(stats["total_requests"], 3)
        self.assertEqual(stats["comandos_desfaziveis"], 3)
        self.assertIn("operacoes", stats)
        self.assertIn("sequenciar", stats["operacoes"])
        self.assertIn("alinhamento", stats["operacoes"])
        self.assertIn("analise_variacao", stats["operacoes"])
    
    def test_comando_obter_info(self):
        """Testa comando obtendo informações."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        comando.executar()
        
        info = comando.obter_info()
        
        self.assertEqual(info["nome"], "Sequenciar Amostra_001")
        self.assertEqual(info["status"], "concluido")
        self.assertIsNotNone(info["resultado"])
        self.assertIsNone(info["erro"])
        self.assertIsNotNone(info["tempo_execucao"])
    
    def test_comando_obter_info_com_erro(self):
        """Testa comando obtendo informações com erro."""
        comando = SequenciarCommand("", "illumina")
        
        try:
            comando.executar()
        except:
            pass
        
        info = comando.obter_info()
        
        self.assertEqual(info["status"], "falhou")
        self.assertIsNone(info["resultado"])
        self.assertIsNotNone(info["erro"])
    
    def test_macro_comando_aninhado(self):
        """Testa macro comando com comandos aninhados."""
        sub_macro = MacroCommand("Sub Pipeline", [
            SequenciarCommand("Amostra_001", "illumina"),
            AlinharCommand("sequenciamento.fastq", "hg38")
        ])
        
        macro_principal = MacroCommand("Pipeline Principal", [
            SequenciarCommand("Amostra_002", "illumina"),
            sub_macro,
            AnalisarCommand("alinhado.bam", "variacao")
        ])
        
        resultado = macro_principal.executar()
        
        self.assertEqual(resultado["status"], "sucesso")
        self.assertEqual(resultado["total_comandos"], 3)  # Sub macro conta como 1
        self.assertEqual(resultado["comandos_sucesso"], 3)
    
    def test_tempo_execucao_comandos(self):
        """Testa tempo de execução dos comandos."""
        comando = SequenciarCommand("Amostra_001", "illumina")
        
        inicio = time.time()
        comando.executar()
        fim = time.time()
        
        info = comando.obter_info()
        tempo_execucao = info["tempo_execucao"]
        
        self.assertIsNotNone(tempo_execucao)
        self.assertGreater(tempo_execucao, 0)
        self.assertLess(tempo_execucao, fim - inicio + 0.1)  # Pequena margem de erro
    
    def test_comandos_concorrentes(self):
        """Testa comandos executados concorrentemente."""
        import threading
        
        resultados = []
        erros = []
        
        def executar_comando():
            try:
                comando = SequenciarCommand("Amostra_Concorrente", "illumina")
                resultado = comando.executar()
                resultados.append(resultado)
            except Exception as e:
                erros.append(e)
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=executar_comando)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        self.assertEqual(len(erros), 0)
        self.assertEqual(len(resultados), 5)
        
        for resultado in resultados:
            self.assertEqual(resultado["status"], "sucesso")


if __name__ == "__main__":
    unittest.main()
