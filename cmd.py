import os
import requests
import subprocess

def download_kali_iso(url, output_path):
    """Kali Linux ISO dosyasını indirir."""
    print("Kali Linux ISO indiriliyor...")
    response = requests.get(url, stream=True)
    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f"Kali Linux ISO indirildi: {output_path}")

def create_virtualbox_vm(vm_name, iso_path):
    """VirtualBox kullanarak bir sanal makine oluşturur ve ISO'yu bağlar."""
    try:
        print("VirtualBox VM oluşturuluyor...")
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--register"], check=True)
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--memory", "2048", "--cpus", "2", "--ostype", "Debian_64"], check=True)
        subprocess.run(["VBoxManage", "createhd", "--filename", f"{vm_name}.vdi", "--size", "20000"], check=True)
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", f"{vm_name}.vdi"], check=True)
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_path], check=True)
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--boot1", "dvd"], check=True)
        print(f"{vm_name} adlı sanal makine oluşturuldu.")
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")

def start_virtualbox_vm(vm_name):
    """VirtualBox sanal makinesini başlatır."""
    print(f"{vm_name} başlatılıyor...")
    subprocess.run(["VBoxManage", "startvm", vm_name], check=True)

def main():
    kali_iso_url = "https://cdimage.kali.org/kali-rolling/kali-linux-2023.1-live-amd64.iso"
    iso_output_path = "kali-linux.iso"
    vm_name = "KaliLinuxVM"

    # ISO'yu indir
    if not os.path.exists(iso_output_path):
        download_kali_iso(kali_iso_url, iso_output_path)
    else:
        print(f"ISO zaten mevcut: {iso_output_path}")

    # VirtualBox VM oluştur ve başlat
    create_virtualbox_vm(vm_name, iso_output_path)
    start_virtualbox_vm(vm_name)

if __name__ == "__main__":
    main()