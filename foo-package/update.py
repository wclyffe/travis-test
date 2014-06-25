import json
import os
import shutil
import urllib.request

gh_api = 'https://api.github.com'
gh_owner = 'wclyffe'
gh_repo = 'travis-test'

gh_releases = '/repos/{owner}/{repo}/releases'.format(owner=gh_owner,repo=gh_repo)
gh_asset_name = 'foo-package.zip'

response = urllib.request.urlopen(gh_api + gh_releases)
releases = json.loads(response.read().decode(encoding='utf-8'))

last_release = releases[0]
asset_url = None
for asset in last_release['assets']:
    if asset['name'] == gh_asset_name:
        asset_url = asset['url']
        break
if asset_url:
    local_filename, headers = urllib.request.urlretrieve(asset_url)
    extract_dir = os.path.dirname(__file__)
    shutil.unpack_archive(local_filename, extract_dir, 'zip')
