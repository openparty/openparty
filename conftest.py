import os, sys

sys.path.insert(0, "")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
pytest_plugins = ["django"]
