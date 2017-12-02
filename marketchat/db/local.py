# local.py

local_data = {}


def get_storage(event):
    user_id = event.source.user_id

    storage = local_data.get(user_id)
    if storage:
        local_data[user_id] = storage = {}

    return storage


__all__ = ['get_storage']
