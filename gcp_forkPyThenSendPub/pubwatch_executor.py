#!/usr/bin/env python

# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This sample script shows how to use the reusable Executor utility to
watch a topic and execute a command when a message is received
"""

import logging
import os
import sys

from cloud_handler import CloudLoggingHandler
from cron_executor import Executor

PROJECT = 'myinstancepubsubapp'  # change this to match your project
TOPIC = 'runPredEngine'

script_path = os.path.abspath(os.path.join(os.getcwd(), 'run_pycontainer_task.py'))

pycontainer_task = "python -u %s" % script_path


root_logger = logging.getLogger('cron_executor')
root_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root_logger.addHandler(ch)

cloud_handler = CloudLoggingHandler(on_gce=True, logname="task_runner")
root_logger.addHandler(cloud_handler)

# create the executor that watches the topic, and will run the job task
pub_executor = Executor(topic=TOPIC, project=PROJECT, task_cmd=pycontainer_task, subname='pycontainer_task')

# add a cloud logging handler and stderr logging handler
job_cloud_handler = CloudLoggingHandler(on_gce=True, logname=pub_executor.subname)
pub_executor.job_log.addHandler(job_cloud_handler)
pub_executor.job_log.addHandler(ch)
pub_executor.job_log.setLevel(logging.DEBUG)


# watches indefinitely
pub_executor.watch_topic()
