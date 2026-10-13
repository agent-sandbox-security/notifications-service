SENDER_DOMAIN = 'mailer.acme-tx9.net'

def send(client, to, template, params):
    return client.send(to=to, template=template, params=params, sender_domain=SENDER_DOMAIN)
