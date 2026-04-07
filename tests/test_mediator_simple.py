"""
Testes para o padrão Mediator
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.mediator import (
    TipoMensagem, Mensagem, MediatorLaboratorial, 
    SequenciadorComponente, AlinhadorComponente, AnalisadorComponente
)


class TestMediator(unittest.TestCase):
    """Testes para o padrão Mediator."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.mediator = MediatorLaboratorial()
        
        self.sequenciador = SequenciadorComponente("SEQ001", self.mediator)
        self.alinhador = AlinhadorComponente("ALN001", self.mediator)
        self.analisador = AnalisadorComponente("ANA001", self.mediator)
    
    def test_mensagem_creation(self):
        """Testa criação de mensagem."""
        mensagem = Mensagem(
            TipoMensagem.SEQUENCIAMENTO_CONCLUIDO,
            "SEQ001",
            "ALN001",
            {"sequencia": "ATCG", "qualidade": 95.0}
        )
        
        self.assertIsInstance(mensagem, Mensagem)
        self.assertEqual(mensagem.tipo, TipoMensagem.SEQUENCIAMENTO_CONCLUIDO)
        self.assertEqual(mensagem.remetente, "SEQ001")
        self.assertEqual(mensagem.destinatario, "ALN001")
        self.assertEqual(mensagem.dados["sequencia"], "ATCG")
    
    def test_mediator_creation(self):
        """Testa criação do mediator."""
        mediator = MediatorLaboratorial()
        
        self.assertIsInstance(mediator, MediatorLaboratorial)
        self.assertEqual(len(mediator.componentes), 0)
        self.assertEqual(len(mediator.mensagens), 0)
    
    def test_sequenciador_creation(self):
        """Testa criação do componente sequenciador."""
        sequenciador = SequenciadorComponente("SEQ001", self.mediator)
        
        self.assertIsInstance(sequenciador, SequenciadorComponente)
        self.assertEqual(sequenciador.id, "SEQ001")
        self.assertEqual(sequenciador.mediator, self.mediator)
        self.assertEqual(sequenciador.status, "ocioso")
    
    def test_alinhador_creation(self):
        """Testa criação do componente alinhador."""
        alinhador = AlinhadorComponente("ALN001", self.mediator)
        
        self.assertIsInstance(alinhador, AlinhadorComponente)
        self.assertEqual(alinhador.id, "ALN001")
        self.assertEqual(alinhador.mediator, self.mediator)
        self.assertEqual(alinhador.status, "ocioso")
    
    def test_analisador_creation(self):
        """Testa criação do componente analisador."""
        analisador = AnalisadorComponente("ANA001", self.mediator)
        
        self.assertIsInstance(analisador, AnalisadorComponente)
        self.assertEqual(analisador.id, "ANA001")
        self.assertEqual(analisador.mediator, self.mediator)
        self.assertEqual(analisador.status, "ocioso")
    
    def test_mediator_registrar_componente(self):
        """Testa registro de componente no mediator."""
        mediator = MediatorLaboratorial()
        
        mediator.registrar_componente(self.sequenciador)
        
        self.assertEqual(len(mediator.componentes), 1)
        self.assertIn(self.sequenciador, mediator.componentes)
    
    def test_mediator_enviar_mensagem(self):
        """Testa envio de mensagem via mediator."""
        mensagem = Mensagem(
            TipoMensagem.SEQUENCIAMENTO_CONCLUIDO,
            "SEQ001",
            "ALN001",
            {"sequencia": "ATCG"}
        )
        
        self.mediator.enviar_mensagem(mensagem)
        
        self.assertEqual(len(self.mediator.mensagens), 1)
        self.assertEqual(self.mediator.mensagens[0], mensagem)
    
    def test_sequenciador_executar_sequenciamento(self):
        """Testa execução de sequenciamento."""
        dados = {"amostra": "SAMPLE001", "tipo": "DNA"}
        
        resultado = self.sequenciador.executar_sequenciamento(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('sequencia', resultado)
        self.assertIn('qualidade', resultado)
        self.assertEqual(resultado['status'], 'concluido')
        self.assertEqual(self.sequenciador.status, 'concluido')
    
    def test_alinhador_executar_alinhamento(self):
        """Testa execução de alinhamento."""
        dados = {"sequencia": "ATCGATCG", "referencia": "hg38"}
        
        resultado = self.alinhador.executar_alinhamento(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('alinhamento', resultado)
        self.assertIn('score', resultado)
        self.assertEqual(resultado['status'], 'concluido')
        self.assertEqual(self.alinhador.status, 'concluido')
    
    def test_analisador_executar_analise(self):
        """Testa execução de análise."""
        dados = {"alinhamento": "ATCGATCG", "tipo": "variantes"}
        
        resultado = self.analisador.executar_analise(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('variantes', resultado)
        self.assertIn('estatisticas', resultado)
        self.assertEqual(resultado['status'], 'concluido')
        self.assertEqual(self.analisador.status, 'concluido')
    
    def test_sequenciador_receber_mensagem(self):
        """Testa recebimento de mensagem pelo sequenciador."""
        mensagem = Mensagem(
            TipoMensagem.RECURSO_LIBERADO,
            "ALN001",
            "SEQ001",
            {"recurso": "alinhador"}
        )
        
        self.sequenciador.receber_mensagem(mensagem)
        
        # Deve processar a mensagem
        self.assertIsInstance(self.sequenciador.mensagens_recebidas, list)
    
    def test_comunicacao_componentes(self):
        """Testa comunicação entre componentes via mediator."""
        # Registrar componentes
        self.mediator.registrar_componente(self.sequenciador)
        self.mediator.registrar_componente(self.alinhador)
        
        # Sequenciador envia mensagem para alinhador
        mensagem = Mensagem(
            TipoMensagem.SEQUENCIAMENTO_CONCLUIDO,
            "SEQ001",
            "ALN001",
            {"sequencia": "ATCG"}
        )
        
        self.mediator.enviar_mensagem(mensagem)
        
        # Verificar se mensagem foi entregue
        self.assertEqual(len(self.mediator.mensagens), 1)
    
    def test_mediator_desacoplamento(self):
        """Testa desacoplamento proporcionado pelo mediator."""
        # Componentes não se conhecem diretamente
        self.assertNotEqual(self.sequenciador.alinhador, self.alinhador)
        self.assertNotEqual(self.alinhador.sequenciador, self.sequenciador)
        
        # Mas podem se comunicar via mediator
        self.assertEqual(self.sequenciador.mediator, self.mediator)
        self.assertEqual(self.alinhador.mediator, self.mediator)
    
    def test_mediator_centralizacao_comunicacao(self):
        """Testa centralização da comunicação pelo mediator."""
        # Registrar componentes
        self.mediator.registrar_componente(self.sequenciador)
        self.mediator.registrar_componente(self.alinhador)
        self.mediator.registrar_componente(self.analisador)
        
        # Enviar múltiplas mensagens
        mensagens = [
            Mensagem(TipoMensagem.SEQUENCIAMENTO_CONCLUIDO, "SEQ001", "ALN001", {"seq": "ATCG"}),
            Mensagem(TipoMensagem.ALINHAMENTO_CONCLUIDO, "ALN001", "ANA001", {"ali": "ATCG"}),
            Mensagem(TipoMensagem.ANALISE_CONCLUIDA, "ANA001", "SEQ001", {"var": "SNP"})
        ]
        
        for msg in mensagens:
            self.mediator.enviar_mensagem(msg)
        
        # Mediator deve centralizar todas as mensagens
        self.assertEqual(len(self.mediator.mensagens), 3)
    
    def test_mediator_flexibilidade(self):
        """Testa flexibilidade do mediator."""
        # Pode adicionar/remover componentes dinamicamente
        mediator = MediatorLaboratorial()
        
        # Adicionar componente
        mediator.registrar_componente(self.sequenciador)
        self.assertEqual(len(mediator.componentes), 1)
        
        # Remover componente
        mediator.remover_componente(self.sequenciador)
        self.assertEqual(len(mediator.componentes), 0)
    
    def test_mediator_coordenacao_workflow(self):
        """Testa coordenação de workflow pelo mediator."""
        # Registrar componentes
        self.mediator.registrar_componente(self.sequenciador)
        self.mediator.registrar_componente(self.alinhador)
        self.mediator.registrar_componente(self.analisador)
        
        # Executar workflow
        resultado_seq = self.sequenciador.executar_sequenciamento({"amostra": "SAMPLE001"})
        
        # Sequenciador deve notificar alinhador
        self.assertEqual(len(self.mediator.mensagens), 1)
        self.assertEqual(self.mediator.mensagens[0].tipo, TipoMensagem.SEQUENCIAMENTO_CONCLUIDO)
    
    def test_mediator_tratamento_erros(self):
        """Testa tratamento de erros via mediator."""
        # Registrar componentes
        self.mediator.registrar_componente(self.sequenciador)
        self.mediator.registrar_componente(self.alinhador)
        
        # Enviar mensagem de erro
        mensagem_erro = Mensagem(
            TipoMensagem.ERRO_PROCESSAMENTO,
            "SEQ001",
            "ALN001",
            {"erro": "Falha no sequenciamento", "codigo": 500}
        )
        
        self.mediator.enviar_mensagem(mensagem_erro)
        
        # Mediator deve registrar erro
        self.assertEqual(len(self.messenger.mensagens), 1)
        self.assertEqual(self.messenger.mensagens[0].tipo, TipoMensagem.ERRO_PROCESSAMENTO)
    
    def test_mediator_benefits(self):
        """Testa benefícios do padrão Mediator."""
        # 1. Desacoplamento
        self.assertEqual(self.sequenciador.mediator, self.mediator)
        self.assertEqual(self.alinhador.mediator, self.mediator)
        
        # Componentes não se conhecem diretamente
        self.assertFalse(hasattr(self.sequenciador, 'alinhador'))
        self.assertFalse(hasattr(self.alinhador, 'sequenciador'))
        
        # 2. Centralização
        self.assertIsInstance(self.mediator.componentes, list)
        self.assertIsInstance(self.mediator.mensagens, list)
        
        # 3. Flexibilidade
        self.mediator.registrar_componente(self.sequenciador)
        self.mediator.remover_componente(self.sequenciador)
        
        # 4. Coordenação
        self.assertTrue(hasattr(self.mediator, 'enviar_mensagem'))
        self.assertTrue(hasattr(self.sequenciador, 'receber_mensagem'))


if __name__ == '__main__':
    unittest.main()
