FROM netboxcommunity/netbox:v3.4

COPY ../ /opt/netbox-initializers/
COPY ./test/config/plugins.py /etc/netbox/config/
WORKDIR /opt/netbox-initializers/
RUN /opt/netbox/venv/bin/pip install -e .
WORKDIR /opt/netbox/netbox
