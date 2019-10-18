import os


def setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pogoda.settings")
    import django
    django.setup()