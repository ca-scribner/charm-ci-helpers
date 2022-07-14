from juju import Juju
from bundle import Bundle


def get_newest_charm_revision(charm: str, channel: str):
    """Returns the newest revision of a charm in a channel"""
    charm_info = Juju.info(charm)
    channel_map = charm_info["channel-map"]
    try:
        tracked_channel_release = channel_map[channel]
    except KeyError:
        raise ValueError(f"No channel {channel} in `juju info {charm} --format yaml`")
    return tracked_channel_release["revision"]


def main(source_bundle_file: str, output_bundle_file: str):
    bundle = Bundle(source_bundle_file)
    applications = bundle.applications

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

    bundle.dump(output_bundle_file)


if __name__ == "__main__":
    import typer
    typer.run(main)
