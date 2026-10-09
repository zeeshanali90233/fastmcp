from fastmcp import FastMCP

mcp = FastMCP("Demo Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"It's sunny in {city}, 30°C"

@mcp.tool
def tell_instructor_name() -> str:
    """Get the name of the instructor."""
    return "Zeeshan Ali"


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)  # served at http://localhost:8000/mcp