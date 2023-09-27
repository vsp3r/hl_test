import importlib
import os
import signal
import sys
import threading
import logging

class SignalMonitor:
    def __init__(self, param_file, bot_instance):
        """Monitors for changes in params.py"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__class__.__name__)
        self.param_file = param_file
        self.bot_instance = bot_instance
        self.initial_modification_time = os.path.getmtime(self.param_file)

        # sets up signal handler, using arbitrary SIGUSR1
        signal.signal(signal.SIGUSR1, self.handle_signal)

        # Create a thread for signal monitoring
        self.signal_thread = threading.Thread(target=self.signal_monitor_thread)
        self.signal_thread.daemon = True  # Allow the program to exit when the main thread exits
        self.signal_thread.start()

    def load_and_update_params(self):
        with open(self.param_file, 'r') as params_file:
            new_params_code = params_file.read()
            local_vars = {}
            # Execute the code from params.py in the context of local_vars
            exec(new_params_code, None, local_vars)
            # Update the bot instance's attributes
            for key, value in local_vars.items():
                setattr(self.bot_instance, key, value)

    def handle_signal(self, signum, frame):
        print(f"{self.param_file} has been modified. Reloading parameters...")
        self.load_and_update_params()

    def signal_monitor_thread(self):
        self.load_and_update_params()
        try:
            # Wait indefinitely for signals
            signal.pause()
        except KeyboardInterrupt:
            sys.exit(0)