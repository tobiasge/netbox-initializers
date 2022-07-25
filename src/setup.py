from setuptools import find_packages, setup

setup(
    name="netbox-initializers",
    version="3.2",
    description="Load initial data into Netbox",
    install_requires=["ruamel.yaml==0.17.21"],
    packages=find_packages() + ["netbox_initializers.initializers.yaml"],
    package_data={"netbox_initializers.initializers.yaml": ["*.yml"]},
    include_package_data=True,
    zip_safe=False,
)
