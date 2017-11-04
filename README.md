[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ae753c7f858c42df8a4bdb87846dfa2d)](https://www.codacy.com/app/LeonGrund/GitHubListener?utm_source=github.com&utm_medium=referral&utm_content=LeonGrund/GitHubListener&utm_campaign=badger)
[![Build Status](https://travis-ci.org/LeonGrund/GitHubListener.svg?branch=master)](https://travis-ci.org/LeonGrund/GitHubListener)


# **GitHubListener**
&nbsp;

![Topology](/GHL-topology.png)

### Dependencies:
* #### Docker
* #### ngrok
&nbsp;

### Setup:
* #### [Install Docker](https://www.docker.com/get-docker)
* #### [Install ngrok](https://ngrok.com/download)
* #### Initiate Docker Swarm
* #### Fork **this** repository
* #### Fork [helloworld-docker-app](LINK) repository
* #### Run ngrok to expose localhost to URL
* #### Create GitHub webhook
* #### Run GitHubListener
* #### Test GitHubListener
&nbsp;

## Initiate Docker Swarm
* Check if Docker was installed correctly, run the following command in console:
```shell
docker images
```
![Docker images](/GHL-docker_images.png)

* Initiate Docker Swarm:
```shell
docker swarm init
```
&nbsp;

## Fork GitHubListener repository
* Run the following commands at local directory where all your other Git repositories are located:
~~~
...
~~~

## Create GitHub Webhook
* Webhooks send a POST request to a specified URL every time an [Event](LINK) happens
* Navigate to your repositories on GitHunb and go to **helloworld-docker-app**
* Do the following:
~~~
Settings > Webhook > Create
~~~
* Use the URL ngrok generated:

~~~
...
~~~

## Run GitHubListener
* Run '''GHListener.py''' in console:
~~~
python GHListener.py
~~~
* The following output should be printed in console:
~~~
...
~~~










#### Remove all images
##### docker rmi -f $(docker images -q)


## Templates:
* Needed for every git repository
* Note: port ```4000:4000``` is utilized by ```GitHubListener.py```

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


_Dockerfile_

~~~
FROM <docker_image>

COPY <file> <path>

CMD [ "<fist_arg>", "<second_arg>" ]

~~~




#### Create a public HTTPS URL for **GitHubListener** running locally connected to port 4000:
Open your console and enter.

'''
ngrok http 4000*
'''

#### Start GitHubListener
Open console at GitHubListener.py directory and enter:

'''
python GHListener.py
'''
