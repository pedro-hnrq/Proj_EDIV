from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpRequest
from .uploaded_file import ChunkUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


def request_budget(request):
    if request.method == 'GET':
        return render(request, 'request_budget.html')
    elif request.method == 'POST':
        file = request.FILES.get('file')
        print(type(file))
        if file and isinstance(file, (InMemoryUploadedFile, TemporaryUploadedFile)):
            file_upload = ChunkUploadedFile(file)
            file_upload.save_disk()
            return HttpResponse('TESTE')
        else:
            return HttpResponse('Arquivo inválido')

        