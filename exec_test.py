# import time
# from signal_monitor import SignalMonitor

# class Bot:
#     def __init__(self):
#         self.sig_mon = SignalMonitor('params.py', self)
#         # self.params = params
#         # self.print_params()
#         self.params = {}

#     def print_params(self):
#         print("Current parameters:")
#         # for key, value in params.items():
#         #     print(f"{key}: {value}")
#         print(self.params)

#     def run(self):
#         while True:
#             try:
#                 # Your trading logic here
#                 # Example: buy/sell based on self.params

#                 # Sleep for a while to avoid excessive checking
#                 time.sleep(5)

#                 # Print the current parameters
#                 self.print_params()

#             except KeyboardInterrupt:
#                 break

# if __name__ == "__main__":
#     # Load initial parameters from params.py
#     # with open('params.py', 'r') as params_file:
#     #     new_params_code = params_file.read()
#     #     params = {}
#     #     exec(new_params_code, globals(), params)

#     bot = Bot()

#     bot.run()


import os
import signal
import threading
import time

class MyClass:
    def __init__(self):
        self.max_pos = None
        self.params = {}
        self.file_path = 'params.py'
        self.last_modified_time = 0  # Store the last modified time of the file

        # Execute the code in params.py initially
        self.execute_params_code()
        self.print_attributes()

        # Create an event for signaling when the file is modified
        self.file_modified_event = threading.Event()

        # Create a thread for file monitoring
        self.monitor_thread = threading.Thread(target=self.monitor_file_changes)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def execute_params_code(self):
        # Create an instance of MyClass
        my_instance = self

        # Execute the code in params.py within a custom namespace
        namespace = {'self': my_instance}

        with open(self.file_path, 'r') as file:
            code = file.read()
            exec(code, namespace)

    def print_attributes(self):
        print(f'max_pos: {self.max_pos}')
        print(f'params: {self.params}')

    def monitor_file_changes(self):
        def signal_handler(signum, frame):
            self.file_modified_event.set()

        # Set up a signal handler for SIGUSR1
        signal.signal(signal.SIGUSR1, signal_handler)

        while True:
            try:
                file_modified_time = os.path.getmtime(self.file_path)
                if file_modified_time > self.last_modified_time:
                    self.last_modified_time = file_modified_time
                    # Signal that the file has been modified
                    self.file_modified_event.set()

            except Exception as e:
                print(e)
               # pass  # Handle the case where the file is deleted

            # Wait for the signal with a timeout (1 second)
            self.file_modified_event.wait(1)
            self.file_modified_event.clear()

# Create an instance of MyClass
my_instance = MyClass()

# You can modify params.py externally, and the changes will be reflected immediately
# Example: Modify params.py and send SIGUSR1 signal to this process

#hanges will be reflected immediately
# Example: Modify params.py and send SIGUSR1 signal to this process

# You can modify params.py externally, and the changes will be reflected immediately
# Example: Modify params.py and send SIGUSR1 signal to this process

