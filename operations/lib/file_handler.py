import os
import zipfile
from django.conf import settings
import datetime
from django import http
from django.core.files import File
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import StringIO

from django.template.loader import get_template
from django.template import Context

from operations.models import Document

def zip_generated_files(file_list=[]):
    if not len(file_list) > 0:
        # create pdfs for testing
        x = 1
        while x < 3:
            filename = '%s_sample_%s.pdf' % (x,str(uuid.uuid4())[:5])
            file_list.append(filename)
            write_save_pdf('pdf_sample.html',{}, filename)
            x +=1


    zip_location = '/tmp/Python_%s.zip' % str(uuid.uuid4())[:5]


    zip = zipfile.ZipFile(zip_location, 'a')
    for file_name in file_list:
        location = "/tmp/%s"%file_name
        if os.path.exists(location):

            zip.write(location, os.path.basename(location))
            os.remove(location)
    zip.close()
    upload_file = UploadFile.objects.create(model_type="ZIP",
                                            description="Upoaded zip file",
                                            created_at=datetime.datetime.now())

    upload_file.file_name = File(open(zip_location, 'rd'))
    upload_file.save()
    os.remove(zip_location)

def file_download(file, document=None, content_type='application/force-download'):
    document = document or file.document.name
    response =  response = HttpResponse(open(settings.MEDIA_ROOT + "/" + document),
                            content_type=content_type)

    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(document)
    return response

def save_file(user, name, file_path, file_type="Download", description=None):    
    upload_file = Document.objects.create(file_type=file_type,
                                            description=description,
                                            created_at=datetime.datetime.now(),
                                            created_by=user)
    upload_file.document_name = name
    upload_file.document.name = 'uploads/documents/%s' % name
    upload_file.save()
    return upload_file
