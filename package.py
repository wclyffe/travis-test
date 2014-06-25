import configparser
import json
import os
import shutil
import urllib.request


gh_api = 'https://api.github.com'
gh_owner = 'wclyffe'
gh_repo = 'travis-test'

gh_releases = '/repos/{owner}/{repo}/releases'.format(owner=gh_owner,repo=gh_repo)
gh_tags = '/repos/{owner}/{repo}/tags'.format(owner=gh_owner,repo=gh_repo)

response = urllib.request.urlopen(gh_api + gh_releases)
releases = json.loads(response.read().decode(encoding='utf-8'))
last_release = releases[0]

last_release_tag_name = last_release['tag_name']
last_release_date = last_release['published_at']

response = urllib.request.urlopen(gh_api + gh_tags)
tags = json.loads(response.read().decode(encoding='utf-8'))
last_release_tag = None
for tag in tags:
    if tag['name'] == last_release_tag_name:
        last_release_tag = tag
        break
last_release_commit = last_release_tag['commit']['sha']

current_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = 'foo-package'

release_info = configparser.ConfigParser()
release_info['VERSION'] = {'tag_name': last_release_tag_name,
                           'date': last_release_date,
                           'commit': last_release_commit}
with open('release_info', 'w') as configfile:
    release_info.write(configfile)


archive_name = shutil.make_archive(base_name='foo-package',
                                   format="zip",
                                   root_dir=current_dir,
                                   base_dir=package_dir)

print("archive_name: {}".format(archive_name))
