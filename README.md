# mcp-ethereum

## Setup

### Install uv
To install uv, run the following command:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Claude configuration
To use with Claude Desktop, add the server config:
```bash
{
  "mcpServers": {
    "ethereum": {
      "command": "uv",
      "args": [
        "--directory",
        "ABSOLUTE_PATH/mcp-ethereum",
        "run",
        "ethereum.py"
      ]
      "env": {
        "ALCHEMY_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```