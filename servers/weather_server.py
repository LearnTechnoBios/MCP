from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    print("This is a log from the weather Server")
    return "VERYYY Hot"


if __name__ == "__main__":
    mcp.run(transport="stdio")