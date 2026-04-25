FROM netboxcommunity/netbox:v4.5

COPY ../ /opt/netbox-initializers/
COPY ./test/config/plugins.py /etc/netbox/config/
WORKDIR /opt/netbox-initializers/
RUN /usr/local/bin/uv pip install -e .
WORKDIR /opt/netbox/netbox
