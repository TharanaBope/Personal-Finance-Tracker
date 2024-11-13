import tkinter as tk # Importing the tkinter module as tk
from tkinter import ttk,messagebox
import json
transactions = {} #Dictionary to store transactions
#GUI 
class FinanceTrackerGUI: # FinanceTrackerGUI class
    def __init__(self, root): # Initialize the class with a root window
        self.root = root # Assign the root window
        self.root.title("Personal Finance Tracker") # Set the title 
        self.search_var = tk.StringVar() # Initialize a StringVar object for search input
        self.create_widgets()
        self.transactions = self.load_transactions("Expense.json")
        self.display_transactions(self.transactions) # Display loaded transactions in the GUI

    def create_widgets(self):
        style = ttk.Style() # Call ttk.Style object to customize the appearance of widgets
        style.configure("Treeview.Heading", font=("Times New Roman", 15, "bold")) # Configure the style for Treeview headings to use a specific font
        style.configure("Treeview", font=('Arial Nova',10)) 
        style.configure("TScrollbar", troughcolor='lightgray', thumbcolor='darkgray') 

        # Frame for search bar and button
        self.search_frame = ttk.Frame(self.root, padding="10") 
        self.search_frame.pack(side=tk.TOP, fill=tk.X)

        self.search_label = ttk.Label(self.search_frame, text="SEARCH :", font=("Times New Roman", 14, "bold")) #Search label
        self.search_label.grid(row=0, column=0, padx=10, pady=10)

        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, font=('Arial Nova', 12),width=50) #Search Entry
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew') 

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_transactions) #Search Button
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.show_all_button = ttk.Button(self.search_frame, text='Show All/Clear Search', command=self.show_all_transactions) #View All / Clear Shearch Button
        self.show_all_button.grid(row=1, column=2, padx=0, pady=0) 

        self.transaction_details_label = ttk.Label(self.search_frame, text="TRANSACTION DETAILS", font=("Times New Roman", 20, "bold"), foreground='red') # Transaction Details Lable
        self.transaction_details_label.grid(row=1, column=1, padx=0, pady=5) 

        # Frame for table and scrollbar
        self.main_frame = ttk.Frame(self.root) 
        self.main_frame.pack(fill=tk.BOTH, expand=True , padx=50 , pady=10) 

        # Treeview for displaying transactions
        self.treeview = ttk.Treeview(self.main_frame, columns=("Date", "Transaction", "Amount"), show="headings")  #Treeview widget for displaying transactions, with specific columns and headings
        self.treeview.heading("Date", text="Date", command=self.sort_by_date)
        self.treeview.heading("Transaction", text="Transaction", command=self.sort_by_transaction)
        self.treeview.heading("Amount", text="Amount", command=self.sort_by_amount)
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Center the text in each column of the Treeview
        for column in self.treeview["columns"]:
            self.treeview.column(column, anchor="center")

        # Scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.treeview.yview, style='TScrollbar') # Create a vertical scrollbar for the Treeview
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y, expand=True) # Pack the scrollbar to the left of the main frame
        self.treeview.configure(yscrollcommand=self.scrollbar.set) # Configure the Treeview to update the scrollbar's position when scrolled

    def load_transactions(self, filename): 
        try: 
            with open(filename, 'r') as file: # Open the file in read mode
                return json.load(file) 
        except FileNotFoundError: # Catch the FileNotFoundError exception
            messagebox.showerror("Error", f"{filename} not found.")# Display Error message box indicating file not found
            return {} # Return an empty dictionary 
        except json.JSONDecodeError: # Catch the JSONDecodeError exception
            messagebox.showerror("Error", "Transactions file is not properly formatted.") # Display error message box indicating the transactions file is not properly formatted
            return {} 

    def display_transactions(self, transactions): 
        for item in self.treeview.get_children(): # Loop through all items currently in the treeview
            self.treeview.delete(item) # Delete each item to clear the treeview
        for category, items in transactions.items(): # Loop through each category in the transactions dictionary
            for item in items: 
                self.treeview.insert('', 'end', values=(item['date'], category, item['amount'])) # Insert a new row into the treeview for each item, with values for date, category, and amount

    def search_transactions(self): 
        search_term = self.search_var.get().lower() # Retrieve the search term from the search_var StringVar
        if not search_term:# Check if the search term is empty, and if so, show an error message and exit the method
            messagebox.showerror("Error", "Please enter a search.")
            return
        found = False# Initialize a flag to indicate whether any matching transactions were found
        for category, items in self.transactions.items():# Loop through each category in the transactions dictionary
            for item in items: # Loop through each item within the current category
                if search_term in item['date'].lower() or search_term in str(item['amount']) or search_term in category.lower(): # Check if the search term is found in the date, amount, or category of the item
                    found = True # If a match is found, set the found flag to True and break out of the inner loop
                    break
            if found: # If a match was found in the current category, break out of the outer loop
                break
        if not found:  # If no matching transactions were found, show an error message and exit the method
            messagebox.showerror("Error", "No Item found matching your search.")
            return
        for item in self.treeview.get_children(): # Clear the treeview by deleting all existing items
            self.treeview.delete(item)
        for category, items in self.transactions.items(): # Loop through each category in the transactions dictionary again
            for item in items: # Loop through each item within the current category
                if search_term in item['date'].lower() or search_term in str(item['amount']) or search_term in category.lower(): # Check if the search term is found in the date, amount, or category of the item
                    self.treeview.insert('', 'end', values=(item['date'], category, item['amount'])) # If a match is found, insert a new row into the treeview for the item
    
    def show_all_transactions(self):
        self.display_transactions(self.transactions) # Clear the current search results and display all transactions again
        self.search_var.set("")
    def sort_by_date(self): 
        self.sort_by_column("Date", False) # Call the sort_by_column method with "Date" as the column to sort by and False for the reverse flag

    def sort_by_transaction(self):
        self.sort_by_column("Transaction", False) 

    def sort_by_amount(self):
        self.sort_by_column("Amount", False) 

    def sort_by_column(self, col, reverse):
        data = [(self.treeview.set(k, col), k) for k in self.treeview.get_children()] # Create a list of tuples containing the values of the specified column and the item ID for each item in the treeview
        if col == "Amount":# If the column is "Amount", sort the data by converting the values to floats for numerical sorting
            data.sort(key=self.sort_key_amount, reverse=reverse)
        else:  # Otherwise, sort the data as strings
            data.sort(key=self.sort_key_other, reverse=reverse)
        for index in range(len(data)): # Move each item in the treeview to its new position based on the sorted data
            val, k = data[index]
            self.treeview.move(k, '', index)
        self.treeview.heading(col, command=self.sort_by_column_toggle(col)) # Update the heading of the sorted column to toggle the sort direction on the next click

    def sort_key_amount(self, item): # Define the sort_key_amount method within the FinanceTrackerGUI class
        return float(item[0]) # Return the value of the item as a float for sorting

    def sort_key_other(self, item): # Define the sort_key_other method within the FinanceTrackerGUI class
        return item[0] # Return the value of the item as a string for sorting

    def sort_by_column_toggle(self, col): # Define the sort_by_column_toggle method within the FinanceTrackerGUI class
        def toggle_sort(): # Define a nested function to toggle the sort direction of the specified column
            self.sort_by_column(col, not self.treeview.heading(col)['text'].endswith('▲'))  # Call the sort_by_column method with the current sort direction reversed
        return toggle_sort # Return the nested function
