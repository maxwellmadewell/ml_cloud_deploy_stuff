#Pub Watcher Service (Linux) 

##Service Install 
- Copy pubwatch.service into /etc/systemd/system/
- sudo systemctl daemon-reload
- sudo systemctl enable pubwatch.service
- sudo systemctl start pubwatch.service

##WorkFlow
- Pubwatch service starts pubwatch_executor.py
  - creates executor to watch TOPIC
  - runs cloud logging handler
- TOPIC triggers run_pycontainer_task.py
##ISSUES
- Popen(shell=False) giving exception when calling docker run command
  - Was using shell=True.  Retry shell=False
  - Popen shell=true - was getting PID from p.pid where p = subprocess.Popen(shell=True)
    - Is the PID the shell? Is p.pid the shell PID?
    - might need to use something else to get PID of docker process
    - 