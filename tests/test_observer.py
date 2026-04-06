import unittest
import sys
import os
import time

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.comportamentais.observer import (
    Pesquisador, SistemaAlerta, AnaliseGenomica, TipoEvento
)


class TestObserver(unittest.TestCase):
    """Testes para o padrão Observer."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.pesquisador = Pesquisador("Dr. Teste", "teste@lab.com", "genomica")
        self.sistema_alerta = SistemaAlerta("Teste", "alto")
    
    def test_criacao_observador(self):
        """Testa criação de observadores."""
        self.assertEqual(self.pesquisador.nome, "Dr. Teste")
        self.assertEqual(self.pesquisador.email, "teste@lab.com")
        self.assertEqual(self.pesquisador.especialidade, "genomica")
        self.assertEqual(len(self.pesquisador.notificacoes_recebidas), 0)
    
    def test_definir_interesses(self):
        """Testa definição de interesses do observador."""
        interesses = [TipoEvento.ANALISE_CONCLUIDA, TipoEvento.ANALISE_FALHOU]
        self.pesquisador.definir_interesses(interesses)
        self.assertEqual(self.pesquisador.interesses, interesses)
    
    def test_receber_notificacao_interesse(self):
        """Testa recebimento de notificação de interesse."""
        self.pesquisador.definir_interesses([TipoEvento.ANALISE_CONCLUIDA])
        
        evento = TipoEvento.ANALISE_CONCLUIDA
        from patterns.comportamentais.observer import Evento
        evento_obj = Evento(evento, "Teste", {"resultado": "sucesso"})
        
        self.pesquisador.atualizar(evento_obj)
        self.assertEqual(len(self.pesquisador.notificacoes_recebidas), 1)
    
    def test_receber_notificacao_sem_interesse(self):
        """Testa recebimento de notificação sem interesse."""
        self.pesquisador.definir_interesses([TipoEvento.ANALISE_CONCLUIDA])
        
        evento = TipoEvento.ANALISE_FALHOU
        from patterns.comportamentais.observer import Evento
        evento_obj = Evento(evento, "Teste", {"erro": "falha"})
        
        self.pesquisador.atualizar(evento_obj)
        self.assertEqual(len(self.pesquisador.notificacoes_recebidas), 0)
    
    def test_sistema_alerta(self):
        """Testa funcionalidade do sistema de alerta."""
        self.sistema_alerta.adicionar_regra_alerta(TipoEvento.ANALISE_FALHOU, "alta")
        
        evento = TipoEvento.ANALISE_FALHOU
        from patterns.comportamentais.observer import Evento
        evento_obj = Evento(evento, "Teste", {"erro": "falha crítica"})
        
        self.sistema_alerta.atualizar(evento_obj)
        self.assertEqual(len(self.sistema_alerta.alertas), 1)
        self.assertEqual(self.sistema_alerta.alertas[0]["prioridade"], "alta")
    
    def test_analise_genomica_observador(self):
        """Testa análise genômica como sujeito observável."""
        analise = AnaliseGenomica("TESTE_001", "Análise de teste")
        analise.adicionar_observador(self.pesquisador)
        
        self.assertEqual(len(analise.observadores), 1)
        self.assertIn(self.pesquisador, analise.observadores)
    
    def test_notificacao_conclusao_analise(self):
        """Testa notificação de conclusão de análise."""
        analise = AnaliseGenomica("TESTE_001", "Análise de teste")
        analise.adicionar_observador(self.pesquisador)
        self.pesquisador.definir_interesses([TipoEvento.ANALISE_CONCLUIDA])
        
        resultado = {"variantes": 100, "qualidade": "alta"}
        analise.concluir_analise(resultado)
        
        self.assertEqual(len(self.pesquisador.notificacoes_recebidas), 1)
        self.assertEqual(self.pesquisador.notificacoes_recebidas[0].tipo, TipoEvento.ANALISE_CONCLUIDA)
    
    def test_notificacao_falha_analise(self):
        """Testa notificação de falha de análise."""
        analise = AnaliseGenomica("TESTE_001", "Análise de teste")
        analise.adicionar_observador(self.pesquisador)
        self.pesquisador.definir_interesses([TipoEvento.ANALISE_FALHOU])
        
        erro = "Erro de processamento"
        analise.falhar_analise(erro)
        
        self.assertEqual(len(self.pesquisador.notificacoes_recebidas), 1)
        self.assertEqual(self.pesquisador.notificacoes_recebidas[0].tipo, TipoEvento.ANALISE_FALHOU)
    
    def test_multiplos_observadores(self):
        """Testa múltiplos observadores no mesmo sujeito."""
        pesquisador2 = Pesquisador("Dra. Teste2", "teste2@lab.com", "proteomica")
        
        analise = AnaliseGenomica("TESTE_001", "Análise de teste")
        analise.adicionar_observador(self.pesquisador)
        analise.adicionar_observador(pesquisador2)
        
        self.assertEqual(len(analise.observadores), 2)
        
        # Notificar conclusão
        resultado = {"variantes": 100, "qualidade": "alta"}
        analise.concluir_analise(resultado)
        
        # Ambos devem receber notificação se tiverem interesse
        self.pesquisador.definir_interesses([TipoEvento.ANALISE_CONCLUIDA])
        pesquisador2.definir_interesses([TipoEvento.ANALISE_CONCLUIDA])
        
        analise.concluir_analise(resultado)
        
        self.assertEqual(len(self.pesquisador.notificacoes_recebidas), 2)
        self.assertEqual(len(pesquisador2.notificacoes_recebidas), 2)
    
    def test_remover_observador(self):
        """Testa remoção de observador."""
        analise = AnaliseGenomica("TESTE_001", "Análise de teste")
        analise.adicionar_observador(self.pesquisador)
        
        self.assertEqual(len(analise.observadores), 1)
        
        analise.remover_observador(self.pesquisador)
        self.assertEqual(len(analise.observadores), 0)
    
    def test_historico_eventos(self):
        """Testa histórico de eventos do sujeito."""
        analise = AnaliseGenomica("TESTE_001", "Análise de teste")
        analise.adicionar_observador(self.pesquisador)
        
        analise.iniciar_analise()
        analise.concluir_analise({"variantes": 100})
        
        historico = analise.obter_historico_eventos()
        self.assertEqual(len(historico), 2)
        self.assertEqual(historico[0].tipo, TipoEvento.ANALISE_INICIADA)
        self.assertEqual(historico[1].tipo, TipoEvento.ANALISE_CONCLUIDA)


if __name__ == "__main__":
    unittest.main()
