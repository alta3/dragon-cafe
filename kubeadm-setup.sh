#!/bin/sh
echo 'Installing K8s Node'
sudo apt-get update
sudo apt-get install libseccomp2  # Might be already installed
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo bash -c 'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list'
sudo apt-get update
sudo apt-get install -y kubelet=1.22.0-00 kubeadm=1.22.0-00 kubectl=1.22.0-00
sudo apt-mark hold kubelet kubeadm kubectl
sudo echo '[Service]' > /etc/systemd/system/kubelet.service.d/0-containerd.conf
sudo echo 'Environment="KUBELET_EXTRA_ARGS=--container-runtime=remote --runtime-request-timeout=15m --container-runtime-endpoint=unix:///run/containerd/containerd.sock"' >> /etc/systemd/system/kubelet.service.d/0-containerd.conf
sudo echo 'net.ipv4.ip_forward = 1' > /etc/sysctl.d/10-ip-forwarding.conf
sysctl net.ipv4.ip_forward=1
sudo echo 'br_netfilter' > /etc/modules-load.d/br_nf.conf
sudo modprobe br_netfilter
sudo systemctl daemon-reload