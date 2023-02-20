from configurations.values import BooleanValue

from config.settings.base import Base


class Development(Base):
    DEBUG = BooleanValue(True)

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": Base.BASE_DIR / "db.sqlite3",
        }
    }
