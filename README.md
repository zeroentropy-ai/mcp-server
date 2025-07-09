## ZeroEntropy MCP Server

*Setup*

```bash
uv sync
```

*Run*

```bash
uv run src/server.py
```

To run the MCP server from browser:

```bash
mcp dev src/server.py --dev
```

Add to claude code:
```
vim ~/Library/Application\ Support/Claude/claude_desktop_config.json

Add to claude code:
{
  "mcpServers": {
    "zeroentropy": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/mahimamanik/Desktop/projects/zeroEntropy/mcp-server",
        "run",
        "server.py"
      ],
      "env": {
        "ZEROENTROPY_API_KEY": "ADD YOUR API KEY HERE"
      }
    }
  }
}
```

You can find the API key in the ZeroEntropy dashboard: https://dashboard.zeroentropy.dev/api-keys
