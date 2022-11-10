#!/bin/bash

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo privilege to run this script"

echo Installing the required dependencies
while read -r p ; do sudo apt-get install -y $p ; done < <(cat << "EOF"
    docker
    docker.io
    git
    make
    gcc
    packer
    
EOF
)

echo Installing masscan 
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make install
cd ..

echo creating NGINX docker container...

docker build -t nginx/nginx -f ./dockerbuild/Dockerfile.nginx .

docker run -d --network="host" --name nginx nginx/nginx
