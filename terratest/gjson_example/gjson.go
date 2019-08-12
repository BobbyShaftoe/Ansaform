package gjson_example

import "github.com/tidwall/gjson"

const gJSON = `{"name":{"first":"Janet","last":"Prichard"},"age":47}`

func pJSON() {
	value := gjson.Get(gJSON, "name.last")
	println(value.String())
}
