import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    # Step 1: Create GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Step 2: GraphQL query
    query = gql(
        """
        query {
            allCustomers {
                edges {
                    node {
                        id
                    }
                }
            }
            allOrders {
                edges {
                    node {
                        id
                        totalAmount
                    }
                }
            }
        }
        """
    )

    # Step 3: Execute query
    result = client.execute(query)

    # Step 4: Calculate totals
    total_customers = len(result["allCustomers"]["edges"])
    total_orders = len(result["allOrders"]["edges"])
    total_revenue = sum(float(edge["node"]["totalAmount"]) for edge in result["allOrders"]["edges"])

    # Step 5: Log to file
    log_file = "/tmp/crmreportlog.txt"
    with open(log_file, "a") as f:
        f.write(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - "
            f"Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
        )

    print("CRM report generated!")
