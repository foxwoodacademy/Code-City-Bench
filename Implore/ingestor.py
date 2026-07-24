import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from docx import Document
import os
import socket
from urllib.parse import urlparse

class Ingestor:
    def _is_safe_url(self, url):
        """Block local/private IP ranges (SSRF defense)."""
        try:
            domain = urlparse(url).hostname
            ip = socket.gethostbyname(domain)
            # Basic check for private/local ranges
            if ip.startswith(('127.', '192.168.', '10.', '172.')):
                return False
            return True
        except:
            return False

    def fetch_url(self, url):
        if not self._is_safe_url(url):
            raise Exception(f"Unsafe URL: {url} (Blocked by SSRF policy)")
        response = requests.get(url)
        # ...

    def read_file(self, file_path):
        """Read content from a PDF or DOCX file."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() for page in reader.pages])
        elif ext == '.docx':
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            with open(file_path, 'r') as f:
                return f.read()
