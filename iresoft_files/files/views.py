import datetime
from statistics import median
from typing import List, Optional

from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from hurry.filesize import size
from ninja import NinjaAPI, Schema, File, FilterSchema, Query
from ninja.files import UploadedFile
from ninja.pagination import paginate, PageNumberPagination

from .models import SavedFile

api = NinjaAPI(
    title="iresoft files task",
    description="docs available here: https://github.com/Toxic5698/iresoft-files-task"
)


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


@api.get("", response=List[FileSchemaOut])
@paginate(PageNumberPagination)
def files_list(request, filters: FileSchemaFilter = Query(...), **kwargs):
    queryset = SavedFile.objects.all()
    files = filters.filter(queryset)
    return list(files)


@api.get("download/{file_id}")
def download_file(request, file_id: int):
    file = get_object_or_404(SavedFile, id=file_id)
    response = FileResponse(open(file.file.path, 'rb'))
    return response


@api.post("upload")
def upload_file(request, file: UploadedFile = File(...)):
    new_file = SavedFile.objects.create(
        file_name=file.name,
        file_size=file.size,
        file_type=file.content_type,
        file=file
    )
    return {'successfully_uploaded': new_file.file_name}


@api.delete("delete/{file_id}")
def delete_file(request, file_id: int):
    file = get_object_or_404(SavedFile, id=file_id)
    file.delete()
    return {"successfully_deleted": file.file_name}


@api.get("stats/")
def get_stats(request):
    all_sizes = list(SavedFile.objects.all().values_list("file_size", flat=True))
    stats = {
        "files_count": len(all_sizes),
        "total_size": size(sum(all_sizes)),
        "average_size": size(sum(all_sizes) / len(all_sizes)),
        "median_size": size(median(all_sizes)),
        "biggest_file": size(max(all_sizes)),
        "smallest_file": size(min(all_sizes))
    }
    return stats
