# See++

Shares your clipboad between your devices.

Currently under development.

## Version 0.1.1 (pre-release) plan

Planned to support one way text-only sync from Android to Mac using the Telegram API.

### Android client

#### Features

- On first launch, the user will be asked to authenticate Telegram
- On Launching the application, text from the clipboard is copied, paired up with a **unique prefix**, and sent to the "Saved Messages" (and show a progress bar while this is being done)
- The app will then show a successfully shared message

#### Technology

- Built using simple HTML + PWA, with caching enabled
- Can be added to home screen via the Google Chrome browser
- Will be hosted on Github Pages

### Mac client

#### Features

- On first launch, the user will be asked to authenticate Telegram
- Will act as a Push endpoint for Telegram
- On receiving a push notification from Telegram, it will verify if:
  - The message has been received in the "Saved Messages" section
  - Contains the [**unique prefix**](./README.md#android-client)
- If both conditions are true, then the client will:
  - Copy the text data (without the prefix) to clipboard
  - Send a desktop notification once both are done.

#### Technology

- Built using [Electron](https://electronjs.org) (so that it can easily be ported to other platforms in subsequent releases)

### Other Features

- Have a cleanup feature to delete old messages (sent via seeplusplus) from Telegram.
  - Maybe have a 1 hour self desctruct timer or something. Needs more research.
