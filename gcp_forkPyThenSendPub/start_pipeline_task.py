#!/usr/bin/env python

# Copyright 2015 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

    # http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Update PROJECT, TOPIC (stop instance after pipeline finishes), MSG must
have zone and label associated with Instance to stop.
"""
import os
import sys
import subprocess
import json
from google.cloud import pubsub_v1

PROJECT = "myinstancepubsubapp"
TOPIC = "stop-instance-event"
IMAGE = "hello-world"
MSG = {"zone": "us-west1-b", "label": "env=dev"}

print("[DOCKER] Starting container: {}".format(IMAGE))

p = subprocess.Popen(['docker', 'run', IMAGE], shell=False)
print("[DOCKER] Child Process, {},  PID: {}".format(IMAGE, p.pid))
print("--------------------")
os.system("ps -p {}".format(p.pid))
os.waitpid(p.pid, 0)
print("--------------------")

publisher = pubsub_v1.PublisherClient()
# fully qualified identifier - `projects/{PROJECT}/topics/{TOPIC}`
topic_path = publisher.topic_path(PROJECT, TOPIC)
print("[GCP] - Attempting Publish to: {}".format(topic_path))

# Data requirement - bytestring
json_msg = json.dumps(MSG)
publish_future = publisher.publish(topic_path, json_msg.encode("utf-8"))
print(publish_future.result())
print("[GCP] = Future response from client: {}".format(publish_future.result()))
print("[GCP] Published messages to {}.".format(topic_path))

sys.exit(0)
