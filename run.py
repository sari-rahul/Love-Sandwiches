import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creads.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def validate_sales_data(values):
    """
    Inside the try ,tries to convert the values to integer
     and Raises value error if strings cannot be converted into int
     or if there aren't exactly 6 values.The loop will be
     repeated till the data is valid. 

    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                 f"Exactly 6 values required ,you added {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again..\n")
        return False

    return True


def get_sales_data():
    """
    Get sales data from the user 
    """
    while True:

        print("\nPlease enter the sales data from the last market")
        print("Data should be six figures separated by commas.")
        print("For Example:10,20,30,40,50,60 \n")

        data_str = input("Enter your data here :")

        sales_data = data_str.split(",")

        if validate_sales_data(sales_data):
            print("\nData valid")
            break

    return sales_data


def update_worksheet(data, worksheet):
    """
    Update the worksheet as per the data passed and the worksheet name
    """
    print(f"\nUpdating {worksheet} worksheet....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated sucessfully!!")

    
def calculate_surplus_data(sales_row):
    """
    Compares sales with stock and gets the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock.
        positive surplus indicates waste.
        negative surplus indicates extra made when the item is sold out

    """ 
    print("\nCalculating Surplus data.....")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock)-sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate average of each item from
    the last 5 day's sales and add 10% to it
    """
    print("\nCalculating the stock data...\n")
    
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data

def main():
    """
    run all functions
    """    
    data = get_sales_data()

    sales_data = [int(num) for num in data]

    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries()
    new_stock = calculate_stock_data(sales_columns)
    update_worksheet(new_stock,"stock")

    print("\nThe New stock should be :\n",new_stock)

print("\n\nWelcome to LOVE SANDWICHES data Automation")
print("------------------------------------------")
main()
