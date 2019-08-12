package terratest_helpers

// https://github.com/Jeffail/gabs

import (
	"fmt"
	"github.com/Jeffail/gabs/v2"
	"io/ioutil"
)

//Terraform outputs from plan
type terraformOutputsMap map[string]string

//Terraform Variables from plan
type terraformVariablesMap map[string]string

//Terraform Configurations from plan
type terraformConfigurationsMap map[string]string

//TFVars struct for attributes
type terraformOutputs struct {
	Outputs       terraformOutputsMap
	Variables     terraformVariablesMap
	Configuration terraformConfigurationsMap
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

// Two data structures a returned
// dataObjects map[string]interface{} represents the actual data structure
// dataObjectsTypes map[string]string is a map of keys and values are types of data in data structure

func (T *terraformOutputs) getAttributes(filepath string) (error, map[string]string, map[string]interface{}) {

	var err error
	var file []byte
	var dataObjects map[string]interface{}
	var dataObjectsTypes map[string]string

	terraformPlanPath := filepath

	file, err = ioutil.ReadFile(terraformPlanPath)
	check(err)

	print("file %T\n", file)

	jsonParsed, err := gabs.ParseJSON(file)
	check(err)

	fmt.Printf("%s\n", jsonParsed)

	return err, dataObjectsTypes, dataObjects

}
