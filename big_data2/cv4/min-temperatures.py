from pyspark import SparkConf, SparkContext

# conf = SparkConf().setMaster("spark://e59872432739:7077").setAppName("MinTemperatures")
# conf = SparkConf().setMaster("local").setAppName("MinTemperatures")


def parse_line(line):
    fields = line.split(',')
    station_id = fields[0]
    entry_type = fields[2]
    temperature = fields[3]  # float(fields[3]) * .1 * (9.0 / 5.0) + 32.0
    return station_id, entry_type, temperature


def main():

    # cat /etc/hosts on spark container

    conf = SparkConf().setMaster("spark://172.18.0.2:7077").setAppName("MinTemperatures")
    sc = SparkContext(conf=conf)

    lines = sc.textFile("/files/1800.csv")
    parsed_lines = lines.map(parse_line)
    min_temps = parsed_lines.filter(lambda x: "TMIN" in x[1])
    station_temps = min_temps.map(lambda x: (x[0], x[2]))
    min_temps = station_temps.reduceByKey(lambda x, y: min(x, y))
    results = min_temps.collect()

    for result in results:
        print(result[0] + "\t{:.2f}F".format(result[1]))


def parseLine(line):
    fields = line.split(',')
    stationID = fields[0]
    entryType = fields[2]
    temperature = float(fields[3]) * 0.1 * (9.0 / 5.0) + 32.0
    return (stationID, entryType, temperature)


if __name__ == "__main__":
    conf = SparkConf().setMaster("spark://172.18.0.2:7077").setAppName("MaxTemperatures")
    sc = SparkContext(conf=conf)

    lines = sc.textFile("/files/1800.csv")
    parsedLines = lines.map(parseLine)
    #maxTemps = parsedLines.filter(lambda x: "TMAX" in x[1])
    stationTemps = parsedLines.map(lambda x: (x[0], x[2]))
    maxTemps = stationTemps.reduceByKey(lambda x, y: max(x, y))
    results = maxTemps.collect()

    for result in results:
        print(result[0] + "\t{:.2f}C".format((result[1] - 32) / 1.8))





