from pathlib import Path
import yaml


class Bundle:
    def __init__(self, filename: str):
        self._filename = filename
        self._data = None
        self.load_bundle()

    def load_bundle(self):
        self._data = yaml.safe_load(Path(self._filename).read_text())

    @property
    def applications(self):
        return self._data['applications']

    def to_dict(self):
        return self._data

    def dump(self, filename: str):
        """Dumps as yaml to a file"""
        with open(filename, 'w') as fout:
            yaml.dump(self.to_dict(), fout)
