async def transform_url(original_url, name):
    new = original_url.replace('.jpg?', f'?file={name}&')
    return new
