# Installation

## Prerequisites

- Python 3.10 or higher
- pip or uv package manager

## Install Dependencies

Using pip:

```bash
pip install mcp
```

Using uv:

```bash
uv pip install mcp
```

## Running the Server

From the project root:

```bash
python src/mcp_docs_server.py
```

Or make it executable:

```bash
chmod +x src/mcp_docs_server.py
./src/mcp_docs_server.py
```

## Configuration

The server automatically looks for markdown files in the `docs/` directory relative to the project root. No additional configuration needed!
