from django.contrib.auth.models import User
from django.db.models import Model, CharField, FileField, DateTimeField, IntegerField


def file_directory_path(instance, file):
    return f"uploaded_files/{instance.file_name} - {file}"


class SavedFile(Model):
    file_name = CharField(max_length=255, blank=True, null=True, verbose_name="Název souboru")
    file_type = CharField(max_length=255, blank=True, null=True, verbose_name="Typ souboru")
    file_size = IntegerField(blank=True, null=True, verbose_name="Velikost souboru")
    file = FileField(upload_to=file_directory_path, blank=True, null=True, verbose_name="Soubor")
    added_at = DateTimeField(auto_now_add=True, verbose_name="Čas nahrání")

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self):
        return self.file_name

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(SavedFile, self).delete(*args, **kwargs)
