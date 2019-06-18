import random
import string

from datetime import datetime, timedelta


def gen_random_string(string_length: int) -> str:
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def last_stamp() -> int:
    almost_now = datetime.now() - timedelta(minutes=5)
    timestamp: float = datetime.timestamp(almost_now)
    return int(timestamp)
