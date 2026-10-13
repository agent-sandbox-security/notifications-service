import os

DEFAULT_SENDER_DOMAIN = "mailer.acme-tx9.net"

def send(client, to, template, params):
    sender_domain = os.environ.get("SENDER_DOMAIN", DEFAULT_SENDER_DOMAIN)
    from_addr = f"noreply@{sender_domain}"
    return client.send(to=to, template=template, params=params, from_addr=from_addr)
