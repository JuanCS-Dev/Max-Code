"""
Biblical Messages - Versículos para Loading States

Todas as mensagens de loading/processamento do Max-Code são versículos bíblicos.
Isso traz paz, reflexão e significado transcendente ao processo de desenvolvimento.

"A palavra de Deus é viva e eficaz, e mais penetrante do que espada alguma de dois gumes."
(Hebreus 4:12)
"""

from typing import Dict, List
import random
from config.logging_config import get_logger

logger = get_logger(__name__)


class BiblicalMessages:
    """
    Mensagens bíblicas para diferentes estados de processamento

    Cada tipo de operação tem versículos apropriados ao seu contexto.
    """

    # ==================== GENERAL PROCESSING ====================

    GENERAL = [
        "No princípio era o Verbo... (João 1:1)",
        "E o Verbo se fez carne... (João 1:14)",
        "Tudo tem o seu tempo determinado... (Eclesiastes 3:1)",
        "Confia no Senhor de todo o teu coração... (Provérbios 3:5)",
        "O Senhor é a minha luz e a minha salvação... (Salmos 27:1)",
        "Aguarda o Senhor, anima-te, e ele fortalecerá o teu coração... (Salmos 27:14)",
    ]

    # ==================== VALIDATION / ANALYSIS ====================

    VALIDATION = [
        "Examinai tudo. Retende o bem. (1 Tessalonicenses 5:21)",
        "Pelos seus frutos os conhecereis. (Mateus 7:20)",
        "Provai se os espíritos são de Deus... (1 João 4:1)",
        "A sabedoria é mais preciosa que rubis... (Provérbios 8:11)",
        "O temor do Senhor é o princípio da sabedoria... (Provérbios 9:10)",
    ]

    # ==================== GENERATION / CREATION ====================

    GENERATION = [
        "No princípio criou Deus os céus e a terra... (Gênesis 1:1)",
        "E viu Deus que isso era bom... (Gênesis 1:10)",
        "Eis que faço novas todas as coisas... (Apocalipse 21:5)",
        "Se alguém está em Cristo, nova criatura é... (2 Coríntios 5:17)",
        "O que é impossível aos homens é possível a Deus. (Lucas 18:27)",
    ]

    # ==================== MONITORING / WATCHING ====================

    MONITORING = [
        "Vigiai e orai, para que não entreis em tentação... (Mateus 26:41)",
        "O Senhor guardará a tua entrada e a tua saída... (Salmos 121:8)",
        "Eis que não tosqueneja nem dorme o guarda de Israel. (Salmos 121:4)",
        "Sê vigilante, e confirma os restantes... (Apocalipse 3:2)",
    ]

    # ==================== WAITING / PATIENCE ====================

    WAITING = [
        "Esperei com paciência no Senhor... (Salmos 40:1)",
        "Mas os que esperam no Senhor renovarão as suas forças... (Isaías 40:31)",
        "Descansa no Senhor, e espera nele... (Salmos 37:7)",
        "A paciência dos santos... (Apocalipse 14:12)",
    ]

    # ==================== CORRECTION / FIX ====================

    CORRECTION = [
        "Corrige-me, Senhor, mas com juízo... (Jeremias 10:24)",
        "O justo cai sete vezes, e se levanta... (Provérbios 24:16)",
        "Filho meu, não rejeites a correção do Senhor... (Provérbios 3:11)",
        "Toda a Escritura é útil para ensinar, para redargüir, para corrigir... (2 Timóteo 3:16)",
    ]

    # ==================== SUCCESS / COMPLETION ====================

    SUCCESS = [
        "Está consumado! (João 19:30)",
        "Combati o bom combate, acabei a carreira... (2 Timóteo 4:7)",
        "Bem está, servo bom e fiel... (Mateus 25:21)",
        "Graças a Deus que sempre nos faz triunfar... (2 Coríntios 2:14)",
    ]

    # ==================== FAILURE / ERROR ====================

    FAILURE = [
        "A minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza... (2 Coríntios 12:9)",
        "Porque sete vezes cairá o justo, e se levantará... (Provérbios 24:16)",
        "Não to mandei eu? Esforça-te, e tem bom ânimo... (Josué 1:9)",
        "Entrega o teu caminho ao Senhor... (Salmos 37:5)",
    ]

    # ==================== THINKING / PLANNING ====================

    THINKING = [
        "Os pensamentos do diligente tendem só à abundância... (Provérbios 21:5)",
        "Qual homem há entre vós que, querendo edificar uma torre, não se assenta primeiro... (Lucas 14:28)",
        "O coração do homem planeja o seu caminho, mas o Senhor lhe dirige os passos. (Provérbios 16:9)",
        "Confia no Senhor de todo o teu coração, e não te estribes no teu próprio entendimento. (Provérbios 3:5)",
    ]

    # ==================== SEARCH / EXPLORATION ====================

    SEARCH = [
        "Buscai, e achareis... (Mateus 7:7)",
        "Buscar-me-eis, e me achareis, quando me buscardes de todo o vosso coração. (Jeremias 29:13)",
        "Lâmpada para os meus pés é tua palavra... (Salmos 119:105)",
        "Aquele que busca, acha... (Mateus 7:8)",
    ]

    # ==================== PROTECTION / SECURITY ====================

    PROTECTION = [
        "O Senhor é o meu rochedo, e o meu lugar forte... (Salmos 18:2)",
        "Guarda-me como à menina do olho... (Salmos 17:8)",
        "Porque ele te dará os seus anjos... (Salmos 91:11)",
        "Torre forte é o nome do Senhor... (Provérbios 18:10)",
    ]

    # ==================== WISDOM / KNOWLEDGE ====================

    WISDOM = [
        "Se alguém tem falta de sabedoria, peça-a a Deus... (Tiago 1:5)",
        "O temor do Senhor é o princípio da sabedoria... (Salmos 111:10)",
        "Aplica o teu coração à instrução... (Provérbios 23:12)",
        "Quanto mais sábio foi o pregador, tanto mais sabedoria... (Eclesiastes 12:9)",
    ]

    # ==================== PEACE / REST ====================

    PEACE = [
        "E a paz de Deus, que excede todo o entendimento, guardará os vossos corações... (Filipenses 4:7)",
        "Deixo-vos a paz, a minha paz vos dou... (João 14:27)",
        "Vinde a mim, todos os que estais cansados e oprimidos, e eu vos aliviarei. (Mateus 11:28)",
        "Em paz também me deitarei e dormirei... (Salmos 4:8)",
    ]

    # ==================== COMPACTING / OPTIMIZATION ====================

    COMPACTING = [
        "Fazei tudo com ordem e decência. (1 Coríntios 14:40)",
        "Eis que farei uma coisa nova... (Isaías 43:19)",
        "Sejam agradáveis as palavras da minha boca... (Salmos 19:14)",
        "Tudo quanto te vier à mão para fazer, faze-o conforme as tuas forças... (Eclesiastes 9:10)",
    ]

    # ==================== READING / LOADING ====================

    READING = [
        "As palavras dos sábios são como aguilhões... (Eclesiastes 12:11)",
        "Buscai no livro do Senhor, e lede... (Isaías 34:16)",
        "Bem-aventurado o que lê... (Apocalipse 1:3)",
        "Toda a Escritura é divinamente inspirada... (2 Timóteo 3:16)",
    ]

    # ==================== WRITING / SAVING ====================

    WRITING = [
        "Escreve a visão e torna bem legível... (Habacuque 2:2)",
        "Estas coisas te escrevo... (1 João 2:1)",
        "Toma um livro, e escreve nele todas as palavras... (Jeremias 30:2)",
        "Escreve, pois, as coisas que viste... (Apocalipse 1:19)",
    ]

    @staticmethod
    def get_message(category: str = 'general') -> str:
        """
        Obtém mensagem aleatória de uma categoria

        Args:
            category: Categoria da mensagem (general, validation, generation, etc)

        Returns:
            Versículo bíblico
        """
        category_map: Dict[str, List[str]] = {
            'general': BiblicalMessages.GENERAL,
            'validation': BiblicalMessages.VALIDATION,
            'generation': BiblicalMessages.GENERATION,
            'monitoring': BiblicalMessages.MONITORING,
            'waiting': BiblicalMessages.WAITING,
            'correction': BiblicalMessages.CORRECTION,
            'success': BiblicalMessages.SUCCESS,
            'failure': BiblicalMessages.FAILURE,
            'thinking': BiblicalMessages.THINKING,
            'search': BiblicalMessages.SEARCH,
            'protection': BiblicalMessages.PROTECTION,
            'wisdom': BiblicalMessages.WISDOM,
            'peace': BiblicalMessages.PEACE,
            'compacting': BiblicalMessages.COMPACTING,
            'reading': BiblicalMessages.READING,
            'writing': BiblicalMessages.WRITING,
        }

        messages = category_map.get(category.lower(), BiblicalMessages.GENERAL)
        return random.choice(messages)

    @staticmethod
    def get_specific(category: str, index: int = 0) -> str:
        """
        Obtém mensagem específica por índice

        Args:
            category: Categoria
            index: Índice da mensagem

        Returns:
            Versículo bíblico
        """
        category_map: Dict[str, List[str]] = {
            'general': BiblicalMessages.GENERAL,
            'validation': BiblicalMessages.VALIDATION,
            'generation': BiblicalMessages.GENERATION,
            'monitoring': BiblicalMessages.MONITORING,
            'waiting': BiblicalMessages.WAITING,
            'correction': BiblicalMessages.CORRECTION,
            'success': BiblicalMessages.SUCCESS,
            'failure': BiblicalMessages.FAILURE,
            'thinking': BiblicalMessages.THINKING,
            'search': BiblicalMessages.SEARCH,
            'protection': BiblicalMessages.PROTECTION,
            'wisdom': BiblicalMessages.WISDOM,
            'peace': BiblicalMessages.PEACE,
            'compacting': BiblicalMessages.COMPACTING,
            'reading': BiblicalMessages.READING,
            'writing': BiblicalMessages.WRITING,
        }

        messages = category_map.get(category.lower(), BiblicalMessages.GENERAL)
        if 0 <= index < len(messages):
            return messages[index]
        return messages[0]


