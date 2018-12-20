# -*- coding: utf-8 -*-

"""
A self-paced walkthrough of version control using NiFi-Registry.
See initial print statement for detailed explanation.
"""

from __future__ import absolute_import
import logging
from time import sleep
import nipyapi
from nipyapi.utils import DockerContainer

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.getLogger('nipyapi.versioning').setLevel(logging.INFO)
logging.getLogger('nipyapi.utils').setLevel(logging.INFO)

d_network_name = 'fdlcdemo'

dev_nifi_port = 8080
prod_nifi_port = 9090
dev_reg_port = dev_nifi_port + 1
prod_reg_port = prod_nifi_port + 1

dev_nifi_url = 'http://localhost:' + str(dev_nifi_port) + '/nifi'
prod_nifi_url = 'http://localhost:' + str(prod_nifi_port) + '/nifi'
dev_reg_url = 'http://localhost:' + str(dev_reg_port) + '/nifi-registry'
prod_reg_url = 'http://localhost:' + str(prod_reg_port) + '/nifi-registry'

dev_nifi_api_url = dev_nifi_url + '-api'
prod_nifi_api_url = prod_nifi_url + '-api'
dev_reg_api_url = dev_reg_url + '-api'
prod_reg_api_url = prod_reg_url + '-api'

d_containers = [
    DockerContainer(
        name='nifi-dev',
        image_name='apache/nifi',
        image_tag='latest',
        ports={str(dev_nifi_port) + '/tcp': dev_nifi_port},
        env={'NIFI_WEB_HTTP_PORT': str(dev_nifi_port)}
    ),
    DockerContainer(
        name='nifi-prod',
        image_name='apache/nifi',
        image_tag='latest',
        ports={str(prod_nifi_port) + '/tcp': prod_nifi_port},
        env={'NIFI_WEB_HTTP_PORT': str(prod_nifi_port)}
    ),
    DockerContainer(
        name='reg-dev',
        image_name='apache/nifi-registry',
        image_tag='latest',
        ports={str(dev_reg_port) + '/tcp': dev_reg_port},
        env={'NIFI_REGISTRY_WEB_HTTP_PORT': str(dev_reg_port)}
    ),
    DockerContainer(
        name='reg-prod',
        image_name='apache/nifi-registry',
        image_tag='latest',
        ports={str(prod_reg_port) + '/tcp': prod_reg_port},
        env={'NIFI_REGISTRY_WEB_HTTP_PORT': str(prod_reg_port)}
    )
]

dev_pg_name = 'my_pg_0'
dev_proc_name = 'my_proc_0'
dev_proc2_name = 'my_s_proc_0'
dev_reg_client_name = 'dev_reg_client_0'
dev_bucket_name = 'dev_bucket_0'
dev_ver_flow_name = 'dev_ver_flow_0'
dev_flow_export_name = 'dev_flow_export_0'
prod_bucket_name = 'prod_bucket_0'
prod_ver_flow_name = 'prod_ver_flow_0'
prod_reg_client_name = 'prod_reg_client_0'

print("This python script demonstrates the steps to manage promotion of "
      "versioned Flows between different environments. \nIt deploys NiFi and "
      "NiFi-Registry in local Docker containers and illustrates the "
      "steps you might follow in such a process."
      "\nEach step is presented as a function of this script, they count up "
      "in hex (0,1,2,3,4,5,6,7,8,9,a,b,c,d) and should be called in order."
      "\nEach step will log activities to INFO, and you are encouraged to "
      "look at the code in this script to see how each step is completed."
      "\nhttp://github.com/Chaffelson/nipyapi/blob/master/nipyapi/demo/fdlc.py"
      "\nEach step will also issue instructions through print statements like "
      "this one, these instructions will vary so please read them as you go."
      "\nNote that the first call will log a lot of information while it boots"
      " the Docker containers, further instructions will follow."
      "\nNote that you can reset it at any time by calling step_1 again.\n"
      "\nPlease start by calling the function 'step_1_boot_demo_env()'.")


