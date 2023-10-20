from django.test import TestCase
from .models import SavedFile
from django.core.files.uploadedfile import SimpleUploadedFile
from ninja import Router
import os


class FileApiTests(TestCase):
    def setUp(self):
        # Přidáme nějaké testovací soubory do databáze
        file1 = SimpleUploadedFile("test_file.txt", b"file_content")
        file2 = SimpleUploadedFile("test_file2.txt", b"file_content2")

        self.saved_file1 = SavedFile.objects.create(
            file_name="Test File 1",
            file_type="text/plain",
            file_size=len(b"file_content"),
            file=file1
        )
        self.saved_file2 = SavedFile.objects.create(
            file_name="Test File 2",
            file_type="text/plain",
            file_size=len(b"file_content2"),
            file=file2
        )

        # Inicializujeme Ninja API router pro testování
        self.router = Router()

    def test_files_list(self):
        # Vytvoříme request a zavoláme /list/ endpoint
        request = self.factory.get("/list/")
        response = self.router(request)
        self.assertEqual(response.status_code, 200)

        # Zkontrolujeme, že seznam souborů v odpovědi obsahuje všechny soubory
        response_data = response.data
        self.assertEqual(len(response_data), 2)

    def test_download_file(self):
        # Vytvoříme request a zavoláme /download/<file_id> endpoint
        file_id = self.saved_file1.id
        request = self.factory.get(f"/download/{file_id}/")
        response = self.router(request)
        self.assertEqual(response.status_code, 200)

        # Zkontrolujeme, že obsah souboru se shoduje s očekávaným obsahem
        self.assertEqual(response.content, b"file_content")

    def test_upload_file(self):
        # Vytvoříme testovací soubor pro upload
        file_content = b"new_file_content"
        uploaded_file = SimpleUploadedFile("new_test_file.txt", file_content)

        # Vytvoříme request a zavoláme /upload endpoint
        request = self.factory.post("/upload/", {"file": uploaded_file})
        response = self.router(request)
        self.assertEqual(response.status_code, 200)

        # Zkontrolujeme, že soubor byl úspěšně uploadován
        self.assertEqual(SavedFile.objects.count(), 3)
        new_file = SavedFile.objects.last()
        self.assertEqual(new_file.file_name, "new_test_file.txt")
        self.assertEqual(new_file.file_size, len(file_content))
        self.assertEqual(new_file.file_type, "text/plain")

    def test_delete_file(self):
        # Vytvoříme request a zavoláme /delete/<file_id> endpoint
        file_id = self.saved_file1.id
        request = self.factory.delete(f"/delete/{file_id}/")
        response = self.router(request)
        self.assertEqual(response.status_code, 200)

        # Zkontrolujeme, že soubor byl úspěšně smazán
        self.assertEqual(SavedFile.objects.count(), 1)

    def test_get_stats(self):
        # Vytvoříme request a zavoláme /stats/ endpoint
        request = self.factory.get("/stats/")
        response = self.router(request)
        self.assertEqual(response.status_code, 200)

        # Zkontrolujeme, že data v odpovědi odpovídají očekávání
        response_data = response.data
        self.assertEqual(response_data["files_count"], 2)
        # Zde můžete pokračovat s kontrolou dalších statistik...
