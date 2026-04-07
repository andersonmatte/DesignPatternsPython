"""
Testes para o padrão Mediator
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from patterns.comportamentais.mediator import (
    ComponenteLaboratorial, MediatorLaboratorial, Sequenciador, Alinhador, Analisador, MediatorConcreto
)


class TestMediator(unittest.TestCase):
    """Testes para o padrão Mediator."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.mediator = MediatorConcreto()
        
        self.sequenciador = Sequenciador("SEQ001")
        self.alinhador = Alinhador("ALN001")
        self.analisador = Analisador("ANA001")
        
        # Registrar componentes no mediator
        self.mediator.registrar_componente("sequenciador", self.sequenciador)
        self.mediator.registrar_componente("alinhador", self.alinhador)
        self.mediator.registrar_componente("analisador", self.analisador)
    
    def test_mediator_concreto_creation(self):
        """Testa criação do mediator concreto."""
        self.assertIsInstance(self.mediator, MediatorConcreto)
        self.assertIsInstance(self.mediator, MediatorLaboratorial)
        self.assertEqual(len(self.mediator.componentes), 3)
    
    def test_sequenciador_creation(self):
        """Testa criação do sequenciador."""
        self.assertIsInstance(self.sequenciador, Sequenciador)
        self.assertIsInstance(self.sequenciador, ComponenteLaboratorial)
        self.assertEqual(self.sequenciador.id_componente, "SEQ001")
        self.assertEqual(self.sequenciador.nome, "Sequenciador")
    
    def test_alinhador_creation(self):
        """Testa criação do alinhador."""
        self.assertIsInstance(self.alinhador, Alinhador)
        self.assertIsInstance(self.alinhador, ComponenteLaboratorial)
        self.assertEqual(self.alinhador.id_componente, "ALN001")
        self.assertEqual(self.alinhador.nome, "Alinhador")
    
    def test_analisador_creation(self):
        """Testa criação do analisador."""
        self.assertIsInstance(self.analisador, Analisador)
        self.assertIsInstance(self.analisador, ComponenteLaboratorial)
        self.assertEqual(self.analisador.id_componente, "ANA001")
        self.assertEqual(self.analisador.nome, "Analisador")
    
    def test_mediator_registrar_componente(self):
        """Testa registro de componente no mediator."""
        novo_mediator = MediatorConcreto()
        novo_sequenciador = Sequenciador("SEQ002")
        
        novo_mediator.registrar_componente("novo_sequenciador", novo_sequenciador)
        
        self.assertEqual(len(novo_mediator.componentes), 1)
        self.assertIn("novo_sequenciador", novo_mediator.componentes)
        self.assertEqual(novo_mediator.componentes["novo_sequenciador"], novo_sequenciador)
        self.assertEqual(novo_sequenciador.mediator, novo_mediator)
    
    def test_mediator_notificar(self):
        """Testa notificação no mediator."""
        # Mock do método de processamento do alinhador
        with patch.object(self.alinhador, 'processar_mensagem') as mock_processar:
            mensagem = {
                'origem': 'sequenciador',
                'tipo': 'sequencia_gerada',
                'dados': {'sequencia': 'ATCGATCG', 'amostra': 'SAMPLE001'}
            }
            
            self.mediator.notificar(self.sequenciador, mensagem)
            
            # Verifica se o alinhador recebeu a mensagem
            mock_processar.assert_called_once_with(mensagem)
    
    def test_sequenciador_sequenciar_amostra(self):
        """Testa sequenciamento de amostra."""
        resultado = self.sequenciador.sequenciar_amostra("SAMPLE001")
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('sequencia', resultado)
        self.assertIn('amostra', resultado)
        self.assertIn('timestamp', resultado)
        self.assertEqual(resultado['status'], 'Sequenciado')
        self.assertEqual(resultado['amostra'], 'SAMPLE001')
    
    def test_sequenciador_sequenciar_amostra_com_mediator(self):
        """Testa sequenciamento com notificação via mediator."""
        # Mock do mediator
        mock_mediator = Mock()
        self.sequenciador.mediator = mock_mediator
        
        resultado = self.sequenciador.sequenciar_amostra("SAMPLE001")
        
        # Verifica se o mediator foi notificado
        mock_mediator.notificar.assert_called_once()
        
        # Verifica o conteúdo da notificação
        chamada = mock_mediator.notificar.call_args
        self.assertEqual(chamada[0][0], self.sequenciador)  # Origem
        self.assertEqual(chamada[0][1]['tipo'], 'sequencia_gerada')  # Tipo da mensagem
        self.assertEqual(chamada[0][1]['dados']['amostra'], 'SAMPLE001')  # Dados
    
    def test_alinhador_alinhar_sequencia(self):
        """Testa alinhamento de sequência."""
        dados = {'sequencia': 'ATCGATCG', 'amostra': 'SAMPLE001'}
        resultado = self.alinhador.alinhar_sequencia(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('alinhamento', resultado)
        self.assertIn('referencia', resultado)
        self.assertIn('score', resultado)
        self.assertEqual(resultado['status'], 'Alinhado')
    
    def test_alinhador_alinhar_sequencia_com_mediator(self):
        """Testa alinhamento com notificação via mediator."""
        mock_mediator = Mock()
        self.alinhador.mediator = mock_mediator
        
        dados = {'sequencia': 'ATCGATCG', 'amostra': 'SAMPLE001'}
        resultado = self.alinhador.alinhar_sequencia(dados)
        
        # Verifica se o mediator foi notificado
        mock_mediator.notificar.assert_called_once()
        
        # Verifica o conteúdo da notificação
        chamada = mock_mediator.notificar.call_args
        self.assertEqual(chamada[0][0], self.alinhador)
        self.assertEqual(chamada[0][1]['tipo'], 'alinhamento_concluido')
    
    def test_analisador_analisar_dados(self):
        """Testa análise de dados."""
        dados = {
            'alinhamento': 'ATCGATCG',
            'score': 0.95,
            'amostra': 'SAMPLE001'
        }
        resultado = self.analisador.analisar_dados(dados)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('status', resultado)
        self.assertIn('analise', resultado)
        self.assertIn('variantes', resultado)
        self.assertIn('qualidade', resultado)
        self.assertEqual(resultado['status'], 'Analisado')
    
    def test_analisador_analisar_dados_com_mediator(self):
        """Testa análise com notificação via mediator."""
        mock_mediator = Mock()
        self.analisador.mediator = mock_mediator
        
        dados = {
            'alinhamento': 'ATCGATCG',
            'score': 0.95,
            'amostra': 'SAMPLE001'
        }
        resultado = self.analisador.analisar_dados(dados)
        
        # Verifica se o mediator foi notificado
        mock_mediator.notificar.assert_called_once()
        
        # Verifica o conteúdo da notificação
        chamada = mock_mediator.notificar.call_args
        self.assertEqual(chamada[0][0], self.analisador)
        self.assertEqual(chamada[0][1]['tipo'], 'analise_concluida')
    
    def test_mediator_workflow_completo(self):
        """Testa fluxo de trabalho completo via mediator."""
        # Iniciar o processo no sequenciador
        resultado_seq = self.sequenciador.sequenciar_amostra("SAMPLE001")
        
        # O mediator deve ter coordenado as notificações
        # Verificar se os componentes receberam as mensagens
        self.assertEqual(resultado_seq['status'], 'Sequenciado')
        
        # O processo deve continuar automaticamente através do mediator
        # (em uma implementação real, o mediator coordenaria o fluxo completo)
    
    def test_mediator_comunicacao_indireta(self):
        """Testa comunicação indireta entre componentes."""
        # Componentes não se comunicam diretamente
        self.assertNotEqual(self.sequenciador.mediator, self.alinhador)
        self.assertNotEqual(self.alinhador.mediator, self.analisador)
        
        # Mas através do mediator
        self.assertEqual(self.sequenciador.mediator, self.alinhador.mediator)
        self.assertEqual(self.alinhador.mediator, self.analisador.mediator)
    
    def test_mediator_desacoplamento(self):
        """Testa desacoplamento proporcionado pelo mediator."""
        # Componentes não conhecem outros componentes diretamente
        self.assertFalse(hasattr(self.sequenciador, 'alinhador'))
        self.assertFalse(hasattr(self.alinhador, 'analisador'))
        self.assertFalse(hasattr(self.analisador, 'sequenciador'))
        
        # Apenas conhecem o mediator
        self.assertTrue(hasattr(self.sequenciador, 'mediator'))
        self.assertTrue(hasattr(self.alinhador, 'mediator'))
        self.assertTrue(hasattr(self.analisador, 'mediator'))
    
    def test_mediator_centralizacao_logica(self):
        """Testa centralização da lógica de comunicação."""
        # O mediator centraliza a lógica de como as mensagens são roteadas
        with patch.object(self.mediator, 'rotear_mensagem') as mock_rotear:
            mensagem = {'tipo': 'teste', 'dados': {}}
            self.mediator.notificar(self.sequenciador, mensagem)
            
            mock_rotear.assert_called_once_with(self.sequenciador, mensagem)
    
    def test_mediator_roteamento_mensagens(self):
        """Testa roteamento de mensagens do mediator."""
        # Mensagem do sequenciador deve ir para o alinhador
        mensagem_seq = {
            'origem': 'sequenciador',
            'tipo': 'sequencia_gerada',
            'dados': {'sequencia': 'ATCGATCG'}
        }
        
        with patch.object(self.alinhador, 'processar_mensagem') as mock_processar:
            self.mediator.notificar(self.sequenciador, mensagem_seq)
            mock_processar.assert_called_once_with(mensagem_seq)
        
        # Mensagem do alinhador deve ir para o analisador
        mensagem_alin = {
            'origem': 'alinhador',
            'tipo': 'alinhamento_concluido',
            'dados': {'alinhamento': 'ATCGATCG'}
        }
        
        with patch.object(self.analisador, 'processar_mensagem') as mock_processar:
            self.mediator.notificar(self.alinhador, mensagem_alin)
            mock_processar.assert_called_once_with(mensagem_alin)
    
    def test_mensagem_invalida(self):
        """Testa tratamento de mensagem inválida."""
        mensagem_invalida = {'tipo': 'desconhecido', 'dados': {}}
        
        # Não deve lançar exceção, mas deve registrar ou ignorar
        try:
            self.mediator.notificar(self.sequenciador, mensagem_invalida)
        except Exception as e:
            self.fail(f"Não deveria lançar exceção para mensagem inválida: {e}")
    
    def test_componente_sem_mediator(self):
        """Testa componente sem mediator."""
        componente = Sequenciador("TEST")
        
        # Operação deve funcionar mesmo sem mediator
        resultado = componente.sequenciar_amostra("SAMPLE001")
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['status'], 'Sequenciado')
    
    def test_mediator_remover_componente(self):
        """Testa remoção de componente do mediator."""
        self.mediator.registrar_componente("temp", Sequenciador("TEMP"))
        self.assertEqual(len(self.mediator.componentes), 4)
        
        self.mediator.remover_componente("temp")
        self.assertEqual(len(self.mediator.componentes), 3)
        self.assertNotIn("temp", self.mediator.componentes)
    
    def test_mediator_obter_componente(self):
        """Testa obtenção de componente do mediator."""
        componente = self.mediator.obter_componente("sequenciador")
        
        self.assertEqual(componente, self.sequenciador)
        
        # Componente inexistente deve retornar None
        inexistente = self.mediator.obter_componente("inexistente")
        self.assertIsNone(inexistente)
    
    def test_mediator_listar_componentes(self):
        """Testa listagem de componentes do mediator."""
        componentes = self.mediator.listar_componentes()
        
        self.assertIsInstance(componentes, list)
        self.assertEqual(len(componentes), 3)
        self.assertIn("sequenciador", componentes)
        self.assertIn("alinhador", componentes)
        self.assertIn("analisador", componentes)
    
    def test_mediator_estatisticas(self):
        """Testa estatísticas do mediator."""
        # Enviar algumas mensagens
        self.mediator.notificar(self.sequenciador, {'tipo': 'sequencia_gerada'})
        self.mediator.notificar(self.alinhador, {'tipo': 'alinhamento_concluido'})
        
        stats = self.mediator.get_estatisticas()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_componentes', stats)
        self.assertIn('total_mensagens', stats)
        self.assertIn('mensagens_por_tipo', stats)
        self.assertEqual(stats['total_componentes'], 3)
        self.assertGreater(stats['total_mensagens'], 0)
    
    def test_mediator_extensibilidade(self):
        """Testa extensibilidade do mediator."""
        # Adicionar novo tipo de componente
        class NovoComponente(ComponenteLaboratorial):
            def __init__(self, id_comp):
                super().__init__(id_comp, "Novo Componente")
            
            def processar_mensagem(self, mensagem):
                return {"status": "Processado", "componente": self.nome}
        
        novo_componente = NovoComponente("NOVO001")
        self.mediator.registrar_componente("novo", novo_componente)
        
        # Deve funcionar com os componentes existentes
        self.assertEqual(len(self.mediator.componentes), 4)
        self.assertIn("novo", self.mediator.componentes)
    
    def test_mediator_tratamento_erros(self):
        """Testa tratamento de erros no mediator."""
        # Componente que lança exceção
        componente_com_erro = Mock()
        componente_com_erro.processar_mensagem.side_effect = Exception("Erro de teste")
        componente_com_erro.id_componente = "erro"
        
        self.mediator.registrar_componente("erro", componente_com_erro)
        
        # Não deve propagar a exceção
        try:
            self.mediator.notificar(self.sequenciador, {'tipo': 'teste'})
        except Exception as e:
            self.fail(f"Mediator não deveria propagar exceção: {e}")
    
    def test_mediator_performance(self):
        """Testa performance do mediator com muitas mensagens."""
        import time
        
        # Enviar muitas mensagens
        start_time = time.time()
        for i in range(100):
            self.mediator.notificar(self.sequenciador, {
                'tipo': 'sequencia_gerada',
                'dados': {'sequencia': f'SEQ{i}', 'amostra': f'SAMPLE{i}'}
            })
        end_time = time.time()
        
        # Deve ser razoavelmente rápido
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)  # Menos de 1 segundo
    
    def test_mediator_padrao_observer(self):
        """Testa se mediator implementa aspects do padrão Observer."""
        # Componentes podem ser vistos como observers
        mensagens_recebidas = []
        
        def coletar_mensagem(origem, mensagem):
            mensagens_recebidas.append((origem.id_componente, mensagem['tipo']))
        
        # Mock para coletar mensagens
        with patch.object(self.alinhador, 'processar_mensagem') as mock_processar:
            mock_processar.side_effect = lambda msg: coletar_mensagem(self.sequenciador, msg)
            
            self.mediator.notificar(self.sequenciador, {'tipo': 'teste1'})
            self.mediator.notificar(self.sequenciador, {'tipo': 'teste2'})
            
            self.assertEqual(len(mensagens_recebidas), 2)
            self.assertEqual(mensagens_recebidas[0], ('SEQ001', 'teste1'))
            self.assertEqual(mensagens_recebidas[1], ('SEQ001', 'teste2'))
    
    def test_mediator_vantagens_desvantagens(self):
        """Testa vantagens e desvantagens do padrão Mediator."""
        # Vantagens:
        # 1. Desacoplamento
        self.assertFalse(hasattr(self.sequenciador, 'alinhador'))
        
        # 2. Centralização
        self.assertEqual(self.sequenciador.mediator, self.alinhador.mediator)
        
        # 3. Simplificação
        self.assertTrue(hasattr(self.sequenciador, 'mediator'))
        
        # Desvantagens (potenciais):
        # 1. Ponto único de falha
        # 2. Complexidade do mediator
        # 3. Possível gargalo de performance
        
        # O mediator deve ser bem projetado para mitigar desvantagens
        self.assertIsInstance(self.mediator, MediatorConcreto)
        self.assertTrue(hasattr(self.mediator, 'componentes'))
        self.assertTrue(hasattr(self.mediator, 'notificar'))


if __name__ == '__main__':
    unittest.main()
