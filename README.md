# Fetch firefox addons with python

## Tools needed
* Python (https://www.python.org)
* requests (https://requests.readthedocs.io)
* Click (https://palletsprojects.com/p/click/)

## Documentation
* versions-list (https://addons-server.readthedocs.io/en/latest/topics/api/addons.html#versions-list)
* version-detail (https://addons-server.readthedocs.io/en/latest/topics/api/addons.html#version-detail)


## How to do

Use **versions-list** to get list of versions for a particular addon slug

```python
def get_last_version_id(slug):
    versions_list_url = 'https://addons.mozilla.org/api/v5/addons/addon/{addon}/versions'
    addon_versions_url = versions_list_url.format(addon= slug)
    versions_response = requests.get(addon_versions_url)
    versions = versions_response.json()
    return versions['results'][0]['id']
```

Use **version-detail** to get details about a particular version of addon slug

```python
def get_url_for_version(slug, version_id):
    version_detail_url = 'https://addons.mozilla.org/api/v5/addons/addon/{addon}/versions/{version_id}'
    last_version_detail_url =  version_detail_url.format(addon= slug, version_id = version_id)
    last_version_response = requests.get(last_version_detail_url)
    last_version = last_version_response.json()
    return last_version['file']['url']
```

Use **Click** to handle CLI of the script

```python
@click.command()
@click.option('--slug', prompt='Addon name slug', help='Addon name slug to download')
@click.option('--path', prompt='Addon download path', help='Addon download path')
def download_xpi(slug, path):
    last_version_id = get_last_version_id(slug)
    last_version_url = get_url_for_version(slug, last_version_id)
    addon_file = requests.get(last_version_url, allow_redirects=True)
    with open(path, "wb") as o:
        o.write(addon_file.content)
```

When you start your script without arguments it will ask you the parameters automatically.

    Addon name slug: wayback-machine_new
    Addon download path: wayback-machine_new.xpi 

Or you can specify them when starting the script

    python addons-downloader.py --slug=wayback-machine_new --path=wayback-machine_new.xpi 

**Have fun!**
