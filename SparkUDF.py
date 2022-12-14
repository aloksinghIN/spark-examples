import re
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *


def parse_gender(gender):
    female_pattern = r"^f$|f.m|w.m"
    male_pattern = r"^m$|ma|m.l"
    if re.search(female_pattern, gender.lower()):
        return "Female"
    elif re.search(male_pattern, gender.lower()):
        return "Male"
    else:
        return "Unknown"


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("UDF in spark") \
        .master("local[2]") \
        .getOrCreate()

    survey_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("data/survey.csv")

    survey_df.show(10)

    #using udf in dataframe way

    parse_gender_udf = udf(parse_gender, returnType=StringType())
    print("Catalog Entry:")
    [print(r) for r in spark.catalog.listFunctions() if "parse_gender" in r.name]

    survey_df2 = survey_df.withColumn("Gender", parse_gender_udf("Gender"))
    survey_df2.show(10)

    # using udf in spark-sql way
    spark.udf.register("parse_gender_udf", parse_gender, StringType())
    print("Catalog Entry:")
    [print(r) for r in spark.catalog.listFunctions() if "parse_gender" in r.name]

    survey_df3 = survey_df.withColumn("Gender", expr("parse_gender_udf(Gender)"))
    survey_df3.show(10)
