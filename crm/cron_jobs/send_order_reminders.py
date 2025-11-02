#!/usr/bin/env python3

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the date 7 days ago (as YYYY-MM-DD string for Date type)
seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date().isoformat()

# GraphQL query (fixed field name and argument)
query = gql(
    """
    query($date: Date!) {
        allOrders(orderDateGte: $date) {
            edges {
                node {
                    id
                    customer {
                        email
                    }
                }
            }
        }
    }
    """
)

params = {"date": seven_days_ago}

# Execute query
result = client.execute(query, variable_values=params)
orders_edges = result.get("allOrders", {}).get("edges", [])

# Log reminders
log_file = "/tmp/order_reminders_log.txt"
with open(log_file, "a") as f:
    for edge in orders_edges:
        order = edge["node"]
        f.write(f"{datetime.datetime.now()} - Order ID: {order['id']}, Customer: {order['customer']['email']}\n")

print("Order reminders processed!")
