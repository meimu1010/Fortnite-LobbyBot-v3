import rebootpy
import asyncio
import json
import os
from datetime import datetime, timezone, timedelta
import math

# ANSIエスケープシーケンス（テキストカラー定義）
RED, GREEN, YELLOW, RESET = "\033[31m", "\033[32m", "\033[33m", "\033[0m"

# 設定値
DEVICE_AUTHS_FILE = 'device_auths.json'
NAME_LOG_FILE = 'name.txt'
MAX_REQUESTS = 2500
DEFAULT_RETRY_SECONDS = 60

# デバイス認証情報の読み込み・保存
def load_device_auths():
    if os.path.exists(DEVICE_AUTHS_FILE):
        with open(DEVICE_AUTHS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_device_auths(auths):
    with open(DEVICE_AUTHS_FILE, 'w') as f:
        json.dump(auths, f, indent=4)

# name.txt にターゲット情報を保存
def save_target_info(display_name, account_id):
    with open(NAME_LOG_FILE, 'a', encoding='utf-8') as f:
        time_str = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time_str}] ユーザー名: {display_name} / アカウントID: {account_id}\n")

# グローバル変数
device_auths = load_device_auths()
total_request_count = 0
total_block_failures = 0
total_throttle_failures = 0
total_logins = 0
target_user_found = None
blocked_accounts = set()
target_info_saved = False  # ★追加：一度だけ保存する制御フラグ

# ウィンドウタイトル更新関数
def update_window_title():
    os.system(f'title アカウント数: {total_logins}, ブロック: {total_block_failures}, レート制限: {total_throttle_failures}')

class MyBot(rebootpy.Client):
    def __init__(self, device_id, account_id, secret, target_identifier, bot_number):
        auth = rebootpy.AdvancedAuth(device_id=device_id, account_id=account_id, secret=secret)
        super().__init__(auth=auth)
        self.target_identifier = target_identifier
        self.bot_number = bot_number
        self.target_user = None
        self.account_id = account_id

    @staticmethod
    def get_current_time():
        return datetime.now(timezone(timedelta(hours=9))).strftime("%H:%M:%S")

    async def event_ready(self):
        global target_user_found, total_logins, target_info_saved
        total_logins += 1
        print(f'[{self.get_current_time()}] ボット {self.bot_number}: ログインしました: {self.user.display_name}')
        update_window_title()

        if target_user_found is None:
            self.target_user = await self.fetch_user(self.target_identifier)
            if self.target_user is None:
                print(f"[{self.get_current_time()}] ボット {self.bot_number}: ターゲット '{self.target_identifier}' 不明。")
                await self.close()
                return
            target_user_found = self.target_user
            print(f"[{self.get_current_time()}] ターゲット '{self.target_user.display_name}' 発見。")

            # ★ここで一度だけ name.txt に保存
            if not target_info_saved:
                save_target_info(self.target_user.display_name, self.target_user.id)
                target_info_saved = True
        else:
            self.target_user = target_user_found

        await self.loop_interaction()

    async def loop_interaction(self):
        global total_request_count, total_block_failures, total_throttle_failures

        if self.account_id in blocked_accounts:
            print(f'{RED}[{self.get_current_time()}] {self.user.display_name}: ブロックされたアカウントのため処理スキップ{RESET}')
            return

        while total_request_count < MAX_REQUESTS:
            try:
                await asyncio.sleep(self.bot_number - 1)
                try:
                    await self.add_friend(self.target_user.id)
                    total_request_count += 1
                    print(f'{GREEN}[{self.get_current_time()}] {self.user.display_name}: {self.target_user.display_name} にフレンドリクエスト送信 ({total_request_count}回目){RESET}')
                except rebootpy.errors.HTTPException as e:
                    error_msg = str(e)
                    current_time = self.get_current_time()

                    if 'already_exists' in error_msg or 'friend_request_already_sent' in error_msg:
                        print(f'[{current_time}] ボット {self.bot_number}: 既にリクエスト済み。')
                    elif 'cannot_friend_blocked_account' in error_msg:
                        total_block_failures += 1
                        blocked_accounts.add(self.account_id)
                        update_window_title()
                        print(f'{RED}[{current_time}] {self.user.display_name}: {self.target_user.display_name} がブロックされています。{RESET}')
                        break
                    elif 'throttled' in error_msg:
                        total_throttle_failures += 1
                        update_window_title()
                        retry_after_seconds = self.get_retry_after(e)
                        print(f'{YELLOW}[{current_time}] {self.user.display_name}: 制限中。{retry_after_seconds}秒後再試行。{RESET}')
                        await asyncio.sleep(retry_after_seconds)
                    elif 'account_banned' in error_msg:
                        print(f'{RED}[{current_time}] {self.user.display_name}: アカウントBAN。処理中止。{RESET}')
                        break
                    else:
                        raise e

                await self.block_user(self.target_user.id)
                await self.unblock_user(self.target_user.id)

            except rebootpy.errors.Forbidden:
                print(f'{RED}[{self.get_current_time()}] {self.user.display_name}: リクエスト送信不可。{RESET}')
                break

            if total_request_count >= MAX_REQUESTS:
                print(f"{YELLOW}リクエスト最大回数 ({MAX_REQUESTS}) 達成。{RESET}")
                break

            await asyncio.sleep(13 - (self.bot_number - 1))

    @staticmethod
    def get_retry_after(error):
        retry_after_seconds = DEFAULT_RETRY_SECONDS
        if hasattr(error.response, 'headers') and 'Retry-After' in error.response.headers:
            retry_after = error.response.headers['Retry-After']
            try:
                retry_after_seconds = int(retry_after)
            except ValueError:
                retry_after_datetime = datetime.strptime(retry_after, "%a, %d %b %Y %H:%M:%S GMT")
                retry_after_seconds = math.ceil((retry_after_datetime - datetime.now(timezone.utc)).total_seconds())
        return retry_after_seconds

async def safe_start(client):
    try:
        await client.start()
    except Exception as e:
        print(f"{RED}[{client.get_current_time()}] ボット {client.bot_number}: 起動失敗: {e}{RESET}")

async def main():
    target_identifier = input("フレンドリクエストを送るユーザー名またはアカウントIDを入力: ")

    clients = []
    for i, auth in enumerate(device_auths.values()):
        try:
            client = MyBot(auth['device_id'], auth['account_id'], auth['secret'], target_identifier, i + 1)
            clients.append(client)
        except Exception as e:
            print(f"{RED}ボット {i + 1}: 認証情報が無効です: {e}{RESET}")
            continue
    await asyncio.gather(*(safe_start(client) for client in clients))

if __name__ == "__main__":
    asyncio.run(main())
