"""Run before main.py: preserve startup output and keep the console open."""
import atexit
import faulthandler
import os
from pathlib import Path
import sys
import tempfile
import threading
from datetime import datetime

# Reproduce live server behaviour, not the local dummy-data environment.
os.environ['APP_ENV'] = 'production'

_log = None
_lock = threading.RLock()
_name = 'startup-{}-{}.log'.format(
    datetime.now().strftime('%Y%m%d-%H%M%S'), os.getpid())
_roots = [Path(os.environ.get('LOCALAPPDATA') or Path.home()),
          Path(tempfile.gettempdir())]
for _root in _roots:
    try:
        _folder = _root / 'ManageMeStock-Diagnostic' / 'logs'
        _folder.mkdir(parents=True, exist_ok=True)
        _log_path = _folder / _name
        _log = _log_path.open('a', encoding='utf-8', buffering=1)
        break
    except OSError:
        continue


class _Tee:
    def __init__(self, stream):
        self.stream = stream

    def write(self, text):
        with _lock:
            if self.stream is not None:
                try:
                    self.stream.write(text)
                    self.stream.flush()
                except (OSError, ValueError):
                    pass
            if _log is not None:
                try:
                    _log.write(text)
                    _log.flush()
                except (OSError, ValueError):
                    pass
        return len(text)

    def flush(self):
        for stream in (self.stream, _log):
            if stream is not None:
                try:
                    stream.flush()
                except (OSError, ValueError):
                    pass

    def __getattr__(self, name):
        return getattr(self.stream, name)


sys.stdout = _Tee(sys.stdout)
sys.stderr = _Tee(sys.stderr)
if _log is not None:
    try:
        faulthandler.enable(file=_log, all_threads=True)
    except (OSError, RuntimeError):
        pass

print('ManageMeStock-Diagnostic')
print('PRODUCTION configuration: this app can access and change LIVE data.')
print('Started:', datetime.now().isoformat())
print('Python:', sys.version)
print('Executable:', sys.executable)
print('Working directory:', os.getcwd())
print('Log:', str(_log_path) if _log is not None else 'Unable to create log')


def _finish():
    print('\nApplication exited. Review the output above and the log file.')
    try:
        input('Press Enter to close this diagnostic console...')
    except (EOFError, OSError, RuntimeError):
        pass
    sys.stdout.flush()
    sys.stderr.flush()


atexit.register(_finish)


# Diagnostic-only graphics trial. Set before Qt is imported or initialized.
os.environ['QT_DEBUG_PLUGINS'] = '1'
os.environ['QT_OPENGL'] = 'software'
print('Qt diagnostic hook v2: plugin logging enabled; software OpenGL requested.')
print('Loading QtCore...', flush=True)
from PyQt5 import QtCore


def _qt_message(message_type, context, message):
    # Use Python output so the existing tee also saves native Qt messages.
    try:
        print('[Qt {}] {}'.format(int(message_type), message), flush=True)
    except Exception:
        pass


QtCore.qInstallMessageHandler(_qt_message)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseSoftwareOpenGL)
print('Qt version:', QtCore.qVersion())
print('PyQt version:', QtCore.PYQT_VERSION_STR)
print('QtCore ready; continuing to main.py.', flush=True)
