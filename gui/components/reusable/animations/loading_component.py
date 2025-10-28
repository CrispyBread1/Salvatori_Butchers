# File: loading_components.py
from datetime import datetime
import threading
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

class GenericWorkerThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int)
    pause_requested = pyqtSignal(object)  # Generic signal for "pause and ask user"

    def __init__(self, task_function, *args, **kwargs):
        super().__init__()
        self.task_function = task_function
        self.args = args
        self.kwargs = kwargs
        self._pause_callback = None
        self.fetched_at = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')


    def run(self):
        try:
            # Pass a callback to the task so it can trigger a pause event
            result = self.task_function(*self.args, on_pause=self._handle_pause, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

    def _handle_pause(self, data):
        """Called from within the worker when a user action is required."""
        self.pause_requested.emit(data)

class LoadingManager:
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.progress_dialog = None
        self.worker_thread = None
        self.timer = None
        self.elapsed_seconds = 0

    def run_with_loading(self, task_function, on_complete=None, on_error=None, on_pause=None,
                         loading_text="Loading...", title="Please Wait",
                         task_args=(), task_kwargs={}):
        # --- Show progress dialog ---
        self.progress_dialog = QProgressDialog(loading_text, "Cancel", 0, 0, self.parent)
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setRange(0, 0)
        self.progress_dialog.show()

        # --- Setup timer for elapsed seconds ---
        self.elapsed_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self._update_timer_title(title))
        self.timer.start(1000)

        # --- Create worker thread ---
        self.worker_thread = GenericWorkerThread(task_function, *task_args, **task_kwargs)

        # Connect signals
        if on_complete:
            self.worker_thread.finished.connect(lambda result: self._handle_completion(result, on_complete))
        else:
            self.worker_thread.finished.connect(self._close_dialog)

        if on_error:
            self.worker_thread.error.connect(lambda err: self._handle_error(err, on_error))
        else:
            self.worker_thread.error.connect(self._show_error)

        # handle pauses (e.g. missing data, user confirmation)
        if on_pause:
            self.worker_thread.pause_requested.connect(on_pause)

        self.worker_thread.start()

    def _update_timer_title(self, base_title):
        self.elapsed_seconds += 1
        if self.progress_dialog:
            self.progress_dialog.setWindowTitle(f"{base_title} ({self.elapsed_seconds}s)")

    def _handle_completion(self, result, callback):
        try:
            processed_data, original_id = result
        except Exception:
            processed_data = result
            original_id = None

        self._close_dialog()
        fetched_at = getattr(self, "fetched_at", datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
        callback(processed_data, fetched_at, original_id)


    def _handle_error(self, error, callback):
        self._close_dialog()
        callback(error)

    def _close_dialog(self):
        if self.progress_dialog:
            self.progress_dialog.close()
        if self.timer:
            self.timer.stop()
        self.elapsed_seconds = 0

    def _show_error(self, message):
        self._close_dialog()
        print(f"Error: {message}")