def gui_run():
    root = tk.Tk() # Create the root window
    root.geometry('750x350') # Set the window size
    app = FinanceTrackerGUI(root) # Initialize the FinanceTrackerGUI with the root window
    root.mainloop() # Start the Tkinter event loop

#CLI
def load_transactions(): #Function to load transactions from Json file
    global transactions 
    try:
        with open ('Expense.json','r') as t_data: 
            transactions = json.load(t_data) 
    except FileNotFoundError:
        print ('File Dose Not Exist.\nNew Expense file Has Been Created.\n') 
        transactions = {}

def save_transactions(): #Function to save transactions to a Json file
    with open('Expense.json', 'w') as t_data: 
        json.dump(transactions, t_data,indent = 4) 

def read_bulk_transactions_from_file(filename): #Function to read bulf trasaction from user input file and add them to the transactions dictionary
    global transactions #transactions as a global variable to access it outside functions
    try: #Try to open the specified file
        with open(filename, 'r') as E: ##open the file in read mode
            for line in E: #loop through each line
                expense_type, amount, date = line.strip().split(',') #split the line into expense type,amount,and date using commas
                expense_type = expense_type.upper() #convert the expense_type to upper case
                expense = {"amount": float(amount), "date": date} #create dictionary for expense with the amount converted to flaot and date
                if expense_type not in transactions: #check if expense_type already exists in transactions dictionary
                    transactions[expense_type] = [] #If not initialize with an empty list
                transactions[expense_type].append(expense) #Append new expense to the list of expenses for the given expense_type
        save_transactions() #after added save to the file
        print(f"Expenses Loaded From {filename} Successfully") #print succesfully message
    except FileNotFoundError:
        print(f"File {filename} Not Found.")

