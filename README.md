# **GitHubListener**

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