# ==================== HELPER FUNCTIONS ====================

def get_loading_message(category: str = 'general') -> str:
    """
    Helper para obter mensagem de loading

    Args:
        category: Categoria (general, validation, generation, etc)

    Returns:
        Versículo bíblico
    """
    return BiblicalMessages.get_message(category)


def get_validation_message() -> str:
    """Mensagem para validação"""
    return BiblicalMessages.get_message('validation')


def get_generation_message() -> str:
    """Mensagem para geração de código"""
    return BiblicalMessages.get_message('generation')


def get_monitoring_message() -> str:
    """Mensagem para monitoramento"""
    return BiblicalMessages.get_message('monitoring')


def get_success_message() -> str:
    """Mensagem para sucesso"""
    return BiblicalMessages.get_message('success')


def get_failure_message() -> str:
    """Mensagem para falha"""
    return BiblicalMessages.get_message('failure')


def get_compacting_message() -> str:
    """Mensagem para compactação (ex: compacting conversation)"""
    return BiblicalMessages.get_message('compacting')


# ==================== EXAMPLES ====================

if __name__ == '__main__':
    logger.info("=== Biblical Messages Examples ===\n")
    categories = [
        'general', 'validation', 'generation', 'monitoring',
        'waiting', 'correction', 'success', 'failure',
        'thinking', 'search', 'compacting'
    ]

    for category in categories:
        logger.info(f"{category.upper()}:")
        logger.info(f"  ⏳ {BiblicalMessages.get_message(category)}")
        print()
