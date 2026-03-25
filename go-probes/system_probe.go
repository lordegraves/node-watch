package main

import (
	"encoding/json"
	"log"
	"os"
	"runtime"
)

type SystemProbe struct {
	Hostname        string `json:"hostname"`
	LogicalCPUCount int    `json:"logical_cpu_count"`
	OS              string `json:"os"`
	Arch            string `json:"arch"`
}

type Output struct {
	SystemProbe SystemProbe `json:"system_probe"`
}

func main() {
	hostname, err := os.Hostname()
	if err != nil {
		log.Fatal(err)
	}

	output := Output{
		SystemProbe: SystemProbe{
			Hostname:        hostname,
			LogicalCPUCount: runtime.NumCPU(),
			OS:              runtime.GOOS,
			Arch:            runtime.GOARCH,
		},
	}

	data, err := json.Marshal(output)
	if err != nil {
		log.Fatal(err)
	}

	_, err = os.Stdout.Write(data)
	if err != nil {
		log.Fatal(err)
	}
}
