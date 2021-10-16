#!/usr/bin/env/ python

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

project_id = "myinstancepubsubapp"
topic_id = "stop-instance-event"
imagename = "hello-world"

print(f"[DOCKER] Starting container: {imagename}")
try:
    p = subprocess.Popen(['docker', 'run', imagename], shell=True)
    print(f"[SUBPROCESS]: Child PID: {p.pid}")
except:
    print(f"[DOCKER] - Error starting docker image.")
    pass

publisher = pubsub_v1.PublisherClient()
# fully qualified identifier - `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)
print(f"[GCP] - Attempting Publish to: {topic_path}")

#Example message data - not required to initiate cloud function
msg_data = imagename

# Data requirement - bytestring
msg_data = msg_data.encode("utf-8")

# When publishing to Google Client returns a future.
future = publisher.publish(topic_path, msg_data)
print(f"Google Client Future response: {future.result}")
print(f"Published messages to {topic_path}.")

sys.exit(0)
