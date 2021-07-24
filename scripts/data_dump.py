import psycopg2

DATABASE_URL = "postgresql://cliff:password@localhost:5432/cliff"
TABLE_NAME = "core_item"
CSV_FILE_PATH = "dev/dump/Greendeck SE Assignment Task 1.csv"


def dump_csv_file_to_postgres_table():
    """
    Load csv file and dump the contents to the core_item table.
    Make sure you've created the table first before importing the csv file.
    """
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with open(
            CSV_FILE_PATH, "r", encoding="latin1"
        ) as csv_dump, conn.cursor() as cursor:
            next(csv_dump)  # Skip the header row.
            cursor.copy_from(
                csv_dump,
                TABLE_NAME,
                sep=",",
                columns=(
                    "name",
                    "brand_name",
                    "regular_price_value",
                    "offer_price_value",
                    "currency",
                    "classification_l1",
                    "classification_l2",
                    "classification_l3",
                    "classification_l4",
                    "image_url",
                ),
            )
        # commit the changes and close the conn.
        conn.commit()
        conn.close()
        print(f"Succeffully dumped the csv file to {TABLE_NAME} table.")

    except psycopg2.Error:
        print(
            f"Table {TABLE_NAME} does not exist. Make sure you start the server first and then dump the csv data."  # noqa
        )


dump_csv_file_to_postgres_table()
