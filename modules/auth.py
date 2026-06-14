import asyncio
from aioconsole import aprint
import rebootpy


class DeviceCodeAuth(rebootpy.Auth):
    """Device Code ONLY auth (rebootpy対応版)"""

    def __init__(self, timeout: int = 60, **kwargs):
        super().__init__(**kwargs)

        self.switch_token = kwargs.get(
            "switch_token",
            "OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
        )

        self.timeout = timeout
        self._device_code = None

    @property
    def identifier(self) -> str:
        return self._device_code or "device_auth"

    async def authenticate(self, priority: int = 0) -> None:
        data = await self._device_flow(priority)
        self._update_data(data)

    async def _device_flow(self, priority: int = 0) -> dict:
        # 1. client token
        client_data = await self.client.http.account_oauth_grant(
            auth=f"basic {self.switch_token}",
            data={
                "grant_type": "client_credentials",
                "token_type": "eg1"
            },
            priority=priority
        )

        self.client_access_token = client_data["access_token"]

        # 2. device code発行
        r = rebootpy.http.AccountPublicService(
            "/account/api/oauth/deviceAuthorization"
        )

        device_data = await self.client.http.post(
            r,
            auth=f"bearer {self.client_access_token}",
            data={
                "grant_type": "device_code",
                "prompt": "login"
            },
            priority=priority
        )

        self._device_code = device_data["device_code"]

        await aprint(
            f"[DEVICE LOGIN]\n"
            f"{device_data['verification_uri_complete']}"
        )

        # 3. ポーリング
        token_data = await self._poll(device_data["device_code"], priority)

        self.switch_access_token = token_data["access_token"]

        # 4. exchange → session
        code = await self.client.http.epicgames_get_exchange_data(
            self.switch_access_token
        )

        return await self.exchange_code_for_session(
            self.ios_token,
            code["code"],
            priority=priority
        )

    async def _poll(self, device_code: str, priority: int):
        while True:
            try:
                return await self.client.http.account_oauth_grant(
                    auth=f"basic {self.switch_token}",
                    data={
                        "grant_type": "device_code",
                        "device_code": device_code,
                        "token_type": "eg1"
                    },
                    priority=priority
                )
            except rebootpy.HTTPException as e:
                if e.message_code != "errors.com.epicgames.account.oauth.authorization_pending":
                    raise
                await asyncio.sleep(3)