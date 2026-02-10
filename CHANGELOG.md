# Changelog

## Version 2.0 - Final Release (February 2026)

### Major Features

#### Multi-File Support
- **File Switching**: Work with multiple XML files without restarting
  - `switch_xml_file` tool - Change current document
  - `list_workspace_files` tool - Browse available files
  - `get_current_file` tool - Check what's loaded
- **Upload Processing**: Drag & drop XML files into Claude for instant analysis
- **Workspace Management**: Work with directories of XML files

#### Portable Paths
- **No Absolute Paths Required**: Config works on any computer
- All paths resolve relative to installation directory
- Perfect for classroom distribution
- No per-user configuration needed

#### Read-Only Filesystem Support
- Works in restricted environments (Claude's computer, Docker, etc.)
- Graceful fallback to temp directories for backups
- Never crashes due to filesystem permissions

### Bug Fixes

#### Path Resolution
- Fixed: Relative paths now work from any launch directory
- Fixed: Config paths resolve relative to server script location
- Fixed: Multi-user installations work without editing config

#### Backup System
- Fixed: Backup creation doesn't fail in read-only filesystems
- Fixed: Graceful fallback to system temp directory
- Fixed: Query operations work even when backups impossible

#### File Access
- Fixed: Workspace directory detection
- Fixed: Schema path resolution
- Fixed: Cross-platform path handling (Windows/Mac/Linux)

### Improvements

#### User Experience
- Natural language interface - no syntax to memorize
- Helpful error messages with suggestions
- Automatic file discovery
- Pattern matching for file selection

#### Reliability
- Comprehensive error handling
- Diagnostic tool for troubleshooting
- Detailed logging for debugging
- Graceful degradation when features unavailable

#### Documentation
- Single comprehensive README
- Clear installation steps
- Practical examples
- Troubleshooting guide

### Technical Changes

#### Core Engine
- Saxon-HE 12.9.0 integration
- XPath 3.1 full support
- XQuery 3.1 full support
- XSLT 3.0 full support

#### MCP Protocol
- Proper async/await implementation
- Tool registration with schemas
- Error handling and reporting
- stdio-based communication

#### File Management
- Dynamic file switching
- Content-based processing
- Directory traversal
- Pattern-based filtering

---

## Version 1.0 - Initial Release (January 2026)

### Features
- XPath 3.1 queries via Saxon-HE
- XQuery 3.1 processing
- XSLT 3.0 transformations
- Relax NG validation via jingtrang
- Claude Desktop integration via MCP
- Single file processing

### Known Limitations (Fixed in v2.0)
- Required absolute paths in config
- Failed in read-only filesystems
- Single file only (no switching)
- Manual file management

---

## Upgrade Notes

### From v1.0 to v2.0

**No breaking changes!** v2.0 is fully backward compatible.

**New features available:**
- File switching commands
- Upload processing
- Portable configuration

**Recommended actions:**
1. Update to v2.0
2. Simplify config.json (use relative paths)
3. Restart Claude Desktop
4. Try new multi-file features

**Optional:**
- Remove absolute paths from config
- Update to relative paths: `./data/file.xml`

---

## Future Roadmap

### Planned Features
- GitHub Codespaces integration (Stage 2)
- Assignment management system
- Student progress tracking
- Schematron rule engine
- ODD schema support
- Web interface option

### Under Development
- Batch processing scripts
- Git integration
- Collaborative features
- Custom validation libraries

---

## Credits

- Powered by Saxon-HE (Saxonica)
- Uses Model Context Protocol (MCP)
- Validation via Jing/Trang (Relax NG)

