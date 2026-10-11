from fastmcp import FastMCP
import yagmail
from dotenv import load_dotenv
import os
import requests

load_dotenv()

yagmail.register(os.getenv("EMAIL"), os.getenv("PASSWORD"))

mcp = FastMCP("Demo Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool
def get_weather(city: str) -> float:
    """Get the weather for a city."""
    response = requests.get(f"https://p2pclouds.up.railway.app/v1/learn/weather?city={city}")
    data = response.json()
    return data['current']['temp_c']

@mcp.tool
def tell_instructor_name() -> str:
    """Get the name of the instructor."""
    return "Zeeshan Ali"

@mcp.tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    yagmail.SMTP(os.getenv("EMAIL"), os.getenv("PASSWORD")).send(to, subject, body)
    return "Email sent successfully"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)  # served at http://localhost:8000/mcp