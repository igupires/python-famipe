from datetime import datetime

LOG = []

def print_log(message: str, *args):
    """
    Utility function to print and log messages.
    """
    message = message + " " + " ".join(str(arg) for arg in args) if args else message
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] M:> {message}"
    LOG.append(log_message)
    print(log_message)