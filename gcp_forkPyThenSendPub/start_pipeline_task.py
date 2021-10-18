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
This is simply an example task, meant to replace an executable bit of code
that does work on your system
"""
import time
import os
import sys
import subprocess
from google.cloud import pubsub_v1

# TODO - update PROJECT, TOPIC (stop instance after pipeline finishes), STARTAPP

PROJECT = "myinstancepubsubapp"
TOPIC = "stop-instance-event"
IMAGE = "hello-world"

print(f"[DOCKER] Starting container: {IMAGE}")

p = subprocess.Popen(['docker', 'run', IMAGE], shell=False)
print("--------------------")
print("****")
print(f"[DOCKER] Child Process PID: {p.pid}")
print("****")
os.system(f"ps -p {p.pid}")
os.waitpid(p.pid, 0)
print("--------------------")

publisher = pubsub_v1.PublisherClient()
# fully qualified identifier - `projects/{PROJECT}/topics/{TOPIC}`
topic_path = publisher.topic_path(PROJECT, TOPIC)
print(f"[GCP] - Attempting Publish to: {topic_path}")

#Example message data - not required to initiate cloud function
msg_data = IMAGE

# Data requirement - bytestring
msg_data = msg_data.encode("utf-8")

# When publishing to Google Client returns a future.
future = publisher.publish(topic_path, msg_data)
print(f"[GCP] = Future response from client: {future.result}")
print(f"[GCP] Published messages to {topic_path}.")

sys.exit(0)
