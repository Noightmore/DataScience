from pyspark import SparkConf, SparkContext


def parse_line(line):
    fields = line.split(',')
    customer_id, _, price = fields[0], fields[1], float(fields[2])
    return customer_id, price


def total_spent_by_customer():
    conf = SparkConf().setAppName("TotalSpentByCustomer")
    sc = SparkContext(conf=conf)

    lines = sc.textFile("/files/customer-orders.csv")
    entries = lines.map(parse_line)

    # Reduce by customer to calculate total spent by each customer
    customer_totals = entries.reduceByKey(lambda x, y: x + y)

    # Swap key-value pairs for sorting and sort by total spent in descending order
    sorted_customer_totals = customer_totals.map(lambda x: (x[1], x[0])).sortByKey(ascending=False)

    results = sorted_customer_totals.collect()

    # Print the results
    for result in results:
        customer, price = result[1], result[0]
        print(f"{customer}: {price:.2f}")


if __name__ == "__main__":
    total_spent_by_customer()
