package main

import (
	"fmt"
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
		return false
	} else {
		return true
	}
}

func main() {
	ro_devices := 0
	var ro_list []string

	drives := get_devices()

	metric := "metric %s_writeable %s"
	for i := 0; i < len(drives); i++ {
		drive := drives[i]
		rw := test_rw(drive)
		if !(rw) {
			ro_devices += 1
			append(ro_list, drive)
		}
		fmt.Sprintln(metric, drive, rw)

		fmt.Sprintln("metric ro_devices %s", ro_devices)
		fmt.Sprintln("metric ro_list %s", strings.Join(ro_list, ""))
	}
}
