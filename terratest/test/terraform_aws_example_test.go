package test

import (
	"fmt"
	terratestHelpers "test/terratest-helpers"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ec2"
	"testing"
	//"github.com/gruntwork-io/terratest/modules/aws"
	//"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
)

func TestTerraformAwsExample(t *testing.T) {

	terraformDir := "../../template"

	tfvarsFile := "../../dev/terraform.tfvars"
	tfvarsFileRelativePath := "../dev/terraform.tfvars"

	tfvarsFiles := []string{tfvarsFileRelativePath}

	tfv := &terratestHelpers.TFVars{}
	if err := tfv.ParseTFVars(tfvarsFile); err != nil {
		fmt.Printf("Error: %s", err)
	}

	environment := tfv.Vars["environment"]
	accountId := tfv.Vars["account_id"]
	awsRegion := tfv.Vars["aws_region"]

	fmt.Printf("Environment: %s\n", environment)
	fmt.Printf("AWS Region: %s\n", accountId)
	fmt.Printf("Account ID: %s\n", awsRegion)

	t.Parallel()

	fmt.Printf("Creating Session\n")
	// Create session for aws clients
	thisSession := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(awsRegion),
		//Region: aws.String(awsRegion),
	}))

	fmt.Printf("Creating Client\n")
	// Create ec2 client
	svc := ec2.New(thisSession)

	// Describe instances and filter on tags for service type
	//input := &ec2.DescribeInstancesInput{
	//	Filters: []*ec2.Filter{
	//		{
	//			Name: aws.String("tag:service_type"),
	//			Values: []*string{
	//				aws.String("example service"),
	//			},
	//		},
	//	},
	//}

	//noinspection GoInvalidCompositeLiteral
	input := &ec2.DescribeInstancesInput{
		DryRun: nil,
		Filters: []*ec2.Filter{
			{
				Name: aws.String("tag:service_type"),
				Values: []*string{
					aws.String("example service"),
				},
			},
		},
		InstanceIds: nil,
		MaxResults:  nil,
		NextToken:   nil,
	}

	result, err := svc.DescribeInstances(input)
	if err != nil {
		if errLocal, ok := err.(awserr.Error); ok {
			switch errLocal.Code() {
			default:
				fmt.Println(errLocal.Error())
			}
		} else {
			// Print the error, cast err to awserr.Error to get the Code and
			// Message from an error.
			fmt.Println(err.Error())
		}
		return
	}
	fmt.Printf("%s\n", result)

	terraformOptions := &terraform.Options{
		//TerraformBinary: "",
		//Targets:         nil,
		//Vars:            nil,

		TerraformDir: terraformDir,
		VarFiles:     tfvarsFiles,

		EnvVars: map[string]string{
			"AWS_DEFAULT_REGION": awsRegion,
		},

		BackendConfig:            nil,
		RetryableTerraformErrors: nil,
		MaxRetries:               0,
		TimeBetweenRetries:       0,
		Upgrade:                  false,
		NoColor:                  false,
		SshAgent:                 nil,
		NoStderr:                 false,
		OutputMaxLineSize:        0,
	}

	// Defer destroy until end of deploy run
	defer terraform.Destroy(t, terraformOptions)

	// Init Terraform first
	terraform.InitAndApply(t, terraformOptions)

	// Run terraform output to get the values of output variables
	// Instance id
	instanceId := terraform.Output(t, terraformOptions, "main_security_group_id")
	fmt.Println(instanceId)
	// Ami that backs the ec2 instance

	// Instance tags - Use method from AWS SDK here
	// instanceTags := aws.GetTagsForEc2Instance(t, awsRegion, instanceId)

}