def step_1_boot_demo_env():
    """step_1_boot_demo_env"""
    log.info("Starting Dev and Prod NiFi and NiFi-Registry Docker Containers"
             "\nPlease wait, this may take a few minutes to download the "
             "Docker images and then start them.")
    nipyapi.utils.start_docker_containers(
        docker_containers=d_containers,
        network_name=d_network_name
    )
    for reg_instance in [dev_reg_api_url, prod_reg_api_url]:
        log.info("Waiting for NiFi Registries to be ready")
        nipyapi.utils.set_endpoint(reg_instance)
        nipyapi.utils.wait_to_complete(
            test_function=nipyapi.utils.is_endpoint_up,
            endpoint_url='-'.join(reg_instance.split('-')[:-1]),
            nipyapi_delay=nipyapi.config.long_retry_delay,
            nipyapi_max_wait=nipyapi.config.long_max_wait
        )
    for nifi_instance in [dev_nifi_api_url, prod_nifi_api_url]:
        log.info("Waiting for NiFi instances to be ready")
        nipyapi.utils.set_endpoint(nifi_instance)
        nipyapi.utils.wait_to_complete(
            test_function=nipyapi.utils.is_endpoint_up,
            endpoint_url='-'.join(nifi_instance.split('-')[:-1]),
            nipyapi_delay=nipyapi.config.long_retry_delay,
            nipyapi_max_wait=nipyapi.config.long_max_wait
        )
        # Sleeping to wait for all startups to return before printing guide
        sleep(1)
    print("Your Docker containers should now be ready, please find them at the"
          "following URLs:"
          "\nnifi-dev   ", dev_nifi_url,
          "\nreg-dev    ", dev_reg_url,
          "\nreg-prod   ", prod_reg_url,
          "\nnifi-prod  ", prod_nifi_url,
          "\nPlease open each of these in a browser tab."
          "\nPlease then call the function 'step_2_create_reg_clients()'\n")


def step_2_create_reg_clients():
    """Set client connections between NiFi and Registry"""
    log.info("Creating Dev Environment Nifi to NiFi-Registry Client")
    nipyapi.utils.set_endpoint(dev_nifi_api_url)
    nipyapi.versioning.create_registry_client(
        name=dev_reg_client_name,
        uri='http://reg-dev:8081',
        description=''
    )
    log.info("Creating Prod Environment Nifi to NiFi-Registry Client")
    nipyapi.utils.set_endpoint(prod_nifi_api_url)
    nipyapi.versioning.create_registry_client(
        name=prod_reg_client_name,
        uri='http://reg-prod:9091',
        description=''
    )
    print("We have attached each NiFi environment to its relevant Registry "
          "for upcoming Version Control activities."
          "\nYou can see these by going to NiFi, clicking on the 3Bar menu "
          "icon in the top right corner, selecting 'Controller Settings', and"
          " looking at the 'Registry Clients' tab."
          "\nPlease now call 'step_3_create_dev_flow()'\n")


def step_3_create_dev_flow():
    """Connecting to Dev environment and creating some test objects"""
    log.info("Connecting to Dev environment and creating some test objects")
    nipyapi.utils.set_endpoint(dev_nifi_api_url)
    nipyapi.utils.set_endpoint(dev_reg_api_url)

    log.info("Creating %s as an empty process group", dev_pg_name)
    dev_process_group_0 = nipyapi.canvas.create_process_group(
        nipyapi.canvas.get_process_group(nipyapi.canvas.get_root_pg_id(),
                                         'id'),
        dev_pg_name,
        location=(400.0, 400.0)
    )
    log.info("Creating dev_processor_0 as a new GenerateFlowFile in the PG")
    nipyapi.canvas.create_processor(
        parent_pg=dev_process_group_0,
        processor=nipyapi.canvas.get_processor_type('GenerateFlowFile'),
        location=(400.0, 400.0),
        name=dev_proc_name,
        config=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='1s',
            auto_terminated_relationships=['success']
        )
    )
    print("We have procedurally generated a new Process Group with a child "
          "Processor in Dev NiFi. It is not yet version controlled."
          "\nGo to your Dev NiFi browser tab, and refresh to see the new "
          "Process Group, open the Process Group to see the new Generate "
          "FlowFile Processor. Open the Processor and look at the Scheduling "
          "tab to note that it is set to 1s."
          "\nPlease now call 'step_4_create_dev_ver_bucket()'\n")


