package just_parse_json

import (
	"encoding/json"
	"fmt"
)

func dumpJSON(v interface{}, kn string) {
	iterMap := func(x map[string]interface{}, root string) {
		var knf string
		if root == "root" {
			knf = "%q:%q"
		} else {
			knf = "%s:%q"
		}
		for k, v := range x {
			dumpJSON(v, fmt.Sprintf(knf, root, k))
		}
	}

	iterSlice := func(x []interface{}, root string) {
		var knf string
		if root == "root" {
			knf = "%q:[%d]"
		} else {
			knf = "%s:[%d]"
		}
		for k, v := range x {
			dumpJSON(v, fmt.Sprintf(knf, root, k))
		}
	}

	switch vv := v.(type) {
	case string:
		fmt.Printf("%s => (string) %q\n", kn, vv)
	case bool:
		fmt.Printf("%s => (bool) %v\n", kn, vv)
	case float64:
		fmt.Printf("%s => (float64) %f\n", kn, vv)
	case map[string]interface{}:
		fmt.Printf("%s => (map[string]interface{}) ...\n", kn)
		iterMap(vv, kn)
	case []interface{}:
		fmt.Printf("%s => ([]interface{}) ...\n", kn)
		iterSlice(vv, kn)
	case nil: // added case
		fmt.Printf("%s => (nil) null\n", kn)
	default:
		fmt.Printf("%s => (unknown?) ...\n", kn)
	}
}

func parseIt() {
	b := []byte(`
		[{
			"Name":"Wednesday",
			"Age":6,
			"Parents": [
				"Gomez",
				"Morticia",
				{
					"meh": false,
					"set": [
						1, 
						"2",
						[
							3.000001,
							"4",
							{
								"none": false
							}
						]
					]
				}
			],
			"foo": {
				"foo": "bar",
				"baz": 1,
				"box": true
			}
		}]
	`)

	var f interface{}
	if err := json.Unmarshal(b, &f); err != nil {
		panic(err)
	}
	dumpJSON(f, "root")
}
