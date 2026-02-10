# DigitAI XML-MCP: Professional XML Processing with Claude Desktop

AI-powered XML analysis using Saxon-HE (XPath 3.1, XQuery 3.1, XSLT 3.0) through Claude Desktop's natural language interface.

---

## Quick Start

### Prerequisites
- **Python 3.12**
- **Claude Desktop** ([download](https://claude.com/download))

### Installation (5 minutes)

```bash
# 1. Set up environment
cd digitxml-mcp
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python diagnose.py
```

### Configure Claude Desktop

**macOS:** Edit `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this (replace with YOUR actual path):

```json
{
  "mcpServers": {
    "digitxml-mcp": {
      "command": "/path/to/digitxml-mcp/.venv/bin/python",
      "args": ["/path/to/digitxml-mcp/mcp_server.py"]
    }
  }
}
```

**Get your path:**
```bash
cd digitxml-mcp
pwd
echo "$(pwd)/.venv/bin/python"
echo "$(pwd)/mcp_server.py"
```

### Test It

1. **Restart Claude Desktop** (completely quit and reopen)
2. Ask Claude: `What XML tools do you have available?`
3. Should see: `xpath_query, xquery_query, xslt_transform...`

---

## What You Can Do

### Basic Queries
```
Find all ingredients in syllabubRecipe.xml
Count the number of paragraphs in chapter1.xml
Extract all @id attributes from the document
```

### Advanced Analysis
```
Use XQuery to find ingredients not mentioned in any recipe step
Check if all @ref attributes point to valid @id values
Generate a report of all element types and their frequencies
```

### Transformations
```
Add @unit="cups" to all quantity elements without units
Convert all dates from MM/DD/YYYY to ISO format
Create an HTML table of contents from section headings
```

### Validation
```
Validate manuscript.xml against the TEI schema
Find all elements that don't follow the schema rules
Check for duplicate @xml:id values
```

---

## Multi-File Features

### Switch Between Files

```
What XML files are in my workspace?
Switch to chapter2.xml
Which file am I currently using?
```

### Upload Files

Drag any XML file into Claude chat:
```
[drag file] Validate this against my schema
[drag file] Find all person names in this document
```

### Batch Processing

```
For each XML file in my workspace:
  - Validate against schema
  - Count elements
  - Generate summary report
```

---

## Configuration

### config.json

All paths are relative to the installation directory (no absolute paths needed!):

```json
{
  "xml_data_path": "./data/syllabubRecipe.xml",
  "xml_schema_path": "./schemas/recipe.rnc",
  "backup_dir": "./backups",
  "log_dir": "./logs"
}
```

### Directory Mode

Work with multiple files:

```json
{
  "xml_data_path": "./data/",
  "default_file": "syllabubRecipe.xml",
  "xml_schema_path": "./schemas/",
  "backup_dir": "./backups"
}
```

---

## Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `xpath_query` | XPath 3.1 queries | Find all `<title>` elements |
| `xquery_query` | XQuery 3.1 queries | Complex data extraction |
| `xslt_transform` | XSLT 3.0 transforms | Modify document structure |
| `get_structure_summary` | Analyze structure | Document overview |
| `find_irregularities` | Validation checks | Find issues |
| `apply_transformation` | Safe transforms | With validation |
| `batch_corrections` | Multiple fixes | Systematic updates |
| `switch_xml_file` | Change files | Work with different docs |
| `list_workspace_files` | Browse files | See available XMLs |
| `create_backup` | Save state | Before changes |
| `reload_document` | Refresh | After external edits |

---

## Example Workflows

### Workflow 1: Find Inconsistencies

```
You: Check if all ingredients in the recipe are actually used in the steps

Claude: [Uses XQuery to cross-reference]
        Found 8 ingredients
        6 are mentioned in steps
        2 unused: vanilla, nutmeg
        
        Would you like me to suggest where to add them?
```

### Workflow 2: Batch Validation

```
You: For each XML file in data/, validate against schema and report errors

Claude: Processing 5 files...
        
        ✓ syllabubRecipe.xml - Valid
        ⚠ chapter1.xml - Missing required @id on line 45
        ✓ chapter2.xml - Valid
        ✗ notes.xml - Not well-formed (unclosed tag line 12)
        ✓ metadata.xml - Valid
```

### Workflow 3: Transform Documents

```
You: Add a @created attribute with today's date to all <chapter> elements

Claude: [Generates XSLT]
        Preview of changes:
        
        Before: <chapter title="Introduction">
        After:  <chapter title="Introduction" created="2026-02-10">
        
        Apply to all 15 chapters? (I'll create a backup first)
```

---

## Troubleshooting

### "File not found" Errors

**Check paths are relative:**
```json
✓ "./data/file.xml"
✗ "/Users/you/data/file.xml"
```

**Verify files exist:**
```bash
ls -la data/
```

### MCP Server Not Connecting

**Run diagnostic:**
```bash
python diagnose.py
```

**Check Claude Desktop logs:**
- macOS: `~/Library/Logs/Claude/mcp*.log`
- Windows: `%APPDATA%\Claude\logs\`

**Test server manually:**
```bash
source .venv/bin/activate
python mcp_server.py
# Should start without errors
```

### Import Errors

**Activate virtual environment:**
```bash
source .venv/bin/activate  # or .venv\Scripts\activate
pip list | grep saxonche   # Should show saxonche 12.9.0
```

---

## Technical Details

### Architecture

```
Claude Desktop (UI)
      ↓ MCP Protocol
MCP Server (Python)
      ↓ Calls
Saxon-HE Engine
      ↓ Processes
Your XML Files
```

### Technologies

- **Saxon-HE 12.9** - Industry-standard XML processor
- **XPath 3.1** - Advanced querying with functions
- **XQuery 3.1** - FLWOR expressions, modules
- **XSLT 3.0** - Streaming, try/catch, packages
- **Relax NG** - Schema validation (via jingtrang)
- **MCP** - Model Context Protocol for tool integration

### Key Features

- ✅ **Portable paths** - Works on any computer without config changes
- ✅ **Read-only safe** - Works even in restricted filesystems
- ✅ **Multi-file** - Switch between documents dynamically
- ✅ **Upload support** - Drag & drop processing
- ✅ **Natural language** - No need to remember syntax
- ✅ **Safe operations** - Automatic backups before changes
- ✅ **Professional grade** - Saxon-HE is industry standard

---

## Project Structure

```
digitxml-mcp/
├── mcp_server.py              # MCP server (use this!)
├── saxon_mcp_server.py        # Saxon engine wrapper
├── config.json                # Configuration
├── requirements.txt           # Python dependencies
├── diagnose.py               # Installation checker
│
├── data/                      # Your XML files
│   └── syllabubRecipe.xml            # Example
│
├── schemas/                   # Validation schemas
│   └── recipe.rnc            # Example Relax NG
│
├── backups/                   # Automatic backups
└── logs/                      # Server logs
```

---

## Use Cases

### Digital Humanities
- TEI document processing
- Manuscript validation
- Cross-reference checking
- Metadata enrichment

### Technical Documentation
- DocBook transformation
- Link validation
- Format conversion
- Content management

### Data Quality
- Batch validation
- Schema compliance
- Consistency checking
- Error reporting

### Publishing
- Multi-format output
- Content transformation
- Quality assurance
- Automated workflows

---

## Advanced Features

### Custom Namespaces

Edit `saxon_mcp_server.py`:
```python
self.xpath_proc.declare_namespace('tei', 'http://www.tei-c.org/ns/1.0')
```

### Pattern Matching

```
Show me all files matching "chapter*.xml"
List files in subdirectory data/manuscripts/
```

### Cross-File Analysis

```
Extract character names from chapter1.xml
Now check if these characters appear in chapter2.xml
Generate a character consistency report
```

---

## Resources

- **Saxon Documentation**: https://www.saxonica.com/documentation/
- **XPath 3.1**: https://www.w3.org/TR/xpath-31/
- **XQuery 3.1**: https://www.w3.org/TR/xquery-31/
- **XSLT 3.0**: https://www.w3.org/TR/xslt-30/
- **Relax NG**: https://relaxng.org/
- **MCP Protocol**: https://modelcontextprotocol.io/

---

## Support

**Need help?**
1. Run `python diagnose.py` to check installation
2. Check logs for error messages
3. Verify paths are relative in config.json
4. Test server manually: `python mcp_server.py`

---

**Ready to process XML with AI?** Configure Claude Desktop and start asking questions in natural language! 🚀
