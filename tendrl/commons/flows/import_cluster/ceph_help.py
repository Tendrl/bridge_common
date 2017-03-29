# flake8: noqa
import json
import subprocess

import pkg_resources
from ruamel import yaml

from tendrl.commons.utils import ansible_module_runner

def import_ceph():
    logging_file_name = "ceph-integration_logging.yaml"
    logging_config_file_path = "/etc/tendrl/ceph-integration/"
    attributes = {}
    if NS.config.data['package_source_type'] == 'pip':
        _cmd = "nohup tendrl-ceph-integration &"
        name = "https://github.com/Tendrl/ceph-integration/archive/master.tar.gz"
        attributes["name"] = name
        attributes["editable"] = "false"
        ansible_module_path = "core/packaging/language/pip.py"
    elif NS.config.data['package_source_type'] == 'rpm':
        name = "tendrl-ceph-integration"
        _cmd = "systemctl restart %s" % name
        ansible_module_path = "core/packaging/os/yum.py"
        attributes["name"] = name
    else:
        return False

    try:
        runner = ansible_module_runner.AnsibleRunner(
            ansible_module_path,
            **attributes
        )
        runner.run()
    except ansible_module_runner.AnsibleExecutableGenerationFailed:
        return False
    
    with open(logging_config_file_path + logging_file_name,
              'w+') as f:
        f.write(pkg_resources.resource_string(__name__, logging_file_name))

    config_data = {"etcd_port": int(NS.config.data['etcd_port']),
                   "etcd_connection": str(NS.config.data['etcd_connection']),
                   "log_cfg_path": logging_config_file_path + logging_file_name,
                   "log_level": "DEBUG",
                    "logging_socket_path": "/var/run/tendrl/message.sock",
                    "tags": json.dumps(["tendrl/integration/ceph"])}
    with open("/etc/tendrl/ceph-integration/ceph-integration.conf.yaml",
              'w') as outfile:
        yaml.dump(config_data, outfile, default_flow_style=False)
    
    subprocess.Popen(_cmd.split())
