#!/usr/bin/env python3.12
"""
DigitAI XML-MCP Diagnostic Tool
Run this to verify your installation and configuration
"""

import sys
import os
import json
from pathlib import Path
import subprocess


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_check(name, status, message=""):
    """Print a check result"""
    symbol = "✓" if status else "✗"
    status_text = "PASS" if status else "FAIL"
    print(f"{symbol} {name}: {status_text}")
    if message:
        print(f"  → {message}")


def check_python_version():
    """Check Python version"""
    print_header("Python Version")
    version = sys.version_info
    is_correct = version.major == 3 and version.minor == 12
    
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    print_check("Python 3.12", is_correct, 
                f"Found {version.major}.{version.minor}" if not is_correct else "")
    return is_correct


def check_virtual_env():
    """Check if running in virtual environment"""
    print_header("Virtual Environment")
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    print_check("Virtual environment active", in_venv,
                "Run 'source .venv/bin/activate' first" if not in_venv else "")
    return in_venv


def check_dependencies():
    """Check if required packages are installed"""
    print_header("Dependencies")
    
    required = {
        'saxonche': '12.9.0',
        'mcp': '1.25.0',
        'jingtrang': '0.1.2',
        'lxml': None,
        'pydantic': None
    }
    
    all_installed = True
    for package, expected_version in required.items():
        try:
            # Try importing the package
            if package == 'mcp':
                # MCP has submodules, try importing server
                from mcp.server import Server
                mod = __import__('mcp')
            else:
                mod = __import__(package)
            
            # Try to get version
            version = 'unknown'
            if hasattr(mod, '__version__'):
                version = mod.__version__
            elif package == 'mcp':
                # MCP might not have __version__ but if import worked, it's installed
                version = 'installed'
            
            # Check version if expected
            if expected_version and version != 'unknown' and version != 'installed':
                status = version.startswith(expected_version.split('.')[0])
                msg = f"v{version}" + ("" if status else f" (expected {expected_version})")
            elif version == 'installed':
                # For packages without version, if import worked, it's OK
                status = True
                msg = "installed (version check skipped)"
            else:
                status = True
                msg = f"v{version}"
            
            print_check(package, status, msg)
            all_installed = all_installed and status
            
        except ImportError as e:
            print_check(package, False, f"Not installed ({str(e)})")
            all_installed = False
    
    return all_installed


def check_project_structure():
    """Check if project files exist"""
    print_header("Project Structure")
    
    required_files = [
        'saxon_mcp_server.py',
        'mcp_server.py',
        'config.json',
        'requirements.txt',
        'data/syllabubRecipe.xml',
        'schemas/recipe.rnc'
    ]
    
    all_exist = True
    for file in required_files:
        exists = Path(file).exists()
        print_check(file, exists, "Missing" if not exists else "")
        all_exist = all_exist and exists
    
    return all_exist


def check_config():
    """Validate configuration file"""
    print_header("Configuration")
    
    config_path = Path('config.json')
    if not config_path.exists():
        print_check("config.json", False, "File not found")
        return False
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        print_check("config.json", True, "Valid JSON")
        
        # Check paths
        xml_path = Path(config.get('xml_data_path', ''))
        schema_path = Path(config.get('xml_schema_path', ''))
        
        xml_exists = xml_path.exists()
        print_check(f"XML file: {xml_path}", xml_exists)
        
        schema_exists = schema_path.exists()
        print_check(f"Schema file: {schema_path}", schema_exists)
        
        return xml_exists
        
    except json.JSONDecodeError as e:
        print_check("config.json", False, f"Invalid JSON: {e}")
        return False


