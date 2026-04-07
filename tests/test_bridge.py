"""
Testes para o padrão Bridge
"""

import unittest
from unittest.mock import Mock, patch
from patterns.estruturais.bridge import (
    AlgoritmoProcessamento, AlinhamentoGlobal, AlinhamentoLocal,
    ProcessadorDados, ProcessadorBasico, ProcessadorAvancado
)


class TestBridge(unittest.TestCase):
    """Testes para o padrão Bridge."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.alinhamento_global = AlinhamentoGlobal()
        self.alinhamento_local = AlinhamentoLocal()
        
        self.processador_basico_global = ProcessadorBasico(self.alinhamento_global)
        self.processador_basico_local = ProcessadorBasico(self.alinhamento_local)
        
        self.processador_avancado_global = ProcessadorAvancado(self.alinhamento_global)
        self.processador_avancado_local = ProcessadorAvancado(self.alinhamento_local)
    
    def test_sequenciador_illumina_creation(self):
        """Testa criação do sequenciador Illumina."""
        sequenciador = SequenciadorIllumina()
        
        self.assertIsInstance(sequenciador, ImplementacaoEquipamento)
        self.assertEqual(sequenciador.plataforma, "Illumina")
        self.assertEqual(sequenciador.tecnologia, "Sequenciamento por Síntese")
    
    def test_sequenciator_nanopore_creation(self):
        """Testa criação do sequenciador Oxford Nanopore."""
        sequenciador = SequenciadorOxfordNanopore()
        
        self.assertIsInstance(sequenciador, ImplementacaoEquipamento)
        self.assertEqual(sequenciador.plataforma, "Oxford Nanopore")
        self.assertEqual(sequenciador.tecnologia, "Sequenciamento em Tempo Real")
    
    def test_sequenciador_illumina_operar(self):
        """Testa operação do sequenciador Illumina."""
        resultado = self.sequenciador_illumina.operar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('plataforma', resultado)
        self.assertIn('tecnologia', resultado)
        self.assertIn('dados', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['plataforma'], 'Illumina')
        self.assertEqual(resultado['status'], 'Operação concluída')
    
    def test_sequenciator_nanopore_operar(self):
        """Testa operação do sequenciador Oxford Nanopore."""
        resultado = self.sequenciator_nanopore.operar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('plataforma', resultado)
        self.assertIn('tecnologia', resultado)
        self.assertIn('dados', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['plataforma'], 'Oxford Nanopore')
        self.assertEqual(resultado['status'], 'Operação concluída')
    
    def test_sequenciador_illumina_calibrar(self):
        """Testa calibração do sequenciador Illumina."""
        resultado = self.sequenciador_illumina.calibrar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('plataforma', resultado)
        self.assertIn('calibracao', resultado)
        self.assertTrue(resultado['calibracao'])
    
    def test_sequenciator_nanopore_calibrar(self):
        """Testa calibração do sequenciador Oxford Nanopore."""
        resultado = self.sequenciator_nanopore.calibrar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('plataforma', resultado)
        self.assertIn('calibracao', resultado)
        self.assertTrue(resultado['calibracao'])
    
    def test_sequenciador_illumina_manutencao(self):
        """Testa manutenção do sequenciador Illumina."""
        resultado = self.sequenciador_illumina.manutencao()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('plataforma', resultado)
        self.assertIn('manutencao', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['status'], 'Manutenção concluída')
    
    def test_sequenciator_nanopore_manutencao(self):
        """Testa manutenção do sequenciador Oxford Nanopore."""
        resultado = self.sequenciator_nanopore.manutencao()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('plataforma', resultado)
        self.assertIn('manutencao', resultado)
        self.assertIn('status', resultado)
        self.assertEqual(resultado['status'], 'Manutenção concluída')
    
    def test_equipamento_basico_creation(self):
        """Testa criação de equipamento básico."""
        equip = EquipamentoBasico(self.sequenciador_illumina)
        
        self.assertIsInstance(equip, AbstracaoEquipamento)
        self.assertEqual(equip.implementacao, self.sequenciador_illumina)
        self.assertEqual(equip.nivel_funcionalidade, "Básico")
    
    def test_equipamento_avancado_creation(self):
        """Testa criação de equipamento avançado."""
        equip = EquipamentoAvancado(self.sequenciator_nanopore)
        
        self.assertIsInstance(equip, AbstracaoEquipamento)
        self.assertEqual(equip.implementacao, self.sequenciator_nanopore)
        self.assertEqual(equip.nivel_funcionalidade, "Avançado")
    
    def test_equipamento_basico_operar(self):
        """Testa operação de equipamento básico."""
        resultado = self.equip_basico_illumina.operar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('abstracao', resultado)
        self.assertIn('implementacao', resultado)
        self.assertEqual(resultado['abstracao']['nivel'], 'Básico')
        self.assertEqual(resultado['implementacao']['plataforma'], 'Illumina')
    
    def test_equipamento_avancado_operar(self):
        """Testa operação de equipamento avançado."""
        resultado = self.equip_avancado_nanopore.operar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('abstracao', resultado)
        self.assertIn('implementacao', resultado)
        self.assertEqual(resultado['abstracao']['nivel'], 'Avançado')
        self.assertEqual(resultado['implementacao']['plataforma'], 'Oxford Nanopore')
    
    def test_equipamento_basico_calibrar(self):
        """Testa calibração de equipamento básico."""
        resultado = self.equip_basico_illumina.calibrar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('abstracao', resultado)
        self.assertIn('implementacao', resultado)
        self.assertTrue(resultado['implementacao']['calibracao'])
    
    def test_equipamento_avancado_calibrar(self):
        """Testa calibração de equipamento avançado."""
        resultado = self.equip_avancado_nanopore.calibrar()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('abstracao', resultado)
        self.assertIn('implementacao', resultado)
        self.assertTrue(resultado['implementacao']['calibracao'])
    
    def test_equipamento_basico_manutencao(self):
        """Testa manutenção de equipamento básico."""
        resultado = self.equip_basico_illumina.manutencao()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('abstracao', resultado)
        self.assertIn('implementacao', resultado)
        self.assertEqual(resultado['implementacao']['status'], 'Manutenção concluída')
    
    def test_equipamento_avancado_manutencao(self):
        """Testa manutenção de equipamento avançado."""
        resultado = self.equip_avancado_nanopore.manutencao()
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('abstracao', resultado)
        self.assertIn('implementacao', resultado)
        self.assertEqual(resultado['implementacao']['status'], 'Manutenção concluída')
    
    def test_bridge_independence(self):
        """Testa independência entre abstração e implementação."""
        # Mesma implementação, abstrações diferentes
        resultado_basico = self.equip_basico_illumina.operar()
        resultado_avancado = self.equip_avancado_illumina.operar()
        
        # Implementação deve ser a mesma
        self.assertEqual(
            resultado_basico['implementacao']['plataforma'],
            resultado_avancado['implementacao']['plataforma']
        )
        
        # Abstração deve ser diferente
        self.assertNotEqual(
            resultado_basico['abstracao']['nivel'],
            resultado_avancado['abstracao']['nivel']
        )
    
    def test_bridge_extensibility(self):
        """Testa extensibilidade do padrão Bridge."""
        # Mesma abstração, implementações diferentes
        resultado_illumina = self.equip_basico_illumina.operar()
        resultado_nanopore = self.equip_basico_nanopore.operar()
        
        # Abstração deve ser a mesma
        self.assertEqual(
            resultado_illumina['abstracao']['nivel'],
            resultado_nanopore['abstracao']['nivel']
        )
        
        # Implementação deve ser diferente
        self.assertNotEqual(
            resultado_illumina['implementacao']['plataforma'],
            resultado_nanopore['implementacao']['plataforma']
        )
    
    def test_change_implementation_runtime(self):
        """Testa mudança de implementação em tempo de execução."""
        equip = EquipamentoBasico(self.sequenciador_illumina)
        
        # Operação com implementação inicial
        resultado_illumina = equip.operar()
        self.assertEqual(resultado_illumina['implementacao']['plataforma'], 'Illumina')
        
        # Mudar implementação
        equip.mudar_implementacao(self.sequenciator_nanopore)
        
        # Operação com nova implementação
        resultado_nanopore = equip.operar()
        self.assertEqual(resultado_nanopore['implementacao']['plataforma'], 'Oxford Nanopore')
    
    def test_illumina_specific_features(self):
        """Testa características específicas do Illumina."""
        resultado = self.sequenciador_illumina.operar()
        
        self.assertIn('read_length', resultado['dados'])
        self.assertIn('throughput', resultado['dados'])
        self.assertIn('accuracy', resultado['dados'])
        
        # Valores típicos do Illumina
        self.assertGreaterEqual(resultado['dados']['accuracy'], 0.99)
        self.assertLessEqual(resultado['dados']['read_length'], 300)
    
    def test_nanopore_specific_features(self):
        """Testa características específicas do Oxford Nanopore."""
        resultado = self.sequenciator_nanopore.operar()
        
        self.assertIn('read_length', resultado['dados'])
        self.assertIn('throughput', resultado['dados'])
        self.assertIn('accuracy', resultado['dados'])
        
        # Valores típicos do Nanopore
        self.assertGreaterEqual(resultado['dados']['read_length'], 1000)
        self.assertLessEqual(resultado['dados']['accuracy'], 0.95)
    
    def test_equipamento_avancado_additional_features(self):
        """Testa funcionalidades adicionais do equipamento avançado."""
        resultado = self.equip_avancado_illumina.operar()
        
        self.assertIn('funcionalidades_avancadas', resultado['abstracao'])
        funcionalidades = resultado['abstracao']['funcionalidades_avancadas']
        
        self.assertIn('análise_em_tempo_real', funcionalidades)
        self.assertIn('ajuste_automatico', funcionalidades)
        self.assertIn('otimizacao_parametros', funcionalidades)
    
    def test_multiple_operations_sequence(self):
        """Testa sequência de múltiplas operações."""
        equip = EquipamentoAvancado(self.sequenciador_illumina)
        
        # Calibrar
        calibracao = equip.calibrar()
        self.assertTrue(calibracao['implementacao']['calibracao'])
        
        # Operar
        operacao = equip.operar()
        self.assertEqual(operacao['implementacao']['plataforma'], 'Illumina')
        
        # Manutenção
        manutencao = equip.manutencao()
        self.assertEqual(manutencao['implementacao']['status'], 'Manutenção concluída')
    
    def test_error_handling_invalid_implementation(self):
        """Testa tratamento de erros com implementação inválida."""
        with self.assertRaises(AttributeError):
            equip = EquipamentoBasico(None)
            equip.operar()
    
    def test_bridge_pattern_benefits(self):
        """Testa benefícios do padrão Bridge."""
        # 1. Desacoplamento entre abstração e implementação
        self.assertNotEqual(
            type(self.equip_basico_illumina).__name__,
            type(self.sequenciador_illumina).__name__
        )
        
        # 2. Extensibilidade independente
        self.assertTrue(hasattr(self.equip_basico_illumina, 'operar'))
        self.assertTrue(hasattr(self.sequenciador_illumina, 'operar'))
        
        # 3. Mudança em tempo de execução
        self.assertTrue(hasattr(self.equip_basico_illumina, 'mudar_implementacao'))
    
    def test_abstraction_methods_delegation(self):
        """Testa delegação de métodos da abstração para implementação."""
        equip = EquipamentoBasico(self.sequenciador_illumina)
        
        # Mock da implementação
        mock_implementacao = Mock()
        mock_implementacao.operar.return_value = {'test': 'result'}
        equip.implementacao = mock_implementacao
        
        resultado = equip.operar()
        
        # Verifica se o método foi delegado
        mock_implementacao.operar.assert_called_once()
        self.assertIn('abstracao', resultado)
        self.assertIn('implementacao', resultado)
    
    def test_consistency_between_operations(self):
        """Testa consistência entre diferentes operações."""
        equip = EquipamentoAvancado(self.sequenciador_illumina)
        
        operacao = equip.operar()
        calibracao = equip.calibrar()
        manutencao = equip.manutencao()
        
        # Todas as operações devem manter a mesma plataforma
        self.assertEqual(operacao['implementacao']['plataforma'], 'Illumina')
        self.assertEqual(calibracao['implementacao']['plataforma'], 'Illumina')
        self.assertEqual(manutencao['implementacao']['plataforma'], 'Illumina')
        
        # Todas as operações devem manter o mesmo nível de funcionalidade
        self.assertEqual(operacao['abstracao']['nivel'], 'Avançado')
        self.assertEqual(calibracao['abstracao']['nivel'], 'Avançado')
        self.assertEqual(manutencao['abstracao']['nivel'], 'Avançado')


if __name__ == '__main__':
    unittest.main()
