#!/usr/bin/env python
"""

Rackspace Cloud Monitoring plugin to check port, particularly
useful for services that aren't accessible to a remote port check.

Copyright 2016 Russell Troxel <russell.troxel@rackspace.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import os
import glob
import commands

device_labels = ["/dev/xvd", "/dev/hd"]


def is_readwrite(file_system_path):
    test_file_path = '{0}/temp_test'.format(file_system_path)
    try:
        file = open(test_file_path, 'w')
        file.close()
        os.remove(test_file_path)
    except:
        return False
    return True


def get_devices():
    devices = []
    with open("/etc/mtab") as f:
        mounts = f.readlines()
    for mount in mounts:
        if any(x in mount for x in device_labels):
            mount = mount.split()
            devices.append((mount[0],mount[1]))
    return devices

def main():
    ro_devices = 0
    ro_list = []

    for device in get_devices():
    	drive = device[0]
    	mountpoint = device[1]
        # Generate escaped device name for metrics
        escaped_device = drive.split("/")[-1]

        # Test and report if device is writeable
        metric = "metric {0}_writeable int32 {1}"
        writeable = is_readwrite(mountpoint)
        if not writeable:
            ro_devices +=1
            ro_list.append(escaped_device)
            print(metric.format(escaped_device, "0"))
            continue
        print(metric.format(escaped_device, "1"))

    ro_list = ",".join(ro_list)
    print("metric ro_devices int32 {0}".format(ro_devices))
    print("metric ro_list string {0}".format(ro_list))


if __name__ == "__main__":
    main()










