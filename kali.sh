#!/bin/bash

# Türkçe karakterler ve yaygın kullanılan harfler, sayılar
CHARS="abcçdefgğhıijklmnoöprsştuüvyz"
NUMBERS="0123456789"
SPECIALS="@_-."

# Wordlist dosyasının adı
OUTPUT="rockyou.txt"

# Kullanıcıdan şifre uzunluğu ve sayı alıyoruz
read -p "Şifre uzunluğu (örneğin 6-12): " MIN_LEN
read -p "Şifre maksimum uzunluğu (örneğin 12): " MAX_LEN
read -p "Kaç şifre oluşturulacak? " COUNT

# Dosyayı temizliyoruz
> $OUTPUT
echo "[*] $OUTPUT dosyası oluşturuldu."

generate_password() {
    LENGTH=$((RANDOM % (MAX_LEN - MIN_LEN + 1) + MIN_LEN))
    PASSWORD=""
    for (( i=0; i<LENGTH; i++ )); do
        CHAR_POOL="$CHARS$NUMBERS$SPECIALS"
        PASSWORD+="${CHAR_POOL:RANDOM%${#CHAR_POOL}:1}"
    done
    echo "$PASSWORD" >> $OUTPUT
}

echo "[*] Şifreler oluşturuluyor..."
for (( i=0; i<COUNT; i++ )); do
    generate_password
done

echo "[+] $COUNT adet şifre $OUTPUT dosyasına kaydedildi."
echo "[!] İşlem tamamlandı. Wordlist dosyasını kontrol edebilirsiniz."