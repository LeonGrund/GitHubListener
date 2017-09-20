
sudo raspi-config
sudo ifconfig



## Build image at repository with tag
docker build ../dockerTestApp -t dta

## run image
docker run dta

## ssh into container
docker exec -it d1bea44b0d6f bin/sh


# ngrok
default:
ngrok http 4000
