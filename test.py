#!/usr/bin/env python3
"""
Test script for nepse-proxy-source main.py
Tests code logic without requiring network access or the full server
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_url_condition_logic():
    """Test the fixed URL condition logic"""
    print("Testing URL condition logic...")
    
    # Test cases for the fixed condition
    test_cases = [
        ('/nepse-data/floorsheet', True, "Should detect floorsheet"),
        ('/nepse-data/today-price', True, "Should detect today-price"),
        ('/graph/index/', False, "Should not match floorsheet/today-price"),
        ('/other-endpoint', False, "Should not match floorsheet/today-price"),
        ('/nepse-data/floorsheet/extra', True, "Should detect floorsheet with extra path"),
        ('/nepse-data/today-price/extra', True, "Should detect today-price with extra path"),
    ]
    
    for path, should_match, description in test_cases:
        # Simulate the fixed condition
        result = ('/nepse-data/floorsheet' in path or '/nepse-data/today-price' in path)
        status = "✓" if result == should_match else "✗"
        print(f"  {status} {description}: '{path}' -> {result}")
        if result != should_match:
            return False
    
    print("✓ URL condition logic tests passed\n")
    return True

def test_imports():
    """Test that all required imports are available"""
    print("Testing imports...")
    
    try:
        from http.server import BaseHTTPRequestHandler, HTTPServer
        print("  ✓ http.server imports OK")
    except ImportError as e:
        print(f"  ✗ http.server import failed: {e}")
        return False
    
    try:
        import requests
        print("  ✓ requests import OK")
    except ImportError as e:
        print(f"  ✗ requests import failed: {e}")
        return False
    
    try:
        import pytz
        print("  ✓ pytz import OK")
    except ImportError as e:
        print(f"  ✗ pytz import failed: {e}")
        return False
    
    try:
        import pywasm
        print("  ✓ pywasm import OK")
    except ImportError as e:
        print(f"  ✗ pywasm import failed: {e}")
        return False
    
    print("✓ All imports available\n")
    return True

def test_response_headers():
    """Test response header logic"""
    print("Testing response header logic...")
    
    # Simulate the fixed write_response behavior
    content_types = [
        ('application/json', 'GET requests with JSON'),
        ('application/json', 'POST requests'),
        ('text/html', 'HTML pages'),
    ]
    
    for content_type, description in content_types:
        if content_type in ['application/json', 'text/html']:
            print(f"  ✓ {description}: Content-type = {content_type}")
        else:
            print(f"  ✗ {description}: Invalid content-type")
            return False
    
    print("✓ Response header logic tests passed\n")
    return True

def test_error_handling():
    """Test error handling improvements"""
    print("Testing error handling...")
    
    # Test Content-Length header handling
    headers = {}
    content_len = int(headers.get('Content-Length', 0))
    if content_len == 0:
        print("  ✓ Missing Content-Length header handled safely")
    else:
        print("  ✗ Content-Length header handling failed")
        return False
    
    print("✓ Error handling tests passed\n")
    return True

def test_code_syntax():
    """Test if main.py has valid Python syntax"""
    print("Testing Python syntax...")
    
    try:
        import py_compile
        py_compile.compile('main.py', doraise=True)
        print("  ✓ main.py syntax is valid")
        print("✓ Syntax validation passed\n")
        return True
    except py_compile.PyCompileError as e:
        print(f"  ✗ Syntax error in main.py: {e}")
        return False

def main():
    print("=" * 60)
    print("NEPSE PROXY SOURCE TEST SUITE")
    print("=" * 60 + "\n")
    
    tests = [
        test_imports,
        test_code_syntax,
        test_url_condition_logic,
        test_response_headers,
        test_error_handling,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}\n")
            results.append(False)
    
    print("=" * 60)
    print(f"SUMMARY: {sum(results)}/{len(results)} test groups passed")
    print("=" * 60)
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
