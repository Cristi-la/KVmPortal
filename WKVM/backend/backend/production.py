# EMAIL_HOST = "smtp.sendgrid.net"
# EMAIL_HOST_USER = config("SENDGRID_USERNAME")
# EMAIL_HOST_PASSWORD = config("SENDGRID_PASSWORD")
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# SECURE_HSTS_PRELOAD = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=3600, cast=int)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = "DENY"

# WEBPACK_LOADER["DEFAULT"]["CACHE"] = True

# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "standard": {
#             "format": "%(levelname)-8s [%(asctime)s] [%(request_id)s] [%(correlation_id)s] %(name)s: %(message)s"
#         },
#     },
#     "handlers": {
#         "null": {
#             "class": "logging.NullHandler",
#         },
#         "mail_admins": {
#             "level": "ERROR",
#             "class": "django.utils.log.AdminEmailHandler",
#             "filters": ["require_debug_false"],
#         },
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "filters": ["request_id", "correlation_id"],
#             "formatter": "standard",
#         },
#     },
#     "loggers": {
#         "": {"handlers": ["console"], "level": "INFO"},
#         "django.security.DisallowedHost": {
#             "handlers": ["null"],
#             "propagate": False,
#         },
#         "django.request": {
#             "handlers": ["mail_admins"],
#             "level": "ERROR",
#             "propagate": True,
#         },
#         "log_request_id.middleware": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     },
# }
