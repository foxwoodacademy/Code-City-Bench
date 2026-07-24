#!/usr/bin/env python3
"""
DocGenius - Automated Documentation Generation Service
AI system that generates and maintains up-to-date documentation from code

Status: STUB (Initial implementation - needs expansion)
"""

import os
import ast
from typing import Dict, List, Optional, Tuple
import json
from dataclasses import dataclass

@dataclass
class DocumentationElement:
    """Represents a documentation element"""
    element_type: str  # "module", "class", "function", "method"
    name: str
    docstring: str
    parameters: List[Dict]
    return_type: Optional[str]
    return_description: Optional[str]
    examples: List[str]
    related_elements: List[str]

class DocGeniusEngine:
    """Main documentation generation engine"""
    
    def __init__(self):
        self.documentation_db = {}
        self.template_engine = DocumentationTemplateEngine()
    
    def extract_documentation(self, file_path: str) -> List[DocumentationElement]:
        """Extract documentation from a Python file"""
        elements = []
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                tree = ast.parse(content)
            
            # Analyze AST to extract documentation elements
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    elements.append(self._process_class(node))
                elif isinstance(node, ast.FunctionDef):
                    elements.append(self._process_function(node))
                elif isinstance(node, ast.AsyncFunctionDef):
                    elements.append(self._process_async_function(node))
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return elements
    
    def _process_class(self, node: ast.ClassDef) -> DocumentationElement:
        """Process a class definition"""
        docstring = ast.get_docstring(node) or ""
        
        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        return DocumentationElement(
            element_type="class",
            name=node.name,
            docstring=docstring,
            parameters=[],
            return_type=None,
            return_description=None,
            examples=[],
            related_elements=methods
        )
    
    def _process_function(self, node: ast.FunctionDef) -> DocumentationElement:
        """Process a function definition"""
        docstring = ast.get_docstring(node) or ""
        
        # Extract parameters
        parameters = []
        for arg in node.args.args:
            parameters.append({
                "name": arg.arg,
                "type": "any",  # TODO: Extract type hints
                "description": ""
            })
        
        # Extract return type and description from docstring
        return_type = None
        return_description = None
        
        if docstring:
            lines = docstring.split('\n')
            for line in lines:
                if line.strip().lower().startswith("returns:"):
                    return_description = line.strip()[8:].strip()
                elif line.strip().lower().startswith("rtype:"):
                    return_type = line.strip()[7:].strip()
        
        return DocumentationElement(
            element_type="function",
            name=node.name,
            docstring=docstring,
            parameters=parameters,
            return_type=return_type,
            return_description=return_description,
            examples=[],
            related_elements=[]
        )
    
    def _process_async_function(self, node: ast.AsyncFunctionDef) -> DocumentationElement:
        """Process an async function definition"""
        func_doc = self._process_function(node)
        func_doc.element_type = "async_function"
        return func_doc
    
    def generate_documentation(self, elements: List[DocumentationElement], output_format: str = "markdown") -> str:
        """Generate documentation from extracted elements"""
        return self.template_engine.render(elements, output_format)
    
    def update_documentation(self, source_dir: str, output_dir: str):
        """Scan directory and generate/update documentation"""
        all_elements = []
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, source_dir)
                    output_path = os.path.join(output_dir, relative_path).replace('.py', '.md')
                    
                    elements = self.extract_documentation(file_path)
                    all_elements.extend(elements)
                    
                    # Create output directory if needed
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    # Generate documentation file
                    with open(output_path, 'w') as f:
                        f.write(self.generate_documentation(elements))
        
        return all_elements

class DocumentationTemplateEngine:
    """Handles documentation template rendering"""
    
    def render(self, elements: List[DocumentationElement], output_format: str = "markdown") -> str:
        """Render documentation elements using templates"""
        if output_format == "markdown":
            return self._render_markdown(elements)
        elif output_format == "json":
            return json.dumps([self._element_to_dict(el) for el in elements], indent=2)
        
        return "Unsupported output format"
    
    def _render_markdown(self, elements: List[DocumentationElement]) -> str:
        """Render elements as Markdown"""
        output = []
        
        for element in elements:
            if element.element_type == "module":
                output.append(f"# {element.name}\n\n{element.docstring}\n")
            elif element.element_type == "class":
                output.append(f"## Class: {element.name}\n\n{element.docstring}\n")
                if element.related_elements:
                    output.append("### Methods\n")
                    for method in element.related_elements:
                        output.append(f"- `{method}`\n")
            elif element.element_type in ["function", "async_function", "method"]:
                async_prefix = "async " if element.element_type == "async_function" else ""
                output.append(f"### {async_prefix}Function: {element.name}\n\n")
                output.append(f"```python\n{element.name}({', '.join(p['name'] for p in element.parameters)})\n```\n\n")
                output.append(f"{element.docstring}\n")
                
                if element.parameters:
                    output.append("#### Parameters\n")
                    for param in element.parameters:
                        output.append(f"- `{param['name']}` ({param['type']}): {param['description']}\n")
                
                if element.return_type or element.return_description:
                    output.append("#### Returns\n")
                    if element.return_type:
                        output.append(f"- **Type**: `{element.return_type}`\n")
                    if element.return_description:
                        output.append(f"- **Description**: {element.return_description}\n")
        
        return '\n'.join(output)
    
    def _element_to_dict(self, element: DocumentationElement) -> Dict:
        """Convert element to dictionary for JSON output"""
        return {
            "type": element.element_type,
            "name": element.name,
            "docstring": element.docstring,
            "parameters": element.parameters,
            "return_type": element.return_type,
            "return_description": element.return_description,
            "examples": element.examples,
            "related_elements": element.related_elements
        }

# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DocGenius - Automated Documentation Generation")
    parser.add_argument("source", help="Source file or directory")
    parser.add_argument("--output", help="Output file or directory")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    
    args = parser.parse_args()
    
    engine = DocGeniusEngine()
    
    if os.path.isfile(args.source):
        if not args.output:
            args.output = args.source.replace('.py', '.md')
        
        elements = engine.extract_documentation(args.source)
        documentation = engine.generate_documentation(elements, args.format)
        
        with open(args.output, 'w') as f:
            f.write(documentation)
        
        print(f"Documentation generated: {args.output}")
    elif os.path.isdir(args.source):
        if not args.output:
            args.output = os.path.join(args.source, "docs")
        
        os.makedirs(args.output, exist_ok=True)
        elements = engine.update_documentation(args.source, args.output)
        
        print(f"Documentation generated for {len(elements)} elements in {args.output}")
    else:
        print(f"Error: Path {args.source} does not exist")
        exit(1)