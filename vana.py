import requests
import random
import time
import json

# Fungsi untuk membaca data proxy dari file
def read_proxy_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            proxies = {
                "http": file.readline().strip(),
                "https": file.readline().strip()
            }
        return proxies
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan, tidak menggunakan proxy.")
        return None

# Fungsi untuk mendapatkan data dari akun Telegram
def process_account(query_data, proxies=None):
    url_tasks = "https://www.vanadatahero.com/api/tasks/1"
    url_player = "https://www.vanadatahero.com/api/player"

    headers = {
        "Content-Type": "application/json",
        "x-telegram-web-app-init-data": query_data
    }

    # Menghasilkan poin acak
    points_to_add = random.randint(100, 300)
    payload = {
        "status": "completed",
        "points": points_to_add
    }

    # Mengirim permintaan ke API Tasks
    response_tasks = requests.post(url_tasks, json=payload, headers=headers, proxies=proxies)

    if response_tasks.status_code == 200:
        print("Tugas berhasil.")
    else:
        print("Error tugas:", response_tasks.text)

    # Mengambil data dari API Player
    response_player = requests.get(url_player, headers=headers, proxies=proxies)

    if response_player.status_code == 200:
        player_data = response_player.json()
        current_points = player_data.get("points", 0)
        username = player_data.get("tgUsername", "Tidak ada username")
        print(f"Points bertambah: {points_to_add}")
        print(f"Points sekarang: {current_points}")
    else:
        print("Error player:", response_player.text)

# Membaca proxy dari file
proxies = read_proxy_data('proxy.txt')

# Membaca query data dari file
with open('data.txt', 'r') as file:
    query_data_list = file.readlines()

# Memproses setiap akun Telegram
while True:  # Perulangan tak terbatas
    for query_data in query_data_list:
        query_data = query_data.strip()  # Menghapus spasi dan newline
        try:
            # Mengambil username dari query_data
            user_info = json.loads(query_data.split('&user=')[1].split('&')[0].replace('%7B', '{').replace('%22', '"').replace('%7D', '}').replace('%2C', ',').replace('%3A', ':'))
            username = user_info.get('username', 'Tidak ada username')
            
            print(f"\nMemproses akun: {username}")
            process_account(query_data, proxies)
        except (IndexError, json.JSONDecodeError) as e:
            print(f"Format query tidak valid: {query_data}. Error: {e}")
        
        time.sleep(1)  # Jeda satu detik antara setiap permintaan

    # Jeda 1 menit setelah semua akun selesai
    print("\nSemua akun selesai, menunggu 1 menit...")
    time.sleep(60)
