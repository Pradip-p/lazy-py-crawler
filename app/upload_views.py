from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid

@csrf_exempt
def custom_upload_file(request):
    """
    Custom file upload handler for CKEditor 5
    Handles image uploads from the blog editor
    """
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']

        # Generate unique filename
        ext = os.path.splitext(upload.name)[1]
        filename = f"{uuid.uuid4()}{ext}"

        # Save file to media directory
        file_path = os.path.join('uploads', 'blog', filename)
        saved_path = default_storage.save(file_path, upload)

        # Generate URL
        file_url = os.path.join(settings.MEDIA_URL, saved_path)

        return JsonResponse({
            'url': file_url,
            'uploaded': 1
        })

    return JsonResponse({
        'uploaded': 0,
        'error': {
            'message': 'No file uploaded'
        }
    })
