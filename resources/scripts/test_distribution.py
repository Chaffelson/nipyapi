#!/usr/bin/env python3
"""
Distribution validation script for nipyapi.

Tests that a built wheel/sdist can be installed and imported in a clean environment.
This should be run as part of the release process to ensure the packaged distribution
actually works before publishing to PyPI.

Usage:
    python resources/scripts/test_distribution.py
    
Or via make:
    make test-dist
"""
import tempfile
import subprocess
import sys
import os
import glob

def validate_distribution():
    """Test that the built wheel can be imported and used in a clean environment."""
    
    # Find wheel file
    wheels = glob.glob('dist/*.whl')
    if not wheels:
        print("❌ No wheel found in dist/ directory")
        print("Run 'make dist' first to build distribution")
        return False
        
    wheel_file = wheels[0]
    wheel_name = os.path.basename(wheel_file)

    # A build without git tags (e.g. a shallow clone) falls back to 0.0.x
    # instead of the real release version; refuse to validate it.
    wheel_version = wheel_name.split('-')[1]
    if wheel_version.startswith('0.0.') or 'unknown' in wheel_version:
        print(f"❌ Wheel has a fallback version: {wheel_version}")
        print("Build from a checkout with git tags (e.g. fetch-depth: 0 in CI)")
        return False

    print(f"🧪 Testing distribution: {wheel_name}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = os.path.join(tmpdir, 'test_env')
        
        print("📦 Creating clean virtual environment...")
        try:
            subprocess.run([
                sys.executable, '-m', 'venv', venv_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
            
        # Set up paths for the virtual environment
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(venv_path, 'Scripts', 'pip')
            python_path = os.path.join(venv_path, 'Scripts', 'python')
        else:  # Unix/Linux/macOS
            pip_path = os.path.join(venv_path, 'bin', 'pip')
            python_path = os.path.join(venv_path, 'bin', 'python')
            
        print(f"📥 Installing wheel: {wheel_name}")
        try:
            subprocess.run([
                pip_path, 'install', wheel_file
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install wheel: {e}")
            return False
            
        print("🔍 Testing imports and basic functionality...")
        
        test_script = '''
import sys
try:
    print("=== Import Tests ===")
    
    # Test main import
    import nipyapi
    print(f"✅ nipyapi imported: {nipyapi.__version__}")
    
    # Test core modules
    import nipyapi.canvas
    import nipyapi.security  
    import nipyapi.utils
    print("✅ Core modules imported successfully")
    
    # Test generated API clients
    import nipyapi.nifi
    import nipyapi.registry
    print("✅ Generated API clients imported successfully")
    
    # Test basic functionality
    test_data = {"test": "data", "numbers": [1, 2, 3]}
    yaml_output = nipyapi.utils.dump(test_data, mode="yaml")
    json_output = nipyapi.utils.dump(test_data, mode="json")
    
    # Test round-trip
    loaded_yaml = nipyapi.utils.load(yaml_output)
    loaded_json = nipyapi.utils.load(json_output)
    
    if loaded_yaml == test_data and loaded_json == test_data:
        print("✅ YAML/JSON round-trip functionality works")
    else:
        print("❌ YAML/JSON round-trip failed")
        sys.exit(1)
        
    print("✅ All import and functionality tests passed!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                python_path, '-c', test_script
            ], capture_output=True, text=True, timeout=30)
            
            print(result.stdout)
            
            if result.stderr:
                print(f"STDERR: {result.stderr}")
                
            if result.returncode != 0:
                print("❌ Import tests failed!")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Test timed out after 30 seconds")
            return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Test execution failed: {e}")
            return False
            
    print("🎉 Distribution validation successful!")
    print("The built wheel can be installed and imported correctly.")
    return True

if __name__ == "__main__":
    success = validate_distribution()
    sys.exit(0 if success else 1)
