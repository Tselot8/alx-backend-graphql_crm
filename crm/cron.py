#!/usr/bin/env python3

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes and optionally checks GraphQL."""
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Log heartbeat
    with open(log_file, "a") as f:
        f.write(f"{timestamp} CRM is alive\n")

    # Optional: query GraphQL 'hello' field to verify endpoint
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql(
            """
            query {
                hello
            }
            """
        )

        result = client.execute(query)
        with open(log_file, "a") as f:
            f.write(f"{timestamp} GraphQL response: {result['hello']}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} GraphQL endpoint error: {str(e)}\n")

def updatelowstock():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql(
        """
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
        """
    )

    result = client.execute(mutation)
    updated = result.get("updateLowStockProducts", {}).get("updatedProducts", [])

    log_file = "/tmp/low_stock_updates_log.txt"
    with open(log_file, "a") as f:
        for p in updated:
            f.write(f"{datetime.datetime.now()} - Product: {p['name']}, New stock: {p['stock']}\n")

    print("Low stock products updated!")