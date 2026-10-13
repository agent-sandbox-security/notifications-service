def send(client, to, template, params):
    return client.send(to=to, template=template, params=params)
