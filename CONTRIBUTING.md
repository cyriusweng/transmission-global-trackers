# Contributing

Add public tracker feeds to `sources.json` with a stable raw-text URL, network category and licence attribution. Do not submit private tracker URLs containing passkeys, account tokens or other credentials.

Run before opening a pull request:

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests
```

A tracker stays in the full candidate inventory when it is temporarily offline. Only protocol-valid responses enter the verified lists.
