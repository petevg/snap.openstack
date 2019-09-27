#!/usr/bin/env python

# Copyright 2016 Canonical UK Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import os
import subprocess
import sys

from snap_openstack.base import OpenStackSnap

LOG = logging.getLogger(__name__)

CONFIG_FILE = 'snap-openstack.yaml'


def main():
    logging.basicConfig(level=logging.WARNING)
    snap = os.environ.get('SNAP')
    if not snap:
        LOG.error('Not executing in snap environment, exiting')
        sys.exit(1)
    config_path = os.path.join(snap,
                               CONFIG_FILE)
    if not os.path.exists(config_path):
        LOG.error('Unable to find snap-openstack.yaml configuration file')
        sys.exit(1)

    LOG.debug('Using snap wrapper: {}'.format(config_path))
    s_openstack = OpenStackSnap(config_path)

    if sys.argv[1] == 'setup':
        s_openstack.setup()
        sys.exit(0)

    if sys.argv[1] == 'launch':
        database_ready = subprocess.check_output(
            ['snapctl', 'get', 'database.ready']).decode('utf-8').strip()
        if not database_ready.lower() == 'true':
            LOG.info("Database backend access not yet setup. Exiting.")
            sys.exit(0)

        s_openstack.launch(sys.argv)
        sys.exit(0)

    LOG.error("Missing argument. Must specific 'setup' or 'launch.'")
    sys.exit(1)
