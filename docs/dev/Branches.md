# Git branching model

## `main` branch

All new features and bugfixes will first be merged into the main branch. The `Major.Minor` version number will follow those from Netbox with which the plugin is compatible.

## `netbox/vX.Y` branches

After a new Netbox release is published the state of the main branch is copied into a new `netbox/vX.Y` branch. For example after the release of Netbox 3.4 the `main` branch will be copied to `netbox/v3.3`. Only after that copy is made changes for Netbox 3.4 can be merged into `main`.
These branches are in maintenance mode. No new feature will be merged but bugfixes can be backported from `main` if they are relevant.
