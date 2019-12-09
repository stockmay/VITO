echo virsh net-define network.xml
virsh net-define network.xml
echo virsh net-start vito
virsh net-start vito
echo virsh net-autostart vito
virsh net-autostart vito
#Prepare Docker
echo docker network create --subnet=172.12.0.0/24 vito-management
docker network create --subnet=172.12.0.0/24 vito-management
echo sysctl -w net.ipv4.ip_forward = 1
sysctl -w net.ipv4.ip_forward=1
#Create Management Container
#Binds: /experiments und /mnt/vito
echo cd ../Manager
cd ../Manager
echo docker build -t vito . -f Dockerfile
docker build -t vito . -f Dockerfile
echo mkdir -p /tmp/vito/experiments
mkdir -p /tmp/vito/experiments
echo mkdir -p /tmp/vito/results
mkdir -p /tmp/vito/results
echo mkdir -p /usr/testbed
mkdir -p /usr/testbed
