import os
import sys

def reset_init_files():
    """Verwijdert en maakt __init__.py bestanden opnieuw aan."""
    folders = [
        "code",
        "code/algorithms",
        "code/classes",
        "code/utils",
        "data/Nationaal"
    ]
    
    # Verwijder alle bestaande __init__.py bestanden
    for folder in folders:
        init_path = os.path.join(folder, "__init__.py")
        if os.path.exists(init_path):
            os.remove(init_path)
        
    # Voeg __init__.py bestanden opnieuw toe
    for folder in folders:
        open(os.path.join(folder, "__init__.py"), "w").close()
    
    print("Alle __init__.py bestanden opnieuw ingesteld.")

def clear_pycache():
    """Verwijdert __pycache__ en .pyc bestanden."""
    os.system("find . -name '__pycache__' -type d -exec rm -r {} +")
    os.system("find . -name '*.pyc' -delete")
    print("Cache bestanden verwijderd.")

def fix_pythonpath():
    """Voegt de code map toe aan PYTHONPATH als deze ontbreekt."""
    code_path = os.path.abspath("code")
    if code_path not in sys.path:
        sys.path.append(code_path)
        print(f"Toegevoegd aan sys.path: {code_path}")
    else:
        print("code/ al aanwezig in sys.path")

def test_imports():
    """Test of imports correct werken."""
    try:
        import algorithms.greedy_selector
        import classes.station
        import utils.helper
        print("Alle imports werken correct!")
    except ModuleNotFoundError as e:
        print(f"Import error: {e}")

if __name__ == "__main__":
    reset_init_files()
    clear_pycache()
    fix_pythonpath()
    test_imports()