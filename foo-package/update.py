import configparser
import datetime
import json
import os
import shutil
import urllib.request


gh_api = 'https://api.github.com'
gh_owner = 'wclyffe'
gh_repo = 'travis-test'
gh_asset_name = 'foo-package.zip'
current_dir = os.path.dirname(os.path.abspath(__file__))


def last_release_info(owner, repo):
    gh_releases = '/repos/{owner}/{repo}/releases'.format(owner=owner,repo=repo)
    response = urllib.request.urlopen(gh_api + gh_releases)
    releases = json.loads(response.read().decode(encoding='utf-8'))
    last_release = releases[0]
    return last_release


def asset_download(release, asset_name):
    asset_url = None
    for asset in release['assets']:
        if asset['name'] == asset_name:
            asset_url = asset['url']
            break
    if asset_url:
        req = urllib.request.Request(asset_url)
        req.add_header('Accept', 'application/octet-stream')

        with urllib.request.urlopen(req) as response, open(asset_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)


def update_inplace(asset_name):
    extract_dir = current_dir
    p = extract_dir.rfind('/')
    extract_dir = extract_dir[:p]
    shutil.unpack_archive(asset_name, extract_dir, 'zip')
    os.remove(asset_name)


def check_new_version(owner, repo):
    last_release = last_release_info(owner, repo)
    release_info = configparser.ConfigParser()
    release_info.read(os.path.join(current_dir, 'release_info'))
    # compare dates
    curr_release_date = datetime.datetime.strptime(release_info['VERSION']['date'], "%Y-%m-%dT%H:%M:%SZ")
    print(curr_release_date)
    last_release_date = datetime.datetime.strptime(last_release['published_at'], "%Y-%m-%dT%H:%M:%SZ")
    print(last_release_date)
    if curr_release_date < last_release_date:
        print("There's a new release :-)")
        return last_release
    else:
        print("You're up to date")
        return None


if __name__ == '__main__':
    new_release = check_new_version(gh_owner, gh_repo)
    if new_release:
        asset_download(new_release, gh_asset_name)
        update_inplace(gh_asset_name)
