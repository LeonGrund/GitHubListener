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


#### Use Raspberry Pi as Docker cluster
##### download ngrok Linux ARM *link*
##### follow instruction on website
##### expose port 4000: ./ngrok http 4000

#### Install Python Dependencies:
##### sudo pip install pyyaml










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
