"""
Testes para o padrão Chain of Responsibility
"""

import unittest
from unittest.mock import Mock
import logging
from patterns.comportamentais.chain_of_responsibility import (
    SequenceRequest, SequenceHandler, DNAValidator, RNAValidator,
    SequenceQualityChecker, ContaminationChecker, SequenceProcessor,
    SequenceAnalysisSystem
)


class TestChainOfResponsibility(unittest.TestCase):
    """Testes para o padrão Chain of Responsibility."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        logging.disable(logging.CRITICAL)
        self.system = SequenceAnalysisSystem()
    
    def tearDown(self):
        """Limpeza após os testes."""
        logging.disable(logging.NOTSET)
    
    def test_sequence_request_creation(self):
        """Testa criação de requisição de sequência."""
        request = SequenceRequest("ATCGATCG", "DNA")
        
        self.assertEqual(request.sequence, "ATCGATCG")
        self.assertEqual(request.sequence_type, "DNA")
        self.assertTrue(request.is_valid)
        self.assertEqual(len(request.errors), 0)
        self.assertEqual(len(request.processing_steps), 0)
    
    def test_sequence_request_with_metadata(self):
        """Testa criação de requisição com metadados."""
        metadata = {"source": "test", "quality": "high"}
        request = SequenceRequest("ATCGATCG", "DNA", metadata)
        
        self.assertEqual(request.metadata, metadata)
    
    def test_dna_validator_valid_sequence(self):
        """Testa validador DNA com sequência válida."""
        validator = DNAValidator()
        request = SequenceRequest("ATCGATCG", "DNA")
        
        result = validator.handle(request)
        
        self.assertTrue(result.is_valid)
        self.assertIn("DNA validation passed", result.processing_steps[0])
    
    def test_dna_validator_invalid_sequence(self):
        """Testa validador DNA com sequência inválida."""
        validator = DNAValidator()
        request = SequenceRequest("ATCGXTCG", "DNA")
        
        result = validator.handle(request)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Invalid DNA bases found", result.errors[0])
        self.assertIn("X", result.errors[0])
    
    def test_rna_validator_valid_sequence(self):
        """Testa validador RNA com sequência válida."""
        validator = RNAValidator()
        request = SequenceRequest("AUCGAUCG", "RNA")
        
        result = validator.handle(request)
        
        self.assertTrue(result.is_valid)
        self.assertIn("RNA validation passed", result.processing_steps[0])
    
    def test_rna_validator_invalid_sequence(self):
        """Testa validador RNA com sequência inválida."""
        validator = RNAValidator()
        request = SequenceRequest("ATCGATCG", "RNA")
        
        result = validator.handle(request)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Invalid RNA bases found", result.errors[0])
    
    def test_quality_checker_good_sequence(self):
        """Testa verificador de qualidade com boa sequência."""
        checker = SequenceQualityChecker()
        request = SequenceRequest("ATCGATCGATCGATCG", "DNA")
        
        result = checker.handle(request)
        
        self.assertTrue(result.is_valid)
        self.assertIn("Quality check passed", result.processing_steps[0])
        self.assertIn("quality_score", result.metadata)
        self.assertIn("gc_content", result.metadata)
    
    def test_quality_checker_poor_sequence(self):
        """Testa verificador de qualidade com sequência ruim."""
        checker = SequenceQualityChecker(min_quality_score=0.9)
        request = SequenceRequest("ATCG", "DNA")  # Sequência muito curta
        
        result = checker.handle(request)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Low quality score", result.errors[0])
    
    def test_contamination_checker_clean_sequence(self):
        """Testa verificador de contaminação com sequência limpa."""
        checker = ContaminationChecker()
        request = SequenceRequest("ATCGATCG", "DNA")
        
        result = checker.handle(request)
        
        self.assertTrue(result.is_valid)
        self.assertIn("Contamination check passed", result.processing_steps[0])
    
    def test_contamination_checker_contaminated_sequence(self):
        """Testa verificador de contaminação com sequência contaminada."""
        checker = ContaminationChecker()
        request = SequenceRequest("AAAAAAATCG", "DNA")
        
        result = checker.handle(request)
        
        self.assertFalse(result.is_valid)
        self.assertIn("Contamination detected", result.errors[0])
        self.assertIn("AAAAAA", result.errors[0])
    
    def test_sequence_processor(self):
        """Testa processador de sequência."""
        processor = SequenceProcessor()
        request = SequenceRequest("ATCGATCG", "DNA")
        
        result = processor.handle(request)
        
        self.assertTrue(result.is_valid)
        self.assertIn("Sequence processing completed", result.processing_steps[0])
        self.assertIn("processed_data", result.metadata)
        self.assertIn("reverse_complement", result.metadata["processed_data"])
    
    def test_chain_integration_valid_sequence(self):
        """Testa integração completa da cadeia com sequência válida."""
        result = self.system.analyze_sequence("ATCGATCGATCG", "DNA")
        
        self.assertTrue(result.is_valid)
        self.assertGreater(len(result.processing_steps), 0)
        self.assertIn("processed_data", result.metadata)
    
    def test_chain_integration_invalid_sequence(self):
        """Testa integração completa da cadeia com sequência inválida."""
        result = self.system.analyze_sequence("ATCGXTCG", "DNA")
        
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
        self.assertNotIn("processed_data", result.metadata)
    
    def test_handler_chain_setup(self):
        """Testa configuração da cadeia de handlers."""
        # Verifica se a cadeia foi configurada corretamente
        self.assertIsNotNone(self.system.handler_chain)
        self.assertIsInstance(self.system.handler_chain, DNAValidator)
    
    def test_handler_pass_to_next(self):
        """Testa passagem para o próximo handler."""
        validator = DNAValidator()
        request = SequenceRequest("ATCGATCG", "RNA")  # Não é DNA
        
        # Mock do próximo handler
        next_handler = Mock()
        next_handler.handle.return_value = request
        validator.set_next(next_handler)
        
        result = validator.handle(request)
        
        next_handler.handle.assert_called_once_with(request)
    
    def test_gc_content_calculation(self):
        """Testa cálculo de conteúdo GC."""
        checker = SequenceQualityChecker()
        
        # Testa sequência com 50% de GC
        gc_content = checker._calculate_gc_content("ATCGATCG")
        self.assertEqual(gc_content, 0.5)
        
        # Testa sequência vazia
        gc_content = checker._calculate_gc_content("")
        self.assertEqual(gc_content, 0.0)
    
    def test_quality_score_calculation(self):
        """Testa cálculo de score de qualidade."""
        checker = SequenceQualityChecker()
        
        # Testa com sequência longa
        score = checker._calculate_quality_score("ATCGATCGATCGATCG", 0.5)
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_reverse_complement(self):
        """Testa geração de reverse complement."""
        processor = SequenceProcessor()
        
        # Testa sequência simples
        rc = processor._get_reverse_complement("ATCG")
        self.assertEqual(rc, "CGAT")
        
        # Testa com RNA
        rc = processor._get_reverse_complement("AUCG")
        self.assertEqual(rc, "CGAT")
    
    def test_request_add_step_and_error(self):
        """Testa adição de passos e erros na requisição."""
        request = SequenceRequest("ATCG", "DNA")
        
        request.add_step("Test step")
        self.assertIn("Test step", request.processing_steps)
        
        request.add_error("Test error")
        self.assertFalse(request.is_valid)
        self.assertIn("Test error", request.errors)
    
    def test_sequence_case_conversion(self):
        """Testa conversão de maiúsculas/minúsculas."""
        request = SequenceRequest("atcgaTcG", "DNA")
        
        self.assertEqual(request.sequence, "ATCGATCG")
    
    def test_different_sequence_types(self):
        """Testa diferentes tipos de sequência."""
        # DNA
        result_dna = self.system.analyze_sequence("ATCGATCG", "DNA")
        self.assertTrue(result_dna.is_valid)
        
        # RNA
        result_rna = self.system.analyze_sequence("AUCGAUCG", "RNA")
        self.assertTrue(result_rna.is_valid)
        
        # Tipo inválido (deve ser ignorado pelos validadores específicos)
        result_invalid = self.system.analyze_sequence("ATCGATCG", "UNKNOWN")
        self.assertTrue(result_invalid.is_valid)  # Passa pelos validadores específicos


if __name__ == '__main__':
    unittest.main()
