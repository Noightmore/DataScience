from pyspark.sql import SparkSession


def main():
    # Create a Spark session
    spark = SparkSession.builder.appName("Idnes").master("local").getOrCreate()

    # using a data frame load local file ./data/idnes.txt
    df = spark.read.text("./data/idnes.txt")

    # convert each lone to json
    df = df.selectExpr("CAST(value AS STRING)")

    # parse json and process content
    df = df.selectExpr("get_json_object(value, '$.content') as content")
    df = df.selectExpr("lower(content) as content")
    df = df.selectExpr("regexp_replace(content, '[.,_*\n]', '') as content")
    df = df.selectExpr("split(content, ' ') as words")
    df = df.selectExpr("explode(words) as word")

    # filter out empty strings
    df = df.filter("length(word) > 6")

    # count words
    df = df.groupBy("word").count()
    df = df.orderBy("count", ascending=False)
    df.show(50)

    # stop spark session
    spark.stop()


if __name__ == "__main__":
    main()


# slova jakekoliv delky:
#
# +-----+-------+
# | word|  count|
# +-----+-------+
# |    a|2851447|
# |    v|2848880|
# |   se|2501054|
# |   na|2449395|
# |   že|1431621|
# |   je|1151879|
# |    z| 986876|
# |    s| 906844|
# |    o| 874131|
# |   to| 864282|
# |   do| 824990|
# |    i| 753547|
# |   ve| 593512|
# |   za| 575907|
# |  ale| 543217|
# |podle| 527616|
# |   by| 502233|
# |    k| 502225|
# |  pro| 471459|
# |   si| 459535|
# |   po| 412512|
# |   od| 341522|
# |který| 338130|
# |   už| 327017|
# |které| 315090|
# | jako| 303992|
# |  tak| 299315|
# | jeho| 272471|
# | také| 268188|
# | bude| 268166|
# | jsou| 268004|
# |   až| 261329|
# |  aby| 259502|
# |  byl| 256694|
# |    u| 245323|
# | před| 244806|
# |    -| 216711|
# | jsem| 216597|
# |  při| 216444|
# | řekl| 215217|
# |která| 214641|
# |   má| 211133|
# |  jen| 210414|
# | nebo| 209882|
# |   ze| 207947|
# | však| 203727|
# |   co| 189182|
# | když| 177302|
# |  jak| 176768|
# | bylo| 173037|
# +-----+-------+
# only showing top 50 rows


# slova delky 6:
#
# +------------+------+
# |        word| count|
# +------------+------+
# |     policie|156678|
# |   například|106646|
# |     protože|100661|
# |     několik| 84852|
# |   policisté| 76447|
# |   prezident| 76083|
# |   policejní| 68565|
# |     ministr| 65971|
# |     dalších| 65447|
# |     procent| 65152|
# |     jednání| 61460|
# |     milionů| 59878|
# |     případě| 57424|
# |  prezidenta| 56281|
# |     všechny| 54716|
# |   nemocnice| 53415|
# |     idnescz| 50893|
# |     pondělí| 50393|
# |     nakonec| 48647|
# |    poslední| 47188|
# |     později| 46687|
# |ministerstvo| 45425|
# | společnosti| 45132|
# |  rozhodnutí| 44127|
# |ministerstva| 42689|
# |    sociální| 42506|
# |   informace| 42388|
# |    předseda| 41832|
# |   prohlásil| 41815|
# |    několika| 41736|
# |     situace| 41681|
# |   zahraničí| 41185|
# |     premiér| 40805|
# |     situaci| 40425|
# |     oblasti| 39927|
# |     čtvrtek| 39739|
# |    evropské| 38593|
# |     zároveň| 38490|
# |   především| 38396|
# |     jednoho| 38334|
# |     dokonce| 38212|
# |  posledních| 38137|
# |    ministra| 35283|
# |    podařilo| 35243|
# |     některé| 33701|
# |  společnost| 33369|
# |    opatření| 32950|
# |   informací| 32798|
# |     všichni| 32574|
# |   listopadu| 32143|
# +------------+------+
# only showing top 50 rows


