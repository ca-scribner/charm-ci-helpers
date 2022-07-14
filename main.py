from pathlib import Path
import yaml
from juju import Juju


def load_bundle(bundle_file):
    return yaml.safe_load(Path(bundle_file).read_text())



def main(source_bundle_file: str, output_bundle_file: str):
    bundle = load_bundle(source_bundle_file)
    applications = bundle['applications']

    for name, application in applications.items():
        # Skip charms we're not "tracking" a channel for
        if "_tracked_channel" not in application:
            continue

        charm_name = application["charm"]
        charm_info = Juju.info(charm_name)
        try:
            tracked_channel_revision = charm_info["channel-map"][application["_tracked_channel"]]["revision"]
            if application["revision"] != tracked_channel_revision:
                # If revision is not up to date - update in situ from tracked channel
                application["revision"] = tracked_channel_revision
        except Exception as e:
            print("I should handle some of these")
            raise e

    with open(output_bundle_file, 'w') as fout:
        yaml.dump(bundle, fout)



if __name__ == "__main__":
    import typer
    typer.run(main)
