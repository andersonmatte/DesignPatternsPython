"""
Testes para o padrão Memento
"""

import unittest
import datetime
from unittest.mock import Mock, patch
from patterns.comportamentais.memento import (
    ExperimentMemento, GenomicExperiment, Caretaker, ExperimentManager
)


class TestMemento(unittest.TestCase):
    """Testes para o padrão Memento."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.experiment = GenomicExperiment("EXP001", "ATCGATCG", "alignment")
        self.caretaker = Caretaker()
        self.manager = ExperimentManager()
    
    def test_experiment_memento_creation(self):
        """Testa criação de memento."""
        state = {
            'experiment_id': 'EXP001',
            'sequence': 'ATCGATCG',
            'analysis_type': 'alignment',
            'status': 'Created'
        }
        
        memento = ExperimentMemento(state)
        
        self.assertEqual(memento.state['experiment_id'], 'EXP001')
        self.assertEqual(memento.state['sequence'], 'ATCGATCG')
        self.assertIsInstance(memento.timestamp, datetime.datetime)
        self.assertTrue(memento.name.startswith('Experiment_'))
    
    def test_memento_immutable_state(self):
        """Testa que o estado do memento é imutável."""
        original_state = {'test': 'value'}
        memento = ExperimentMemento(original_state)
        
        # Modifica o estado original
        original_state['test'] = 'modified'
        
        # O memento não deve ser afetado
        self.assertEqual(memento.state['test'], 'value')
    
    def test_memento_summary(self):
        """Testa geração de resumo do memento."""
        state = {
            'sequence': 'ATCGATCGATCG',
            'analysis_type': 'alignment',
            'status': 'Completed'
        }
        memento = ExperimentMemento(state)
        
        summary = memento.get_summary()
        
        self.assertIn('Experiment_', summary)
        self.assertIn('alignment', summary)
        self.assertIn('12bp', summary)
        self.assertIn('Completed', summary)
    
    def test_genomic_experiment_creation(self):
        """Testa criação de experimento genômico."""
        experiment = GenomicExperiment("EXP001", "ATCGATCG", "alignment")
        
        self.assertEqual(experiment.experiment_id, "EXP001")
        self.assertEqual(experiment.sequence, "ATCGATCG")
        self.assertEqual(experiment.analysis_type, "alignment")
        self.assertEqual(experiment.status, "Created")
        self.assertIsInstance(experiment.created_at, datetime.datetime)
        self.assertIsInstance(experiment.modified_at, datetime.datetime)
    
    def test_genomic_experiment_set_parameters(self):
        """Testa definição de parâmetros do experimento."""
        self.experiment.set_parameters(threshold=0.8, algorithm="blast")
        
        self.assertEqual(self.experiment.parameters['threshold'], 0.8)
        self.assertEqual(self.experiment.parameters['algorithm'], "blast")
        self.assertIn("Parameters updated", self.experiment.history[-1])
    
    def test_genomic_experiment_run_alignment_analysis(self):
        """Testa execução de análise de alinhamento."""
        self.experiment.analysis_type = "alignment"
        self.experiment.run_analysis()
        
        self.assertEqual(self.experiment.status, "Completed")
        self.assertIn('alignment_score', self.experiment.results)
        self.assertIn('matches', self.experiment.results)
        self.assertIn('reference', self.experiment.results)
    
    def test_genomic_experiment_run_assembly_analysis(self):
        """Testa execução de análise de montagem."""
        self.experiment.analysis_type = "assembly"
        self.experiment.run_analysis()
        
        self.assertEqual(self.experiment.status, "Completed")
        self.assertIn('contigs', self.experiment.results)
        self.assertIn('n50', self.experiment.results)
        self.assertIn('gc_content', self.experiment.results)
    
    def test_genomic_experiment_run_annotation_analysis(self):
        """Testa execução de análise de anotação."""
        self.experiment.analysis_type = "annotation"
        self.experiment.run_analysis()
        
        self.assertEqual(self.experiment.status, "Completed")
        self.assertIn('genes_found', self.experiment.results)
        self.assertIn('proteins_found', self.experiment.results)
        self.assertIn('go_terms', self.experiment.results)
    
    def test_genomic_experiment_run_basic_analysis(self):
        """Testa execução de análise básica."""
        self.experiment.analysis_type = "unknown"
        self.experiment.run_analysis()
        
        self.assertEqual(self.experiment.status, "Completed")
        self.assertIn('length', self.experiment.results)
        self.assertIn('gc_content', self.experiment.results)
        self.assertIn('quality_metrics', self.experiment.results)
    
    def test_genomic_experiment_modify_sequence(self):
        """Testa modificação de sequência."""
        original_length = len(self.experiment.sequence)
        new_sequence = "ATCGATCGATCGATCG"
        
        self.experiment.modify_sequence(new_sequence)
        
        self.assertEqual(self.experiment.sequence, new_sequence)
        self.assertEqual(self.experiment.status, "Modified")
        self.assertIn("Sequence modified", self.experiment.history[-1])
        self.assertIn(f"{original_length}bp -> {len(new_sequence)}bp", self.experiment.history[-1])
    
    def test_genomic_experiment_reset_results(self):
        """Testa reset de resultados."""
        self.experiment.run_analysis()
        self.assertIsNotNone(self.experiment.results)
        
        self.experiment.reset_results()
        
        self.assertEqual(self.experiment.status, "Reset")
        self.assertEqual(len(self.experiment.results), 0)
        self.assertIn("Results reset", self.experiment.history[-1])
    
    def test_genomic_experiment_save_and_restore(self):
        """Testa salvamento e restauração do experimento."""
        # Modifica o experimento
        self.experiment.set_parameters(threshold=0.8)
        self.experiment.run_analysis()
        
        # Salva o estado
        memento = self.experiment.save()
        
        # Modifica novamente
        self.experiment.modify_sequence("GCTAGCTA")
        
        # Restaura o estado
        self.experiment.restore(memento)
        
        # Verifica se foi restaurado corretamente
        self.assertEqual(self.experiment.sequence, "ATCGATCG")
        self.assertEqual(self.experiment.status, "Completed")
        self.assertEqual(self.experiment.parameters['threshold'], 0.8)
    
    def test_caretaker_add_memento(self):
        """Testa adição de memento ao caretaker."""
        memento1 = ExperimentMemento({'test': 'value1'})
        memento2 = ExperimentMemento({'test': 'value2'})
        
        self.caretaker.add_memento(memento1)
        self.assertEqual(self.caretaker.get_memento_count(), 1)
        
        self.caretaker.add_memento(memento2)
        self.assertEqual(self.caretaker.get_memento_count(), 2)
    
    def test_caretaker_max_mementos_limit(self):
        """Testa limite máximo de mementos."""
        caretaker = Caretaker(max_mementos=3)
        
        # Adiciona mais mementos que o limite
        for i in range(5):
            memento = ExperimentMemento({'test': f'value{i}'})
            caretaker.add_memento(memento)
        
        # Deve manter apenas os últimos 3
        self.assertEqual(caretaker.get_memento_count(), 3)
        self.assertEqual(caretaker.get_memento(0).state['test'], 'value2')
        self.assertEqual(caretaker.get_memento(2).state['test'], 'value4')
    
    def test_caretaker_get_memento(self):
        """Testa obtenção de memento específico."""
        memento1 = ExperimentMemento({'test': 'value1'})
        memento2 = ExperimentMemento({'test': 'value2'})
        
        self.caretaker.add_memento(memento1)
        self.caretaker.add_memento(memento2)
        
        retrieved = self.caretaker.get_memento(1)
        self.assertEqual(retrieved.state['test'], 'value2')
        
        # Índice inválido deve retornar None
        self.assertIsNone(self.caretaker.get_memento(5))
    
    def test_caretaker_navigation(self):
        """Testa navegação entre mementos."""
        memento1 = ExperimentMemento({'test': 'value1'})
        memento2 = ExperimentMemento({'test': 'value2'})
        memento3 = ExperimentMemento({'test': 'value3'})
        
        self.caretaker.add_memento(memento1)
        self.caretaker.add_memento(memento2)
        self.caretaker.add_memento(memento3)
        
        # Posição inicial deve ser o último
        current = self.caretaker.get_current_memento()
        self.assertEqual(current.state['test'], 'value3')
        
        # Navega para anterior
        previous = self.caretaker.get_previous_memento()
        self.assertEqual(previous.state['test'], 'value2')
        
        # Navega para próximo
        next_memento = self.caretaker.get_next_memento()
        self.assertEqual(next_memento.state['test'], 'value3')
        
        # Tentativa de ir além dos limitos
        self.assertIsNone(self.caretaker.get_next_memento())
        self.caretaker.get_previous_memento()
        self.caretaker.get_previous_memento()
        self.assertIsNone(self.caretaker.get_previous_memento())
    
    def test_caretaker_list_mementos(self):
        """Testa listagem de mementos."""
        memento1 = ExperimentMemento({'sequence': 'ATCG', 'status': 'Created'})
        memento2 = ExperimentMemento({'sequence': 'GCTA', 'status': 'Completed'})
        
        self.caretaker.add_memento(memento1)
        self.caretaker.add_memento(memento2)
        
        summaries = self.caretaker.list_mementos()
        
        self.assertEqual(len(summaries), 2)
        self.assertIn('Created', summaries[0])
        self.assertIn('Completed', summaries[1])
        self.assertIn('4bp', summaries[0])
        self.assertIn('4bp', summaries[1])
    
    def test_caretaker_clear_mementos(self):
        """Testa limpeza de mementos."""
        self.caretaker.add_memento(ExperimentMemento({'test': 'value'}))
        self.assertEqual(self.caretaker.get_memento_count(), 1)
        
        self.caretaker.clear_mementos()
        
        self.assertEqual(self.caretaker.get_memento_count(), 0)
        self.assertIsNone(self.caretaker.get_current_memento())
    
    def test_experiment_manager_create_experiment(self):
        """Testa criação de experimento pelo manager."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        
        self.assertIsNotNone(self.manager.experiment)
        self.assertEqual(self.manager.experiment.experiment_id, "EXP001")
        self.assertEqual(self.manager.experiment.sequence, "ATCGATCG")
        self.assertEqual(self.manager.experiment.analysis_type, "alignment")
        self.assertEqual(self.manager.caretaker.get_memento_count(), 1)
    
    def test_experiment_manager_modify_experiment(self):
        """Testa modificação de experimento pelo manager."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        
        self.manager.modify_experiment(
            sequence="ATCGATCGATCGATCG",
            parameters={"threshold": 0.8}
        )
        
        self.assertEqual(self.manager.experiment.sequence, "ATCGATCGATCGATCG")
        self.assertEqual(self.manager.experiment.parameters['threshold'], 0.8)
        self.assertEqual(self.manager.caretaker.get_memento_count(), 2)
    
    def test_experiment_manager_run_analysis(self):
        """Testa execução de análise pelo manager."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        
        self.manager.run_analysis()
        
        self.assertEqual(self.manager.experiment.status, "Completed")
        self.assertIsNotNone(self.manager.experiment.results)
        self.assertEqual(self.manager.caretaker.get_memento_count(), 2)
    
    def test_experiment_manager_undo(self):
        """Testa funcionalidade de undo."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        self.manager.modify_experiment(sequence="GCTAGCTA")
        
        original_sequence = self.manager.experiment.sequence
        
        self.manager.modify_experiment(sequence="TTTTTTTT")
        self.assertEqual(self.manager.experiment.sequence, "TTTTTTTT")
        
        # Undo deve restaurar para o estado anterior
        success = self.manager.undo()
        self.assertTrue(success)
        self.assertEqual(self.manager.experiment.sequence, original_sequence)
    
    def test_experiment_manager_redo(self):
        """Testa funcionalidade de redo."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        self.manager.modify_experiment(sequence="GCTAGCTA")
        
        # Undo
        self.manager.undo()
        self.assertEqual(self.manager.experiment.sequence, "ATCGATCG")
        
        # Redo
        success = self.manager.redo()
        self.assertTrue(success)
        self.assertEqual(self.manager.experiment.sequence, "GCTAGCTA")
    
    def test_experiment_manager_undo_limit(self):
        """Testa limites do undo."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        
        # Tentar undo sem estados anteriores
        success = self.manager.undo()
        self.assertFalse(success)
    
    def test_experiment_manager_redo_limit(self):
        """Testa limites do redo."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        self.manager.modify_experiment(sequence="GCTAGCTA")
        
        # Não há nada para redo
        success = self.manager.redo()
        self.assertFalse(success)
        
        # Undo e depois redo
        self.manager.undo()
        success = self.manager.redo()
        self.assertTrue(success)
    
    def test_experiment_manager_get_history(self):
        """Testa obtenção de histórico."""
        self.manager.create_experiment("EXP001", "ATCGATCG", "alignment")
        self.manager.modify_experiment(sequence="GCTAGCTA")
        self.manager.run_analysis()
        
        history = self.manager.get_history()
        
        self.assertEqual(len(history), 3)
        self.assertIn('EXP001', history[0])
        self.assertIn('EXP001', history[1])
        self.assertIn('EXP001', history[2])
    
    def test_experiment_manager_no_experiment_error(self):
        """Testa erro quando não há experimento criado."""
        with self.assertRaises(ValueError):
            self.manager.run_analysis()
        
        with self.assertRaises(ValueError):
            self.manager.modify_experiment(sequence="GCTAGCTA")
    
    def test_gc_content_calculation(self):
        """Testa cálculo de conteúdo GC."""
        # 50% de GC
        gc_content = self.experiment._calculate_gc_content("ATCGATCG")
        self.assertEqual(gc_content, 0.5)
        
        # 100% de GC
        gc_content = self.experiment._calculate_gc_content("GCGCGCGC")
        self.assertEqual(gc_content, 1.0)
        
        # 0% de GC
        gc_content = self.experiment._calculate_gc_content("ATATATAT")
        self.assertEqual(gc_content, 0.0)
        
        # Sequência vazia
        gc_content = self.experiment._calculate_gc_content("")
        self.assertEqual(gc_content, 0.0)
    
    def test_complexity_score_calculation(self):
        """Testa cálculo de score de complexidade."""
        # Todas as 4 bases
        complexity = self.experiment._calculate_complexity("ATCG")
        self.assertEqual(complexity, 1.0)
        
        # Apenas 2 bases
        complexity = self.experiment._calculate_complexity("ATAT")
        self.assertEqual(complexity, 0.5)
        
        # Apenas 1 base
        complexity = self.experiment._calculate_complexity("AAAA")
        self.assertEqual(complexity, 0.25)
    
    def test_experiment_info(self):
        """Testa obtenção de informações do experimento."""
        info = self.experiment.get_info()
        
        self.assertIn("EXP001", info)
        self.assertIn("alignment", info)
        self.assertIn("Created", info)
        self.assertIn("8bp", info)


if __name__ == '__main__':
    unittest.main()
