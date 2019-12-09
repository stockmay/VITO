FROM archlinux/base

#NFS
#RUN pacman -Sy nfs-utils --noconfirm
#COPY Config/exports /etc/exports
#RUN mkdir /mnt/vito
#RUN mkdir /experiments
#RUN exportfs -av

#SSH
COPY Config/id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
COPY Config/ssh_config /root/.ssh/config

#Python3
RUN pacman -Sy python3 openssh rsync grep --noconfirm

#VITO
COPY VITO /VITO
COPY Config/templateconfig.xml /VITO/templateconfig.xml

COPY Config/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["./start.sh"]
