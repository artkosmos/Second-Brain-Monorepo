from typing import Annotated

from fastapi import Depends

from config import Settings, get_settings

type SettingsDep = Annotated[Settings, Depends(get_settings)]
