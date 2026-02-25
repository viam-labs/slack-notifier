import asyncio
import json
import urllib.request
from typing import (Any, ClassVar, Dict, Mapping, Optional, Sequence, Tuple)

from google.protobuf.json_format import MessageToDict

from typing_extensions import Self
from viam.components.generic import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes


class Notifications(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("10zing", "slack-notifier"), "notifications"
    )

    slack_webhook_url: str
    station_id: str

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        notifier = super().new(config, dependencies)
        attrs = MessageToDict(config.attributes, preserving_proto_field_name=True)
        notifier.slack_webhook_url = attrs.get("slack_webhook_url", "")
        notifier.station_id = attrs.get("station_id", "unknown-station") or "unknown-station"
        return notifier

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        attrs = MessageToDict(config.attributes, preserving_proto_field_name=True)
        if "slack_webhook_url" not in attrs:
            raise Exception("missing required slack_webhook_url attribute")
        if not attrs["slack_webhook_url"]:
            raise Exception("slack_webhook_url cannot be empty")
        return [], []

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        """
        Accepts:
          {"action": "checkout", "item_name": "Hex Wrench Set #3", "tag_id": "RF-0042", "image_url": "https://..."}
          {"action": "return",   "item_name": "Hex Wrench Set #3", "tag_id": "RF-0042"}
        """
        result = {}
        action    = command.get("action", "")
        item_name = command.get("item_name", "Unknown item")
        tag_id    = command.get("tag_id", "unknown")
        image_url = command.get("image_url", "")

        if action == "checkout":
            message = self._build_checkout_message(item_name, tag_id, image_url)
            result["sent"] = await self._send_slack(message)
            result["action"] = "checkout"
        elif action == "return":
            message = self._build_return_message(item_name, tag_id)
            result["sent"] = await self._send_slack(message)
            result["action"] = "return"
        else:
            result["error"] = f"unknown action: {action}"

        return result

    def _build_checkout_message(self, item_name: str, tag_id: str, image_url: str) -> dict:
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "📦 Checkout Detected"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Item:*\n{item_name}"},
                    {"type": "mrkdwn", "text": f"*Tag ID:*\n{tag_id}"},
                    {"type": "mrkdwn", "text": f"*Station:*\n{self.station_id}"},
                ]
            }
        ]
        if image_url:
            blocks.append({
                "type": "image",
                "image_url": image_url,
                "alt_text": f"Checkout photo for {item_name}"
            })
        return {"blocks": blocks}

    def _build_return_message(self, item_name: str, tag_id: str) -> dict:
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "✅ Item Returned"}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Item:*\n{item_name}"},
                        {"type": "mrkdwn", "text": f"*Tag ID:*\n{tag_id}"},
                        {"type": "mrkdwn", "text": f"*Station:*\n{self.station_id}"},
                    ]
                }
            ]
        }

    async def _send_slack(self, message: dict) -> bool:
        try:
            data = json.dumps(message).encode("utf-8")
            req = urllib.request.Request(
                self.slack_webhook_url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, urllib.request.urlopen, req)
            self.logger.info("Slack notification sent successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
            return False

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> Sequence[Geometry]:
        raise NotImplementedError()