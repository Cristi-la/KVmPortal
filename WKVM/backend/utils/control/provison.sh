egrep -c '{vmx}|{vmdk}' /proc/cpuinfo
# No virtualization techonlogy is enabled


lscpi | grep "Virtualization"
# Virt technlogy



sudo dnf install qemu-kvm libvirt-deamon libvirt-client virt-manager
sudo usermod -aG kvm $USER


sudo virt-host-validate qemu

sudo systemctl enable --now libvirtd
sudo systemctl start libvirtd
sudo systemctl status libvirtd