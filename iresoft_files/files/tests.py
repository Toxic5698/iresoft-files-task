from django.test import TestCase
from .models import SavedFile
from django.core.files.uploadedfile import SimpleUploadedFile


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

    def test_files_list(self):
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)

    def test_download_file(self):
        file_id = self.saved_file2.id
        response = self.client.get(f"/download/{file_id}")
        self.assertEqual(response.status_code, 200)

    def test_upload_file(self):
        file_content = b"new_file_content"
        uploaded_file = SimpleUploadedFile("new_test_file.txt", file_content)

        response = self.client.post("/upload", {"file": uploaded_file})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(SavedFile.objects.count(), 3)
        new_file = SavedFile.objects.last()
        self.assertEqual(new_file.file_name, "new_test_file.txt")
        self.assertEqual(new_file.file_size, len(file_content))
        self.assertEqual(new_file.file_type, "text/plain")

    def test_delete_file(self):
        file_id = self.saved_file1.id
        response = self.client.delete(f"/delete/{file_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SavedFile.objects.count(), 1)

    def test_get_stats(self):
        response = self.client.get("/stats/")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["files_count"], 2)
