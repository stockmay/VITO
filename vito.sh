docker rm vito
docker run --name vito -v /tmp/vito/experiments:/experiments -v /tmp/vito/results:/mnt/vito --net vito-management --ip 172.12.0.10 --privileged vito:latest
