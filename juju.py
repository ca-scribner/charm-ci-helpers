from subprocess import Popen, PIPE
from ruamel.yaml import YAML


class Juju:
    @staticmethod
    def juju(*args, raise_on_stderr: bool=False):
        cmd = ["juju"] + list(args)
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout = proc.stdout.read().decode('utf-8')
        stderr = proc.stderr.read().decode('utf-8')
        if raise_on_stderr and stderr:
            raise ValueError(f"failed to run juju command successfully.  Got this from stderr: {stderr}")
        return stdout, stderr

    @classmethod
    def info(cls, charm_name: str):
        stdout, stderr = cls.juju("info", charm_name, "--format", "yaml", raise_on_stderr=False)
        failure_message = f"Failed to load valid yaml from `juju info`, got \nSTDERR='{stderr}'\nSTDOUT='{stdout}'"
        try:
            yaml = YAML(typ='rt')
            data_dict = yaml.load(stdout)
        except:
            raise ValueError(failure_message)

        if not data_dict:
            raise ValueError(failure_message)

        return data_dict
