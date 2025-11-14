#!/usr/bin/env python3
"""
MCP Server that dynamically serves markdown documentation files as resources.
"""
import asyncio
import logging
from pathlib import Path
from typing import TypedDict

from mcp.server import Server
from mcp.types import Resource, TextContent, Tool
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComponentInfo(TypedDict):
    """Information about a documentation component."""
    name: str
    category: str
    path: str
    full_path: str


def _get_all_components(docs_path: Path) -> list[ComponentInfo]:
    """Dynamically discover all component markdown files."""
    components: list[ComponentInfo] = []

    # Find all .md files in the docs directory
    md_files = docs_path.rglob("*.md")

    for md_file in md_files:
        relative_path = Path(md_file).relative_to(docs_path)
        component_name = relative_path.stem
        category = (
            relative_path.parent.name if relative_path.parent.name != "." else "general"
        )

        components.append(
            {
                "name": component_name,
                "category": category,
                "path": str(relative_path),
                "full_path": str(md_file),
            }
        )

    return sorted(components, key=lambda x: (x["category"], x["name"]))


class DocsServer:
    """MCP Server for documentation resources."""

    def __init__(self, docs_path: Path):
        self.docs_path = docs_path
        self.server = Server("mcp-docs-server")
        self.components: list[ComponentInfo] = []

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register all MCP protocol handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List all available documentation resources."""
            # Refresh components on each list call to pick up new files
            self.components = _get_all_components(self.docs_path)

            resources = []
            for component in self.components:
                # Create a URI for each document
                uri = f"docs://{component['category']}/{component['name']}"
                resources.append(
                    Resource(
                        uri=uri,
                        name=f"{component['category']}/{component['name']}",
                        mimeType="text/markdown",
                        description=f"Documentation for {component['name']} in {component['category']} category"
                    )
                )

            logger.info(f"Listed {len(resources)} documentation resources")
            return resources

        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read the content of a documentation resource."""
            # Parse the URI: docs://category/name
            if not uri.startswith("docs://"):
                raise ValueError(f"Invalid URI scheme: {uri}")

            path_part = uri[7:]  # Remove "docs://"
            parts = path_part.split("/")

            if len(parts) < 2:
                raise ValueError(f"Invalid URI format: {uri}")

            category = parts[0]
            name = parts[1]

            # Find the matching component
            component = next(
                (c for c in self.components if c["category"] == category and c["name"] == name),
                None
            )

            if not component:
                raise ValueError(f"Resource not found: {uri}")

            # Read the file content
            file_path = Path(component["full_path"])
            if not file_path.exists():
                raise ValueError(f"File not found: {file_path}")

            content = file_path.read_text(encoding="utf-8")
            logger.info(f"Read resource: {uri} ({len(content)} bytes)")

            return content

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="search_docs",
                    description="Search through all documentation files for a given query",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to find in documentation"
                            },
                            "category": {
                                "type": "string",
                                "description": "Optional category to filter search results"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls."""
            if name == "search_docs":
                query = arguments.get("query", "").lower()
                category_filter = arguments.get("category")

                # Refresh components
                self.components = _get_all_components(self.docs_path)

                results = []
                for component in self.components:
                    # Apply category filter if provided
                    if category_filter and component["category"] != category_filter:
                        continue

                    file_path = Path(component["full_path"])
                    if file_path.exists():
                        content = file_path.read_text(encoding="utf-8")

                        # Simple search: check if query is in content
                        if query in content.lower():
                            # Extract a snippet around the match
                            lines = content.split("\n")
                            matching_lines = [
                                f"Line {i+1}: {line}"
                                for i, line in enumerate(lines)
                                if query in line.lower()
                            ]

                            result_text = (
                                f"## {component['category']}/{component['name']}\n"
                                f"**Path:** {component['path']}\n\n"
                                f"**Matches:**\n" + "\n".join(matching_lines[:5])
                            )
                            results.append(result_text)

                if not results:
                    return [TextContent(
                        type="text",
                        text=f"No results found for query: '{query}'"
                    )]

                return [TextContent(
                    type="text",
                    text=f"Found {len(results)} result(s):\n\n" + "\n\n---\n\n".join(results)
                )]

            raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """Run the MCP server."""
        logger.info(f"Starting docs server with docs path: {self.docs_path}")

        # Initial component discovery
        self.components = _get_all_components(self.docs_path)
        logger.info(f"Discovered {len(self.components)} documentation files")

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point."""
    # Get the docs path relative to this file
    server_dir = Path(__file__).parent.parent
    docs_path = server_dir / "docs"

    if not docs_path.exists():
        logger.error(f"Docs directory not found: {docs_path}")
        logger.info("Creating docs directory...")
        docs_path.mkdir(parents=True, exist_ok=True)

    server = DocsServer(docs_path)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
