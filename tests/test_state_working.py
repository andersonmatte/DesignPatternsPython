"""
Testes para o padrão State
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.state import (
    StatusEquipamento, EstadoEquipamento, EquipamentoLaboratorial
)


class TestState(unittest.TestCase):
    """Testes para o padrão State."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.equipamento = EquipamentoLaboratorial("PCR001", "Termociclador")
    
    def test_status_equipamento_enum(self):
        """Testa enum StatusEquipamento."""
        self.assertEqual(StatusEquipamento.DISPONIVEL.value, "disponivel")
        self.assertEqual(StatusEquipamento.EM_USO.value, "em_uso")
        self.assertEqual(StatusEquipamento.MANUTENCAO.value, "manutencao")
        self.assertEqual(StatusEquipamento.CALIBRACAO.value, "calibracao")
        self.assertEqual(StatusEquipamento.DESLIGADO.value, "desligado")
        self.assertEqual(StatusEquipamento.ERRO.value, "erro")
    
    def test_equipamento_creation(self):
        """Testa criação do equipamento."""
        equipamento = EquipamentoLaboratorial("PCR001", "Termociclador")
        
        self.assertIsInstance(equipamento, EquipamentoLaboratorial)
        self.assertEqual(equipamento.id, "PCR001")
        self.assertEqual(equipamento.nome, "Termociclador")
        self.assertEqual(equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        self.assertIsNotNone(equipamento.estado)
    
    def test_equipamento_ligar(self):
        """Testa ligar equipamento."""
        self.equipamento.ligar()
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        self.assertIsNotNone(self.equipamento.estado)
    
    def test_equipamento_desligar(self):
        """Testa desligar equipamento."""
        self.equipamento.desligar()
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DESLIGADO)
    
    def test_equipamento_iniciar_uso(self):
        """Testa iniciar uso do equipamento."""
        # Primeiro ligar
        self.equipamento.ligar()
        
        # Iniciar uso
        resultado = self.equipamento.iniciar_uso("user1", "PCR protocol")
        
        self.assertTrue(resultado)
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.EM_USO)
        self.assertEqual(self.equipamento.usuario_atual, "user1")
        self.assertEqual(self.equipamento.protocolo_atual, "PCR protocol")
    
    def test_equipamento_iniciar_uso_desligado(self):
        """Testa iniciar uso com equipamento desligado."""
        # Manter desligado
        self.equipamento.desligar()
        
        # Tentar iniciar uso
        resultado = self.equipamento.iniciar_uso("user1", "PCR protocol")
        
        self.assertFalse(resultado)
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DESLIGADO)
    
    def test_equipamento_finalizar_uso(self):
        """Testa finalizar uso do equipamento."""
        # Iniciar uso primeiro
        self.equipamento.ligar()
        self.equipamento.iniciar_uso("user1", "PCR protocol")
        
        # Finalizar uso
        self.equipamento.finalizar_uso()
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        self.assertIsNone(self.equipamento.usuario_atual)
        self.assertIsNone(self.equipamento.protocolo_atual)
    
    def test_equipamento_iniciar_manutencao(self):
        """Testa iniciar manutenção do equipamento."""
        self.equipamento.iniciar_manutencao("Calibração mensal")
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.MANUTENCAO)
        self.assertEqual(self.equipamento.motivo_manutencao, "Calibração mensal")
    
    def test_equipamento_finalizar_manutencao(self):
        """Testa finalizar manutenção do equipamento."""
        # Iniciar manutenção primeiro
        self.equipamento.iniciar_manutencao("Calibração mensal")
        
        # Finalizar manutenção
        self.equipamento.finalizar_manutencao()
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        self.assertIsNone(self.equipamento.motivo_manutencao)
    
    def test_equipamento_iniciar_calibracao(self):
        """Testa iniciar calibração do equipamento."""
        self.equipamento.iniciar_calibracao("Calibração de temperatura")
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.CALIBRACAO)
        self.assertEqual(self.equipamento.tipo_calibracao, "Calibração de temperatura")
    
    def test_equipamento_finalizar_calibracao(self):
        """Testa finalizar calibração do equipamento."""
        # Iniciar calibração primeiro
        self.equipamento.iniciar_calibracao("Calibração de temperatura")
        
        # Finalizar calibração
        self.equipamento.finalizar_calibracao()
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        self.assertIsNone(self.equipamento.tipo_calibracao)
    
    def test_equipamento_registrar_erro(self):
        """Testa registro de erro no equipamento."""
        self.equipamento.registrar_erro("Falha no sensor de temperatura", "E001")
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.ERRO)
        self.assertEqual(self.equipamento.erro_descricao, "Falha no sensor de temperatura")
        self.assertEqual(self.equipamento.erro_codigo, "E001")
    
    def test_equipamento_limpar_erro(self):
        """Testa limpeza de erro no equipamento."""
        # Registrar erro primeiro
        self.equipamento.registrar_erro("Falha no sensor", "E001")
        
        # Limpar erro
        self.equipamento.limpar_erro()
        
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        self.assertIsNone(self.equipamento.erro_descricao)
        self.assertIsNone(self.equipamento.erro_codigo)
    
    def test_equipamento_obter_status(self):
        """Testa obtenção de status do equipamento."""
        status = self.equipamento.obter_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('id', status)
        self.assertIn('nome', status)
        self.assertIn('status_atual', status)
        self.assertIn('estado_atual', status)
        self.assertIn('timestamp', status)
        
        self.assertEqual(status['id'], "PCR001")
        self.assertEqual(status['nome'], "Termociclador")
    
    def test_equipamento_obter_historico(self):
        """Testa obtenção de histórico do equipamento."""
        # Realizar algumas operações
        self.equipamento.ligar()
        self.equipamento.iniciar_uso("user1", "PCR")
        self.equipamento.finalizar_uso()
        
        historico = self.equipamento.obter_historico()
        
        self.assertIsInstance(historico, list)
        self.assertGreater(len(historico), 0)
        
        # Verificar se as operações foram registradas
        operacoes = [h['operacao'] for h in historico]
        self.assertIn('ligar', operacoes)
        self.assertIn('iniciar_uso', operacoes)
        self.assertIn('finalizar_uso', operacoes)
    
    def test_state_transitions(self):
        """Testa transições de estado válidas."""
        # Estado inicial: DISPONIVEL
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        
        # DISPONIVEL -> EM_USO
        self.equipamento.iniciar_uso("user1", "PCR")
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.EM_USO)
        
        # EM_USO -> DISPONIVEL
        self.equipamento.finalizar_uso()
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        
        # DISPONIVEL -> MANUTENCAO
        self.equipamento.iniciar_manutencao("Calibração")
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.MANUTENCAO)
        
        # MANUTENCAO -> DISPONIVEL
        self.equipamento.finalizar_manutencao()
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
    
    def test_state_invalid_transitions(self):
        """Testa transições de estado inválidas."""
        # Tentar iniciar uso desligado
        self.equipamento.desligar()
        resultado = self.equipamento.iniciar_uso("user1", "PCR")
        self.assertFalse(resultado)
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DESLIGADO)
    
    def test_state_behavior_changes(self):
        """Testa mudança de comportamento com diferentes estados."""
        # Comportamento quando disponível
        self.equipamento.ligar()
        resultado_disponivel = self.equipamento.iniciar_uso("user1", "PCR")
        self.assertTrue(resultado_disponivel)
        
        # Comportamento quando em uso
        resultado_em_uso = self.equipamento.iniciar_uso("user2", "PCR2")
        self.assertFalse(resultado_em_uso)  # Não deve permitir
        
        # Comportamento quando em manutenção
        self.equipamento.iniciar_manutencao("Manutenção")
        resultado_manutencao = self.equipamento.iniciar_uso("user3", "PCR3")
        self.assertFalse(resultado_manutencao)  # Não deve permitir
    
    def test_state_polymorphism(self):
        """Testa polimorfismo dos estados."""
        # Mudar para diferentes estados
        self.equipamento.ligar()
        self.equipamento.iniciar_uso("user1", "PCR")
        self.equipamento.iniciar_manutencao("Manutenção")
        
        # Em cada estado, o objeto equipamento deve responder consistentemente
        status = self.equipamento.obter_status()
        self.assertIsInstance(status, dict)
        self.assertIn('estado_atual', status)
        
        # O nome do estado deve mudar
        self.assertIn(self.equipamento.estado.nome, status['estado_atual'])
    
    def test_state_encapsulation(self):
        """Testa encapsulamento da lógica de estado."""
        # Cliente não precisa conhecer detalhes da implementação
        self.equipamento.ligar()
        self.equipamento.iniciar_uso("user1", "PCR")
        
        # Interface simples e consistente
        self.assertTrue(hasattr(self.equipamento, 'iniciar_uso'))
        self.assertTrue(hasattr(self.equipamento, 'finalizar_uso'))
        self.assertTrue(hasattr(self.equipamento, 'obter_status'))
        
        # Estado interno é encapsulado
        self.assertIsNotNone(self.equipamento.estado)
        # Mas cliente não manipula estado diretamente
    
    def test_state_benefits(self):
        """Testa benefícios do padrão State."""
        # 1. Comportamento baseado em estado
        self.equipamento.ligar()
        resultado1 = self.equipamento.iniciar_uso("user1", "PCR")
        self.assertTrue(resultado1)
        
        self.equipamento.desligar()
        resultado2 = self.equipamento.iniciar_uso("user2", "PCR")
        self.assertFalse(resultado2)
        
        # 2. Transições controladas
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DESLIGADO)
        
        # 3. Localização de lógica
        self.assertIsNotNone(self.equipamento.estado)
        
        # 4. Polimorfismo
        status = self.equipamento.obter_status()
        self.assertIsInstance(status, dict)
    
    def test_state_workflow_complete(self):
        """Testa workflow completo do equipamento."""
        # Workflow típico de laboratório
        self.equipamento.ligar()  # DISPONIVEL
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        
        self.equipamento.iniciar_calibracao("Calibração diária")  # CALIBRACAO
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.CALIBRACAO)
        
        self.equipamento.finalizar_calibracao()  # DISPONIVEL
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        
        self.equipamento.iniciar_uso("user1", "PCR protocol")  # EM_USO
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.EM_USO)
        
        self.equipamento.finalizar_uso()  # DISPONIVEL
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        
        self.equipamento.iniciar_manutencao("Manutenção preventiva")  # MANUTENCAO
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.MANUTENCAO)
        
        self.equipamento.finalizar_manutencao()  # DISPONIVEL
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DISPONIVEL)
        
        self.equipamento.desligar()  # DESLIGADO
        self.assertEqual(self.equipamento.status_atual, StatusEquipamento.DESLIGADO)


if __name__ == '__main__':
    unittest.main()
