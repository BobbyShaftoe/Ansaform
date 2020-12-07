
# CONCEPTS

## Implicitness of description

Something that we express the names and nature of a domain with 
- Understood
- Agreed
- Adopted
- Adhered
- Answers to questions about our domain
- We're stewards, sheriffs and custodians
- We like it tidy because we dont like cleaning up
- We don't like it when people are loose with it and mess it up
- We like rows
  a. and on each row an observation
  b. and for every relationship there's a column 

## Standards

### Schemas

Use meaningful property names that reflect the semantic type of the value

#### Common Formalised Attributes
1. An accepted standardisation of infrastructure resource within the Public Cloud domain
2. Something that is practiced, not just decided on
3. Confidence in the accuracy and consistency of meta data coming from any source within the Cloud technology value 
chain

```
Development 
          \ VCS --> Branches --> Commits --> Builds --> Build logs
                                           | -- Code analysis --> Insights  \         
                                           | -- Test reports   \             \   
                                           | -- Documentation   \             |                                      
                                           |                     |            |
                                            \                    |  -- ::Working Corpus::     
                                             \
                                              \  -- Deployment --> Infra attribs --> Graph schemas   
                                               \                 | -- Testing -->  reports      \ 
                                                |                                       \        | 
                                                |                                        |       |
                                                | --> --> -->  Graph super schema [pub cloud domain]
                                                                                                \ 
                                                                                                 | -- Reports Analysis 
                                                                                                              \ 
                                                                                                              ::Audit::
                                                                                                             ::Resource::
```
4.  and Solid expectations for consistent 
reliability in 
reporting

#### Data Stewardship
Quite naturally it follows that having an accepted and disciplined practice, describing all 
resources within the infrastructure domain will achieve the desired state:

1. A tidy corpus of all reporting, meta information and documentation, and more importantly, little deviation 
in the schema that describes the domain overall
2. A distributed schema that depends with no dependency on any database service or related network transport; viz. 
any report produced from meta files is a localised graph that has no edge dependencies at the border nodes 






### Complete Project Reference
_"When it comes to releasing software @hashicorp ranks high on the list of maintainers that do it right.
Versioned archives with docs, source, build scripts, and the website._" 

_"OS specific executables; even NetBSD is shown love._" 

_"They also provide Docker images if that's your thing._" 

Kelsey Hightower (@kelseyhightower)  `https://t.co/BPQT3GiDXc`


```
  171  sudo cp Sentinel/sentinel /usr/local/bin
  172  sudo chmod 0755 Sentinel/sentinel /usr/local/bin
  175  sudo -R chmod 0755 Sentinel/sentinel /usr/local/bin
  176  sudo  chmod -R 0755 Sentinel/sentinel /usr/local/bin
  178  sudo  chmod -R 0755  /usr/local/bin/sentinel
  180  sentinel
  187  go get github.com/tapirs/tfjson
  189  go get github.com/tapirs/tfjson
  202  tfjson
  229  tfjson plan.out
  231  sentinel apply -global input="`tfjson plan.out`" policy.tf
  232  sentinel apply -global input="`tfjson plan.out`" tf.policy
  234  sentinel apply -global input="`tfjson plan.out`" tf.policy
  248  terraform plan -help
  249  terraform plan -out=plan.out
  250  terraform-11 plan -out=plan.out
  264  git clone https://github.com/multicloud-iac/terraform-sentinel-policies.git
  265  sentinel apply -global input="`tfjson plan.out`" tf.policy
  266  history | egrep 'json|state|plan'
  267  history | egrep 'json|state|plan|sentinel'
```


```
# file tf.policy
allowed_node_sizes = [
	"s-1vcpu-2gb",
]

allowed_regions = [
	"ams3",
]

allowed_tf_versions = [
	"0.12.0",
]

node_pool_max_size = 3

tf_version = rule {
	input.terraform_version in allowed_tf_versions
}

no_destroys = func() {
	for input.resource_changes as change {
		if change.change.actions contains "destroy" {
			print("No destroys allowed")
			return (false)
		}
	}
	return (true)
}

max_nodepool_size = func() {
	for input.resource_changes as change {
		if change.address contains "digitalocean_kubernetes_cluster" {
			for change.change.after.node_pool as pool {
				if pool.node_count > node_pool_max_size {
					error("Node pool", pool.name, "shouldn't exceed max node size", node_pool_max_size, "it's currently", pool.node_count)
				}
			}
		}
	}
	return (true)
}

region_check = func() {
	for input.configuration.root_module.resources as resource {
		if resource.expressions.region.constant_value not in allowed_regions {
			return (false)
		}
	}
	return (true)
}

node_size = func() {
	for input.resource_changes as change {
		if change.address contains "digitalocean_kubernetes_cluster" {
			for change.change.after.node_pool as pool {
				if pool.size not in allowed_node_sizes {
					return (false)
				}
			}
		}
	}
	return (true)
}

main = rule {
	tf_version and no_destroys() and region_check() and max_nodepool_size() and node_size()
}
```
