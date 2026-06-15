# -*- coding: utf-8 -*-
import json
import os
import asyncio
import rebootpy
from rebootpy.auth import DeviceAuth as _DeviceAuth

DEVICE_AUTH_FILE = 'device_auths.json'


def get_device_auth_details():
    if os.path.isfile(DEVICE_AUTH_FILE):
        with open(DEVICE_AUTH_FILE, 'r') as f:
            return json.load(f)
    return {}


def store_device_auth_details(email: str, details: dict):
    existing = get_device_auth_details()
    existing[email.lower()] = details
    with open(DEVICE_AUTH_FILE, 'w') as f:
        json.dump(existing, f, indent=4)


class DebugDeviceAuth(_DeviceAuth):
    """DeviceAuthのレスポンスをデバッグ出力する"""
    async def ios_authenticate(self, priority: int = 0) -> dict:
        payload = {
            'grant_type': 'device_auth',
            'device_id': self.device_id,
            'account_id': self.account_id,
            'secret': self.secret,
            'token_type': self.access_token_type
        }
        print(f'[DEBUG] device_auth payload: {payload}')
        try:
            data = await self.client.http.account_oauth_grant(
                auth=f'basic {self.ios_token}',
                data=payload,
                priority=priority
            )
            print(f'[DEBUG] device_auth response keys: {list(data.keys())}')
            return data
        except rebootpy.HTTPException as e:
            print(f'[DEBUG] HTTPException: {e.message_code}')
            print(f'[DEBUG] raw: {e.raw}')
            raise


def make_auth(email: str) -> rebootpy.AdvancedAuth:
    saved = get_device_auth_details().get(email.lower(), {})
    auth = rebootpy.AdvancedAuth(
        device_id=saved.get('device_id'),
        account_id=saved.get('account_id'),
        secret=saved.get('secret'),
        prompt_device_code=not bool(saved),
        open_link_in_browser=False,
        prompt_code_if_invalid=True,
    )
    return auth