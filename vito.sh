docker rm vito
docker run --name vito -v /vito/experiments:/experiments -v /vito/results:/mnt/vito --net vito-management --ip 172.12.0.10 vito:latest
