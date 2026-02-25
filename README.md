# slack-notifier

A Viam module that sends Slack notifications when items are checked out or returned. Use it alongside RFID readers, barcode scanners, or any Viam component that can issue `do_command` calls.

## Models

- [`10zing:slack-notifier:notifications`](10zing_slack-notifier_notifications.md) - Generic component that posts checkout and return events to a Slack channel via an incoming webhook.

## Setup

1. Create an [incoming webhook](https://api.slack.com/messaging/webhooks) in your Slack workspace and copy the URL.
2. Add the module to your robot in the Viam app.
3. Configure the `notifications` component with your webhook URL (see model docs for details).