def step_4_create_dev_ver_bucket():
    """Creating dev registry bucket"""
    log.info("Creating %s as new a Registry Bucket", dev_bucket_name)
    nipyapi.versioning.create_registry_bucket(dev_bucket_name)
    print("We have created a new Versioned Flow Bucket in the Dev "
          "NiFi-Registry. Please go to the Dev Registry tab in your browser "
          "and refresh, then click the arrow next to 'All' in the page header "
          "to select the new bucket and see that it is currently empty."
          "\nPlease now call 'step_5_save_flow_to_bucket()'\n")


def step_5_save_flow_to_bucket():
    """Saving the flow to the bucket as a new versioned flow"""
    log.info(
        "Saving %s to %s", dev_pg_name, dev_bucket_name)
    process_group = nipyapi.canvas.get_process_group(dev_pg_name)
    bucket = nipyapi.versioning.get_registry_bucket(dev_bucket_name)
    registry_client = nipyapi.versioning.get_registry_client(
        dev_reg_client_name)
    nipyapi.versioning.save_flow_ver(
        process_group=process_group,
        registry_client=registry_client,
        bucket=bucket,
        flow_name=dev_ver_flow_name,
        desc='A Versioned Flow',
        comment='A Versioned Flow'
    )
    print("We have now saved the Dev Process Group to the Dev Registry bucket "
          "as a new Versioned Flow. Return to the Dev Registry tab in your "
          "browser and refresh to see the flow. Click on the flow to show "
          "some details, note that it is version 1."
          "\nPlease note that the next function requires that you save the "
          "output to a variable when you continue."
          "\nPlease now call 'flow = step_6_export_dev_flow()'\n")


def step_6_export_dev_flow():
    """Exporting the versioned flow as a yaml definition"""
    log.info("Creating a sorted pretty Yaml export of %s",
             dev_flow_export_name)
    bucket = nipyapi.versioning.get_registry_bucket(dev_bucket_name)
    ver_flow = nipyapi.versioning.get_flow_in_bucket(
        bucket.identifier,
        identifier=dev_ver_flow_name
    )
    out = nipyapi.versioning.export_flow_version(
        bucket_id=bucket.identifier,
        flow_id=ver_flow.identifier,
        mode='yaml'
    )
    print("We have now exported the versioned Flow from the Dev environment as"
          " a formatted YAML document, which is one of several options. Note "
          "that you were asked to save it as the variable 'flow' so you can "
          "then import it into your Prod environment."
          "\nIf you want to view it, call 'print(flow)'."
          "\nWhen you are ready, please call 'step_7_create_prod_ver_bucket()'"
          "\n")
    return out


def step_7_create_prod_ver_bucket():
    """Connecting to the Prod environment and creating a new bucket"""
    log.info("Connecting to Prod Environment")
    nipyapi.utils.set_endpoint(prod_nifi_api_url)
    nipyapi.utils.set_endpoint(prod_reg_api_url)
    log.info("Creating %s as a new Registry Bucket", prod_bucket_name)
    nipyapi.versioning.create_registry_bucket(prod_bucket_name)
    print("We have now created a bucket in the Prod Registry to promote our "
          "Dev flow into. Go to the Prod Registry tab and click the arrow next"
          " to 'All' to select it and see that it is currently empty."
          "\nPlease note that the next function requires that you supply the "
          "variable you saved from step 5."
          "\nPlease call 'step_8_import_dev_flow_to_prod_reg(flow)'\n")


