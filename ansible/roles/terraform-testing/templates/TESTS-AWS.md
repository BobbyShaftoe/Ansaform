# tests-aws


```
 ----- [VPC] ----------------------------------
  
    [ROUTE TABLE]  
                    
  -- [SUBNET] {cidr} --------------  | --- [SUBNET] {cidr} -----------                   
    
  
           [ELB] {listeners} {sg}
             |
     -----------------     
     |                |
   [EC2] {sg}      [EC2] {sg}      
     |
  (volume) {cmk}


```


### TESTING

##### FLOW

1. Enumerate resources
2. Build logical structure of infra from depends on 
3. Analyse infra pattern
4. Determine conditions from pattern
5. Select tests


##### RESOURCES

- VPC CIDR
- ROUTE TABLE - ROUTES
- SUBNET CIDRs
- ELB - SGs, LISTENERS
- EC2 - SGs, ROOT VOL + ENCRYPTED / CMK 

##### CONDITIONAL

- How many tiers? Number of subnets





