import json
import uuid

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons.objects.job import Job

def to_camel_case(snake_str):
    return "".join(x.title() for x in snake_str.split('_'))

def ceph_create_ssh_setup_jobs(parameters):
    node_list = parameters['Node[]']
    ssh_job_ids = []
    ssh_setup_script = NS.ceph_provisioner.get_plugin().setup()
    if len(node_list) > 1:
        for node in node_list:
            if NS.node_context.node_id != node:
                new_params = parameters.copy()
                new_params['Node[]'] = [node]
                new_params['ssh_setup_script'] = ssh_setup_script
                # create same flow for each node in node list except $this
                payload = {
                    "node_ids": [node],
                    "run": "tendrl.flows.SetupSsh",
                    "status": "new",
                    "parameters": new_params,
                    "parent": parameters['job_id'],
                    "type": "node"
                }
                _job_id = str(uuid.uuid4())
                Job(job_id=_job_id,
                    status="new",
                    payload=json.dumps(payload)).save()
                ssh_job_ids.append(_job_id)
                Event(
                    Message(
                        job_id=parameters['job_id'],
                        flow_id=parameters['flow_id'],
                        priority="info",
                        publisher=NS.publisher_id,
                        payload={"message": "Created SSH setup job %s for node"
                                            " %s" % (_job_id, node)
                                 }
                    )
                )
    return ssh_job_ids

def gluster_create_ssh_setup_jobs(parameters):
    node_list = parameters['Node[]']
    ssh_job_ids = []
    ssh_key, err = NS.gluster_provisioner.get_plugin().setup()
    if err != "":
        Event(
            Message(
                job_id=parameters['job_id'],
                flow_id=parameters['flow_id'],
                priority="error",
                publisher=NS.publisher_id,
                payload={"message": "Error generating ssh key"
                         }
            )
        )
        return ssh_job_ids

    for node in node_list:
        new_params = parameters.copy()
        new_params['Node[]'] = [node]
        new_params['ssh_key'] = ssh_key
        # Create same flow for each node from list except this one
        payload = {
            "node_ids": [node],
            "run": "tendrl.flows.AuthorizeSshKey",
            "status": "new",
            "parameters": new_params,
            "parent": parameters['job_id'],
            "type": "node"
        }
        _job_id = str(uuid.uuid4())
        Job(
            job_id=_job_id,
            status="new",
            payload=json.dumps(payload)
        ).save()
        ssh_job_ids.append(_job_id)
        Event(
            Message(
                job_id=parameters['job_id'],
                flow_id=parameters['flow_id'],
                priority="info",
                publisher=NS.publisher_id,
                payload={"message": "Created SSH setup job %s for node %s" %
                                    (_job_id, node)
                         }
            )
        )
    return ssh_job_ids

