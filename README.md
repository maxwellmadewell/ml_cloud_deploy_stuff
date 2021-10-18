# ml_cloud_deploy_stuff
Tools to assist in python/docker deployment to cloud infrastructures


##gcp_forkPyThenSendPub
- 3 topics - start instance, start command, stop instance
- Docker container runs and blocks on child subprocess sending GCP Pub message when complete
- TODO DEVELOPER - need to update project id and topic id from GCP in forkPythonBlockSendPubMsg.py

PubSub Topics

Compute Engine Utility
monitors a set of Cloud Pub/Sub topic subscriptions and runs commands on that instance each time it receives a message.


###Testing Locally
- docker build . -t [IMAGENAME]
- [WINDOWS] - docker run -p 9090:8080 -e PORT=8080 -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/[GCPCRED_FILENAME].json -v %GOOGLE_APPLICATION_CREDENTIALS%:/tmp/keys/[GCPCRED_FILENAME].json:ro [IMAGENAME]
- [LINUX] - docker run -p 9090:8080 -e PORT=8080 -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/[GCPCRED_FILENAME].json -v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/keys/[GCPCRED_FILENAME].json:ro [IMAGENAME]

