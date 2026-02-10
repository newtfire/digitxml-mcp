#!/usr/bin/env python3.12
"""
DigitAI XML-MCP Server
Proper MCP Server implementation using the MCP SDK
Provides XML processing tools via Saxon-HE and validation via Jingtrang
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from saxon_mcp_server import SaxonXMLMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("digitxml-mcp")


class DigitXMLMCPServer:
    """MCP Server wrapper for Saxon XML operations"""
    
    def __init__(self, config_path: str = "./config.json"):
        # Determine the directory where this script is located
        self.server_dir = Path(__file__).parent.resolve()
        
        # Resolve config path relative to server directory
        if not Path(config_path).is_absolute():
            config_path = self.server_dir / config_path
        
        self.config = self._load_config(str(config_path))
        self.saxon_server: Optional[SaxonXMLMCPServer] = None
        self.mcp_server = Server("digitxml-mcp")
        
        # Register tools
        self._register_tools()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        config_file = Path(config_path)
        if not config_file.exists():
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return {
                "xml_data_path": "./data/syllabubRecipe.xml",
                "xml_schema_path": "./schemas/recipe.rnc",
                "backup_dir": "./backups",
                "log_dir": "./logs"
            }
        
        with open(config_file) as f:
            return json.load(f)
    
    def _initialize_saxon(self):
        """Initialize Saxon server instance"""
        if self.saxon_server is None:
            # Resolve XML path relative to server directory
            xml_path = Path(self.config['xml_data_path'])
            if not xml_path.is_absolute():
                xml_path = self.server_dir / xml_path
            
            # Resolve schema path relative to server directory
            schema_path = self.config.get('xml_schema_path')
            if schema_path:
                schema_path_obj = Path(schema_path)
                if not schema_path_obj.is_absolute():
                    schema_path = str(self.server_dir / schema_path_obj)
            
            # Use temp directory for backups if configured dir doesn't exist
            backup_dir = self.config.get('backup_dir', './backups')
            backup_path = Path(backup_dir)
            if not backup_path.is_absolute():
                backup_path = self.server_dir / backup_path
            
            if not backup_path.exists():
                try:
                    backup_path.mkdir(parents=True, exist_ok=True)
                except (OSError, PermissionError):
                    # Fall back to temp directory
                    import tempfile
                    backup_path = Path(tempfile.gettempdir())
                    logger.warning(f"Using temporary directory for backups: {backup_path}")
            
            self.saxon_server = SaxonXMLMCPServer(
                xml_path=str(xml_path),
                schema_path=schema_path,
                backup_dir=str(backup_path)
            )
            logger.info(f"Saxon server initialized with {xml_path}")
    
    def _register_tools(self):
        """Register all MCP tools"""
        
        @self.mcp_server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available XML processing tools"""
            return [
                Tool(
                    name="xpath_query",
                    description="Execute XPath 3.1 query on the XML document. Supports advanced features like maps, arrays, arrow operators, and higher-order functions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "xpath": {
                                "type": "string",
                                "description": "XPath 3.1 expression to evaluate"
                            },
                            "version": {
                                "type": "string",
                                "enum": ["3.1", "3.0", "2.0"],
                                "default": "3.1",
                                "description": "XPath version to use"
                            },
                            "return_count": {
                                "type": "boolean",
                                "default": False,
                                "description": "If true, only return count of matches"
                            }
                        },
                        "required": ["xpath"]
                    }
                ),
                Tool(
                    name="xquery_query",
                    description="Execute XQuery 3.1 query for complex data extraction and transformation. Supports FLWOR expressions, functions, and modules.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "xquery": {
                                "type": "string",
                                "description": "XQuery 3.1 expression to evaluate"
                            },
                            "external_vars": {
                                "type": "object",
                                "description": "Optional external variables as key-value pairs"
                            }
                        },
                        "required": ["xquery"]
                    }
                ),
                Tool(
                    name="xslt_transform",
                    description="Apply XSLT 3.0 transformation to modify the XML document. Supports streaming, try/catch, and packages.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "xslt": {
                                "type": "string",
                                "description": "XSLT 3.0 stylesheet as string"
                            },
                            "params": {
                                "type": "object",
                                "description": "Optional stylesheet parameters"
                            },
                            "save_output": {
                                "type": "string",
                                "description": "Optional file path to save output"
                            }
                        },
                        "required": ["xslt"]
                    }
                ),
                Tool(
                    name="get_structure_summary",
                    description="Analyze and summarize XML document structure using XPath",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "max_depth": {
                                "type": "integer",
                                "default": 3,
                                "description": "Maximum depth to analyze"
                            }
                        }
                    }
                ),
                Tool(
                    name="find_irregularities",
                    description="Run validation checks using XPath or XQuery to find inconsistencies",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "checks": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "xpath": {"type": "string"},
                                        "description": {"type": "string"},
                                        "type": {
                                            "type": "string",
                                            "enum": ["xpath", "xquery"],
                                            "default": "xpath"
                                        }
                                    },
                                    "required": ["xpath", "description"]
                                }
                            }
                        },
                        "required": ["checks"]
                    }
                ),
                Tool(
                    name="apply_transformation",
                    description="Apply XSLT transformation to modify the document with validation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "xslt": {
                                "type": "string",
                                "description": "XSLT stylesheet to apply"
                            },
                            "validate": {
                                "type": "boolean",
                                "default": True,
                                "description": "Validate after transformation"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the transformation"
                            }
                        },
                        "required": ["xslt"]
                    }
                ),
                Tool(
                    name="batch_corrections",
                    description="Apply multiple corrections via auto-generated XSLT",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "corrections": {
                                "type": "array",
                                "description": "List of correction operations"
                            },
                            "validate": {
                                "type": "boolean",
                                "default": True
                            }
                        },
                        "required": ["corrections"]
                    }
                ),
                Tool(
                    name="create_backup",
                    description="Create a timestamped backup of the current XML document",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="reload_document",
                    description="Reload XML document from disk",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.mcp_server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls"""
            self._initialize_saxon()
            
            try:
                if name == "xpath_query":
                    result = self.saxon_server.xpath_query(
                        xpath=arguments["xpath"],
                        version=arguments.get("version", "3.1"),
                        return_count=arguments.get("return_count", False)
                    )
                
                elif name == "xquery_query":
                    result = self.saxon_server.xquery_query(
                        xquery=arguments["xquery"],
                        external_vars=arguments.get("external_vars")
                    )
                
                elif name == "xslt_transform":
                    result = self.saxon_server.xslt_transform(
                        xslt=arguments["xslt"],
                        params=arguments.get("params"),
                        save_output=arguments.get("save_output")
                    )
                
                elif name == "get_structure_summary":
                    result = self.saxon_server.get_structure_summary(
                        max_depth=arguments.get("max_depth", 3)
                    )
                
                elif name == "find_irregularities":
                    result = self.saxon_server.find_irregularities(
                        checks=arguments["checks"]
                    )
                
                elif name == "apply_transformation":
                    result = self.saxon_server.apply_transformation(
                        xslt=arguments["xslt"],
                        validate=arguments.get("validate", True),
                        description=arguments.get("description", "")
                    )
                
                elif name == "batch_corrections":
                    result = self.saxon_server.batch_corrections(
                        corrections=arguments["corrections"],
                        validate=arguments.get("validate", True)
                    )
                
                elif name == "create_backup":
                    backup_path = self.saxon_server.create_backup()
                    result = {
                        "success": True,
                        "backup_path": backup_path
                    }
                
                elif name == "reload_document":
                    self.saxon_server.reload_document()
                    result = {
                        "success": True,
                        "message": "Document reloaded"
                    }
                
                else:
                    result = {
                        "success": False,
                        "error": f"Unknown tool: {name}"
                    }
                
                # Format response
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            
            except Exception as e:
                logger.error(f"Error executing {name}: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": str(e),
                        "tool": name
                    }, indent=2)
                )]
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            logger.info("DigitAI XML-MCP Server started")
            await self.mcp_server.run(
                read_stream,
                write_stream,
                self.mcp_server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = DigitXMLMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