def add_transaction(): #Function to add new transacions to transactions dictionary
    while True:
        if not transactions:
            print("No Expense found.")
            print("")
        else:
            print("\nCurrent Expense Types:") #display current expense types
            for expense_type in transactions.keys():
                print(expense_type)
                print('')
            print('Choose Expense Type or Add New Expense Type')
            print('')
             
        try:
            expense_type = input('Enter Type of Expence: ').upper() #prompt user to enter typr off expense to add
            if not expense_type:
                print('Please Enter A Type of Expense!')
                continue
            if expense_type not in transactions: #if entered type does not exist in transactions dictionary add it
                transactions[expense_type] = []
            while True:
                try:
                    amount = float(input('Enter Expense Amount:'))
                    break
                except ValueError:
                    print('Incorrect Value.Try Again!')
            while True: 
                date = input('Enter Expense Date (YYYY-MM-DD):') 
                if len(date) == 10 and date[4] == '-' and date[7] == '-': #validate date formate
                        year = date[:4] 
                        month = date[5:7] 
                        day = date[8:] 
                        if year.isdigit() and month.isdigit() and day.isdigit(): 
                            if 1 <= int(month) <= 12 and 1 <= int(day) <= 31: 
                                break 
                            else:
                                print('Invalid Date Format. Enter Digits In Valid Range.') 
                        else:
                            print('Invalid Date Format. Enter Digit Values.') 
                else:
                    print('Invalid Date Format. Should be YYYY-MM-DD') 

            expense = {'amount': amount,'date': date} #create new expense dictionary with the entered amount and date
            transactions[expense_type].append(expense)  #add new expense to transactions list for the specified type
            save_transactions() 
            print('\nExpense added Successfully!') 
                
        except ValueError: 
                print('Incorrect Value. Try again!')
                continue
        another_Expense = input('Would you like to add another Expense? (Yes/No): ').lower() #Ask user if they want to add another expense
        if another_Expense != 'yes':
            break 
        add_transaction() 

def view_transactions(): #Function to view all transactions
    if not transactions:
        print("No Expense found.")
        return
    else:
      for expense_type, expense_list in transactions.items(): #loop through each transaction type and its corresponding list of transactions
        print(f"\n{expense_type}:")
        number = 1
        for expense in expense_list: #loop over each transaction in list
            print(f"Expense {number}) Amount: {expense['amount']}, Date: {expense['date']}")
            number +=1
            print('') 

def update_transaction(): #Function to update transactions
    if not transactions:
        print("No Expense found.")
        return
    while True:
        print('Current Expense Types') 
        view_transactions()
        print('') 
        expense_type = input("Enter the type of expense to update: ").upper() #prompt the user to enter the type of expense to update
        if expense_type not in transactions:
            print("Expense Type Not Found.\n")
            continue
        while True:
            try:
                number_to_update = int(input('Enter the Expense number to be updated:')) - 1 #prompt user to enter the number of the expense to update
                if not (0 <= number_to_update < len(transactions[expense_type])):
                    raise KeyError('Invalid Expense Number.')
                expense_data = transactions[expense_type][number_to_update]
                print(f'Current Expense details - Amount: {expense_data["amount"]}, Date: {expense_data["date"]}\n')
                while True:
                    update_choice = input('\nWhat would you like to update? (Amount/Date):').lower()
                    if update_choice == 'amount':
                        while True:
                            try:
                                transactions[expense_type][number_to_update]['amount'] = float(input('\nEnter new amount:'))
                                print('New Amount Is Successfully Updated.\n')
                                break
                            except ValueError:
                                print('Invalid Value. Please Enter A Valid Number.')
                    elif update_choice == 'date':
                        while True:
                            try:
                                new_date = input('\nEnter new date (YYYY-MM-DD):')
                                if len(new_date) == 10 and new_date[4] == '-' and new_date[7] == '-': #validate date formate
                                    new_year = new_date[:4]
                                    new_month = new_date[5:7]
                                    new_day = new_date[8:]
                                    if new_year.isdigit() and new_month.isdigit() and new_day.isdigit():
                                        if 1 <= int(new_month) <= 12 and 1 <= int(new_day) <= 31:
                                            transactions[expense_type][number_to_update]['date'] = new_date
                                            print('New Date is successfully updated.\n')
                                            break
                                        else:
                                            print('Invalid Date Format. Enter Digits In Valid Range.')
                                    else:
                                        print('Invalid Date Format. Enter Digit Values.')
                                else:
                                    print('Invalid Date Format. Should be YYYY-MM-DD')
                            except ValueError:
                                print('Invalid Value. Please Enter A Valid Date.')
                    else:
                        print('Invalid Update Choice. Please Try Again!')
                        continue
                    save_transactions()
                    another_choice_update = input('Would you like to update another choice? (Yes/No):') #Ask if the user wants to update another input
                    if another_choice_update.lower() != 'yes': 
                        break
            
            except KeyError as K:
                print(K)
            except ValueError:
                print('Invalid Value. Please Enter A Valid Value.')
            else:
                break
        another_expense_type_update = input('\nWould you like to update another expense type? (Yes/No):') #Ask if the user wants to update another transaction
        if another_expense_type_update.lower() != 'yes': #If user does not want to update another transaction
            print('') 
            print('Expenses Updated Sucessfully!') 
            break

