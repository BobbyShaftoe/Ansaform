package main

// https://github.com/Jeffail/gabs

import (
	"fmt"
	"github.com/Jeffail/gabs/v2"
	"test/gabs_example/gabs_fixture"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	gabsExample()
}

func gabsExample() {

	var gabsExampleJson []byte
	// Example json for attribute reference using Gabs
	gabsExampleJson = gabs_fixture.GetGabsJson()

	jsonParsed, err := gabs.ParseJSON(gabsExampleJson)
	fmt.Printf("%T, %s\n", jsonParsed, jsonParsed)

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
	fmt.Printf("%T, %s\n", gObj, gObj)

	value, ok = gObj.Data().(float64)
	// value == 40.0, ok == true

	value, ok = jsonParsed.Path("does.not.exist").Data().(float64)
	// value == 0.0, ok == false

	// Check the value exists
	exists := jsonParsed.Exists("outter", "inner", "value1")
	// exists == true
	fmt.Printf("Exists returned %t for value1 in heirarchy outter/inner\n", exists)

	// Check the path exists
	exists = jsonParsed.ExistsP("does.not.exist")
	// exists == false

	//Iterating objects
	jsonParsed, err = gabs.ParseJSON([]byte(`{"object":{"first":1,"second":2,"third":3}}`))
	check(err)

	// S is shorthand for Search
	for key, child := range jsonParsed.S("object").ChildrenMap() {
		fmt.Printf("key: %v, type: %T,  ", key, child.Data())
		fmt.Printf("value: %v\n", child.Data().(float64))
	}

	//Iterating arrays
	jsonParsed, err = gabs.ParseJSON([]byte(`{"array":["first","second","third"]}`))
	check(err)

	for _, child := range jsonParsed.S("array").Children() {
		fmt.Println(child.Data().(string))
	}
}
