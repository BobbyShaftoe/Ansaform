package gabs_fixture

//GetGabsJson provides sample data
func GetGabsJson() []byte {

	ExampleJson := []byte(`{
		"outter":{
			"inner":{
				"value1":10,
				"value2":22
			},
			"alsoInner":{
				"value1":20,
				"array1":[
					30, 40
				]
			}
		}
	}`)

	return ExampleJson
}
