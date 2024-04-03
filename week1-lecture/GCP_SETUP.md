### Create a ssh key to access the instances in the project:
1. Use command `ssh-keygen -t rsa -f ~/.ssh/gcp -C vishesh -b 2048` to create a key pair.
2. Go to GCP Metadata section and put the ssh gcp.pub key.
3. Create an instance with your specifications.

### Run the instance
- create a file in ~/.ssh folder called config and configure it as such: 
	```
	Host de-zoomcamp
	    HostName <hostname>
	    User vishesh
	    IdentityFile ~/.ssh/gcp
	```
	and run ssh de-zoomcamp
- or run ssh -i ~/.ssh/gcp vishesh@<_hostname_>
- You would have to change the HostName to that of external IP of the instance.

### Install
1. apt-get update
2. Anaconda
3. Docker & Fix the sudo issue by:
	1. sudo groupadd -f docker
	2. sudo usermod -aG docker $USER
	3. newgrp docker
4. docker-compose:
	1. create and cd to ~/bin
	2. wget it with -O docker-compose postpended
	3. chmod +x docker-compose
	4. add path to bin directory ehich contains all executables with ~/.bashrc export PATH="\${HOME}/bin:${PATH}"
	5. source bashrc

Install terraform on local machine.