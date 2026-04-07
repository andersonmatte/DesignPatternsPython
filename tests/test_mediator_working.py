"""
Testes para o padrão Mediator
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.mediator import (
    TipoMensagem, Mensagem, MediadorInterface, ComponenteBioinformatica,
    Sequenciador, Alinhador, Analisador
)


class TestMediator(unittest.TestCase):
    """Testes para o padrão Mediator."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.mediator = MockMediator()
        
        self.sequenciador = Sequenciador("SEQ001")
        self.alinhador = Alinhador("ALN001")
        self.analisador = Analisador("ANA001")
        
        # Conectar componentes ao mediator
        self.sequenciador.definir_mediador(self.mediator)
        self.alinhador.definir_mediador(self.mediator)
        self.analisador.definir_mediador(self.mediator)
    
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
    
    def test_sequenciador_creation(self):
        """Testa criação do componente sequenciador."""
        sequenciador = Sequenciador("SEQ001")
        
        self.assertIsInstance(sequenciador, ComponenteBioinformatica)
        self.assertEqual(sequenciador.nome, "SEQ001")
        self.assertEqual(sequenciador.estado, "inativo")
        self.assertEqual(sequenciador.capacidade_maxima, 3)
    
    def test_alinhador_creation(self):
        """Testa criação do componente alinhador."""
        alinhador = Alinhador("ALN001")
        
        self.assertIsInstance(alinhador, ComponenteBioinformatica)
        self.assertEqual(alinhador.nome, "ALN001")
        self.assertEqual(alinhador.estado, "inativo")
    
    def test_analisador_creation(self):
        """Testa criação do componente analisador."""
        analisador = Analisador("ANA001")
        
        self.assertIsInstance(analisador, ComponenteBioinformatica)
        self.assertEqual(analisador.nome, "ANA001")
        self.assertEqual(analisador.estado, "inativo")
    
    def test_sequenciador_sequenciar_amostra(self):
        """Testa sequenciamento de amostra."""
        resultado = self.sequenciador.sequenciar_amostra("SAMPLE001")
        
        self.assertIsInstance(resultado, bool)
        self.assertTrue(resultado)
        self.assertIn("SAMPLE001", self.sequenciador.amostras_em_processamento)
    
    def test_sequenciador_capacidade_maxima(self):
        """Testa capacidade máxima do sequenciador."""
        # Adicionar amostras até a capacidade máxima
        self.sequenciador.sequenciar_amostra("SAMPLE001")
        self.sequenciador.sequenciar_amostra("SAMPLE002")
        self.sequenciador.sequenciar_amostra("SAMPLE003")
        
        # Tentar adicionar além da capacidade
        resultado = self.sequenciador.sequenciar_amostra("SAMPLE004")
        
        self.assertFalse(resultado)
        self.assertEqual(len(self.sequenciador.amostras_em_processamento), 3)
    
    def test_sequenciador_finalizar_sequenciamento(self):
        """Testa finalização de sequenciamento."""
        # Adicionar amostra
        self.sequenciador.sequenciar_amostra("SAMPLE001")
        
        # Finalizar
        self.sequenciador.finalizar_sequenciamento("SAMPLE001")
        
        self.assertNotIn("SAMPLE001", self.sequenciador.amostras_em_processamento)
    
    def test_componente_definir_mediador(self):
        """Testa definição de mediador para componente."""
        mediator = MockMediator()
        sequenciador = Sequenciador("SEQ002")
        
        sequenciador.definir_mediador(mediator)
        
        self.assertEqual(sequenciador.mediador, mediator)
        self.assertIn(sequenciador, mediator.componentes)
    
    def test_componente_enviar_mensagem(self):
        """Testa envio de mensagem pelo componente."""
        self.sequenciador.enviar_mensagem(
            TipoMensagem.SEQUENCIAMENTO_CONCLUIDO,
            "ALN001",
            {"sequencia": "ATCG"}
        )
        
        self.assertEqual(len(self.mediator.mensagens_enviadas), 1)
        self.assertEqual(self.mediator.mensagens_enviadas[0].tipo, TipoMensagem.SEQUENCIAMENTO_CONCLUIDO)
    
    def test_componente_broadcast_mensagem(self):
        """Testa broadcast de mensagem pelo componente."""
        self.sequenciador.broadcast_mensagem(
            TipoMensagem.ERRO_PROCESSAMENTO,
            {"erro": "Falha no equipamento"}
        )
        
        self.assertEqual(len(self.messenger.mensagens_broadcast), 1)
        self.assertEqual(self.messenger.mensagens_broadcast[0].tipo, TipoMensagem.ERRO_PROCESSAMENTO)
    
    def test_componente_receber_mensagem(self):
        """Testa recebimento de mensagem pelo componente."""
        mensagem = Mensagem(
            TipoMensagem.ALINHAMENTO_CONCLUIDO,
            "ALN001",
            "SEQ001",
            {"alinhamento": "ATCG"}
        )
        
        self.sequenciador.receber_mensagem(mensagem)
        
        self.assertIn(mensagem, self.sequenciador.historico_mensagens)
    
    def test_componente_obter_status(self):
        """Testa obtenção de status do componente."""
        status = self.sequenciador.obter_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('nome', status)
        self.assertIn('estado', status)
        self.assertIn('mensagens_recebidas', status)
        self.assertIn('ultimas_atividades', status)
        self.assertEqual(status['nome'], "SEQ001")
    
    def test_mediator_registrar_componente(self):
        """Testa registro de componente no mediator."""
        mediator = MockMediator()
        sequenciador = Sequenciador("SEQ002")
        
        mediator.registrar_componente(sequenciador)
        
        self.assertIn(sequenciador, mediator.componentes)
    
    def test_mediator_enviar_mensagem(self):
        """Testa envio de mensagem via mediator."""
        mensagem = Mensagem(
            TipoMensagem.SEQUENCIAMENTO_CONCLUIDO,
            "SEQ001",
            "ALN001",
            {"sequencia": "ATCG"}
        )
        
        self.mediator.enviar_mensagem(mensagem)
        
        self.assertEqual(len(self.mediator.mensagens_enviadas), 1)
        self.assertEqual(self.mediator.mensagens_enviadas[0], mensagem)
    
    def test_mediator_broadcast_mensagem(self):
        """Testa broadcast de mensagem via mediator."""
        mensagem = Mensagem(
            TipoMensagem.RECURSO_LIBERADO,
            "SEQ001",
            "",
            {"recurso": "sequenciador"}
        )
        
        self.mediator.broadcast_mensagem(mensagem)
        
        self.assertEqual(len(self.messenger.mensagens_broadcast), 1)
        self.assertEqual(self.messenger.mensagens_broadcast[0], mensagem)
    
    def test_comunicacao_componentes(self):
        """Testa comunicação entre componentes via mediator."""
        # Sequenciador envia mensagem para alinhador
        self.sequenciador.enviar_mensagem(
            TipoMensagem.SEQUENCIAMENTO_CONCLUIDO,
            "ALN001",
            {"sequencia": "ATCG"}
        )
        
        # Verificar se mediator recebeu
        self.assertEqual(len(self.mediator.mensagens_enviadas), 1)
        
        # Alinhador deve receber mensagem (via mediator)
        mensagem_enviada = self.mediator.mensagens_enviadas[0]
        self.alinhador.receber_mensagem(mensagem_enviada)
        
        # Verificar se alinhador recebeu
        self.assertIn(mensagem_enviada, self.alinhador.historico_mensagens)
    
    def test_mediator_desacoplamento(self):
        """Testa desacoplamento proporcionado pelo mediator."""
        # Componentes não se conhecem diretamente
        self.assertFalse(hasattr(self.sequenciador, 'alinhador'))
        self.assertFalse(hasattr(self.alinhador, 'sequenciador'))
        
        # Mas podem se comunicar via mediator
        self.assertEqual(self.sequenciador.mediador, self.mediator)
        self.assertEqual(self.alinhador.mediador, self.mediator)
    
    def test_mediator_centralizacao(self):
        """Testa centralização da comunicação pelo mediator."""
        # Múltiplos componentes enviam mensagens
        self.sequenciador.enviar_mensagem(TipoMensagem.SEQUENCIAMENTO_CONCLUIDO, "ALN001")
        self.alinhador.enviar_mensagem(TipoMensagem.ALINHAMENTO_CONCLUIDO, "ANA001")
        self.analisador.broadcast_mensagem(TipoMensagem.ANALISE_CONCLUIDA)
        
        # Mediator deve centralizar todas as mensagens
        self.assertEqual(len(self.mediator.mensagens_enviadas), 2)
        self.assertEqual(len(self.messenger.mensagens_broadcast), 1)
    
    def test_mediator_flexibilidade(self):
        """Testa flexibilidade do mediator."""
        # Pode adicionar/remover componentes dinamicamente
        novo_sequenciador = Sequenciador("SEQ002")
        
        # Adicionar
        self.mediator.registrar_componente(novo_sequenciador)
        self.assertIn(novo_sequenciador, self.mediator.componentes)
        
        # Remover
        self.mediator.componentes.remove(novo_sequenciador)
        self.assertNotIn(novo_sequenciador, self.mediator.componentes)
    
    def test_mediator_benefits(self):
        """Testa benefícios do padrão Mediator."""
        # 1. Desacoplamento
        self.assertEqual(self.sequenciador.mediador, self.mediator)
        self.assertEqual(self.alinhador.mediador, self.mediator)
        
        # Componentes não se conhecem diretamente
        self.assertFalse(hasattr(self.sequenciador, 'alinhador'))
        
        # 2. Centralização
        self.assertIsInstance(self.mediator.componentes, list)
        
        # 3. Flexibilidade
        self.assertTrue(hasattr(self.mediator, 'registrar_componente'))
        self.assertTrue(hasattr(self.mediator, 'enviar_mensagem'))
        
        # 4. Coordenação
        self.assertTrue(hasattr(self.sequenciador, 'enviar_mensagem'))
        self.assertTrue(hasattr(self.sequenciador, 'receber_mensagem'))


class MockMediator(MediadorInterface):
    """Mock para testes do mediator."""
    
    def __init__(self):
        self.componentes = []
        self.mensagens_enviadas = []
        self.mensagens_broadcast = []
    
    def registrar_componente(self, componente: ComponenteBioinformatica) -> None:
        self.componentes.append(componente)
    
    def enviar_mensagem(self, mensagem: Mensagem) -> None:
        self.mensagens_enviadas.append(mensagem)
        
        # Enviar para destinatário específico se existir
        if mensagem.destinatario:
            for componente in self.componentes:
                if componente.nome == mensagem.destinatario:
                    componente.receber_mensagem(mensagem)
                    break
    
    def broadcast_mensagem(self, mensagem: Mensagem) -> None:
        self.mensagens_broadcast.append(mensagem)
        
        # Enviar para todos os componentes
        for componente in self.componentes:
            if componente.nome != mensagem.remetente:
                componente.receber_mensagem(mensagem)


if __name__ == '__main__':
    unittest.main()
