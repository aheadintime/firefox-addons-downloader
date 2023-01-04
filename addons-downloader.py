import requests
import click


@click.command()
@click.option('--slug', prompt='Addon name slug',
              help='Addon name slug to download')
@click.option('--path', prompt='Addon download path',
              help='Addon download path')
def download_xpi(slug, path):

    last_version_id = get_last_version_id(slug)
    last_version_url = get_url_for_version(slug, last_version_id)

    addon_file = requests.get(last_version_url, allow_redirects=True)
    
    with open(path, "wb") as o:
        o.write(addon_file.content)
    

def get_last_version_id(slug):
    versions_list_url = 'https://addons.mozilla.org/api/v5/addons/addon/{addon}/versions'
    
    addon_versions_url = versions_list_url.format(addon= slug)

    versions_response = requests.get(addon_versions_url)

    versions = versions_response.json()

    return versions['results'][0]['id']


def get_url_for_version(slug, version_id):
    version_detail_url = 'https://addons.mozilla.org/api/v5/addons/addon/{addon}/versions/{version_id}'

    last_version_detail_url =  version_detail_url.format(addon= slug, version_id = version_id)

    last_version_response = requests.get(last_version_detail_url)

    last_version = last_version_response.json()

    return last_version['file']['url']


if __name__ == '__main__':
    download_xpi()


