from sqlalchemy import create_engine
import pandas as pd
import docx

################################################### CREATE ORACLE CONNECTION ################################################################################################


DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME =
PASSWORD =
HOST = 'oraasgtd093-scan.nam.nsroot.net'
PORT = 8889
SERVICE = 'PPNR2MD'
ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD + '@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE
engine = create_engine(ENGINE_PATH_WIN_AUTH, echo=True)

##################################################### PULL DATA FROM ORACLE INTO DF ###########################################################################################################################################################################################################


def get_queries():
    __doc__ = """ This function is used to get the queries from the docs and return """
    # Load the Word document
    doc = docx.Document("Queries.docx")

    # Initialize variables to store extracted data
    benchmark_rates_data = ""
    customer_rate_data = ""
    avg_bal_data = ""

    # Initialize a flag to identify the current section
    current_section = None

    # Iterate through paragraphs in the document
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            if text == "benchmark_rates":
                current_section = "benchmark_rates"
            elif text == "total_cd_actual_customer_rate":
                current_section = "customer_rate"
            elif text == "total_cd_actual_avg_bal":
                current_section = "avg_bal"
            else:
                if current_section == "benchmark_rates":
                    benchmark_rates_data += text
                elif current_section == "customer_rate":
                    customer_rate_data += text
                elif current_section == "avg_bal":
                    avg_bal_data += text

    # Remove extra whitespace from extracted data
    benchmark_rates_query = benchmark_rates_data.strip()
    total_cd_actual_customer_rate_query = customer_rate_data.strip()
    total_cd_actual_avg_bal_query = avg_bal_data.strip()
    return (
        benchmark_rates_query,
        total_cd_actual_customer_rate_query,
        total_cd_actual_avg_bal_query,
    )


def calculate_actual_value(first_quarter, half_quarter, last_quarter, current_month):
    __doc__ = """ This function calcualted the actual value and return """
    if current_month in [4, 5]:
        next_quarter = half_quarter
        next_month = 6
    else:
        next_quarter = last_quarter
        next_month = 12
    actual_value = first_quarter + (next_quarter - first_quarter) * (
        current_month - 3
    ) / (next_month - 3)
    return round(actual_value, 2)


def get_the_next_indexing_row(temporary_replenish_rates_table, current_month):
    __doc__ = """ This function is used to return the next indexing row """
    row = [None, current_month]
    for column in range(2, len(temporary_replenish_rates_table.columns)):
        first_quarter = temporary_replenish_rates_table.iloc[0, column]
        half_quarter = temporary_replenish_rates_table.iloc[1, column]
        last_quarter = temporary_replenish_rates_table.iloc[2, column]
        actual_value = calculate_actual_value(
            first_quarter, half_quarter, last_quarter, current_month
        )
        row.append(actual_value)
    return row


def generate_replenish_table(query, engine):
    __doc__ = """ This function is used to generate the replenish table """

    # Read data from the Excel file into a DataFrame
    # replenish_rates_df = pd.read_excel("benchmark_rates.xlsx")

    # Read data from the database into a DataFrame
    replenish_rates_df = pd.read_sql(query, engine)

    # Combine 'Year' and 'Month' columns into a single 'Year_Month' column
    replenish_rates_df["Year_Month"] = (
        replenish_rates_df["Year"].astype(str)
        + "-"
        + replenish_rates_df["Month"].astype(str)
    )

    # Convert "Year_Month" to "MMM-YYYY" format
    replenish_rates_df["Year_Month"] = pd.to_datetime(
        replenish_rates_df["Year_Month"]
    ).dt.strftime("%b-%Y")

    # Pivot the DataFrame to create a pivot table
    pivot_replenish_rates_df = replenish_rates_df.pivot(
        index="SAS_Variable", columns="Year_Month", values="Amount"
    )

    # Reorder columns based on the unique 'Year-Month' combinations
    year_month_order = replenish_rates_df["Year_Month"].unique()
    pivot_replenish_rates_df = pivot_replenish_rates_df[year_month_order]

    # Specify the desired order of 'SAS_Variable' rows
    sas_variable_order = ["US_IR_3M_RFRSWP", "US_IR_6M_RFRSWP", "US_IR_1Y_RFRSWP"]

    # Filter the rows of the pivot DataFrame based on 'SAS_Variable' order
    replenish_rates_table = pivot_replenish_rates_df.loc[sas_variable_order]

    # Reset the index and insert the '##' column with specified values
    replenish_rates_table.reset_index(inplace=True)
    replenish_rates_table.insert(1, "##", [3, 6, 12])

    current_month = 4
    temporary_replenish_rates_table = replenish_rates_table
    for index_to_insert in range(1, 9):
        if current_month != 6:
            next_row = get_the_next_indexing_row(
                temporary_replenish_rates_table, current_month
            )
            replenish_rates_table = pd.concat(
                [
                    replenish_rates_table.iloc[:index_to_insert],
                    pd.DataFrame(
                        [next_row],
                        columns=replenish_rates_table.columns,
                    ),
                    replenish_rates_table.iloc[index_to_insert:],
                ],
                ignore_index=True,
            )
        current_month += 1

    # Save the final DataFrame to an Excel file
    print("Replenish Rate Table Generated Successfully")
    replenish_rates_table.to_excel("replenish_rate.xlsx", index=False)


def handle_data_processing():
    __doc__ = """ Retrieve queries from the documents """

    (
        benchmark_rates_query,
        total_cd_actual_customer_rate_query,
        total_cd_actual_avg_bal_query,
    ) = get_queries()

    # Read various data sheets from Excel files
    total_columns_data_sheet = pd.read_excel("worksheets/total.xlsx")
    new_columns_data_sheet = pd.read_excel("worksheets/new.xlsx")
    cd_status_sheet = pd.read_excel("worksheets/cd_status.xlsx")
    positive_stress = pd.read_excel("worksheets/positive_stress.xlsx")
    negative_stress = pd.read_excel("worksheets/negative_stress.xlsx")
    as_of_two_thousand_nine = pd.read_excel("worksheets/Asof202009.xlsx")

    # Check if benchmark rates query exists, then generate replenish table
    if benchmark_rates_query:
        generate_replenish_table(benchmark_rates_query, engine)


if __name__ == "__main__":
    handle_data_processing()
