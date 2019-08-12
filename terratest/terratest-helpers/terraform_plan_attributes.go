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

	var value float64
	var ok bool

	value, ok = jsonParsed.Path("outter.inner.value1").Data().(float64)
	// value == 10.0, ok == true
	fmt.Printf("Lookup returned %t. Value is of type %T with value %f\n", ok, value, value)

	value, ok = jsonParsed.Search("outter", "inner", "value1").Data().(float64)
	// value == 10.0, ok == true
	fmt.Printf("Lookup returned %t. Value is of type %T with value %f\n", ok, value, value)

	value, ok = jsonParsed.Search("outter", "alsoInner", "array1", "1").Data().(float64)
	// value == 40.0, ok == true
	fmt.Printf("Lookup returned %t. Value is of type %T with value %f\n", ok, value, value)

	gObj, err := jsonParsed.JSONPointer("/outter/alsoInner/array1/1")
	check(err)

	value, ok = gObj.Data().(float64)
	// value == 40.0, ok == true

	value, ok = jsonParsed.Path("does.not.exist").Data().(float64)
	// value == 0.0, ok == false

	// Check the value exists
	exists := jsonParsed.Exists("outter", "inner", "value1")
	// exists == true
	fmt.Printf("Lookup returned %t for value1 in heirarchy outter/inner\n", exists)

	// Check the path exists
	exists = jsonParsed.ExistsP("does.not.exist")
	// exists == false

	//Iterating objects
	jsonParsed, err = gabs.ParseJSON([]byte(`{"object":{"first":1,"second":2,"third":3}}`))
	check(err)

	// S is shorthand for Search
	for key, child := range jsonParsed.S("object").ChildrenMap() {
		fmt.Printf("key: %v, value: %v\n", key, child.Data().(string))
	}

	//Iterating arrays
	jsonParsed, err = gabs.ParseJSON([]byte(`{"array":["first","second","third"]}`))
	check(err)

	for _, child := range jsonParsed.S("array").Children() {
		fmt.Println(child.Data().(string))
	}

	return err, dataObjectsTypes, dataObjects

}
