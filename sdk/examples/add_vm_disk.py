#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time

import ovirtsdk4 as sdk
import ovirtsdk4.types as types

# This example will connect to the server and add a disk to an existing
# virtual machine.

# Create the connection to the server:
connection = sdk.Connection(
    url='https://engine40.example.com/ovirt-engine/api',
    username='admin@internal',
    password='redhat123',
    ca_file='ca.pem',
    debug=True,
)

# Locate the virtual machines service and use it to find the virtual
# machine:
vms_service = connection.system_service().vms_service()
vm = vms_service.list(search='name=myvm')[0]

# Locate the service that manages the disks of the virtual machine:
disks_service = vms_service.vm_service(vm.id).disks_service()

# Use the "add" method of the disks service to add the disk:
disk = disks_service.add(
    types.Disk(
        name='mydisk',
        description='My disk',
        interface=types.DiskInterface.VIRTIO,
        format=types.DiskFormat.COW,
        provisioned_size=1 * 2**20,
        storage_domains=[
            types.StorageDomain(
                name='mydata',
            ),
        ],
    ),
)

# Wait till the disk is OK:
disk_service = disks_service.disk_service(disk.id)
while True:
    time.sleep(5)
    disk = disk_service.get()
    state = disk.status.state
    if state == types.DiskStatus.OK:
        break

# Close the connection to the server:
connection.close()