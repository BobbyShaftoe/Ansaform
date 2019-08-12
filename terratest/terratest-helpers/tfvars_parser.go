package terratest_helpers

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strings"
)

//tfVarsValues map of strings hold the values
type tfVarsValues map[string]string

//TFVars struct for tfvars
type TFVars struct {
	Vars tfVarsValues
}

//tfv Create the map
var tfv = make(map[string]string)

//ParseTFVars Main function that reads tfvars file and returns the values
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

	removeQuotesPattern := regexp.MustCompile(`["\s]`)
	scannerLocal := bufio.NewScanner(file)

	for scannerLocal.Scan() {
		line := scannerLocal.Text()
		if equal := strings.Index(line, "="); equal >= 0 {
			if key := strings.TrimSpace(line[:equal]); len(key) > 0 {
				value := ""
				if len(line) > equal {
					value = strings.TrimSpace(line[equal+1:])
					value = removeQuotesPattern.ReplaceAllString(value, ``)
				}
				tfv[key] = value
			}
		}
	}

	T.Vars = tfv

	if errLocal := scannerLocal.Err(); err != nil {
		log.Fatal(errLocal)
		return errLocal
	}

	return nil
}
