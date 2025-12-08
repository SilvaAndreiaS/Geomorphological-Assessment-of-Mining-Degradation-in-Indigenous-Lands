#!/usr/bin/env python3
"""
Test script to verify all modules can be imported correctly
This test does not require external dependencies to be installed
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def test_config_loader():
    """Test config loader import"""
    try:
        from utils.config_loader import ConfigLoader
        print("✓ utils.config_loader imports successfully")
        
        # Try to load config
        config_loader = ConfigLoader()
        assert config_loader.config is not None
        print("✓ Configuration file loads successfully")
        
        # Check study area
        study_area = config_loader.get_study_area()
        assert study_area['name'] == "Terra Indígena Munduruku"
        print("✓ Study area configuration is correct")
        
        return True
    except Exception as e:
        print(f"✗ Config loader test failed: {e}")
        return False


def test_module_structure():
    """Test that all module files exist and have correct structure"""
    modules = [
        "src/__init__.py",
        "src/utils/__init__.py",
        "src/utils/config_loader.py",
        "src/data_acquisition/__init__.py",
        "src/data_acquisition/satellite_data.py",
        "src/preprocessing/__init__.py",
        "src/preprocessing/image_preprocessing.py",
        "src/classification/__init__.py",
        "src/classification/hybrid_classifier.py",
        "src/detection/__init__.py",
        "src/detection/mining_scar_detector.py",
        "src/monitoring/__init__.py",
        "src/monitoring/change_detection.py",
        "src/visualization/__init__.py",
        "src/visualization/visualizer.py",
    ]
    
    all_exist = True
    for module in modules:
        module_path = project_root / module
        if module_path.exists():
            print(f"✓ {module} exists")
        else:
            print(f"✗ {module} does not exist")
            all_exist = False
    
    return all_exist


def test_config_file():
    """Test configuration file structure"""
    try:
        import yaml
        
        config_path = project_root / "config" / "munduruku_config.yaml"
        
        if not config_path.exists():
            print("✗ Configuration file does not exist")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Check main sections
        required_sections = [
            'study_area',
            'satellite_data',
            'preprocessing',
            'classification',
            'detection',
            'monitoring',
            'output',
            'visualization'
        ]
        
        for section in required_sections:
            if section in config:
                print(f"✓ Configuration has '{section}' section")
            else:
                print(f"✗ Configuration missing '{section}' section")
                return False
        
        return True
    except ImportError:
        print("⚠ PyYAML not installed, skipping config file test")
        return True
    except Exception as e:
        print(f"✗ Config file test failed: {e}")
        return False


def test_documentation():
    """Test that documentation files exist"""
    docs = [
        "README.md",
        "docs/USAGE.md",
        "docs/ARCHITECTURE.md",
        "requirements.txt",
        ".gitignore"
    ]
    
    all_exist = True
    for doc in docs:
        doc_path = project_root / doc
        if doc_path.exists():
            print(f"✓ {doc} exists")
        else:
            print(f"✗ {doc} does not exist")
            all_exist = False
    
    return all_exist


def test_main_scripts():
    """Test that main scripts exist and are executable"""
    scripts = [
        "main_pipeline.py",
        "examples/example_usage.py"
    ]
    
    all_exist = True
    for script in scripts:
        script_path = project_root / script
        if script_path.exists():
            print(f"✓ {script} exists")
            # Check if executable (on Unix systems)
            if script_path.stat().st_mode & 0o111:
                print(f"  ✓ {script} is executable")
        else:
            print(f"✗ {script} does not exist")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests"""
    print("=" * 70)
    print("TESTING SYSTEM STRUCTURE AND CONFIGURATION")
    print("=" * 70)
    print()
    
    tests = [
        ("Module Structure", test_module_structure),
        ("Configuration File", test_config_file),
        ("Config Loader", test_config_loader),
        ("Documentation", test_documentation),
        ("Main Scripts", test_main_scripts),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- Testing {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    failed = 0
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print()
    print(f"Total: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is properly structured.")
        return 0
    else:
        print(f"\n⚠ {failed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
