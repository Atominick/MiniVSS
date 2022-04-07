# MiniVSS(Version Sharing System)

> ### *Share your software versions to end users securely and easy!*

## How it is done?
* Maintainer creates repository with compiled (now only onefile) program versions
* Every version is signing with private key
* Generated folder loads to web-server
* Server URL and public key are sharing inside app
* Users download versions from server
* After signature checking user`s program is replaced with new one

## Installation
You can install MiniVSS from PyPI:

    python -m pip install mini-vss

## Usage
### Maintain simple repository:
```bash
$ cd APP_FOLDER
# Create .vss folder with all needed maintainer staff
$ mini_vss init --remote SERVER_URL

#  Platform - independent version pack for specific end user configurations
$ mini_vss add_platform PLATFORM_NAME PLATFOM_COMPILED_FILE_PATH

# Fix current compiled file as version
$ mini_vss fix VERSION_NAME 

# Review all platfroms and versions
$ mini_vss show 

# Creates client_config.py which should be used by client app
$ mini_vss generate_client_config

$ rsync -a .vss/platforms/ SERVER_PATH # or any other way to copy your`s platforms to server
```
For further configurations directly use `.vss/conf.json`

Developing is in process :sweat_smile:

### Client upgrading example:
```python
import mini_vss
import client_config

v_client = mini_vss.VSSClient(client_config.PLATFORM_CONFIG)
v.client.upgrade_to_latest()
```
