# VITO Handbuch

Manual in German, english translation will follow.
Demo template not included in github repository due to size.

## Installation
Um Vito installieren zu können müssen folgende Tools (Pakete) auf dem System zur Verfügung stehen:

* docker
* qemu
* libvirt
* virt-manager (virt-clone)
* iproute 2

Es muss Root Zugang per SSH auf dem Host mit folgendem Public Key möglich sein:

`ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC2zRjTnN508xQA+fdSK0MCFCBJ3YlaCqMRjbsNHSncmaa1fUe0A8cWBmft4337oZuQiafAmkVYG85To68ZcOZ4NlBYCjG60JhXdlRN325/5Tmude+zm2or3qmyT9VQ1lA3UwdzGr2riZKkz5ITqpimQBlfbckM0vkXJlW7YLzZSXu5W3oXAYkVtuZjrgRvUp0Jf841sMIx/gPT3vxKcDtDba2Tw3uoGrb0Ha8zFobV7+w2sSc24mHVp1vRrbq9O3RGOLJauk5S63bRu+waFqBqb/EwBEK7hhL9C4vjasYSN/xLrBrtN8g/i1X24PfPIm+bV4a14nKeqsEN1AtP3lwVluvAwLyAC/2HmUMCbAOUmyoyz9vihHek39MZUS3e8P66AGwy4HTrnfHZ58l18SMJGl/RJ4j+uFZTK8c1hbGeNhCHnKG0m3x+gpm9W1tPlmo4S3lQLEYi0SZbhJzoevOA9r2a1ZOsI2qvpZxYGuAS7jf6+vG+3Nd2XGXvAET6xrc= root@template`

Vito wird mit `sudo ./initial_setup.sh` installiert.

## Betrieb von VITO

Während des Setups werden auf dem Host zwei Ordner angelegt

Note: Momentan noch /tmp/vito statt /vito
* /vito/experiments
* /vito/results

Im Ordner experiments werden Experimentdefinitionen und evtl. neue Templates im qcow2 Format abgelegt.
Im Ordner Results werden alle Ergebnisse gesammelt

VITO sammelt automatisch alle Dateien im Home Verzeichnis des Root Nutzers aller VMs ein, evtuelle log Dateien müssen vor Ende des Experiments dorthin kopiert werden.

Im Ordner `Files` findet sich ein Beispiel Template und eine Beispiel Konfiguration

## Experiment Definition

Experimentdefinitionen werden nach folgendem Schema erstellt:

```
{
    "Name" : "<Name>",
    "Hosts" : [
        {
            "Name" : "<Name>",
            "Template" :"<Name>",
            "Mac" : <Optional String>
            "Memory" : "<RAM in GB>",
            "CPU" : "<CPU Cores>",
            "Interfaces" : [
                {
                    "Name" : "<Name>",
                    "Bridge" : "<Connected To>",
                    "MTU" : <Optional: 1500>,
                    "IP" : <Optional, String>,
                    "Bandwidth" : <Optional in Mbit>,
                    "Delay" : <Optional in ms>,
                    "Jitter" : <Optional in ms>,
                    "Loss" : <Optional in percent>,
                    "Tcpdump" : <Options, yes or no>,
                    "Routes" : [ 
                        {<Destination>: <Key>}
                    ]
                }
            ],
            "Commands" : [
                {
                    "Command" : "<Command>",
                    "Time" : "<Execution Time>",
                    "Background" : <Background? true or false>
                },
            ]
        },
}
```
Achtung: IP Adressen aus dem Management bereich 172.12.0.0/23 dürfen nicht vergeben werden

## Templates

Vito kann mit eigenen Templates im qcow2 Format erweitert werden. 
Als Template eignet sich jede Linux Installation die folgende Voraussetzungen erfüllt:

* Root Zugang per SSH mit oben genanntem Key
* nfs, iproute2, tcpdump installiert.
* NAT Interface hat den Namen ```eth0```. Es ist zu empfehlen predictive interface names zu deaktivieren.
