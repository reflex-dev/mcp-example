# Resources

The MCP Docs Server exposes documentation files as resources.

## Resource URI Format

Resources use the following URI format:

```
docs://{category}/{name}
```

Where:
- `category`: The subdirectory name (e.g., "getting-started", "api", "examples")
- `name`: The filename without the `.md` extension

## Example Resources

- `docs://getting-started/introduction`
- `docs://getting-started/installation`
- `docs://api/resources`
- `docs://api/tools`

## Listing Resources

Use the MCP `resources/list` method to discover all available documentation resources.

## Reading Resources

Use the MCP `resources/read` method with a resource URI to get the markdown content.

## Dynamic Discovery

The server automatically discovers new markdown files when you call `resources/list`. Just add a new `.md` file to the docs directory and it will be available immediately!
