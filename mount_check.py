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


def get_mountpoint(device):
    cmd = "mount | grep {0}".format(device)
    mount_line = commands.getoutput(cmd)
    if not mount_line:
        return False
    return mount_line.split()[2]


def main():

    disks = []
    partitions = []
    ro_devices = 0
    unmounted_devices = 0


    for label in device_labels:
        disk_glob = "".join((label, "[a-zz]"))
        disks += [disk for disk in glob.glob(disk_glob)]

        partition_glob = "".join((label, "[a-zz][0-256]"))
        partitions += [part for part in glob.glob(partition_glob)]

    for part in partitions:
        disks.remove(part.rstrip("0123456789"))
    devices = partitions + disks
    print("found devices: {0}".format(devices))

    # Ignore Swap Partitions
    with open("/proc/swaps") as f:
        swaps = [swap.split()[0] for swap in f.readlines()[1:]]

    for swap in swaps:
        if swap in devices:
            devices.remove(swap)

    for device in devices:
        
        # Generate escaped device name for metrics
        escaped_device = device.split("/")[-1]

        # Test and report if device is mounted
        metric = "metric {0}_mounted int32 {1}"
        mountpoint = get_mountpoint(device)
        if not mountpoint:
            unmounted_devices +=1
            print(metric.format(escaped_device, "0"))
            continue
        print(metric.format(escaped_device, "1"))

        # Test and report if device is writeable
        metric = "metric {0}_writeable int32 {1}"
        writeable = is_readwrite(mountpoint)
        if not writeable:
            ro_devices +=1
            print(metric.format(escaped_device, "0"))
            continue
        print(metric.format(escaped_device, "1"))

    print("metric ro_devices int32 {0}".format(ro_devices))
    print("metric unmounted_devices int32 {0}".format(unmounted_devices))
    print("metric total_devices int32 {0}".format(len(devices)))

if __name__ == "__main__":
    main()










