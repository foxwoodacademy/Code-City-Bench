# modules/document_ingestion.py

import os
import tempfile
import requests
from tika import parser
import logging

class DocumentIngestionPipeline:
    """Document ingestion and entity extraction using Apache Tika."""
    
    def __init__(self, storage_dir=None):
        """Initialize the document ingestion pipeline.
        
        Args:
            storage_dir (str, optional): Directory to store processed documents.
                If None, a temporary directory will be used.
        """
        self.storage_dir = storage_dir or tempfile.mkdtemp()
        os.makedirs(self.storage_dir, exist_ok=True)
        logging.info(f"Document storage directory: {self.storage_dir}")
    
    def ingest_document(self, file_path=None, file_content=None, url=None):
        """Ingest a document from a file path, content, or URL.
        
        Args:
            file_path (str, optional): Path to the document file.
            file_content (bytes, optional): Raw content of the document.
            url (str, optional): URL to download the document from.
            
        Returns:
            dict: Extracted content and metadata.
        """
        if sum(1 for x in [file_path, file_content, url] if x is not None) != 1:
            raise ValueError("Exactly one of file_path, file_content, or url must be provided")
        
        # Handle URL download
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                file_content = response.content
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to download document from {url}: {e}")
                raise
        
        # Parse with Tika
        try:
            if file_path:
                parsed = parser.from_file(file_path)
            else:  # file_content
                parsed = parser.from_buffer(file_content)
            
            content = parsed.get('content', '').strip()
            metadata = parsed.get('metadata', {})
            
            # Store the document if it has content
            if content and file_path:
                self._store_document(file_path, content, metadata)
            
            return {
                "content": content,
                "metadata": metadata,
                "success": True
            }
            
        except Exception as e:
            logging.error(f"Failed to parse document: {e}")
            return {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
    
    def _store_document(self, original_path, content, metadata):
        """Store the processed document.
        
        Args:
            original_path (str): Original path of the document.
            content (str): Extracted text content.
            metadata (dict): Document metadata.
        """
        try:
            # Create a unique filename based on the original
            filename = os.path.basename(original_path)
            base, _ = os.path.splitext(filename)
            processed_path = os.path.join(self.storage_dir, f"{base}_processed.txt")
            
            # Store the content
            with open(processed_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Store metadata separately
            metadata_path = os.path.join(self.storage_dir, f"{base}_metadata.txt")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")
            
            logging.info(f"Document stored at {processed_path}")
            return processed_path
            
        except Exception as e:
            logging.error(f"Failed to store document: {e}")
            return None
    
    def get_document_types(self):
        """Get the list of supported document types.
        
        Returns:
            list: List of supported document extensions.
        """
        return [
            ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx",
            ".txt", ".rtf", ".html", ".htm", ".xml", ".odt", ".ods", ".odp"
        ]
    
    def extract_entities_from_content(self, content):
        """Extract entities from document content.
        This is a placeholder that would be replaced with actual NLP processing.
        
        Args:
            content (str): Document content.
            
        Returns:
            list: List of (entity, entity_type) tuples.
        """
        # This is a placeholder. In a real implementation, this would use spaCy or another NLP library.
        # For now, we'll just return some mock entities based on keywords in the content.
        entities = []
        
        # Simple keyword matching for demonstration
        if "contract" in content.lower():
            entities.append(("Contract", "DOCUMENT"))
        
        if "agreement" in content.lower():
            entities.append(("Agreement", "DOCUMENT"))
        
        # Look for potential names (very simplistic approach)
        words = content.split()
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 1 and i > 0 and words[i-1] not in ["The", "A", "An"]:
                if word not in ["I", "We", "They", "He", "She", "It"]:
                    entities.append((word, "POTENTIAL_NAME"))
        
        return entities