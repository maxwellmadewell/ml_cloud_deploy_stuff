#!/usr/bin/env/ python

import os
import subprocess
from google.cloud import pubsub_v1

# TODO - Input docker image name, google project id and google pub/sub topic-id
#
project_id = "schedfunctest"
topic_id = "start-instance-event"
imagename = "hello-world"

print(f"[DOCKER] Starting container: {imagename}")
p = subprocess.Popen(['docker', 'run', imagename], shell=True)
print(f"[SUBPROCESS]: Child PID: {p.pid}")
	

publisher = pubsub_v1.PublisherClient()
# fully qualified identifier - `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)
print(f"[GOOGLE-PUB] Publishing to: {topic_path}") 

#Example message data - not required to initiate cloud function
msg_data = imagename

# Data requirement - bytestring
msg_data = msg_data.encode("utf-8")

# When publishing to Google Client returns a future.
future = publisher.publish(topic_path, msg_data)
print(f"Google Client Future response: {future.result}")
print(f"Published messages to {topic_path}.")