def test_saxon():
    """Test Saxon-HE functionality"""
    print_header("Saxon-HE Test")
    
    try:
        import saxonche
        proc = saxonche.PySaxonProcessor(license=False)
        
        # Test XML parsing
        xml = '<test><item>Hello</item></test>'
        node = proc.parse_xml(xml_text=xml)
        
        # Test XPath
        xpath_proc = proc.new_xpath_processor()
        xpath_proc.set_context(xdm_item=node)
        result = xpath_proc.evaluate('//item/text()')
        
        success = True
        print_check("Saxon parsing", success)
        print_check("XPath evaluation", success, f"Result: {result}")
        
        return success
        
    except Exception as e:
        print_check("Saxon test", False, str(e))
        return False


def test_mcp_server():
    """Test if MCP server can initialize"""
    print_header("MCP Server Test")
    
    try:
        from saxon_mcp_server import SaxonXMLMCPServer
        
        # Try to initialize with sample data
        server = SaxonXMLMCPServer(
            xml_path='./data/syllabubRecipe.xml',
            schema_path='./schemas/recipe.rnc',
            backup_dir='./backups'
        )
        
        # Test a simple query
        result = server.xpath_query('//recipe/@title')
        
        success = result.get('success', False)
        print_check("Server initialization", success)
        print_check("XPath query", success, 
                   f"Found {result.get('count', 0)} results" if success else result.get('error', ''))
        
        return success
        
    except Exception as e:
        print_check("MCP server test", False, str(e))
        return False


def check_claude_config():
    """Check Claude Desktop configuration"""
    print_header("Claude Desktop Configuration")
    
    # Determine OS
    if sys.platform == 'darwin':
        config_path = Path.home() / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json'
    elif sys.platform == 'win32':
        config_path = Path(os.environ['APPDATA']) / 'Claude' / 'claude_desktop_config.json'
    else:
        print_check("Unsupported OS", False, "Claude Desktop config check skipped")
        return False
    
    exists = config_path.exists()
    print(f"Config location: {config_path}")
    print_check("Config file exists", exists)
    
    if exists:
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            has_servers = 'mcpServers' in config
            print_check("Has mcpServers section", has_servers)
            
            if has_servers:
                has_digitxml = 'digitxml-mcp' in config['mcpServers']
                print_check("digitxml-mcp configured", has_digitxml)
                
                if has_digitxml:
                    server_config = config['mcpServers']['digitxml-mcp']
                    command = server_config.get('command', '')
                    args = server_config.get('args', [])
                    
                    print(f"  Command: {command}")
                    if args:
                        print(f"  Script: {args[0]}")
                        script_exists = Path(args[0]).exists()
                        print_check("Script path valid", script_exists)
                
                return has_digitxml
            
        except Exception as e:
            print_check("Config parsing", False, str(e))
    
    return exists


def print_summary(results):
    """Print summary and recommendations"""
    print_header("Summary")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("✓ All checks passed! Your installation looks good.")
        print("\nNext steps:")
        print("1. Restart Claude Desktop completely")
        print("2. Start a new conversation")
        print("3. Try: 'What XML processing tools do you have?'")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nFailed checks:")
        for name, passed in results.items():
            if not passed:
                print(f"  • {name}")
        
        print("\nRecommendations:")
        if not results.get('python'):
            print("  • Install Python 3.12 from python.org")
        if not results.get('venv'):
            print("  • Activate virtual environment: source .venv/bin/activate")
        if not results.get('deps'):
            print("  • Install dependencies: pip install -r requirements.txt")
        if not results.get('structure'):
            print("  • Verify all project files are present")
        if not results.get('config'):
            print("  • Check config.json settings")
        if not results.get('claude'):
            print("  • Configure Claude Desktop (see QUICKSTART.md)")


def main():
    """Run all diagnostic checks"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║            DigitAI XML-MCP Diagnostic Tool               ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    results = {
        'python': check_python_version(),
        'venv': check_virtual_env(),
        'deps': check_dependencies(),
        'structure': check_project_structure(),
        'config': check_config(),
        'saxon': test_saxon(),
        'server': test_mcp_server(),
        'claude': check_claude_config()
    }
    
    print_summary(results)
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
