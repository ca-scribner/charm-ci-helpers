from bundle import Bundle


def main(source_bundle_file: str, output_bundle_file: str):
    bundle = Bundle(source_bundle_file)
    updated_bundle = bundle.get_latest_revisions()
    print(bundle.diff(updated_bundle))

    updated_bundle.dump(output_bundle_file)


if __name__ == "__main__":
    import typer
    typer.run(main)
