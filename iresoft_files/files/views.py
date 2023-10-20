import datetime

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema, File, FilterSchema, Query
from ninja.pagination import paginate, PageNumberPagination
from ninja.files import UploadedFile
from typing import List, Optional

from .models import SavedFile

from django.core.files.storage import FileSystemStorage

STORAGE = FileSystemStorage()

api = NinjaAPI()


class FileSchemaOut(Schema):
    id: int
    file_name: str
    file_type: str
    file_size: int
    added_at: datetime.datetime


class FileSchemaFilter(FilterSchema):
    file_name: Optional[str]
    file_type: Optional[str]
    file_size: Optional[int]
    added_at: Optional[datetime.datetime]


@api.get("/", response=List[FileSchemaOut])
@paginate
def files_list(request, filters: FileSchemaFilter = Query(...), **kwargs):
    queryset = SavedFile.objects.all()
    files = filters.filter(queryset)
    return files


@api.get("/{file_id}")
def download_file(request, file_id: int):
    file = get_object_or_404(SavedFile, id=file_id)
    filename = file.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


@api.post("")
def upload_file(request, file: UploadedFile = File(...)):
    new_file = SavedFile.objects.create(
        file_name=file.name,
        file_size=file.size,
        file_type=file.content_type,
        file=file
    )
    return {'successfully_uploaded': new_file.file_name}


@api.delete("/{file_id}")
def delete_file(request, file_id: int):
    file = get_object_or_404(SavedFile, id=file_id)
    file.delete()
    return {"successfully_deleted": file.file_name}

@api.get("/stats")
def get_stats(request):
    all_files = SavedFile.objects.all()
    all_sizes = all_files.values("file_size")
    stats = {
        # "total_size":
        # "average_size":
        # "median_size":
        "files_count": all_files.count()
    }
    return stats
