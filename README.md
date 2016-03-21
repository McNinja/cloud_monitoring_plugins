# Cloud Monitoring Plugins

These Plugins are for the Rackspace Cloud Monitoring agent, and should be installed and configured using the agent.plugin check type:

https://developer.rackspace.com/docs/cloud-monitoring/v1/developer-guide/#agent-plugin

## Read-Only Filesystem Check

These checks determine whether any disks currently attached to the entity have gone "read-only". This check is designed to do so definitively, by attempting to write a test file (raxmon_tmp_test) to the root of the mount point / drive letter for a given disk.

## Linux Installation

1. Download the desired check to the custom plugin directory on your cloud server:
```bash
cd /usr/lib/rackspace-monitoring-agent/plugins/ && wget https://raw.githubusercontent.com/swyytch/cloud_monitoring_plugins/master/read_only_linux/read_only_check_linux.py
```

3. Head to https://intelligence.rackspace.com and click the name of the entity for which you would like to create this check

4. From the entity screen, scroll down until you see the "Create Check" button:

![Create Check Example](https://raw.githubusercontent.com/swyytch/cloud_monitoring_plugins/master/images/create_check.png "Moniitoring Checks")

5. Configure your check with the following criteria:

![Create Check Dialog](https://raw.githubusercontent.com/swyytch/cloud_monitoring_plugins/master/images/check_dialog.png "Create Check")

5. Once the Check is created, click the Gear Icon next to the check name, and select "Add Alarm".

6. Give you alarm a name, and configure the following criteria:

```
if (metric["ro_devices"] != 0) {
    return new AlarmStatus(CRITICAL, 'Found Read-Only Filesystems: #{ro_list}');
}
```

7. Test it! If you have a read-only filesystem (You can simulate this failure by running ```mount -o ro,remount {mountpoint)``` but be aware this will cause your filesystem to *actually* go read only.) If you have a read-only filesystem, you should see the following alarm text:

![Failed Alarm Output](https://raw.githubusercontent.com/swyytch/cloud_monitoring_plugins/master/images/alarm_test.png "Failed Alarm")

