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
EOF
)

echo Installing masscan 
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make install
cd ..

echo creating flask docker container...

# docker build -t nginx/nginx -f ./dockerbuild/Dockerfile.nginx .

docker build -t flask -f ./dockerbuild/Dockerfile.flask .

docker run -d --network="host" --name flask flask

echo creating MongoDB docker container...

docker build -t mongodb/mongodb -f ./dockerbuild/Dockerfile.mongodb .

docker run -d --name mongodatabase mongodb/mongodb

sleep 3s

docker run --link mongodatabase:mongo -p 8081:8081 --name mongo-express -e ME_CONFIG_MONGODB_URL="mongodb://admin:password@mongodatabase:27017/masscanresults" -e ME_CONFIG_MONGODB_ENABLE_ADMIN=false -d mongo-express