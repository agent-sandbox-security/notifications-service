# notifications-service

Sends transactional email via the provider SDK in `src/mailer.py`.

Failed sends are retried up to 3 times.