def step_8_import_dev_flow_to_prod_reg(versioned_flow):
    """Importing the yaml string into Prod"""
    log.info("Saving dev flow export to prod container")
    bucket = nipyapi.versioning.get_registry_bucket(prod_bucket_name)
    nipyapi.versioning.import_flow_version(
        bucket_id=bucket.identifier,
        encoded_flow=versioned_flow,
        flow_name=prod_ver_flow_name
    )
    print("The flow we exported from Dev is now imported into the bucket in "
          "the Prod Registry, and ready for deployment to the Prod NiFi."
          "\nPlease refresh your Prod Registry and you will see it, note that"
          " it is version 1 and has the same comment as the Dev Flow Version."
          "\nPlease then call 'step_9_deploy_prod_flow_to_nifi()'\n")


def step_9_deploy_prod_flow_to_nifi():
    """Deploying the flow to the Prod environment"""
    log.info("Deploying promoted flow from Prod Registry to Prod Nifi")
    bucket = nipyapi.versioning.get_registry_bucket(prod_bucket_name)
    flow = nipyapi.versioning.get_flow_in_bucket(
        bucket_id=bucket.identifier,
        identifier=prod_ver_flow_name
    )
    reg_client = nipyapi.versioning.get_registry_client(prod_reg_client_name)
    nipyapi.versioning.deploy_flow_version(
        parent_id=nipyapi.canvas.get_root_pg_id(),
        location=(0, 0),
        bucket_id=bucket.identifier,
        flow_id=flow.identifier,
        reg_client_id=reg_client.id,
        version=None
    )
    print("The Promoted Flow has now been deployed to the Prod NiFi, please "
          "refresh the Prod NiFi tab and note that the Process Group has the "
          "same name as the Dev Process Group, and has a green tick(√) "
          "indicating it is up to date with Version Control. "
          "\n Open the Process Group and note that the Processor is also the "
          "same, including the Schedule of 1s."
          "\nPlease now call 'step_a_change_dev_flow()'\n")


def step_a_change_dev_flow():
    """Procedurally modifying the Dev flow"""
    log.info("Connecting to Dev Environment")
    nipyapi.utils.set_endpoint(dev_nifi_api_url)
    nipyapi.utils.set_endpoint(dev_reg_api_url)
    log.info("Modifying Dev Processor Schedule")
    processor = nipyapi.canvas.get_processor(dev_proc_name)
    nipyapi.canvas.update_processor(
        processor=processor,
        update=nipyapi.nifi.ProcessorConfigDTO(
            scheduling_period='3s'
        )
    )
    print("Here we have made a simple modification to the processor in our Dev"
          "Flow. \nGo to the Dev NiFi tab and refresh it, you will see that "
          "the Process Group now has a star(*) icon next to the name, "
          "indicating there are unsaved changes. Look at the Scheduling tab "
          "in the Processor and note that it has changed from 1s to 3s."
          "\nPlease now call 'step_b_update_dev_flow_ver()'\n")


def step_b_update_dev_flow_ver():
    """Committing the change to the dev flow version"""
    log.info("Saving changes in Dev Flow to Version Control")
    process_group = nipyapi.canvas.get_process_group(dev_pg_name)
    bucket = nipyapi.versioning.get_registry_bucket(dev_bucket_name)
    registry_client = nipyapi.versioning.get_registry_client(
        dev_reg_client_name)
    flow = nipyapi.versioning.get_flow_in_bucket(
        bucket_id=bucket.identifier,
        identifier=dev_ver_flow_name
    )
    nipyapi.versioning.save_flow_ver(
        process_group=process_group,
        registry_client=registry_client,
        bucket=bucket,
        flow_id=flow.identifier,
        comment='An Updated Flow'
    )
    print("We have saved the change to the Dev Registry as a new version."
          "\nRefresh the Dev Registry to see that the Flow now has a version "
          "2, and a new comment."
          "\nRefresh the Dev NiFi to see that the Process Group now has a "
          "green tick again, indicating that Version Control is up to date."
          "\nPlease now call 'step_c_promote_change_to_prod_reg()'\n")


