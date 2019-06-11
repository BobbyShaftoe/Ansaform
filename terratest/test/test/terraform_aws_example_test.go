package test

import (
		"fmt"

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
	t.Parallel()

	tfVars, _ := TFVars{}.ParseTFVars("../dev/terraform.tfvars")


	// Mock expected name
	// expectedName := fmt.Sprintf("terratest-aws-%s", random.UniqueId())
	// Mock AWS region
	// awsRegion := aws.GetRandomRegion(t, nil, nil)
	awsRegion := "us-east-1"

	// Create session for aws clients
	thisSession := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(awsRegion),
	}))
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
		if aerr, ok := err.(awserr.Error); ok {
			switch aerr.Code() {
			default:
				fmt.Println(aerr.Error())
			}
		} else {
			// Print the error, cast err to awserr.Error to get the Code and
			// Message from an error.
			fmt.Println(err.Error())
		}
		return
	}

	fmt.Println(result)

	terraformOptions := &terraform.Options{
			TerraformDir: "../template",
			Vars: map[string]interface{}{
					// "instance_name": expectedName,

					"account_id":  "088841113972",
					"aws_region":  "us-east-1",
					"environment": "development",
			},
			EnvVars: map[string]string{
					"AWS_DEFAULT_REGION": awsRegion,
			},
			RetryableTerraformErrors: nil,
			MaxRetries:               0,
			TimeBetweenRetries:       0,

	}


	// Defer destroy until end of deploy run
	defer terraform.Destroy(t, terraformOptions)

	// Init Terraform first
	terraform.InitAndApply(t, terraformOptions)

	// Run terraform output to get the values of output variables
	// Instance id
	instanceId := terraform.Output(t, terraformOptions, "ec2_instance_id")
	fmt.Println(instanceId)
	// Ami that backs the ec2 instance
	// amiId = aws.GetAccountId()

	// Instance tags - Use method from AWS SDK here
	// instanceTags := aws.GetTagsForEc2Instance(t, awsRegion, instanceId)

}
