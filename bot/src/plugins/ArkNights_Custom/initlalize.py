from .paths import CUSTOM_DB_PATH


async def costom_init():
    if not CUSTOM_DB_PATH.exists():
        CUSTOM_DB_PATH.mkdir()
        from .database import nickname_conn

        nickname_conn.init_tables()

    

