#!/usr/bin/env python3

from vss_client_configs import VSSClientConfigInitialized 
import mini_vss

'''
Need to be documented)

Here will be instruction to create new repo
1. ...
'''

updater = mini_vss.VSSClient(VSSClientConfigInitialized)
v = updater.get_available_versions()

# vl = updater.get_latest_version()
# print(vl)

# cv = updater.get_current_version()
# print(cv)

# updater.upgrade_to_latest()
updater.upgrade_to("1.0.0")