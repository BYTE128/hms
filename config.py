import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x99\xa1\xec\x90\xb5\x9f[\xdb7\x065\x13s_\xc8\\'