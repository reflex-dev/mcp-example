# Tools

The MCP Docs Server provides tools for searching and working with documentation.

## search_docs

Search through all documentation files for a given query.

### Parameters

- `query` (string, required): The search term to find in documentation
- `category` (string, optional): Filter results to a specific category

### Example Usage

```json
{
  "query": "installation",
  "category": "getting-started"
}
```

### Returns

A list of matching documents with excerpts showing where the query appears.

### Search Behavior

- Case-insensitive search
- Searches through entire file content
- Returns up to 5 matching lines per document
- Shows line numbers for context

## Future Tools

Planned tools for future versions:

- `get_doc_metadata`: Get metadata about a documentation file
- `list_categories`: List all available categories
- `validate_links`: Check for broken internal links
