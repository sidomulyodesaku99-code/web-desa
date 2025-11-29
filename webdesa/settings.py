from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-key")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "sidomulyodesaku.pythonanywhere.com",  # PythonAnywhere domain
]


# ============================================================
# INSTALLED APPS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # aplikasi kamu
    "desaapp",

    # CKEditor
    "django_ckeditor_5",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Whitenoise tidak wajib di PythonAnywhere, tapi boleh tetap.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "webdesa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "desaapp" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webdesa.wsgi.application"


# ============================================================
# DATABASE CONFIG (SWITCH LOCAL / PYTHONANYWHERE)
# ============================================================

ENV = os.getenv("ENV", "local")

if ENV == "production":
    # ============================
    # MySQL PythonAnywhere
    # ============================
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("PA_DB_NAME"),
            "USER": os.getenv("PA_DB_USER"),
            "PASSWORD": os.getenv("PA_DB_PASSWORD"),
            "HOST": os.getenv("PA_DB_HOST"),
            "PORT": "3306",
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }

else:
    # ============================
    # LOCAL DATABASE
    # ============================
    LOCAL_ENGINE = os.getenv("LOCAL_DB_ENGINE", "sqlite")

    if LOCAL_ENGINE == "mysql":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.getenv("LOCAL_NAME"),
                "USER": os.getenv("LOCAL_USER"),
                "PASSWORD": os.getenv("LOCAL_PASSWORD"),
                "HOST": os.getenv("LOCAL_HOST"),
                "PORT": os.getenv("LOCAL_PORT"),
            }
        }
    else:
        # Default SQLite
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ============================================================
# LOGIN
# ============================================================

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "/login-user/"


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC & MEDIA
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "desaapp" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# CKEDITOR CONFIG
# ============================================================

customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

CKEDITOR_5_CONFIGS = {
    "default": {"toolbar": "full"},
    "extends": {
        "toolbar": {
            "items": [
                "heading", "|", "outdent", "indent", "|",
                "bold", "italic", "link", "underline", "strikethrough",
                "code", "highlight", "|",
                "alignment", "codeBlock", "sourceEditing", "insertImage",
                "bulletedList", "numberedList", "todoList", "|",
                "blockQuote", "imageUpload", "|",
                "fontSize", "fontFamily", "fontColor", "fontBackgroundColor",
                "mediaEmbed", "removeFormat", "insertTable",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "alignment": {"options": ["left", "center", "right", "justify"]},
        "image": {
            "toolbar": [
                "imageTextAlternative", "|",
                "imageStyle:alignLeft", "imageStyle:alignRight",
                "imageStyle:alignCenter", "imageStyle:side",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells",
                "tableProperties", "tableCellProperties"
            ],
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3"},
            ]
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
