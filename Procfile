release: flask db upgrade
web: gunicorn app:app --log-file=-
cron: honcho -f procfile_cron start