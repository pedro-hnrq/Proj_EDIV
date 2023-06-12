from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from .uploaded_file import ChunkUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from .utils import is_video
from tinymce.widgets import TinyMCE
from .choices import ServiceTags
from .models import Budgets
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.utils.safestring import mark_safe
# from django.contrib.auth.decorators import login_required



# @login_required(login_url='/auth/login/')
def request_budget(request):
    if request.method == 'GET':
        HTML_FIELD = TinyMCE().render(name='descricao', value='', attrs={'id': 'id_descricao'})
        return render(request, 'request_budget.html', {'HTML_FIELD': HTML_FIELD, 'services': ServiceTags.choices})
    
    elif request.method == 'POST':
        file = request.FILES.get('file')
        service = request.POST.get('service')
        descricao = request.POST.get('descricao')

        if not is_video(file):
            raise HttpResponseBadRequest()
        
        file_upload = ChunkUploadedFile(file)
        file_path = file_upload.save_disk()
        # TODO: Está dando erro no chamada para salvar os vídeos, na parte do client=request.user
        budget = Budgets(
            file_path=file_path,
            data=datetime.now(),
            service_tag=service,
            descricao=descricao,
            client=request.user,            
        )
        budget.save()
        # TODO: Redirecionar para a visualização do orçamento
        messages.add_message(request, constants.SUCCESS, mark_safe( 'Orçamento solicitado com sucesso. <a href="#">Clique aqui</a> para ver o status'))
        
        return redirect(reverse('request_budget'))

        