def delete_transaction(): #Function to delete a transaction
    if not transactions:
        print('No Expenses found!')
        return
    while True:
        print('Current Expense Types')
        view_transactions()
        print('')
        expense_type = input("Enter the type of expense to delete: ").upper() #prompt user to enter the type of expense to delete
        if not expense_type: #check if the user input a type of expense
            print("Please enter a type of expense.")
            continue
        if expense_type not in transactions: #check if user input exists in transactions dictionary
            print("Expense type not found.\n")
            continue
        while True:
            try:
                number_to_delete_input = input('Enter the Expense number of the to delete: ')
                if not number_to_delete_input:
                    print("Please enter a valid expense number.")
                    continue
                number_to_delete = int(number_to_delete_input) - 1
                if 0 <= number_to_delete < len(transactions[expense_type]): #check if user input number is within valid range
                    del transactions[expense_type][number_to_delete] #Delete the spesified transaction from the list
                    print('Transaction deleted successfully.')
                    save_transactions()
                    if not transactions[expense_type]:  #Check if there are any transactions left for this type
                        delete_entire_type = input(f'NO Expenses left in {expense_type}\nWould you like to delete the entire expense type? (Yes/No):').lower() #prompt the user to confirm if they want to delete entire expense type
                        if delete_entire_type == 'yes':
                            del transactions[expense_type]
                            print('Entire expense type and Expenses have been deleted successfully.')
                            save_transactions()
                else:
                    print('Invalid Expense Number.')
                    continue
            except ValueError:
                print('Invalid Value. Please Enter A Valid Index.')
            else:
                break
        another_expense_type_delete = input('\nWould you like to delete another expense type? (Yes/No):') #prompt if would like to delete another type
        if another_expense_type_delete.lower() != 'yes':
            print('') 
            print('Expenses Deleted Successfully!') 
            break

def display_summary(): #Functon to dsiplay a summary af all transactions
    if not transactions:
        print('No transactions found!')
        return
    
    total_expenses = 0

    print("\nSummary of Expenses:\n")
    for expense_type, expenses in transactions.items(): #loop over each expense type in transactions dictionary
        total_expenses_type = sum(expense['amount'] for expense in expenses) #Calculate the total expenses for the current expense type by summing the all expense from that type
        total_expenses += total_expenses_type
        print(f"{expense_type}: Total Expenses = {total_expenses_type}") #print total expenses for the current type of expenses
    
    print(f"\nTotal expenses in all types: {total_expenses}") #print the total across all types 

def main_menu(): 
    load_transactions() 
    while True: 
        print("\nPersonal Finance Tracker") 
        print("1. Load Transactions from File")
        print("2. Add Expense") 
        print("3. View Expenses") 
        print("4. Update Expnse") 
        print("5. Delete Expense") 
        print("6. Display Summary")
        print("7. Display in GUI")
        print("8. Exit") 
        choice = input("Enter your choice: ") 
        print('') 

        if choice == '1':
            filename = input("Enter the filename to load bulk transactions from: ") 
            read_bulk_transactions_from_file(filename) 
        elif choice == '2':
            add_transaction() 
        elif choice == '3':
            view_transactions() 
        elif choice == '4':
            update_transaction() 
        elif choice == '5':
            delete_transaction() 
        elif choice == '6':
            display_summary()
        elif choice == '7':
            print('GUI Loaded')
            gui_run()
            print('----------')
            print('GUI Closed')
        elif choice == '8':
            while True:
                confirm_exit = input('Are you sure you want to exit the program?(Yes/No): ').lower()
                if confirm_exit in ('yes', 'no'):
                    if confirm_exit == 'yes':
                        print("Exiting program.\n")
                        break
                    else:
                        print('\nBack to main menu.\n')
                        break
                else:
                    print("Invalid input. Please enter 'Yes' or 'No'.") 
        else:
            print("Invalid choice. Please try again.") 

if __name__ == "__main__":
    main_menu()
