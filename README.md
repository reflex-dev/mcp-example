# MCP Docs Server

A simple way to make your documentation files available to AI assistants like Claude.

## What Does This Do?

Think of this as a **library catalog for your documentation**. You have a bunch of markdown files (`.md` files) with documentation, guides, or notes. This server:

1. Finds all your markdown files automatically
2. Makes them available to AI tools through something called MCP (Model Context Protocol)
3. Lets AI assistants search through and read your documentation

It's like giving Claude or other AI tools a filing cabinet of your documentation that they can open and read whenever they need information.

## How It Works (Simple Explanation)

1. **You put documentation files in folders** - Just save your `.md` files in organized folders
2. **The server finds them automatically** - No need to manually register each file
3. **AI can read them** - AI assistants can now access and search your documentation

### Real Example

Let's say you have documentation for "Service 1" with these files:
- `user-functions.md` - How user features work
- `call-functions.md` - How calling features work
- `calendar-functions.md` - How calendar features work

You would organize them like this:

```
docs/
└── service-1/
    ├── user-functions.md
    ├── call-functions.md
    └── calendar-functions.md
```

That's it! The server will automatically find these files and make them available as:
- `docs://service-1/user-functions`
- `docs://service-1/call-functions`
- `docs://service-1/calendar-functions`

## Quick Start (Step by Step)

### Step 1: Install Python Requirements

You need Python 3.10 or newer and `uv` (a Python package manager) installed.

Install `uv` if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the required package:

```bash
uv pip install mcp
```

### Step 2: Add Your Documentation Files

Put your markdown files in the `docs/` folder. Organize them in subfolders by topic or service:

```
docs/
├── service-1/
│   ├── user-functions.md
│   ├── call-functions.md
│   └── calendar-functions.md
├── service-2/
│   └── api-guide.md
└── getting-started/
    └── introduction.md
```

The subfolder name (like `service-1`) becomes the category.

### Step 3: Connect to Claude Code

The easiest way is to use the Claude Code CLI. From this project folder, run:

```bash
claude mcp add --transport stdio docs -- uv run python /full/path/to/mcp-example/src/mcp_docs_server.py
```

Replace `/full/path/to/mcp-example` with your actual project path.

Verify it's connected:

```bash
claude mcp list
```

You should see: `docs: ... - ✓ Connected`

That's it! Claude Code can now access your documentation.

## Adding New Documentation

To add new documentation at any time:

1. Create a new `.md` file in the appropriate folder under `docs/`
2. That's it! The server finds new files automatically

For example, to add documentation for a new service:

```
docs/
└── service-3/          # Create new folder
    └── setup.md        # Add your documentation file
```

No need to restart the server or change any code.

## Using with Claude Code

If you're using Claude Code (the CLI tool), follow Step 3 above. The server is already configured and running!

You can now ask Claude Code questions like:
- "List all available docs resources"
- "Read the service-1/user-functions documentation"
- "Search the docs for authentication"

Claude Code will automatically access your documentation files.

### Managing the Server

Check if the server is connected:
```bash
claude mcp list
```

Remove the server:
```bash
claude mcp remove docs
```

Re-add the server if needed:
```bash
claude mcp add --transport stdio docs -- uv run python /full/path/to/mcp-example/src/mcp_docs_server.py
```

## Connecting to Claude Desktop

To make your documentation available in Claude Desktop:

1. Find your Claude Desktop config file:
   - **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. Open the file and add this (replace `/path/to/mcp-example` with your actual folder path):

```json
{
  "mcpServers": {
    "docs": {
      "command": "python",
      "args": ["/path/to/mcp-example/src/mcp_docs_server.py"]
    }
  }
}
```

## Learn More

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Build your own MCP servers
- [MCP Documentation](https://modelcontextprotocol.io) - Learn about Model Context Protocol
- [MCP Python SDK Docs](https://modelcontextprotocol.github.io/python-sdk/) - Complete SDK reference
