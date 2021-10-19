# Google Cloud PubSub Watcher Service (Linux) 

## pubwatch.service
-   starts pubwatch_executor.py on boot

## pubwatch_executor.py
- User updates GCP project id, topic id, and "startup app" 
- When topic is published - runs the startup app, start_pipeline_task.py
- Trigger currently is Google PubSub Topic: "start-ce-pipeline"

## start_pipeline_task.py
- User updates Docker image, topic id, project id, and message (requires zone and label for instance(s) to shutdown)
- Uses subproces.POpen with docker run for image
- os.waitpid() for child subprocess to finish
- once finished publishes "stop-instance" topic to Google Cloud PubSub

## chron_executor.py
- boilerplate GCP code for pub watcher executor class

## Service Install 
- Copy pubwatch.service into /etc/systemd/system/
-   sudo systemctl daemon-reload
-   sudo systemctl enable pubwatch.service
-   sudo systemctl start pubwatch.service
- Copy above files onto instance
- update file references in pubwatch.service
- update project and topic ids, startup app, and message as described above in Python files
- install google-cloud-pubsub, google-cloud-storage using pip
- update user in pubwatch.service to reflect user with above pip modules
-   if errors on install with grpcio - need to install separately first
-       pip3 install --upgrade pip
-       python3 -m pip install --upgrade setuptools
-       pip3 install --no-cache-dir  --force-reinstall -Iv grpcio==1.41.0
- pip3 install --upgrade google-api-python-client
- pip3 install --upgrade oauth2client 
- sudo apt-get install docker.io

## WorkFlow
- Create instance(s) and assign key:value label (e.g. env:dev)
- Cloud Scheduler Publishes "start-instance-topic"
- Cloud Function, startInstancePubSub, triggered by topic, starts instance(s)
-   instances identified by key:value pairs in metadata associated with them upon creation
- Cloud Scheduler Publishes "start-ce-pipeline" 
- Instance receives message using pubwatch.service systemd service 
- Instance starts start_pipeline_task.py to run docker image
- Instance waits for image process to complete, then publishes "stop-instance-topic"
- Cloud Function, stopInstancePubSub, triggered, stops instance
