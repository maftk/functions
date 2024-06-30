import sys
import subprocess
def tryport(module_name):
    try:
        return __import__(module_name)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
        return __import__(module_name)
def tryports(module_name, *symbols):
    try:
        module = __import__(module_name, fromlist=symbols)
        return {symbol: getattr(module, symbol) for symbol in symbols}
    except ImportError:
        print(f"Module '{module_name}' is not installed or not found. Attempting to install...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
        module = __import__(module_name, fromlist=symbols)
        return {symbol: getattr(module, symbol) for symbol in symbols}
    except AttributeError as e:
        print(f"Attribute error: {e}")
        return None
