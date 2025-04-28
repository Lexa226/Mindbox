from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit
from pyspark.sql.utils import AnalysisException
import logging

class DfProductCategories:
    """
    Класс для обработки трёх Spark-таблиц «продукты – категории».
    """
    @staticmethod
    def get_all_products_categories(
        df_products: DataFrame,
        df_categories: DataFrame,
        df_product_categories: DataFrame
    ) -> DataFrame:
        """
        Статический метод класса, который объединяет все пары "продукт-категория" с "продуктами" без категории(NULL) и возвращает их.

        Args:
            df_products (DataFrame): таблица продуктов с колонками product_id, product_name.
            df_categories (DataFrame): таблица категорий с колонками category_id, category_name.
            df_product_categories (DataFrame): таблица со связями между df_products и df_categories с колонками product_id, category_id.

        Returns:
            DataFrame: новый DataFrame с колонками product_name, category_name,
                   где для «сирот» (без категорий) катего­рия = NULL.

        Raises:
            AnalysisException: если одной из таблиц не хватает нужных колонок.
            ValueError: если переданы некорректные данные.
            Exception: неожиданная ошибка.
        """
        try:
            prod_cat_pairs = (
                df_products
                .join(other=df_product_categories, on="product_id", how="inner")
                .join(other=categories, on="category_id", how="inner")
                .select("product_name", "category_name")
            )

            orphans = (
                df_products
                .join(other=df_product_categories, on="product_id", how="left_anti")
                .select("product_name")
                .withColumn("category_name", lit(None).cast("string"))
            )
        except AnalysisException as ae:
            logging.error(f"Ошибка аналитики Spark: {ae}")
            raise
        except ValueError as ve:
            logging.error(f"Переданы некорректные данные: {ve}")
            raise
        except Exception as e:
            logging.error(f"Неожиданная ошибка: {e}")
            raise

        else:
            return prod_cat_pairs.unionByName(orphans)


if __name__ == "__main__":
    spark = SparkSession.builder.appName("Products→Categories").getOrCreate()

    products = spark.read.csv("products.csv",   header=True, inferSchema=True)
    categories = spark.read.csv("categories.csv", header=True, inferSchema=True)
    product_categories = spark.read.csv("product_categories.csv", header=True, inferSchema=True)

    result_df = DfProductCategories.get_all_products_categories(
        df_products=products,
        df_categories=categories,
        df_product_categories=product_categories
    )

    result_df.show()