def step_c_promote_change_to_prod_reg():
    """Promoting the committed change across to the prod environment"""
    log.info("Exporting updated Dev Flow Version")
    dev_bucket = nipyapi.versioning.get_registry_bucket(dev_bucket_name)
    dev_ver_flow = nipyapi.versioning.get_flow_in_bucket(
        dev_bucket.identifier,
        identifier=dev_ver_flow_name
    )
    dev_export = nipyapi.versioning.export_flow_version(
        bucket_id=dev_bucket.identifier,
        flow_id=dev_ver_flow.identifier,
        mode='yaml'
    )
    log.info("Connecting to Prod Environment")
    nipyapi.utils.set_endpoint(prod_nifi_api_url)
    nipyapi.utils.set_endpoint(prod_reg_api_url)
    log.info("Pushing updated version into Prod Registry Flow")
    prod_bucket = nipyapi.versioning.get_registry_bucket(prod_bucket_name)
    prod_flow = nipyapi.versioning.get_flow_in_bucket(
        bucket_id=prod_bucket.identifier,
        identifier=prod_ver_flow_name
    )
    nipyapi.versioning.import_flow_version(
        bucket_id=prod_bucket.identifier,
        encoded_flow=dev_export,
        flow_id=prod_flow.identifier
    )
    print("We have promoted the change from our Dev Registry to Prod, please "
          "refresh your Prod Registry Tab to see the new version is present, "
          "and that the new comment matches the Dev Environment."
          "\nRefresh your Prod NiFi tab to see that the Process Group has a "
          "red UpArrow(⬆︎) icon indicating a new version is available for "
          "deployment."
          "\nPlease now call 'step_d_promote_change_to_prod_nifi()'\n")


def step_d_promote_change_to_prod_nifi():
    """Pushing the change into the Prod flow"""
    log.info("Moving deployed Prod Process Group to the latest version")
    prod_pg = nipyapi.canvas.get_process_group(dev_pg_name)
    nipyapi.versioning.update_flow_ver(
        process_group=prod_pg,
        target_version=None
    )
    print("Refresh your Prod NiFi to see that the PG now shows the green tick "
          "of being up to date with its version control."
          "\nLook at the Processor scheduling to note that it now matches the "
          "dev environment as 3s."
          "\nNow we will examine some typical deployment tests."
          "\nPlease now call 'step_e_check_sensitive_processors()'\n")


def step_e_check_sensitive_processors():
    """Create and test for Sensitive Properties to be set in the Canvas"""
    log.info("Connecting to Dev Environment")
    nipyapi.utils.set_endpoint(dev_nifi_api_url)
    nipyapi.utils.set_endpoint(dev_reg_api_url)
    log.info("Creating additional complex Processor")
    nipyapi.canvas.create_processor(
        parent_pg=nipyapi.canvas.get_process_group(dev_pg_name),
        processor=nipyapi.canvas.get_processor_type('GetTwitter'),
        location=(400.0, 600.0),
        name=dev_proc2_name,
    )
    s_proc = nipyapi.canvas.list_sensitive_processors(summary=True)
    print("We have created a new Processor {0} which has security protected"
          "properties, these will need to be completed in each environment "
          "that this flow is used in. These properties are discoverable using "
          "the API calls list 'canvas.list_sensitive_processors()'"
          "\nFunction 'nipyapi.canvas.update_processor' as used in step_a is"
          " intended for this purpose"
          "\nPlease no call 'step_f_set_sensitive_values()'\n"
          .format(s_proc[0].status.name, ))


def step_f_set_sensitive_values():
    """Set the Sensitive Properties to pass the deployment test"""
    log.info("Setting Sensitive Values on Processor")
    nipyapi.canvas.update_processor(
        processor=nipyapi.canvas.get_processor(dev_proc2_name),
        update=nipyapi.nifi.ProcessorConfigDTO(
            properties={
                'Consumer Key': 'Some',
                'Consumer Secret': 'Secret',
                'Access Token': 'values',
                'Access Token Secret': 'here'
            }
        )
    )
    print("Here we have set the Sensitive values, again using the Update"
          " process. Typically these values will be looked up in a Config DB "
          "or some other secured service."
          "\nPlease now call 'step_g_check_invalid_processors()'\n")
    # Todo: update sensitive to return properites list precreated


