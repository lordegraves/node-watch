package main

import (
	"bufio"
	"encoding/json"
	"os"
	"runtime"
	"strconv"
	"strings"

	"github.com/shirou/gopsutil/v4/mem"
)

type MemoryData struct {
	TotalMB     int     `json:"total_mb"`
	UsedMB      int     `json:"used_mb"`
	PercentUsed float64 `json:"percent_used"`
}

type Output struct {
	MemoryProbe MemoryData `json:"memory_probe"`
}

type ErrorOutput struct {
	MemoryProbe map[string]string `json:"memory_probe"`
}

func parseKBValue(line string) int {
	fields := strings.Fields(line)
	if len(fields) < 2 {
		return 0
	}
	value, err := strconv.Atoi(fields[1])
	if err != nil {
		return 0
	}
	return value
}

func writeJSON(v any) {
	data, err := json.Marshal(v)
	if err != nil {
		fallback := ErrorOutput{
			MemoryProbe: map[string]string{
				"error": "failed to marshal memory probe output",
			},
		}
		data, _ = json.Marshal(fallback)
	}
	_, _ = os.Stdout.Write(data)
}

func readLinuxMemInfo(path string) (MemoryData, error) {
	file, err := os.Open(path)
	if err != nil {
		return MemoryData{}, err
	}
	defer file.Close()

	var memTotalKB int
	var memAvailableKB int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "MemTotal:") {
			memTotalKB = parseKBValue(line)
		}
		if strings.HasPrefix(line, "MemAvailable:") {
			memAvailableKB = parseKBValue(line)
		}
	}

	if err := scanner.Err(); err != nil {
		return MemoryData{}, err
	}

	if memTotalKB == 0 || memAvailableKB == 0 {
		return MemoryData{}, os.ErrInvalid
	}

	usedKB := memTotalKB - memAvailableKB
	totalMB := memTotalKB / 1024
	usedMB := usedKB / 1024
	percentUsed := (float64(usedKB) / float64(memTotalKB)) * 100

	return MemoryData{
		TotalMB:     totalMB,
		UsedMB:      usedMB,
		PercentUsed: round1(percentUsed),
	}, nil
}

func round1(v float64) float64 {
	return float64(int(v*10+0.5)) / 10
}

func main() {
	if runtime.GOOS == "linux" {
		if data, err := readLinuxMemInfo("/host/proc/meminfo"); err == nil {
			writeJSON(Output{MemoryProbe: data})
			return
		}
		if data, err := readLinuxMemInfo("/proc/meminfo"); err == nil {
			writeJSON(Output{MemoryProbe: data})
			return
		}
		writeJSON(ErrorOutput{
			MemoryProbe: map[string]string{
				"error": "failed to read linux memory info",
			},
		})
		return
	}

	vm, err := mem.VirtualMemory()
	if err != nil {
		writeJSON(ErrorOutput{
			MemoryProbe: map[string]string{
				"error": "failed to read system memory info",
			},
		})
		return
	}

	writeJSON(Output{
		MemoryProbe: MemoryData{
			TotalMB:     int(vm.Total / 1024 / 1024),
			UsedMB:      int(vm.Used / 1024 / 1024),
			PercentUsed: round1(vm.UsedPercent),
		},
	})
}
