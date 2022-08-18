from setuptools import find_packages, setup

from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / ".." / "README.md").read_text()

setup(
    name="netbox-initializers",
    version="3.2.1",
    description="Load initial data into Netbox",
    install_requires=["ruamel.yaml==0.17.21"],
    packages=find_packages() + ["netbox_initializers.initializers.yaml"],
    package_data={"netbox_initializers.initializers.yaml": ["*.yml"]},
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
