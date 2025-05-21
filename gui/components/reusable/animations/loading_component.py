# File: loading_components.py
from datetime import datetime
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

class GenericWorkerThread(QThread):
    """A generic worker thread that can run any function in the background"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int)
    
    def __init__(self, task_function, *args, **kwargs):
        super().__init__()
        self.task_function = task_function
        self.args = args
        self.kwargs = kwargs
        
        
    
    def run(self):
        try:
            result = self.task_function(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class LoadingManager:
    """A reusable loading dialog manager for PyQt applications"""

    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.progress_dialog = None
        self.worker_thread = None
        self.timer = None
        self.elapsed_seconds = 0
        
    
    def run_with_loading(self, task_function, on_complete=None, on_error=None,
                         loading_text="Loading...", title="Please Wait",
                         task_args=(), task_kwargs={}):
        
        # Create progress dialog
        self.progress_dialog = QProgressDialog(loading_text, "Cancel", 0, 0, self.parent)
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setRange(0, 0)
        self.progress_dialog.show()
        
        # Setup timer for updating title with elapsed time
        self.elapsed_seconds = 0
        self.fetched_at = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self._update_timer_title(title))
        self.timer.start(1000)  # tick every 1 second

        # Create and start worker thread
        self.worker_thread = GenericWorkerThread(task_function, *task_args, **task_kwargs)

        if on_complete:
            self.worker_thread.finished.connect(lambda result: self._handle_completion(result, on_complete))
        else:
            self.worker_thread.finished.connect(self._close_dialog)

        if on_error:
            self.worker_thread.error.connect(lambda error: self._handle_error(error, on_error))
        else:
            self.worker_thread.error.connect(self._show_error)

        self.worker_thread.start()
    
    def _update_timer_title(self, base_title):
        self.elapsed_seconds += 1
        if self.progress_dialog:
            self.progress_dialog.setWindowTitle(f"{base_title} ({self.elapsed_seconds}s)")

    def _handle_completion(self, result, callback):
        processed_data, original_id = result
        self._close_dialog()
        callback(processed_data, self.fetched_at, original_id)

    def _handle_error(self, error, callback):
        self._close_dialog()
        callback(error)

    def _close_dialog(self):
        if self.progress_dialog:
            self.progress_dialog.close()
        if self.timer:
            self.timer.stop()
            self.timer = None
        self.elapsed_seconds = 0

    def _show_error(self, error_message):
        self._close_dialog()
        print(f"Error occurred: {error_message}")

