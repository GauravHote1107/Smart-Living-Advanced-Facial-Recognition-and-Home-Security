import ntfy_wrapper
from node_client import NodeClient


class Notifier:
    ntfy = None
    if not ntfy:
        ntfy = ntfy_wrapper.Notifier(
            topics="ipcv_cp_g12",
            base_url="https://ntfy.sh/",
            notify_defaults={"title": "Smart Door", "tags": "", "icon": ""},
        )

    @staticmethod
    def send_notification():
        Notifier.ntfy.notify(
            message="Choose what action to take on the door.",
            title="Person Detected",
            tags="warning",
            actions="; ".join(
                [
                    f"http, Unlock Door, {NodeClient._BASE_URL}servo/D1/0, method=GET",
                    f"http, Lock Door, {NodeClient._BASE_URL}servo/D1/180, method=GET, clear=true",
                ]
            ),
        )
