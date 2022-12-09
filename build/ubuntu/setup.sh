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
    python3
    python3-pip
    mongo-tools
EOF
)

echo Update to use correct python...

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

echo Install Django...

sudo pip install Django

echo Installing masscan 
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make install
cd ..

echo "Please enter a username that will be used as the MongoDB username:"
read input
export MS_MONGODB_USERNAME=$input

echo "Please enter a password that will be used as the MongoDB password:"
read input
export MS_MONGODB_PASSWORD=$input

docker run -d --network="host" --name nginx nginx/nginx

echo creating MongoDB docker container...

docker build -t mongodb/mongodb -f ./dockerbuild/Dockerfile.mongodb --build-arg USERNAME=$MS_MONGODB_USERNAME --build-arg PASSWORD=$MS_MONGODB_PASSWORD . 

docker run -d -p 27017:27017 --name mongodatabase mongodb/mongodb

sleep 3s

docker run --link mongodatabase:mongo -p 8081:8081 --name mongo-express -e ME_CONFIG_MONGODB_URL="mongodb://$MS_MONGODB_USERNAME:$MS_MONGODB_PASSWORD@mongodatabase:27017/masscanresults" -e ME_CONFIG_MONGODB_ENABLE_ADMIN=false -d mongo-express