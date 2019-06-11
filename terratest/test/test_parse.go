package main

/*
Example showing how to use tfvars parser

github.com/BobbyShaftoe/terratest-tryout/test/helper is here in the test/helper directory
just move it where it's convenient
*/

import (
	"fmt"
	_ "fmt"
	"github.com/BobbyShaftoe/terratest-tryout/test/helper"
)

func main() {

	tfv := &helper.TFVars{}
	if err := tfv.ParseTFVars("../dev/terraform.tfvars"); err != nil {
			fmt.Printf("Error: %s", err)
	}
	tfvars := tfv.Vars
		//tfvars := helper.TFV

	fmt.Println("Variables in tfvars file:")
	for k := range helper.TFV {
			fmt.Printf("%s ", k)
	}
	fmt.Printf("\n\n")


		fmt.Printf("Environment: %s\n", tfvars["environment"])
		fmt.Printf("AWS Region: %s\n", tfvars["aws_region"])
		fmt.Printf("Account ID: %s\n", tfvars["account_id"])

}








