def send(client, to, template, params):
    # Re-registered provider key per docs/SETUP.md (Issue #52)
    return client.send(to=to, template=template, params=params)
