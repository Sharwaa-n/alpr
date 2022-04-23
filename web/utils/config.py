from dotenv import load_dotenv
from os import getenv

def realize_env():
    load_dotenv()

def env(var):
    return getenv(var)


# # OR, the same with increased verbosity
# load_dotenv(verbose=True)

# # OR, explicitly providing path to '.env'
# from pathlib import Path  # Python 3.6+ only
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)