"""
Testes para o padrão State
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.state import (
    EstadoEquipamento, DisponivelState, EmUsoState, ManutencaoState, EquipamentoLaboratorial
)


class TestState(unittest.TestCase):
    """Testes para o padrão State."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.equipamento = EquipamentoLaboratorial("EQ001", "Microscópio Eletrônico")
        
        # Estados individuais para testes específicos
        self.estado_disponivel = DisponivelState()
        self.estado_em_uso = EmUsoState()
        self.estado_manutencao = ManutencaoState()
    
    def test_estado_disponivel_creation(self):
        """Testa criação do estado disponível."""
        self.assertIsInstance(self.estado_disponivel, EstadoEquipamento)
        self.assertIsInstance(self.estado_disponivel, DisponivelState)
        self.assertEqual(self.estado_disponivel.nome, "Disponível")
    
    def test_estado_em_uso_creation(self):
        """Testa criação do estado em uso."""
        self.assertIsInstance(self.estado_em_uso, EstadoEquipamento)
        self.assertIsInstance(self.estado_em_uso, EmUsoState)
        self.assertEqual(self.estado_em_uso.nome, "Em Uso")
    
    def test_estado_manutencao_creation(self):
        """Testa criação do estado em manutenção."""
        self.assertIsInstance(self.estado_manutencao, EstadoEquipamento)
        self.assertIsInstance(self.estado_manutencao, ManutencaoState)
        self.assertEqual(self.estado_manutencao.nome, "Em Manutenção")
    
    def test_equipamento_laboratorial_creation(self):
        """Testa criação do equipamento laboratorial."""
        self.assertIsInstance(self.equipamento, EquipamentoLaboratorial)
        self.assertEqual(self.equipamento.id_equipamento, "EQ001")
        self.assertEqual(self.equipamento.nome, "Microscópio Eletrônico")
        self.assertIsInstance(self.equipamento.estado, DisponivelState)
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
    
    def test_estado_disponivel_ligar(self):
        """Testa ligar equipamento no estado disponível."""
        resultado = self.estado_disponivel.ligar(self.equipamento)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('acao', resultado)
        self.assertIn('estado', resultado)
        self.assertIn('mensagem', resultado)
        self.assertEqual(resultado['acao'], 'Ligar')
        self.assertEqual(resultado['estado'], 'Disponível')
        self.assertIn('já está ligado', resultado['mensagem'])
    
    def test_estado_disponivel_desligar(self):
        """Testa desligar equipamento no estado disponível."""
        resultado = self.estado_disponivel.desligar(self.equipamento)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Desligar')
        self.assertEqual(resultado['estado'], 'Disponível')
        self.assertIn('desligado com sucesso', resultado['mensagem'])
        
        # Equipamento deve mudar para desligado
        self.assertEqual(self.equipamento.estado_atual, "Desligado")
    
    def test_estado_disponivel_iniciar_uso(self):
        """Testa iniciar uso no estado disponível."""
        resultado = self.estado_disponivel.iniciar_uso(self.equipamento, "Dr. Silva")
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Iniciar Uso')
        self.assertEqual(resultado['estado'], 'Em Uso')
        self.assertIn('iniciado com sucesso', resultado['mensagem'])
        
        # Equipamento deve mudar para em uso
        self.assertIsInstance(self.equipamento.estado, EmUsoState)
        self.assertEqual(self.equipamento.estado_atual, "Em Uso")
        self.assertEqual(self.equipamento.usuario_atual, "Dr. Silva")
    
    def test_estado_disponivel_iniciar_manutencao(self):
        """Testa iniciar manutenção no estado disponível."""
        resultado = self.estado_disponivel.iniciar_manutencao(self.equipamento, "Técnico João")
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Iniciar Manutenção')
        self.assertEqual(resultado['estado'], 'Em Manutenção')
        self.assertIn('manutenção iniciada', resultado['mensagem'])
        
        # Equipamento deve mudar para manutenção
        self.assertIsInstance(self.equipamento.estado, ManutencaoState)
        self.assertEqual(self.equipamento.estado_atual, "Em Manutenção")
        self.assertEqual(self.equipamento.tecnico_manutencao, "Técnico João")
    
    def test_estado_em_uso_ligar(self):
        """Testa ligar equipamento no estado em uso."""
        # Mudar equipamento para estado em uso
        self.equipamento.estado = self.estado_em_uso
        self.equipamento.usuario_atual = "Dr. Silva"
        
        resultado = self.estado_em_uso.ligar(self.equipamento)
        
        self.assertEqual(resultado['estado'], 'Em Uso')
        self.assertIn('já está em uso', resultado['mensagem'])
    
    def test_estado_em_uso_desligar(self):
        """Testa desligar equipamento no estado em uso."""
        # Mudar equipamento para estado em uso
        self.equipamento.estado = self.estado_em_uso
        self.equipamento.usuario_atual = "Dr. Silva"
        
        resultado = self.estado_em_uso.desligar(self.equipamento)
        
        self.assertEqual(resultado['estado'], 'Em Uso')
        self.assertIn('não pode ser desligado', resultado['mensagem'])
    
    def test_estado_em_uso_iniciar_uso(self):
        """Testa iniciar uso no estado em uso."""
        # Mudar equipamento para estado em uso
        self.equipamento.estado = self.estado_em_uso
        self.equipamento.usuario_atual = "Dr. Silva"
        
        resultado = self.estado_em_uso.iniciar_uso(self.equipamento, "Dra. Santos")
        
        self.assertEqual(resultado['estado'], 'Em Uso')
        self.assertIn('já está em uso', resultado['mensagem'])
        self.assertIn('Dr. Silva', resultado['mensagem'])
    
    def test_estado_em_uso_finalizar_uso(self):
        """Testa finalizar uso no estado em uso."""
        # Mudar equipamento para estado em uso
        self.equipamento.estado = self.estado_em_uso
        self.equipamento.usuario_atual = "Dr. Silva"
        
        resultado = self.estado_em_uso.finalizar_uso(self.equipamento)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Finalizar Uso')
        self.assertEqual(resultado['estado'], 'Disponível')
        self.assertIn('finalizado com sucesso', resultado['mensagem'])
        
        # Equipamento deve voltar para disponível
        self.assertIsInstance(self.equipamento.estado, DisponivelState)
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
        self.assertIsNone(self.equipamento.usuario_atual)
    
    def test_estado_em_uso_iniciar_manutencao(self):
        """Testa iniciar manutenção no estado em uso."""
        # Mudar equipamento para estado em uso
        self.equipamento.estado = self.estado_em_uso
        self.equipamento.usuario_atual = "Dr. Silva"
        
        resultado = self.estado_em_uso.iniciar_manutencao(self.equipamento, "Técnico João")
        
        self.assertEqual(resultado['estado'], 'Em Uso')
        self.assertIn('não pode entrar em manutenção', resultado['mensagem'])
    
    def test_estado_manutencao_ligar(self):
        """Testa ligar equipamento no estado manutenção."""
        # Mudar equipamento para estado manutenção
        self.equipamento.estado = self.estado_manutencao
        self.equipamento.tecnico_manutencao = "Técnico João"
        
        resultado = self.estado_manutencao.ligar(self.equipamento)
        
        self.assertEqual(resultado['estado'], 'Em Manutenção')
        self.assertIn('está em manutenção', resultado['mensagem'])
    
    def test_estado_manutencao_desligar(self):
        """Testa desligar equipamento no estado manutenção."""
        # Mudar equipamento para estado manutenção
        self.equipamento.estado = self.estado_manutencao
        self.equipamento.tecnico_manutencao = "Técnico João"
        
        resultado = self.estado_manutencao.desligar(self.equipamento)
        
        self.assertEqual(resultado['estado'], 'Em Manutenção')
        self.assertIn('não pode ser desligado', resultado['mensagem'])
    
    def test_estado_manutencao_iniciar_uso(self):
        """Testa iniciar uso no estado manutenção."""
        # Mudar equipamento para estado manutenção
        self.equipamento.estado = self.estado_manutencao
        self.equipamento.tecnico_manutencao = "Técnico João"
        
        resultado = self.estado_manutencao.iniciar_uso(self.equipamento, "Dr. Silva")
        
        self.assertEqual(resultado['estado'], 'Em Manutenção')
        self.assertIn('não pode ser usado', resultado['mensagem'])
    
    def test_estado_manutencao_finalizar_manutencao(self):
        """Testa finalizar manutenção no estado manutenção."""
        # Mudar equipamento para estado manutenção
        self.equipamento.estado = self.estado_manutencao
        self.equipamento.tecnico_manutencao = "Técnico João"
        
        resultado = self.estado_manutencao.finalizar_manutencao(self.equipamento)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Finalizar Manutenção')
        self.assertEqual(resultado['estado'], 'Disponível')
        self.assertIn('finalizada com sucesso', resultado['mensagem'])
        
        # Equipamento deve voltar para disponível
        self.assertIsInstance(self.equipamento.estado, DisponivelState)
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
        self.assertIsNone(self.equipamento.tecnico_manutencao)
    
    def test_equipamento_ligar(self):
        """Testa método ligar do equipamento."""
        resultado = self.equipamento.ligar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('acao', resultado)
        self.assertIn('estado', resultado)
        self.assertIn('mensagem', resultado)
        self.assertEqual(resultado['acao'], 'Ligar')
    
    def test_equipamento_desligar(self):
        """Testa método desligar do equipamento."""
        resultado = self.equipamento.desligar()
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Desligar')
        self.assertEqual(self.equipamento.estado_atual, "Desligado")
    
    def test_equipamento_iniciar_uso(self):
        """Testa método iniciar uso do equipamento."""
        resultado = self.equipamento.iniciar_uso("Dr. Silva")
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Iniciar Uso')
        self.assertEqual(self.equipamento.estado_atual, "Em Uso")
        self.assertEqual(self.equipamento.usuario_atual, "Dr. Silva")
    
    def test_equipamento_finalizar_uso(self):
        """Testa método finalizar uso do equipamento."""
        # Primeiro iniciar uso
        self.equipamento.iniciar_uso("Dr. Silva")
        
        # Depois finalizar
        resultado = self.equipamento.finalizar_uso()
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Finalizar Uso')
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
        self.assertIsNone(self.equipamento.usuario_atual)
    
    def test_equipamento_iniciar_manutencao(self):
        """Testa método iniciar manutenção do equipamento."""
        resultado = self.equipamento.iniciar_manutencao("Técnico João")
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Iniciar Manutenção')
        self.assertEqual(self.equipamento.estado_atual, "Em Manutenção")
        self.assertEqual(self.equipamento.tecnico_manutencao, "Técnico João")
    
    def test_equipamento_finalizar_manutencao(self):
        """Testa método finalizar manutenção do equipamento."""
        # Primeiro iniciar manutenção
        self.equipamento.iniciar_manutencao("Técnico João")
        
        # Depois finalizar
        resultado = self.equipamento.finalizar_manutencao()
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['acao'], 'Finalizar Manutenção')
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
        self.assertIsNone(self.equipamento.tecnico_manutencao)
    
    def test_equipamento_verificar_status(self):
        """Testa método verificar status do equipamento."""
        resultado = self.equipamento.verificar_status()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('id_equipamento', resultado)
        self.assertIn('nome', resultado)
        self.assertIn('estado_atual', resultado)
        self.assertIn('usuario_atual', resultado)
        self.assertIn('tecnico_manutencao', resultado)
        self.assertIn('operacoes_permitidas', resultado)
        
        self.assertEqual(resultado['id_equipamento'], "EQ001")
        self.assertEqual(resultado['nome'], "Microscópio Eletrônico")
        self.assertEqual(resultado['estado_atual'], "Disponível")
        
        # Operações permitidas devem depender do estado
        operacoes = resultado['operacoes_permitidas']
        self.assertIn('ligar', operacoes)
        self.assertIn('desligar', operacoes)
        self.assertIn('iniciar_uso', operacoes)
        self.assertIn('iniciar_manutencao', operacoes)
    
    def test_transicao_estados_valida(self):
        """Testa transições válidas entre estados."""
        # Disponível -> Em Uso
        self.equipamento.iniciar_uso("Dr. Silva")
        self.assertEqual(self.equipamento.estado_atual, "Em Uso")
        
        # Em Uso -> Disponível
        self.equipamento.finalizar_uso()
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
        
        # Disponível -> Manutenção
        self.equipamento.iniciar_manutencao("Técnico João")
        self.assertEqual(self.equipamento.estado_atual, "Em Manutenção")
        
        # Manutenção -> Disponível
        self.equipamento.finalizar_manutencao()
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
    
    def test_transicao_estados_invalida(self):
        """Testa transições inválidas entre estados."""
        # Tentar iniciar uso quando já está em uso
        self.equipamento.iniciar_uso("Dr. Silva")
        resultado = self.equipamento.iniciar_uso("Dra. Santos")
        
        self.assertIn('já está em uso', resultado['mensagem'])
        self.assertEqual(self.equipamento.usuario_atual, "Dr. Silva")
        
        # Tentar desligar quando está em uso
        resultado = self.equipamento.desligar()
        self.assertIn('não pode ser desligado', resultado['mensagem'])
        self.assertEqual(self.equipamento.estado_atual, "Em Uso")
    
    def test_estado_comportamento_diferente(self):
        """Testa comportamento diferente em cada estado."""
        # Estado Disponível
        resultado_disponivel = self.equipamento.iniciar_uso("Dr. Silva")
        self.assertEqual(resultado_disponivel['estado'], 'Em Uso')
        
        # Estado Em Uso
        resultado_em_uso = self.equipamento.iniciar_uso("Dra. Santos")
        self.assertEqual(resultado_em_uso['estado'], 'Em Uso')
        self.assertIn('já está em uso', resultado_em_uso['mensagem'])
        
        # Estado Manutenção
        self.equipamento.iniciar_manutencao("Técnico João")
        resultado_manutencao = self.equipamento.iniciar_uso("Dr. Silva")
        self.assertEqual(resultado_manutencao['estado'], 'Em Manutenção')
        self.assertIn('não pode ser usado', resultado_manutencao['mensagem'])
    
    def test_state_pattern_beneficios(self):
        """Testa benefícios do padrão State."""
        # 1. Comportamento baseado em estado
        self.equipamento.iniciar_uso("Dr. Silva")
        self.assertEqual(self.equipamento.estado_atual, "Em Uso")
        
        # 2. Transições de estado explícitas
        self.assertIsInstance(self.equipamento.estado, EmUsoState)
        
        # 3. Comportamento encapsulado
        self.assertTrue(hasattr(self.equipamento.estado, 'iniciar_uso'))
        self.assertTrue(hasattr(self.equipamento.estado, 'finalizar_uso'))
        
        # 4. Facilidade de adicionar novos estados
        # (verificado pela estrutura das classes de estado)
    
    def test_mudanca_comportamento_dinamica(self):
        """Testa mudança de comportamento dinâmica."""
        # Comportamento no estado disponível
        resultado1 = self.equipamento.iniciar_uso("Dr. Silva")
        self.assertEqual(resultado1['estado'], 'Em Uso')
        
        # Comportamento no estado em uso
        resultado2 = self.equipamento.iniciar_uso("Dra. Santos")
        self.assertIn('já está em uso', resultado2['mensagem'])
        
        # Comportamento no estado manutenção
        self.equipamento.iniciar_manutencao("Técnico João")
        resultado3 = self.equipamento.iniciar_uso("Dr. Silva")
        self.assertIn('não pode ser usado', resultado3['mensagem'])
    
    def test_estado_desligado(self):
        """Testa estado desligado (implícito)."""
        # Desligar equipamento
        self.equipamento.desligar()
        self.assertEqual(self.equipamento.estado_atual, "Desligado")
        
        # Tentar usar equipamento desligado
        resultado = self.equipamento.iniciar_uso("Dr. Silva")
        self.assertIn('desligado', resultado['mensagem'].lower())
        
        # Ligar equipamento
        resultado = self.equipamento.ligar()
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
    
    def test_estado_consistencia(self):
        """Testa consistência do estado."""
        # Iniciar uso
        self.equipamento.iniciar_uso("Dr. Silva")
        
        # Verificar consistência
        self.assertEqual(self.equipamento.estado_atual, "Em Uso")
        self.assertEqual(self.equipamento.usuario_atual, "Dr. Silva")
        self.assertIsInstance(self.equipamento.estado, EmUsoState)
        
        # Finalizar uso
        self.equipamento.finalizar_uso()
        
        # Verificar consistência após transição
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
        self.assertIsNone(self.equipamento.usuario_atual)
        self.assertIsInstance(self.equipamento.estado, DisponivelState)
    
    def test_multiplas_transicoes(self):
        """Testa múltiplas transições de estado."""
        # Ciclo completo: Disponível -> Em Uso -> Manutenção -> Disponível
        self.equipamento.iniciar_uso("Dr. Silva")
        self.assertEqual(self.equipamento.estado_atual, "Em Uso")
        
        self.equipamento.finalizar_uso()
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
        
        self.equipamento.iniciar_manutencao("Técnico João")
        self.assertEqual(self.equipamento.estado_atual, "Em Manutenção")
        
        self.equipamento.finalizar_manutencao()
        self.assertEqual(self.equipamento.estado_atual, "Disponível")
    
    def test_estado_validacao_parametros(self):
        """Testa validação de parâmetros nos estados."""
        # Iniciar uso sem usuário
        resultado = self.equipamento.iniciar_uso("")
        self.assertIn('usuário inválido', resultado['mensagem'].lower())
        
        # Iniciar manutenção sem técnico
        resultado = self.equipamento.iniciar_manutencao("")
        self.assertIn('técnico inválido', resultado['mensagem'].lower())
    
    def test_estado_historico_transicoes(self):
        """Testa histórico de transições de estado."""
        # Realizar algumas transições
        self.equipamento.iniciar_uso("Dr. Silva")
        self.equipamento.finalizar_uso()
        self.equipamento.iniciar_manutencao("Técnico João")
        self.equipamento.finalizar_manutencao()
        
        # Verificar histórico (se implementado)
        if hasattr(self.equipamento, 'historico_estados'):
            historico = self.equipamento.historico_estados
            self.assertGreater(len(historico), 0)
    
    def test_estado_performance(self):
        """Testa performance das transições de estado."""
        import time
        
        # Realizar muitas transições
        start_time = time.time()
        for i in range(100):
            self.equipamento.iniciar_uso(f"Usuario{i}")
            self.equipamento.finalizar_uso()
        end_time = time.time()
        
        # Deve ser rápido
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)  # Menos de 1 segundo
    
    def test_estado_extensibilidade(self):
        """Testa extensibilidade do padrão State."""
        # Verificar se novos estados podem ser adicionados facilmente
        # (estrutura das classes permite extensão)
        
        self.assertTrue(issubclass(DisponivelState, EstadoEquipamento))
        self.assertTrue(issubclass(EmUsoState, EstadoEquipamento))
        self.assertTrue(issubclass(ManutencaoState, EstadoEquipamento))
        
        # Interface consistente
        metodos_obrigatorios = ['ligar', 'desligar', 'iniciar_uso', 'finalizar_uso', 
                                'iniciar_manutencao', 'finalizar_manutencao']
        
        for estado in [self.estado_disponivel, self.estado_em_uso, self.estado_manutencao]:
            for metodo in metodos_obrigatorios:
                self.assertTrue(hasattr(estado, metodo))


if __name__ == '__main__':
    unittest.main()
