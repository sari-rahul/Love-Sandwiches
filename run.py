import gspread
from google.oauth2.service_account import Credentials

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

        print("Please enter the sales data from the last market")
        print("Data should be six figures separated by commas.")
        print("For Example:10,20,30,40,50,60 \n")

        data_str = input("Enter your data here :")

        sales_data = data_str.split(",")

        if validate_sales_data(sales_data):
            print("Data valid")
            break

    return sales_data


def update_sales_worksheet(data):
    """
    Update sales worksheet,add new row with the list data provided )
    """
    print("Updating  sales worksheet .....\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated sucessfully !!")

def main():    
    data = get_sales_data()
    print(data)
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)

main()