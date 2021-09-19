"""
===============================
Terraform tfstate lookup plugin
===============================

Author: Nicholas Birdsall
Version: 0.1

Date: 30/07/2019

Description:

  Ansible lookup plugin to lookup resources in Terraform state file

<br>
"""

import json
import os
import requests
import yaml
from collections import OrderedDict, defaultdict

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_text, to_native

try:
    import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()

#  Terrraform version 12 as default
#  --------------------------------
_terraform_version = 'v12'


# noinspection PyMissingOrEmptyDocstring
class LookupModule(LookupBase):
    """
    Main class for tfstate lookup package
    """

    def run(self, terms, variables=None, terraform_version=None, **kwargs):
        """
        Run function
        This is the main function than Ansible expects as the hook for when it is called within a task

        :param terms:
        :param variables:
        :param kwargs:
        :rtype: list
        :return: A list containing all or any subset of attributes from the tfstate file
                 Strict convention is returning a list object, any structure can be contained in a list
        returned
        """

        global lookupfile, tfstate_resource_attributes_schema, lookup_args
        lookup_args = kwargs

        #  Attributes in the Terraforem state schema for version 0.12.x
        #  (see above where this is assigned: '_terraform_version' = 'v12')
        #  Values for keys in this dict are updated with attributes from the statefile
        if terraform_version:
            _terraform_version = terraform_version

        (assets, artifacts, module_paths) = ([], [], [])
        (contents_json, tfstate_dict, lookupfile) = (None, None, None)

        self.__valid_lookup_arguments = ['attributes', 'reshape']

        tfstate_resource_attributes_schema = OrderedDict({
            'v12': {
                'module': '',
                'name': '',
                'mode': '',
                'type': '',
                'list': '',
                'provider': ''
            }})

        tfstate_resource_instance_attributes_schema = OrderedDict({
            'v12': {
                'module': '',
                'name': '',
                'mode': '',
                'type': '',
                'list': '',
                'provider': '',
                'instances': ''
            }})

        # tfstate_resource_instances_attributes_schema = OrderedDict({
        #     'v12': {
        # "instances": [
        #     {
        #         "schema_version": 0,
        #         "attributes": {
        #             "architecture": "x86_64",
        #             "block_device_mappings": [
        #                 {
        #                     "device_name": "/dev/sda1",
        #                     "ebs": {
        #                         "delete_on_termination": "false",
        #                         "encrypted": "false",
        #                         "iops": "0",
        #                         "snapshot_id": "snap-010d360e3cba720ba",
        #                         "volume_size": "8",
        #                         "volume_type": "gp2"
        #                     },
        #                     "no_device": "",
        #                     "virtual_name": ""
        #                 }
        #             ],
        #             "creation_date": "2019-01-30T23:40:58.000Z",
        #             "description": "CentOS Linux 7 x86_64 HVM EBS ENA 1901_01",
        #             "executable_users": null,
        #             "filter": [
        #                 {
        #                     "name": "product-code",
        #                     "values": [
        #                         "aw0evgkw8e5c1q413zgy5pjce"
        #                     ]
        #                 }
        #             ],
        #             "hypervisor": "xen",
        #             "id": "ami-02eac2c0129f6376b",
        #             "image_id": "ami-02eac2c0129f6376b",
        #             "image_location": "aws-marketplace/CentOS Linux 7 x86_64 HVM EBS ENA 1901_01-b7ee8a69-ee97-4a49-9e68-afaee216db2e-ami-05713873c6794f575.4",
        #             "image_owner_alias": "aws-marketplace",
        #             "image_type": "machine",
        #             "kernel_id": null,
        #             "most_recent": true,
        #             "name": "CentOS Linux 7 x86_64 HVM EBS ENA 1901_01-b7ee8a69-ee97-4a49-9e68-afaee216db2e-ami-05713873c6794f575.4",
        #             "name_regex": null,
        #             "owner_id": "679593333241",
        #             "owners": [
        #                 "aws-marketplace"
        #             ],
        #             "platform": null,
        #             "product_codes": [
        #                 {
        #                     "product_code_id": "aw0evgkw8e5c1q413zgy5pjce",
        #                     "product_code_type": "marketplace"
        #                 }
        #             ],
        #             "public": true,
        #             "ramdisk_id": null,
        #             "root_device_name": "/dev/sda1",
        #             "root_device_type": "ebs",
        #             "root_snapshot_id": "snap-010d360e3cba720ba",
        #             "sriov_net_support": "simple",
        #             "state": "available",
        #             "state_reason": {
        #                 "code": "UNSET",
        #                 "message": "UNSET"
        #             },
        #             "tags": {},
        #             "virtualization_type": "hvm"
        #         }
        #     }

        for term in terms:
            """
            When the playbook specifies a lookup, this method is run. 
            The arguments to the lookup become the arguments to this method. 
            One additional keyword argument named ``variables`` is added to the method call. 
            It contains the variables available to ansible at the time the lookup is templated. 
            For instance::  "{{ lookup('tfstate', 'template/terraform.tfstate"', attributes='modules') }}
            """
            lookupfile = self.find_file_in_search_path(variables, 'files', term)

            try:
                if lookupfile:
                    b_contents, _ = self._loader._get_file_contents(lookupfile)

                    contents = to_text(b_contents, errors='surrogate_or_strict')
                    contents_json = json.loads(contents)
                    tfstate_dict = OrderedDict(contents_json)

            except AnsibleParserError:
                print(AnsibleError("could not locate file in lookup: {}".format(term)))
                raise
            except AnsibleError as e:
                print(AnsibleError('Something happened, this was original exception: %s' % to_native(e)))
                raise
            except Exception as e:
                print('An unexpected exception happened', str(e))
                raise

            try:
                # Build module paths
                module_path_lists = get_tfstate_modules(contents_json['resources'])
                module_name_attributes, module_all_attributes = get_tfstate_attributes(contents_json['resources'],
                                                                                       lookup_args)

                print('KWARGS', kwargs)

                # DEFAULT: No arguments were passed to function, just return the json of statefile
                if not any(k in lookup_args for k in ('section', 'attributes')):
                    artifacts = [dict(tfstate_dict)]
                    return artifacts

                # Handle the cases where 'attributes' has been passed as argument
                if 'attributes' in lookup_args:
                    if lookup_args['attributes'] == 'list':
                        return [module_path_lists]

                    if lookup_args['attributes'] == 'modules':
                        return module_name_attributes

                    if lookup_args['attributes'] == 'all':
                        return module_all_attributes

                    if lookup_args['attributes'] == 'instances':
                        # Add instance keys to module all attributes
                        return module_all_attributes

                # Process option to return specific sections
                if 'section' in kwargs:
                    assets = contents_json[kwargs['section']]


            except AnsibleParserError:
                print(AnsibleError('Something happened, this was original exception: %s' % to_native(e)))
                raise
            except AnsibleError as e:
                print(AnsibleError('Something happened, this was original exception: %s' % to_native(e)))
            except Exception as e:
                print('An unexpected exception happened', str(e))
                raise

        return artifacts


