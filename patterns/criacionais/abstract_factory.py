from abc import ABC, abstractmethod
from typing import Protocol


class Centrifuga(Protocol):
    """Interface para centrífugas."""
    
    def centrifugar(self, amostra: str, velocidade: int) -> str:
        """Executa centrifugação."""
        pass


class Microscopio(Protocol):
    """Interface para microscópios."""
    
    def observar(self, amostra: str) -> str:
        """Observa amostra no microscópio."""
        pass


class Espectrofotometro(Protocol):
    """Interface para espectrofotômetros."""
    
    def medir_absorbancia(self, amostra: str, comprimento_onda: int) -> float:
        """Mede absorbância da amostra."""
        pass


# Implementações específicas para Genética
class CentrifugaGenetica:
    """Centrífuga especializada para análise genética."""
    
    def centrifugar(self, amostra: str, velocidade: int) -> str:
        return f"Centrifugando amostra {amostra} a {velocidade} rpm para extração de DNA/RNA"


class MicroscopioGenetico:
    """Microscópio especializado para análise genética."""
    
    def observar(self, amostra: str) -> str:
        return f"Observando cromossomos na amostra {amostra} com microscópio genético"


class EspectrofotometroGenetico:
    """Espectrofotômetro especializado para análise genética."""
    
    def medir_absorbancia(self, amostra: str, comprimento_onda: int) -> float:
        # Simulação de medição para DNA/RNA
        return 0.8 + (comprimento_onda % 100) / 1000


# Implementações específicas para Bioquímica
class CentrifugaBioquimica:
    """Centrífuga especializada para análise bioquímica."""
    
    def centrifugar(self, amostra: str, velocidade: int) -> str:
        return f"Centrifugando amostra {amostra} a {velocidade} rpm para separação de proteínas"


class MicroscopioBioquimico:
    """Microscópio especializado para análise bioquímica."""
    
    def observar(self, amostra: str) -> str:
        return f"Observando estruturas proteicas na amostra {amostra} com microscópio bioquímico"


class EspectrofotometroBioquimico:
    """Espectrofotômetro especializado para análise bioquímica."""
    
    def medir_absorbancia(self, amostra: str, comprimento_onda: int) -> float:
        # Simulação de medição para proteínas
        return 0.6 + (comprimento_onda % 80) / 1000


# Implementações específicas para Molecular
class CentrifugaMolecular:
    """Centrífuga especializada para análise molecular."""
    
    def centrifugar(self, amostra: str, velocidade: int) -> str:
        return f"Centrifugando amostra {amostra} a {velocidade} rpm para análise molecular"


class MicroscopioMolecular:
    """Microscópio especializado para análise molecular."""
    
    def observar(self, amostra: str) -> str:
        return f"Observando estruturas moleculares na amostra {amostra} com microscópio molecular"


class EspectrofotometroMolecular:
    """Espectrofotômetro especializado para análise molecular."""
    
    def medir_absorbancia(self, amostra: str, comprimento_onda: int) -> float:
        # Simulação de medição para análise molecular
        return 0.7 + (comprimento_onda % 90) / 1000


class EquipamentoLaboratorialFactory(ABC):
    """Abstract Factory para criação de famílias de equipamentos."""
    
    @abstractmethod
    def criar_centrifuga(self) -> Centrifuga:
        """Cria uma centrífuga especializada."""
        pass
    
    @abstractmethod
    def criar_microscopio(self) -> Microscopio:
        """Cria um microscópio especializado."""
        pass
    
    @abstractmethod
    def criar_espectrofotometro(self) -> Espectrofotometro:
        """Cria um espectrofotômetro especializado."""
        pass


class GeneticaFactory(EquipamentoLaboratorialFactory):
    """Factory para equipamentos de genética."""
    
    def criar_centrifuga(self) -> Centrifuga:
        return CentrifugaGenetica()
    
    def criar_microscopio(self) -> Microscopio:
        return MicroscopioGenetico()
    
    def criar_espectrofotometro(self) -> Espectrofotometro:
        return EspectrofotometroGenetico()


class BioquimicaFactory(EquipamentoLaboratorialFactory):
    """Factory para equipamentos de bioquímica."""
    
    def criar_centrifuga(self) -> Centrifuga:
        return CentrifugaBioquimica()
    
    def criar_microscopio(self) -> Microscopio:
        return MicroscopioBioquimico()
    
    def criar_espectrofotometro(self) -> Espectrofotometro:
        return EspectrofotometroBioquimico()


class MolecularFactory(EquipamentoLaboratorialFactory):
    """Factory para equipamentos de análise molecular."""
    
    def criar_centrifuga(self) -> Centrifuga:
        return CentrifugaMolecular()
    
    def criar_microscopio(self) -> Microscopio:
        return MicroscopioMolecular()
    
    def criar_espectrofotometro(self) -> Espectrofotometro:
        return EspectrofotometroMolecular()


class FactoryProvider:
    """Provider para obter factories específicas."""
    
    @staticmethod
    def get_factory(tipo_laboratorio: str) -> EquipamentoLaboratorialFactory:
        """Retorna a factory apropriada para o tipo de laboratório."""
        if tipo_laboratorio.lower() == "genetica":
            return GeneticaFactory()
        elif tipo_laboratorio.lower() == "bioquimica":
            return BioquimicaFactory()
        elif tipo_laboratorio.lower() == "molecular":
            return MolecularFactory()
        else:
            raise ValueError(f"Tipo de laboratório não suportado: {tipo_laboratorio}")


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo: Factory cria equipamentos especializados
    print("=== Laboratório de Genética ===")
    factory_genetica = FactoryProvider.get_factory("genetica")
    centrifuga_genetica = factory_genetica.criar_centrifuga()
    microscopio_genetico = factory_genetica.criar_microscopio()
    espectrofotometro_genetico = factory_genetica.criar_espectrofotometro()
    
    print(centrifuga_genetica.centrifugar("AMOSTRA_DNA", 15000))
    print(microscopio_genetico.observar("CELULA_001"))
    print(f"Absorbância: {espectrofotometro_genetico.medir_absorbancia('AMOSTRA_DNA', 260):.3f}")
    
    print("\n=== Laboratório de Bioquímica ===")
    factory_bioquimica = FactoryProvider.get_factory("bioquimica")
    centrifuga_bioquimica = factory_bioquimica.criar_centrifuga()
    microscopio_bioquimico = factory_bioquimica.criar_microscopio()
    espectrofotometro_bioquimico = factory_bioquimica.criar_espectrofotometro()
    
    print(centrifuga_bioquimica.centrifugar("AMOSTRA_PROTEINA", 12000))
    print(microscopio_bioquimico.observar("PROTEINA_001"))
    print(f"Absorbância: {espectrofotometro_bioquimico.medir_absorbancia('AMOSTRA_PROTEINA', 280):.3f}")
