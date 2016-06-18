#!./venv/bin/python
import os
import sys

if __name__ == "__main__":
    if os.path.split(sys.argv[0])[1] == "manage.py":
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oncall.dev_settings")
    else:
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oncall.pi_settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
