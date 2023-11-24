from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml import Pipeline

# Initialize Spark session
spark = SparkSession.builder.appName("RealEstatePrediction").getOrCreate()

# Load CSV file into a DataFrame
df = spark.read.csv("/files/realestate.csv", header=True, inferSchema=True)

# Select the relevant columns
selected_columns = ["HouseAge", "DistanceToMRT", "NumberConvenienceStores", "PriceOfUnitArea"]

# Select the last 40 rows for testing
test_data = df.orderBy("no", ascending=False).limit(40)
train_data = df.subtract(test_data)

# Assemble the features into a single vector column
assembler = VectorAssembler(inputCols=["HouseAge", "DistanceToMRT", "NumberConvenienceStores"], outputCol="features")

# Create a DecisionTreeRegressor
dt = DecisionTreeRegressor(featuresCol="features", labelCol="PriceOfUnitArea")

# Create a pipeline with the assembler and the decision tree
pipeline = Pipeline(stages=[assembler, dt])

# Fit the pipeline to the training data
model = pipeline.fit(train_data)

# Make predictions on the test data
predictions = model.transform(test_data)

# Show the predictions
predictions.select("features", "PriceOfUnitArea", "prediction").show(40)

# Evaluate the model (you may want to use a proper evaluation metric depending on your problem)
from pyspark.ml.evaluation import RegressionEvaluator

evaluator = RegressionEvaluator(labelCol="PriceOfUnitArea", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")