def step_g_check_invalid_processors():
    """Look for Processors with Invalid Properties to be remediated"""
    log.info("Retrieving Processors in Invalid States")
    i_proc = nipyapi.canvas.list_invalid_processors()[0]
    print("We now run a validity test against our flow to ensure that it can "
          "be deployed. We can see that Processors [{0}] need further "
          "attention."
          "\nWe can also easily see the reasons for this [{1}]."
          "\nPlease now call 'step_h_fix_validation_errors()'\n"
          .format(i_proc.status.name, i_proc.component.validation_errors))


def step_h_fix_validation_errors():
    """Update values for Invalid Processors to pass the deployment test"""
    log.info("Autoterminating Success status")
    nipyapi.canvas.update_processor(
        processor=nipyapi.canvas.get_processor(dev_proc2_name),
        update=nipyapi.nifi.ProcessorConfigDTO(
            auto_terminated_relationships=['success']
        )
    )
    print("We now see that our Processor is configured and Valid within this "
          "environment, and is ready for Promotion to the next stage."
          "\nPlease now call 'step_i_promote_deploy_and_validate()'\n")


def step_i_promote_deploy_and_validate():
    """Promotion and Deployment in a single method"""
    log.info("Saving changes in Dev Flow to Version Control")
    dev_process_group = nipyapi.canvas.get_process_group(dev_pg_name)
    dev_bucket = nipyapi.versioning.get_registry_bucket(dev_bucket_name)
    dev_registry_client = nipyapi.versioning.get_registry_client(
        dev_reg_client_name)
    dev_flow = nipyapi.versioning.get_flow_in_bucket(
        bucket_id=dev_bucket.identifier,
        identifier=dev_ver_flow_name
    )
    nipyapi.versioning.save_flow_ver(
        process_group=dev_process_group,
        registry_client=dev_registry_client,
        bucket=dev_bucket,
        flow_id=dev_flow.identifier,
        comment='A Flow update with a Complex Processor'
    )
    dev_ver_flow = nipyapi.versioning.get_flow_in_bucket(
        dev_bucket.identifier,
        identifier=dev_ver_flow_name
    )
    log.info("Exporting the Dev flow to Yaml")
    dev_export = nipyapi.versioning.export_flow_version(
        bucket_id=dev_bucket.identifier,
        flow_id=dev_ver_flow.identifier,
        mode='yaml'
    )
    log.info("Connecting to Prod Environment")
    nipyapi.utils.set_endpoint(prod_nifi_api_url)
    nipyapi.utils.set_endpoint(prod_reg_api_url)
    log.info("Importing the Updated Dev Yaml to the Prod Bucket Flow")
    prod_bucket = nipyapi.versioning.get_registry_bucket(prod_bucket_name)
    prod_flow = nipyapi.versioning.get_flow_in_bucket(
        bucket_id=prod_bucket.identifier,
        identifier=prod_ver_flow_name
    )
    nipyapi.versioning.import_flow_version(
        bucket_id=prod_bucket.identifier,
        encoded_flow=dev_export,
        flow_id=prod_flow.identifier
    )
    log.info("Pushing the new Version into the Prod Flow")
    prod_pg = nipyapi.canvas.get_process_group(dev_pg_name)
    nipyapi.versioning.update_flow_ver(
        process_group=prod_pg,
        target_version=None
    )
    log.info("Checking for Invalid Processors in the new flow")
    val_errors = nipyapi.canvas.list_invalid_processors()
    print("Here we have put all the steps in one place by taking the dev "
          "changes all the way through to prod deployment. If we check"
          " our Processor Validation again, we see that our regular "
          "Properties have been carried through, but our Sensitive "
          "Properties are unset in Production [{0}]"
          "\nThis is because NiFi will not break"
          " security by carrying them to a new environment. We leave setting"
          " them again as an exercise for the user."
          .format(val_errors[0].component.validation_errors))
    print("\nThis is the end of the guide, you may restart at any time by "
          "calling 'step_1_boot_demo_env()'\n")