def enumerate_assets(modules_list, enumerate_key):
    """
    Function to enumerate assets objects in a list and return an identifier attribute for each
    """
    module_objects = []
    for module in modules_list:
        module_objects.append({enumerate_key: module[enumerate_key]})
    return module_objects


def get_tfstate_modules(resources):
    """
    Function to enumerate assets objects in a list and return an identifier attribute for each
    """
    modules = set()
    for resource in resources:
        if 'module' not in resource:
            modules.add('root')
        else:
            modules.add(resource['module'])
    return list(modules)


def get_tfstate_attributes(resources, lookup_args):
    """
    Function get_tfstate_attributes

    Generates a simple list of module path and resource names for each resource
    Generates a list of all module attributes for every resource

    :param lookup_args: arguments passed into top level lookup method, as kwargs
    :type lookup_args: kwargs
    :param resources: main body of tfstate data that contains all resource definitions
    :return: Two lists: One of module path and name for every resource,
             and one of all module attributes for each resource
    """

    try:
        # module_name_attributes is simple list of module path and resource name for each resource
        # module_all_attributes is the list of all module attributes for each resource
        # module_all_instance_attribute_keys is the list of all module instance attribute keys for each resource
        [module_name_attributes, module_all_attributes, module_all_instance_attribute_keys] = ([], [], [])

        for resource in resources:

            # 'terraform_version' = 'v12'
            tfstate_resource_attributes_dict = tfstate_resource_attributes_schema[_terraform_version]

            # If 'module' key is absent, the resource is at the root level, and assign 'root' to new key
            if 'module' not in resource:
                resource['module'] = 'root'

            module_name_attributes_dict = {'name': resource['name'], 'module': resource['module']}

            # Update the tfstate resource schema defined in this class, with all resource attributes
            [tfstate_resource_attributes_dict.update({k: resource[k]}) for k in dict(
                tfstate_resource_attributes_dict)
             if k in resource]

            # Update the tfstate resource schema with module names and paths
            tfstate_resource_attributes_dict.update(module_name_attributes_dict)

            # Add all module attributes for current resource to list
            module_all_attributes.append(dict(tfstate_resource_attributes_dict))
            # Add current module path and resource name to list
            module_name_attributes.append(module_name_attributes_dict)

            # Add all instance attribute keys to list
            for instance in resource['instances']:
                module_all_instance_attribute_keys.append(instance.keys())

        # Reshape option passed in as argument of lookup function handled here
        # Depending on type, default data structure is transformed
        # Reshape options are: ['merge', 'flatten', '1l', '2l']
        if 'reshape' in lookup_args:
            module_name_attributes, module_all_attributes = merge_data_structure(module_name_attributes,
                                                                                 module_all_attributes)

    except AnsibleError as e:
        AnsibleError('Something happened, this was original exception: %s' % to_native(e))
    except Exception as e:
        print('An unexpected exception happened', str(e))
        raise

    return module_name_attributes, module_all_attributes


