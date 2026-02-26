# slack-notifier

A Viam module that sends Slack notifications when items are checked out or returned. Use it alongside RFID readers, barcode scanners, or any Viam component that can issue `do_command` calls.

## Models

- [`10zing:slack-notifier:notifications`](10zing_slack-notifier_notifications.md) - Generic component that posts checkout and return events to a Slack channel via an incoming webhook.

## Setup

1. Create an [incoming webhook](https://api.slack.com/messaging/webhooks) in your Slack workspace and copy the URL.
2. Add the module to your robot in the Viam app.
3. Configure the `notifications` component with your webhook URL (see model docs for details).

## DoCommand API

Send commands to the component using `do_command` from any Viam SDK.

### `checkout`

```json
{
  "action": "checkout",
  "item_name": "Hex Wrench Set #3",
  "tag_id": "RF-0042",
  "image_url": "https://example.com/photo.jpg"
}
```

Posts a "Checkout Detected" message to Slack with item name, tag ID, station, timestamp, and optional photo.

### `return`

```json
{
  "action": "return",
  "item_name": "Hex Wrench Set #3",
  "tag_id": "RF-0042"
}
```

Posts an "Item Returned" message to Slack.

### `late_notice`

```json
{
  "action": "late_notice",
  "item_name": "Hex Wrench Set #3",
  "tag_id": "RF-0042",
  "days_overdue": 3,
  "image_url": "https://example.com/photo.jpg"
}
```

Posts an "Overdue Item — Please Return" message to Slack with the number of days overdue and optional checkout photo.

All commands return `{"action": "<action>", "sent": true}` on success or `{"action": "<action>", "sent": false}` if Slack delivery fails.
