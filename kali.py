import os
import subprocess

def install_kali_tools():
    """iSH Shell üzerinde Kali Linux araçlarını kurar."""
    print("Kali Linux araçları yükleniyor...")

    # Alpine Linux için gerekli paketleri yükle
    try:
        subprocess.run(["apk", "update"], check=True)
        subprocess.run(["apk", "add", "bash", "curl", "wget", "nano", "vim"], check=True)

        # Ek Kali araçları benzer fonksiyonlara sahip Alpine paketlerinden kurulabilir
        subprocess.run(["apk", "add", "nmap", "metasploit", "wireshark-cli"], check=True)

        print("Kali Linux araçları başarıyla yüklendi.")
    except subprocess.CalledProcessError as e:
        print(f"Kurulum sırasında bir hata oluştu: {e}")

def main():
    print("iSH Shell için Kali Linux araçlarını kurma başlıyor...")
    install_kali_tools()

if __name__ == "__main__":
    main()