def merge_data_structure(module_name_attributes, module_all_attributes):
    """
    Function that merges the data structures
    :param module_name_attributes:
    :param module_all_attributes:
    :return:
    """
    if 'reshape' in lookup_args:
        if lookup_args['reshape'] == 'merge':
            module_name_attributes_reshaped = [{i['name']: i['module']} for i in module_name_attributes]
            module_name_attributes = module_name_attributes_reshaped

            module_all_attributes_reshaped = {i['module']: [] for i in module_all_attributes}
            for resource in module_all_attributes:
                module_all_attributes_reshaped[resource['module']].append(resource)
            module_all_attributes = [module_all_attributes_reshaped]

    return module_name_attributes, module_all_attributes


def add_instance_attributes():
    """

    :return:
    """
    return []


def enumerate_module_paths(module_path_lists):
    """
    Function to enumerate paths for each module in statefile and build a path for each
    :return:
    :param module_path_lists:
    :return:
    """
    module_paths = []
    for paths in module_path_lists:
        module_path_groups = paths['path']
        module_paths.append('.'.join(module_path_groups))
    return module_paths


def enumerate_attributes(module_path_lists, modules_list, enumerate_key):
    """
    Function to enumerate paths for each module in statefile and build a path for each
    :type modules_list: list of all enumerated modules from statefile
    :return:
    :param modules_list:
    :param enumerate_key:
    :param module_path_lists:
    :return:
    """
    asset_resources = []

    for path, asset in list(zip(module_path_lists, modules_list)):

        if enumerate_key == 'resources':
            selected_resources = list(asset['resources'].keys())
            for resource in selected_resources:
                asset_resources.append({
                    'path': path,
                    'resource': resource,
                    'resource_attributes': asset['resources'][resource]
                })

        if enumerate_key == 'outputs':
            selected_outputs = list(asset['outputs'].keys())
            for output in selected_outputs:
                asset_resources.append({
                    'path': path,
                    'output': output,
                    'output_attributes': asset['outputs'][output]
                })

    return asset_resources


def parse_enumerations(enumerate_key):
    """
    Function to parse enumerations
    :param enumerate_key:
    """
    if enumerate_key == 'path':
        print("TODO")
