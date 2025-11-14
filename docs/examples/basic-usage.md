# Basic Usage Examples

This document provides examples of how to use the MCP Docs Server.

## Example 1: Listing All Documentation

Request all available resources:

```python
# Using the MCP client
resources = await client.list_resources()

for resource in resources:
    print(f"{resource.uri}: {resource.name}")
```

Output:
```
docs://getting-started/introduction: getting-started/introduction
docs://getting-started/installation: getting-started/installation
docs://api/resources: api/resources
docs://api/tools: api/tools
```

## Example 2: Reading a Document

Read the content of a specific document:

```python
content = await client.read_resource("docs://getting-started/introduction")
print(content)
```

## Example 3: Searching Documentation

Search for specific content:

```python
results = await client.call_tool(
    "search_docs",
    {
        "query": "installation",
        "category": "getting-started"
    }
)

print(results)
```

## Example 4: Adding New Documentation

Simply create a new markdown file:

```bash
# Create a new category
mkdir -p docs/tutorials

# Add a new document
echo "# My Tutorial" > docs/tutorials/my-tutorial.md
```

The server will automatically discover it on the next `list_resources` call!
