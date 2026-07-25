"""Reads a Client's `modules` JSON and answers the one question every
module handler needs: is this feature turned on for this client?
No per-client code branching anywhere else in the app — it all funnels
through here.
"""

from app.models import Client


def is_enabled(client: Client, module_id: str) -> bool:
    module = client.modules.get(module_id)
    return bool(module and module.get("enabled"))


def module_setting(client: Client, module_id: str, key: str, default=None):
    module = client.modules.get(module_id) or {}
    return module.get(key, default)


def enabled_modules(client: Client) -> list[str]:
    return [mod_id for mod_id, cfg in client.modules.items() if cfg.get("enabled")]
