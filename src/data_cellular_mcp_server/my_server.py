from typing import Literal
from fastmcp import FastMCP
from datetime import date
import requests

mcp = FastMCP("Cellular data")


@mcp.tool
def query_all_data() -> list[dict]:
    """Query all cellular subscriber data."""
    url = "https://api.data.gov.my/data-catalogue?id=cellular_subscribers"
    response = requests.get(url)
    return response.json()


@mcp.tool
def get_total_cellular_subscribers() -> int:
    """Get total cellular subscribers."""

    data = query_all_data()
    return sum(item["subscriptions"] for item in data if item["plan"] == "total")


@mcp.tool
def get_cellular_subscribers_by_plan(
    plan: Literal["total", "prepaid", "postpaid"],
) -> int:
    """Get cellular subscribers by plan."""

    url = f"https://api.data.gov.my/data-catalogue?id=cellular_subscribers&filter={plan.lower()}@plan"
    data = requests.get(url).json()

    return sum(item["subscriptions"] if item["subscriptions"] else 0 for item in data)


@mcp.tool
def get_cellular_subscribers_by_year(year: int) -> int:
    """Get cellular subscribers by year."""

    if not (2000 < year < 2022):
        raise ValueError("Year must be between 2000 and 2021.")

    url = f"https://api.data.gov.my/data-catalogue?id=cellular_subscribers&date_start={date(year, 1, 1)}@date&date_end={date(year, 12, 31)}@date"
    response_json = requests.get(url=url).json()

    return [item["subscriptions"] for item in response_json if item["plan"] == "total"][
        0
    ]


if __name__ == "__main__":
    # Start an HTTP server on port 8888
    mcp.run(transport="http", host="127.0.0.1", port=8888)
