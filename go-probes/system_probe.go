package main

import (
	"encoding/json"
	"os"
	"runtime"
	"strings"
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

type ErrorOutput struct {
	SystemProbe map[string]string `json:"system_probe"`
}

func readFirstAvailable(paths ...string) string {
	for _, path := range paths {
		data, err := os.ReadFile(path)
		if err == nil {
			value := strings.TrimSpace(string(data))
			if value != "" {
				return value
			}
		}
	}
	return ""
}

func writeJSON(v any) {
	data, err := json.Marshal(v)
	if err != nil {
		fallback := ErrorOutput{
			SystemProbe: map[string]string{
				"error": "failed to marshal system probe output",
			},
		}
		data, _ = json.Marshal(fallback)
	}
	_, _ = os.Stdout.Write(data)
}

func main() {
	hostname := ""

	if runtime.GOOS == "linux" {
		hostname = readFirstAvailable(
			"/host/etc/hostname",
			"/host/proc/sys/kernel/hostname",
		)
	}

	if hostname == "" {
		localHostname, err := os.Hostname()
		if err != nil {
			writeJSON(ErrorOutput{
				SystemProbe: map[string]string{
					"error": "failed to determine hostname",
				},
			})
			return
		}
		hostname = localHostname
	}

	output := Output{
		SystemProbe: SystemProbe{
			Hostname:        hostname,
			LogicalCPUCount: runtime.NumCPU(),
			OS:              runtime.GOOS,
			Arch:            runtime.GOARCH,
		},
	}

	writeJSON(output)
}
