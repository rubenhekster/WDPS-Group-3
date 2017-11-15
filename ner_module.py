import testLibImport as a
from pyspark.context import SparkContext

a.great_me()

sc = SparkContext.getOrCreate()
sc.addPyFile("testLibImport")