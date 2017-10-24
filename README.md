[![Build Status](https://travis-ci.org/LeonGrund/GitHubListener.svg?branch=master)](https://travis-ci.org/LeonGrund/GitHubListener)
# **GitHubListener**

![Topology](/GHL-topology.png)

### Dependencies:
#### -Docker
#### -ngrok




#### Dowload and install:
##### [Docker](https://www.docker.com/get-docker)
##### [ngrok](https://ngrok.com/download)

#### Setup:
##### -Initiate Docker Swarm
##### -Fork this repository
##### -ngrok expose localhost
##### -start GitHubListener
##### -Create GitHub Webhook



#### Remove all images
##### docker rmi -f $(docker images -q)


## Templates:
* Needed for every git repository
* Note: port ```4000:4000``` is used by ```GitHubListener.py```

_docker-commands.yaml_  

~~~
build:
  - docker
  - build
  - -t
  - NAME
  - REPO

service:
  - docker
  - service
  - create
  - -p
  - <port>:<port>
  - --name
  - SERVICE_NAME
  - IMAGE_NAME
  - rm

~~~






#### Create a public HTTPS URL for **GitHubListener** running locally connected to port 4000:
Open your command line and enter.

'''
ngrok http 4000*
'''

#### Start GitHubListener
Open command line at GitHubListener.py directory and enter:

'''
python GHListener.py
'''
