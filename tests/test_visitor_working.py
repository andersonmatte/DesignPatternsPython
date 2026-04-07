"""
Testes para o padrão Visitor
"""

import unittest
from unittest.mock import Mock, patch
from patterns.comportamentais.visitor import (
    TipoComponente, ComponenteGenetico
)


class TestVisitor(unittest.TestCase):
    """Testes para o padrão Visitor."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.gene_proteina = MockComponenteGenetico("BRCA1", "17", 43044295, TipoComponente.GENE_PROTEINA)
        self.gene_regulador = MockComponenteGenetico("TP53", "17", 7579472, TipoComponente.GENE_REGULADOR)
        self.gene_estrutural = MockComponenteGenetico("COL1A1", "17", 48261549, TipoComponente.GENE_ESTRUTURAL)
    
    def test_tipo_componente_enum(self):
        """Testa enum TipoComponente."""
        self.assertEqual(TipoComponente.GENE_PROTEINA.value, "gene_proteina")
        self.assertEqual(TipoComponente.GENE_REGULADOR.value, "gene_regulador")
        self.assertEqual(TipoComponente.GENE_ESTRUTURAL.value, "gene_estrutural")
        self.assertEqual(TipoComponente.GENE_HOUSEKEEPING.value, "gene_housekeeping")
    
    def test_componente_genetico_creation(self):
        """Testa criação de componente genético."""
        componente = MockComponenteGenetico("GENE001", "1", 1000000, TipoComponente.GENE_PROTEINA)
        
        self.assertIsInstance(componente, ComponenteGenetico)
        self.assertEqual(componente.nome, "GENE001")
        self.assertEqual(componente.cromossomo, "1")
        self.assertEqual(componente.posicao, 1000000)
        self.assertEqual(componente.tipo, TipoComponente.GENE_PROTEINA)
    
    def test_componente_genetico_interface(self):
        """Testa interface do componente genético."""
        # Deve ter método aceitar_visitante
        self.assertTrue(hasattr(self.gene_proteina, 'aceitar_visitante'))
        self.assertTrue(callable(self.gene_proteina.aceitar_visitante))
        
        # Deve ter métodos básicos
        self.assertTrue(hasattr(self.gene_proteina, 'obter_info'))
        self.assertTrue(callable(self.gene_proteina.obter_info))
    
    def test_componente_genetico_aceitar_visitante(self):
        """Testa método aceitar_visitante."""
        visitante = MockVisitante()
        
        # Componente aceita visitante
        resultado = self.gene_proteina.aceitar_visitante(visitante)
        
        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
    
    def test_componente_genetico_obter_info(self):
        """Testa método obter_info."""
        info = self.gene_proteina.obter_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('nome', info)
        self.assertIn('cromossomo', info)
        self.assertIn('posicao', info)
        self.assertIn('tipo', info)
        
        self.assertEqual(info['nome'], "BRCA1")
        self.assertEqual(info['cromossomo'], "17")
        self.assertEqual(info['posicao'], 43044295)
        self.assertEqual(info['tipo'], "gene_proteina")
    
    def test_componentes_diferentes_tipos(self):
        """Testa componentes de diferentes tipos."""
        info_proteina = self.gene_proteina.obter_info()
        info_regulador = self.gene_regulador.obter_info()
        info_estrutural = self.gene_estrutural.obter_info()
        
        self.assertEqual(info_proteina['tipo'], "gene_proteina")
        self.assertEqual(info_regulador['tipo'], "gene_regulador")
        self.assertEqual(info_estrutural['tipo'], "gene_estrutural")
    
    def test_visitante_creation(self):
        """Testa criação de visitante."""
        visitante = MockVisitante()
        
        self.assertIsInstance(visitante, MockVisitante)
        self.assertEqual(len(visitante.visitas_realizadas), 0)
    
    def test_visitante_visitar_gene_proteina(self):
        """Testa visita a gene de proteína."""
        visitante = MockVisitante()
        
        resultado = visitante.visitar_gene_proteina(self.gene_proteina)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_visita', resultado)
        self.assertIn('gene', resultado)
        self.assertEqual(resultado['tipo_visita'], "gene_proteina")
        self.assertEqual(resultado['gene']['nome'], "BRCA1")
    
    def test_visitante_visitar_gene_regulador(self):
        """Testa visita a gene regulador."""
        visitante = MockVisitante()
        
        resultado = visitante.visitar_gene_regulador(self.gene_regulador)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_visita', resultado)
        self.assertIn('gene', resultado)
        self.assertEqual(resultado['tipo_visita'], "gene_regulador")
        self.assertEqual(resultado['gene']['nome'], "TP53")
    
    def test_visitante_visitar_gene_estrutural(self):
        """Testa visita a gene estrutural."""
        visitante = MockVisitante()
        
        resultado = visitante.visitar_gene_estrutural(self.gene_estrutural)
        
        self.assertIsInstance(resultado, dict)
        self.assertIn('tipo_visita', resultado)
        self.assertIn('gene', resultado)
        self.assertEqual(resultado['tipo_visita'], "gene_estrutural")
        self.assertEqual(resultado['gene']['nome'], "COL1A1")
    
    def test_visitante_registrar_visita(self):
        """Testa registro de visita pelo visitante."""
        visitante = MockVisitante()
        
        # Realizar visitas
        visitante.visitar_gene_proteina(self.gene_proteina)
        visitante.visitar_gene_regulador(self.gene_regulador)
        
        # Verificar registros
        self.assertEqual(len(visitante.visitas_realizadas), 2)
        self.assertIn("gene_proteina", [v['tipo'] for v in visitante.visitas_realizadas])
        self.assertIn("gene_regulador", [v['tipo'] for v in visitante.visitas_realizadas])
    
    def test_visitante_obter_estatisticas(self):
        """Testa obtenção de estatísticas do visitante."""
        visitante = MockVisitante()
        
        # Realizar algumas visitas
        visitante.visitar_gene_proteina(self.gene_proteina)
        visitante.visitar_gene_regulador(self.gene_regulador)
        visitante.visitar_gene_estrutural(self.gene_estrutural)
        
        stats = visitante.obter_estatisticas()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_visitas', stats)
        self.assertIn('visitas_por_tipo', stats)
        self.assertIn('genes_visitados', stats)
        
        self.assertEqual(stats['total_visitas'], 3)
        self.assertEqual(stats['visitas_por_tipo']['gene_proteina'], 1)
        self.assertEqual(stats['visitas_por_tipo']['gene_regulador'], 1)
        self.assertEqual(stats['visitas_por_tipo']['gene_estrutural'], 1)
    
    def test_visitor_pattern_double_dispatch(self):
        """Testa double dispatch do padrão Visitor."""
        visitante = MockVisitante()
        
        # Componente aceita visitante e chama método específico
        resultado = self.gene_proteina.aceitar_visitante(visitante)
        
        # Verificar se o método correto foi chamado
        self.assertEqual(resultado['tipo_visita'], "gene_proteina")
        self.assertEqual(resultado['gene']['nome'], "BRCA1")
    
    def test_visitor_pattern_extensibilidade(self):
        """Testa extensibilidade do padrão Visitor."""
        # Novo tipo de componente
        novo_componente = MockComponenteGenetico("NEW001", "X", 1000, TipoComponente.GENE_HOUSEKEEPING)
        
        # Novo visitante com método para o novo tipo
        novo_visitante = MockVisitante()
        
        # Visitante pode lidar com novo tipo
        resultado = novo_visitante.visitar_gene_housekeeping(novo_componente)
        
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['tipo_visita'], "gene_housekeeping")
        self.assertEqual(resultado['gene']['nome'], "NEW001")
    
    def test_visitor_pattern_separacao_responsabilidades(self):
        """Testa separação de responsabilidades no Visitor."""
        # Componente só conhece sua estrutura
        info_componente = self.gene_proteina.obter_info()
        self.assertIsInstance(info_componente, dict)
        
        # Visitante só conhece a operação
        visitante = MockVisitante()
        resultado_visita = visitante.visitar_gene_proteina(self.gene_proteina)
        self.assertIsInstance(resultado_visita, dict)
        
        # Operações são separadas
        self.assertTrue(hasattr(self.gene_proteina, 'obter_info'))
        self.assertTrue(hasattr(visitante, 'visitar_gene_proteina'))
    
    def test_visitor_pattern_adicao_operacoes(self):
        """Testa adição de novas operações sem modificar componentes."""
        # Novo visitante com operação diferente
        visitante_analise = MockVisitanteAnalise()
        
        # Aplicar nova operação a componentes existentes
        resultado1 = visitante_analise.visitar_gene_proteina(self.gene_proteina)
        resultado2 = visitante_analise.visitar_gene_regulador(self.gene_regulador)
        
        # Novas operações sem modificar componentes
        self.assertIn('analise', resultado1)
        self.assertIn('analise', resultado2)
        self.assertNotEqual(resultado1['analise'], resultado2['analise'])
    
    def test_visitor_pattern_composicao(self):
        """Testa visitor com estrutura composta."""
        # Criar estrutura de componentes
        componentes = [
            self.gene_proteina,
            self.gene_regulador,
            self.gene_estrutural
        ]
        
        visitante = MockVisitante()
        resultados = []
        
        # Aplicar visitante a todos os componentes
        for componente in componentes:
            resultado = componente.aceitar_visitante(visitante)
            resultados.append(resultado)
        
        # Verificar resultados
        self.assertEqual(len(resultados), 3)
        tipos = [r['tipo_visita'] for r in resultados]
        self.assertIn("gene_proteina", tipos)
        self.assertIn("gene_regulador", tipos)
        self.assertIn("gene_estrutural", tipos)
    
    def test_visitor_benefits(self):
        """Testa benefícios do padrão Visitor."""
        # 1. Adição de operações sem modificar classes
        visitante = MockVisitante()
        resultado = self.gene_proteina.aceitar_visitante(visitante)
        self.assertIsInstance(resultado, dict)
        
        # 2. Operações relacionadas em uma classe
        self.assertTrue(hasattr(visitante, 'visitar_gene_proteina'))
        self.assertTrue(hasattr(visitante, 'visitar_gene_regulador'))
        self.assertTrue(hasattr(visitante, 'visitar_gene_estrutural'))
        
        # 3. Double dispatch
        resultado_dispatch = self.gene_proteina.aceitar_visitante(visitante)
        self.assertEqual(resultado_dispatch['tipo_visita'], "gene_proteina")
        
        # 4. Acumulação de estado
        visitante.visitar_gene_proteina(self.gene_proteina)
        visitante.visitar_gene_regulador(self.gene_regulador)
        stats = visitante.obter_estatisticas()
        self.assertEqual(stats['total_visitas'], 2)


class MockComponenteGenetico(ComponenteGenetico):
    """Mock para testes de componente genético."""
    
    def __init__(self, nome: str, cromossomo: str, posicao: int, tipo: TipoComponente):
        super().__init__(nome, cromossomo, posicao)
        self.tipo = tipo
    
    def aceitar_visitante(self, visitante) -> dict:
        """Aceita visitante e chama método apropriado."""
        if self.tipo == TipoComponente.GENE_PROTEINA:
            return visitante.visitar_gene_proteina(self)
        elif self.tipo == TipoComponente.GENE_REGULADOR:
            return visitante.visitar_gene_regulador(self)
        elif self.tipo == TipoComponente.GENE_ESTRUTURAL:
            return visitante.visitar_gene_estrutural(self)
        elif self.tipo == TipoComponente.GENE_HOUSEKEEPING:
            return visitante.visitar_gene_housekeeping(self)
        else:
            return {"erro": "Tipo não suportado"}
    
    def obter_info(self) -> dict:
        """Retorna informações do componente."""
        return {
            "nome": self.nome,
            "cromossomo": self.cromossomo,
            "posicao": self.posicao,
            "tipo": self.tipo.value
        }


class MockVisitante:
    """Mock para testes de visitante."""
    
    def __init__(self):
        self.visitas_realizadas = []
    
    def visitar_gene_proteina(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene de proteína."""
        resultado = {
            "tipo_visita": "gene_proteina",
            "gene": componente.obter_info(),
            "analise": "Análise de expressão proteica"
        }
        self.visitas_realizadas.append({"tipo": "gene_proteina", "gene": componente.nome})
        return resultado
    
    def visitar_gene_regulador(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene regulador."""
        resultado = {
            "tipo_visita": "gene_regulador",
            "gene": componente.obter_info(),
            "analise": "Análise de regulação gênica"
        }
        self.visitas_realizadas.append({"tipo": "gene_regulador", "gene": componente.nome})
        return resultado
    
    def visitar_gene_estrutural(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene estrutural."""
        resultado = {
            "tipo_visita": "gene_estrutural",
            "gene": componente.obter_info(),
            "analise": "Análise de estrutura proteica"
        }
        self.visitas_realizadas.append({"tipo": "gene_estrutural", "gene": componente.nome})
        return resultado
    
    def visitar_gene_housekeeping(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene housekeeping."""
        resultado = {
            "tipo_visita": "gene_housekeeping",
            "gene": componente.obter_info(),
            "analise": "Análise de expressão constitutiva"
        }
        self.visitas_realizadas.append({"tipo": "gene_housekeeping", "gene": componente.nome})
        return resultado
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas das visitas."""
        visitas_por_tipo = {}
        for visita in self.visitas_realizadas:
            tipo = visita['tipo']
            visitas_por_tipo[tipo] = visitas_por_tipo.get(tipo, 0) + 1
        
        return {
            "total_visitas": len(self.visitas_realizadas),
            "visitas_por_tipo": visitas_por_tipo,
            "genes_visitados": [v['gene'] for v in self.visitas_realizadas]
        }


class MockVisitanteAnalise:
    """Mock para testes de visitante com análise diferente."""
    
    def visitar_gene_proteina(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene de proteína com análise específica."""
        return {
            "tipo_visita": "gene_proteina",
            "gene": componente.obter_info(),
            "analise": f"Análise detalhada de {componente.nome} - Score: 95.5"
        }
    
    def visitar_gene_regulador(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene regulador com análise específica."""
        return {
            "tipo_visita": "gene_regulador",
            "gene": componente.obter_info(),
            "analise": f"Análise detalhada de {componente.nome} - Score: 87.2"
        }
    
    def visitar_gene_estrutural(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene estrutural com análise específica."""
        return {
            "tipo_visita": "gene_estrutural",
            "gene": componente.obter_info(),
            "analise": f"Análise detalhada de {componente.nome} - Score: 92.8"
        }
    
    def visitar_gene_housekeeping(self, componente: MockComponenteGenetico) -> dict:
        """Visita gene housekeeping com análise específica."""
        return {
            "tipo_visita": "gene_housekeeping",
            "gene": componente.obter_info(),
            "analise": f"Análise detalhada de {componente.nome} - Score: 98.1"
        }


if __name__ == '__main__':
    unittest.main()
