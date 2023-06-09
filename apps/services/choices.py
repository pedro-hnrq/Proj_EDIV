from django.db.models import TextChoices

class BudgetStatus(TextChoices):
    SOLICITADO = 'OS', 'Orçamento solicitado'
    EM_ANALISE = 'EA', 'Em análise'
    REALIZADO = 'R', 'Realizado'
    CANCELADO = 'C', 'Cancelado'
    FECHADO = 'F', 'Fechado'

class ServiceTags(TextChoices):
    MOTION = 'M', 'Motion design'
    EDICAO_IMAGEM = 'EI', 'Edicao de imagem'
    EDICAO_VIDEO = 'EV', 'Edicao de vídeo'