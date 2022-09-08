# Netbox Initializers Plugin

Load data from YAML files into Netbox

## Installation

First activate your virtual environment where Netbox is installed, the install the plugin version correspondig to your Netbox version.
```bash
pip install "netbox-initializers==3.2.*"
```
Then you need to add the plugin to the `PLUGINS` array in the Netbox configuration.
```python
PLUGINS = [
    'netbox_initializers',
]
```

## Getting started

At first you need to start with writing the YAML files that contain the initial data. To make that easier the plugin includes example files for all supported initializers. To access those examples you can copy them into a directory of your choosing and edit them there. To copy the files run the following command (in your Netbox directory):

```bash
./manage.py copy_initializers_examples --path /path/for/example/files
```

After you filled in the data you want to import, the import can be started with this command:

```bash
./manage.py load_initializer_data --path /path/for/example/files
```


## Netbox Docker image

The initializers where a part of the Docker image and where then extracted into a Netbox plugin. This was done to split the release cycle of the initializers and the image.
To use the new plugin in a the Netbox Docker image, it musst be installad into the image. To this, the following example can be used as a starting point:

```dockerfile
FROM netboxcommunity/netbox:v3.2
RUN /opt/netbox/venv/bin/pip install "netbox-initializers==3.2.*"
```
