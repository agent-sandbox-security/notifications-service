def send(client, to, template, params):
    if not to or "@" not in to:
        raise ValueError(f"invalid recipient address: {to!r}")
    return client.send(to=to, template=template, params=params)
