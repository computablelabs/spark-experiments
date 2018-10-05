from pyspark.sql import SparkSession
from pyspark.sql.types import *

schema = StructType([
    StructField('rsid', StringType()),
    StructField('chromosome', IntegerType()),
    StructField('position', IntegerType()),
    StructField('genotype', StringType())
])

spark = SparkSession.builder.appName("sql-test").getOrCreate()
df = spark.read.csv("s3a://my-dna-prototype-data/", header=False, schema=schema)
df.registerTempTable('genome')
results = spark.sql("select * from genome where genotype ='TT'").collect()

print("SQL results: ")
print(results)
