# openclaw-microsoft-m365

Python SDK for Microsoft 365 (Graph API).

## Installation

```bash
pip install openclaw-microsoft-m365
```

## Quick Start

```python
from openclaw_microsoft_m365 import Microsoft365Client

client = Microsoft365Client.from_env()
client.authenticate()

# Send mail, manage calendar, OneDrive, Teams, etc.
messages = client.mail.list_messages()
```
