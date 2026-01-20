#!/usr/bin/env python3
"""
Test script for Saxon MCP Server
"""

import json
from saxon_mcp_server import SaxonXMLMCPServer


def test_basic_queries():
    """Test basic XPath queries"""
    server = SaxonXMLMCPServer(
        xml_path="./data/syllabubRecipe.xml",
        schema_path="./schemas/recipe.rnc",
        backup_dir="./backups"
    )

    print("=" * 60)
    print("Testing Saxon MCP Server")
    print("=" * 60)

    # Test 1: Simple XPath
    print("\nTest 1: Simple XPath Query")
    result = server.xpath_query("//section[@kind='equipment']//item")
    print(f"Equipment needed to make recipe: {result}")

    # Test 2: XPath 3.1 features
    print("\nTest 2: XPath 3.1 with Arrow Operator")
    result = server.xpath_query(
        "//section[@kind='equipment']//item => sort()"
    )
    print(f"Sorted equipment for recipe: {result}")
    for item in result:
        print(f"  - {item}")

    # Test 3: XQuery
    print("\nTest 3: XQuery Analysis")
    xquery = """
    for $item in distinct-values(//section[@kind='ingred']//ingred)
    let $steps := //section[@kind='process']//step[contains(., $item)]
    return map {
        'ingredient': $ingred,
        'stepsListed': $steps,
        'count': count($steps)
    }
    """
    result = server.xquery_query(xquery)
    print(f"Ingredient Step analysis:")
    print(json.dumps(result['results'], indent=2))

    # Test 4: Structure summary
    print("\nTest 4: Structure Summary")
    result = server.get_structure_summary()
    print(json.dumps(result['structure'], indent=2))

    # Test 5: Find irregularities
    print("\nTest 5: Find Irregularities")
    result = server.find_irregularities([
        {
            "xpath": "//step[not(.//ingred)]",
            "description": "Steps missing ingredients"
        }
        # ,
        # {
        #     "xpath": "//product[not(@id)]",
        #     "description": "Products missing ID"
        # }
    ])
    print(f"Issues found: {result['total_issues']}")

    print("\n" + "=" * 60)
    # ebb and mrs: why is line 71? is it a fancy border?
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_basic_queries()