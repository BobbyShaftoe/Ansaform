package helper

import (
	"bufio"
		"fmt"
		"log"
	"os"
	"strings"
)

type TFVarsValues map[string]string

type TFVars struct {
	Vars TFVarsValues
}

var TFV = make(map[string]string)


func (T *TFVars) ParseTFVars(filepath string) error {

	tfvFilepath := filepath

	if len(tfvFilepath) == 0 {
		fmt.Println("No path to tfvars file available")
		log.Fatalln("No path to tfvars file available")
		return nil
	}

	file, err := os.Open(tfvFilepath)
	if err != nil {
		log.Fatal(err)
		return err
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if equal := strings.Index(line, "="); equal >= 0 {
			if key := strings.TrimSpace(line[:equal]); len(key) > 0 {
				value := ""
				if len(line) > equal {
					value = strings.TrimSpace(line[equal+1:])
				}
				TFV[key] = value
			}
		}
	}

	T.Vars = TFV

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
		return err
	}

	return nil
}
