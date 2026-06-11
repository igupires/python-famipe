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

def fix_encoding(text: str) -> str:
    return text.encode('utf-8', errors='replace').decode('utf-8')


def decode_request_body(body):
    """Decode a requests body payload for readable logging."""
    if isinstance(body, bytes):
        try:
            return body.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return body.decode('latin-1')
            except UnicodeDecodeError:
                return repr(body)
    return body