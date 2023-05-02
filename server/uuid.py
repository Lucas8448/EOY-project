import random
import string

def generate_uuid():
  chars = string.ascii_lowercase + string.digits
  uuid_parts = ["".join(random.choices(chars, k=4)) for _ in range(7)]
  uuid_string = "-".join(uuid_parts)
  return uuid_string