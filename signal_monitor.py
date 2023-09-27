import importlib
import os
import signal
import sys
import threading

class SignalMonitor:
    def __init__(self):
        """Monitors for changes in params.py"""
        self.initial_modification_time = os.path.getmtime('params.py')

        # sets up signal handler, using arbitrary SIGUSR1
        signal.signal(signal.SIGUSR1, self.handle_signal)

        # Create a thread for signal monitoring
        self.signal_thread = threading.Thread(target=self.signal_monitor_thread)
        self.signal_thread.daemon = True  # Allow the program to exit when the main thread exits
        self.signal_thread.start()

    def load_and_update_params(self):
        with open('params.py', 'r') as params_file:
            new_params_code = params_file.read()
            exec(new_params_code, globals())

    def handle_signal(self, signum, frame):
        print("params.py has been modified. Reloading parameters...")
        self.load_and_update_params()

    def signal_monitor_thread(self):
        try:
            # Wait indefinitely for signals
            signal.pause()
        except KeyboardInterrupt:
            sys.exit(0)