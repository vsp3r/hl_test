import importlib
import logging
import time
from signal_monitor import SignalMonitor  # Import your SignalMonitor class

class MyBot:
    def __init__(self):
        # Initialize the SignalMonitor
        self.signal_monitor = SignalMonitor()
        
        # Load initial parameters from params.py
        self.load_params()

    def load_params(self):
        # Import and reload the params module
        importlib.reload(params)
        
        # Access parameters from params.py
        self.max_pos = params.self.max_pos
        self.EFM_params = params.self.params['EFM']
        
        # Print some parameters
        self.logger.info(f"max_pos: {self.max_pos}")
        self.logger.info(f"EFM_params: {self.EFM_params}")

    def run(self):
        while True:
            # Check for parameter changes in SignalMonitor
            if self.signal_monitor.params_changed:
                self.load_params()  # Reload parameters if they have changed
            time.sleep(1)  # Sleep for 1 second (adjust as needed)

if __name__ == '__main__':
    # Import the params module
    import params
    
    # Create an instance of MyBot
    bot = MyBot()
    
    # Run the bot
    bot.run()
