import copy
from pathlib import Path
from typing import Optional

from ruamel.yaml import YAML

from deepdiff import DeepDiff
from juju import Juju


class Bundle:
    def __init__(self, filename: Optional[str] = None):
        self._filename = filename
        self._data = None
        if self._filename:
            self.load_bundle()

    def deepcopy(self):
        """Returns a new deep copy of this Bundle"""
        newbundle = copy.deepcopy(self)
        return newbundle

    def diff(self, other):
        """Returns a diff between this and another object, in DeepDiff format"""
        return DeepDiff(self._data, other._data, ignore_order=True)

    def dump(self, filename: str):
        """Dumps as yaml to a file"""
        with open(filename, 'w') as fout:
            yaml = YAML(typ='rt')
            yaml.dump(self.to_dict(), fout)

    def get_latest_revisions(self):
        """Return a new Bundle that has the latest revisions of all charms in this bundle"""
        newbundle = self.deepcopy()

        applications = newbundle.applications

        for name, application in applications.items():
            # Skip charms we're not "tracking" a channel for
            if "_tracked_channel" not in application:
                continue

            charm_name = application["charm"]
            channel = application["_tracked_channel"]
            revision = application.get("revision", None)

            newest_revision = get_newest_charm_revision(charm_name, channel)

            if revision != newest_revision:
                # If revision is not up to date - update in situ from tracked channel
                application["revision"] = newest_revision

        return newbundle

    def load_bundle(self):
        """Loads a YAML file as a bundle"""
        yaml = YAML(typ='rt')
        self._data = yaml.load(Path(self._filename).read_text())

    def to_dict(self):
        return self._data

    def __eq__(self, other):
        return (
            self._filename == other._filename
            and self.diff(other) == {}
        )

    @property
    def applications(self):
        return self._data['applications']


def get_newest_charm_revision(charm: str, channel: str):
    """Returns the newest revision of a charm in a channel"""
    charm_info = Juju.info(charm)
    channel_map = charm_info["channel-map"]
    try:
        tracked_channel_release = channel_map[channel]
    except KeyError:
        raise ValueError(f"No channel {channel} in `juju info {charm} --format yaml`")
    return tracked_channel_release["revision"]
