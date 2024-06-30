import sys
import subprocess
def tryport(module_name, alias=None):
    try:
        globals()[alias or module_name] = __import__(module_name)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
        globals()[alias or module_name] = __import__(module_name)
def tryports(module_name, *symbols):
    try:
        module = __import__(module_name, fromlist=symbols)
        for symbol in symbols:
            globals()[symbol] = getattr(module, symbol)
    except ImportError:
        print(f"Module '{module_name}' is not installed or not found. Attempting to install...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
        module = __import__(module_name, fromlist=symbols)
        for symbol in symbols:
            globals()[symbol] = getattr(module, symbol)
    except AttributeError as e:
        print(f"Attribute error: {e}")
