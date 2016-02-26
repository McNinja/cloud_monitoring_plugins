// Rackspace Cloud Monitoring plugin to check port, particularly
// useful for services that aren't accessible to a remote port check.
//
// Copyright 2016 Russell Troxel <russell.troxel@rackspace.com>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/shirou/gopsutil/disk"
)

func get_devices() []string {
	var drives []string

	d, err := disk.DiskPartitions(true)
	if err != nil {
		fmt.Println("status err could not retrieve disk labels")
		panic(err)
	}

	for i := 0; i < len(d); i++ {
		drive := d[i]
		drives = append(drives, drive.Device)
	}
	return drives
}

func test_rw(d string) int {
	p := strings.Join([]string{d, `\rax_tmp_test`}, "")

	_, err := os.Create(p)
	if err != nil {
		return 0
	} else {
		return 1
	}
}

func main() {
	ro_devices := 0
	var ro_list []string

	drives := get_devices()

	metric := "metric %s_writeable %d"
	for i := 0; i < len(drives); i++ {
		drive := drives[i]
		rw := test_rw(drive)
		if rw != 1 {
			ro_devices += 1
			ro_list = append(ro_list, drive)
		}
		fmt.Println(fmt.Sprintf(metric, drive, rw))
	}

	var list string
	if len(ro_list) != 0 {
		list = strings.Join(ro_list, "")
	} else {
		list = "none"
	}

	fmt.Println(fmt.Sprintf("metric ro_devices %d", ro_devices))
	fmt.Println(fmt.Sprintf("metric ro_list %s", list))
}
