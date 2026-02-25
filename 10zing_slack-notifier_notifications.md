# Model `10zing:slack-notifier:notifications`

A generic component that sends Slack messages when items are checked out or returned. Messages are posted to a Slack channel via an [incoming webhook](https://api.slack.com/messaging/webhooks) and include the item name, RFID/barcode tag ID, station name, and an optional photo.

## Configuration

```json
{
  "slack_webhook_url": "https://hooks.slack.com/services/...",
  "station_id": "tool-crib-1"
}
```

### Attributes

| Name                | Type   | Inclusion | Description                                                                 |
|---------------------|--------|-----------|-----------------------------------------------------------------------------|
| `slack_webhook_url` | string | Required  | Incoming webhook URL from your Slack app. Messages are posted here.        |
| `station_id`        | string | Optional  | Human-readable name for this station shown in Slack messages. Defaults to `unknown-station`. |

## DoCommand

Send commands using `do_command` from any Viam SDK or from another component/service.

### `checkout`

Posts a "Checkout Detected" message to Slack. Optionally includes an image.

```json
{
  "action": "checkout",
  "item_name": "Hex Wrench Set #3",
  "tag_id": "RF-0042",
  "image_url": "https://example.com/photo.jpg"
}
```

| Field        | Type   | Inclusion | Description                                      |
|--------------|--------|-----------|--------------------------------------------------|
| `action`     | string | Required  | Must be `"checkout"`.                            |
| `item_name`  | string | Required  | Display name of the item being checked out.      |
| `tag_id`     | string | Required  | RFID or barcode tag identifier.                  |
| `image_url`  | string | Optional  | URL of a photo to include in the Slack message.  |

**Response:**
```json
{"action": "checkout", "sent": true}
```

---

### `return`

Posts an "Item Returned" message to Slack.

```json
{
  "action": "return",
  "item_name": "Hex Wrench Set #3",
  "tag_id": "RF-0042"
}
```

| Field       | Type   | Inclusion | Description                                 |
|-------------|--------|-----------|---------------------------------------------|
| `action`    | string | Required  | Must be `"return"`.                         |
| `item_name` | string | Required  | Display name of the item being returned.    |
| `tag_id`    | string | Required  | RFID or barcode tag identifier.             |

**Response:**
```json
{"action": "return", "sent": true}
```

---

### `late_notice`

Posts an "Overdue Item — Please Return" message to Slack. Optionally includes the photo from the original checkout.

```json
{
  "action": "late_notice",
  "item_name": "Hex Wrench Set #3",
  "tag_id": "RF-0042",
  "days_overdue": 3,
  "image_url": "https://example.com/checkout-photo.jpg"
}
```

| Field          | Type    | Inclusion | Description                                             |
|----------------|---------|-----------|---------------------------------------------------------|
| `action`       | string  | Required  | Must be `"late_notice"`.                                |
| `item_name`    | string  | Required  | Display name of the overdue item.                       |
| `tag_id`       | string  | Required  | RFID or barcode tag identifier.                         |
| `days_overdue` | integer | Required  | Number of days the item has been checked out.           |
| `image_url`    | string  | Optional  | URL of the original checkout photo.                     |

**Response:**
```json
{"action": "late_notice", "sent": true}
```

---

If Slack delivery fails, `"sent"` will be `false` and the error is logged to the Viam robot logs.
