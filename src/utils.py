"""Utility functions for file operations and text processing."""

import json
from typing import List, Dict, Any
from pathlib import Path


def read_text_file(file_path: str, encoding: str = 'utf-8') -> str:
    """Read text from a file.
    
    Args:
        file_path (str): Path to the text file.
        encoding (str): File encoding. Defaults to 'utf-8'.
        
    Returns:
        str: Content of the file.
        
    Raises:
        FileNotFoundError: If file does not exist.
        IOError: If file cannot be read.
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")


def write_text_file(file_path: str, content: str, encoding: str = 'utf-8') -> None:
    """Write text to a file.
    
    Args:
        file_path (str): Path to the output file.
        content (str): Content to write.
        encoding (str): File encoding. Defaults to 'utf-8'.
        
    Raises:
        IOError: If file cannot be written.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file {file_path}: {e}")


def read_json_file(file_path: str) -> Dict[str, Any]:
    """Read JSON from a file.
    
    Args:
        file_path (str): Path to the JSON file.
        
    Returns:
        Dict[str, Any]: Parsed JSON content.
        
    Raises:
        FileNotFoundError: If file does not exist.
        json.JSONDecodeError: If JSON is invalid.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}", e.doc, e.pos)


def write_json_file(file_path: str, data: Dict[str, Any], indent: int = 2) -> None:
    """Write data to a JSON file.
    
    Args:
        file_path (str): Path to the output JSON file.
        data (Dict[str, Any]): Data to serialize.
        indent (int): JSON indentation level. Defaults to 2.
        
    Raises:
        IOError: If file cannot be written.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"Error writing to file {file_path}: {e}")


def batch_read_files(directory: str, extension: str = '.txt') -> Dict[str, str]:
    """Read multiple files from a directory.
    
    Args:
        directory (str): Path to the directory.
        extension (str): File extension to filter. Defaults to '.txt'.
        
    Returns:
        Dict[str, str]: Dictionary mapping filenames to file contents.
    """
    files_content = {}
    try:
        path = Path(directory)
        for file_path in path.glob(f"*{extension}"):
            files_content[file_path.name] = read_text_file(str(file_path))
    except Exception as e:
        raise IOError(f"Error reading files from {directory}: {e}")
    
    return files_content


def format_results(results: List[Dict[str, Any]], format_type: str = 'json') -> str:
    """Format results for output.
    
    Args:
        results (List[Dict[str, Any]]): Results to format.
        format_type (str): Output format ('json', 'csv', 'text'). Defaults to 'json'.
        
    Returns:
        str: Formatted output.
    """
    if format_type == 'json':
        return json.dumps(results, indent=2, ensure_ascii=False)
    elif format_type == 'csv':
        if not results:
            return ''
        keys = results[0].keys()
        lines = [','.join(keys)]
        for result in results:
            lines.append(','.join(str(result.get(k, '')) for k in keys))
        return '\n'.join(lines)
    elif format_type == 'text':
        lines = []
        for i, result in enumerate(results, 1):
            lines.append(f"Result {i}:")
            for key, value in result.items():
                lines.append(f"  {key}: {value}")
        return '\n'.join(lines)
    else:
        raise ValueError(f"Unknown format type: {format_type}")
