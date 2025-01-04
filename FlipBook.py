import requests 
import json
import os
import time

camera_ip = "http://192.168.122.1:8080"  # 替換為你的相機 IP 地址
url = f"{camera_ip}/sony/camera"
FOLDER_PATH = "./photos"

def create_folder(folder_path): #create if folder doesnt exist
    # Check if folder exists, if not create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def camera_shooting(path, duration, frame ,onFinishCallback):
    camera_url = url

    print("initalize camera")

    print("create photo folder")
    create_folder(path)

    totalPic = int(frame * duration)
    interval = 1/frame
    print("Shooting photos...")

    for i in range(0, totalPic):
        print("TakePicture: " + str(i))
        time.sleep(interval)
    
    print("Shooting photos...finish")
    onFinishCallback("photos_folder_done")


def get_photo(photo_folder):
    photos = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if f.endswith(".jpg")]
    photos.sort()
    return photos

def create_canvas(photos):
    print("create Canvas")


def create_pdf(pdfName):
    print("create pdf")


def create_pdf_from_photo(path):
    photos = get_photo(path)

    if not photos:
        print("No pic found")
    else:
        create_canvas(photos)
        create_pdf("filpbook")


def ui_handler():
    print("create UI")
    print("create btn")
    print("execute btn action")
    camera_shooting(
        FOLDER_PATH, 3, 5,
        lambda saveFolderDone: create_pdf_from_photo(FOLDER_PATH)
    )

# 發送指令函數
def send_command(method, params=[]):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "id": 1,
        "version": "1.0"
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 確保 HTTP 狀態碼為 200
        return response.json()
    except requests.RequestException as e:
        print(f"HTTP 請求錯誤: {e}")
        return None

# 拍照命令
def start_rec_mode():
    response = send_command("startContShooting")
    if response is not None:
        # 檢查是否有 'result' 或 'error' 鍵
        if "result" in response:
            print("Start Record Mode")
        elif "error" in response:
            print(f"Start Record Mode Fail: {response['error']}")
        else:
            print("Unknown:", response)
    else:
        print("cant connect camera")

# 拍照命令
def take_picture():
    response = send_command("actTakePicture")
    if response is not None:
        # 檢查是否有 'result' 或 'error' 鍵
        if "result" in response:
            print("拍照成功！照片儲存於相機。")
        elif "error" in response:
            print(f"拍照失敗: {response['error']}")
        else:
            print("未知回應格式:", response)
    else:
        print("無法與相機建立連線。")

 # 連拍命令，拍攝多張照片
def continuous_shooting(num_shots, delay=1):
    print(f"開始連拍，共 {num_shots} 張照片，每張照片間隔 {delay} 秒")
    for i in range(num_shots):
        print(f"拍攝第 {i+1} 張照片...")
        response = send_command("actTakePicture")
        if response is not None:
            if "result" in response:
                print(f"第 {i+1} 張照片拍攝成功！")
            elif "error" in response:
                print(f"第 {i+1} 張照片拍攝失敗: {response['error']}")
            else:
                print(f"第 {i+1} 張照片拍攝結果未知。")
        else:
            print(f"第 {i+1} 張照片無法與相機建立連線。")
        time.sleep(delay)  # 設置間隔時間，控制連拍間的時間

def run_progress():
    # 檢查相機是否處於長時間拍攝模式
    event_response = send_command("getEvent")
    print("事件回應:", event_response)
    
    if event_response and 'Long shooting' in event_response.get("result", []):
        print("相機正在進行長時間拍攝，無法拍照。")
        return
    
    # 確保相機未在錄影模式中（如果需要）
    print("啟動錄影模式...")
    send_command("startRecMode")

    # 等待相機準備（如果需要）
    time.sleep(2)

    # 再次嘗試拍照
    continuous_shooting(5, 0.2)


def main():
    #start_rec_mode()
    run_progress()
    #ui_handler()
    
    
if __name__ == "__main__":
    main()

