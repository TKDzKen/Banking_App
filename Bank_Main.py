# Shitty side project
import random
import csv
import pandas as pd
import time

FILE = "Bank_File.csv"
file_update = pd.read_csv(FILE)
fieldnames = ['Username', 'Password', 'Acc_ID', 'PIN', 'Balance']

# Login Handler
def Login():
  if not User or not Pass or not PIN:
    print("Enter valid data in the provided fields")
    return 
  
  max_attempts = 3
  attempts = 0
  while attempts < max_attempts:
    with open(FILE, 'r') as Bank_File_Verify:
      reader = csv.DictReader(Bank_File_Verify)
      for row in reader:
        if row['Username'] == User and row['Password'] == Pass and row['PIN'] == PIN:
          print("Login successful!")
          ExistingAccount(User, Pass, PIN)
        
      attempts += 1
      print(f"Login failed, attempts made: {attempts}")
      return
    if attempts >= max_attempts:
      print("Too many failed attempts exiting...")
      return None
      exit(1)
      
# Configuring and Making a New Account
def NewAccount(): 
  new_user = input("New username: ")
  new_pass = input("New password: ")
  new_pass_verify = input("Verify new password: ")

  with open(FILE, 'r') as Bank_File:
    reader = csv.DictReader(Bank_File)
    for row in reader:
      if row['Username'] == new_user:
        print("Username is already in use, Please try again...")
        return NewAccount()
      
    with open(FILE, 'r') as Bank_File:
      reader = csv.DictReader(Bank_File)
      for row in reader:
        if row['Password'] == new_pass_verify:
          print("Password is already in use, Please try again...")
          return NewAccount()
    
  while True: 
    if new_pass != new_pass_verify:
      print("New password and verification pass dont match reenter password fields")
      continue
    if not new_pass or not new_user or not new_pass_verify:
      print("Enter all information in the provided fields")
      continue
    
    verify = input(f"Are you sure you want your username to be {new_user} and your password to be {new_pass_verify} (Y/N): ")

    if verify in ["Y", "y", "Yes", "yes"]:
      print("Continuing...")
    if verify in ["N", "n", "No", "no"]:
      print("Returning to reconfigure...")
      continue
    
    account_id = ''.join(str(random.randint(0, 9)) for _ in range(15))
    PIN = input("Please create a 6 digit PIN: ")

    if not PIN:
      print("A PIN is required to be made of security purposes")
      continue
    if len(PIN) <= 5 or len(PIN) > 6:
      print("A PIN with the maximum length of 6 digits is required")
      continue
    
    balance = 0.00

    file_input = [
      {'Username': new_user, 'Password': new_pass_verify, 'Acc_ID': account_id, 'PIN': PIN, 'Balance': balance}
    ]

    with open(FILE, 'a', newline='') as Bank_File:
      writer = csv.DictWriter(Bank_File, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(file_input)
    
    print(f"Please keep your Account ID secret, this is for you personal verification: {account_id}")
    print("Exiting program... select existing account on launch to ensure proper configuration")
    exit(0) 

# Existing Account Function
def ExistingAccount(Username, Password, PIN):
  class Account:
    def __init__(self, Username, Password, PIN, Balance):
      self.Username = Username
      self.__balance = float(Balance)

    def Deposit(self, amount):
      try:
        amount = float(amount)
      except ValueError:
        print("Invalid deposit amount (not a number).")
        return

      if amount > 0:
        self.__balance += amount
        print(f"You have deposited ${amount}, New Balance: ${self.__balance}")
        file_update.loc[file_update['Username'] == Username, 'Balance'] = self.__balance
        file_update.to_csv("Bank_File.csv", index=False)
      else:
        print("Invalid deposit amount (must be positive).")
        return 
    
    def Withdraw(self, amount):
      try:
        amount = float(amount)
      except ValueError:
        print("Invalid withdraw amount (not a number).")
        return

      if amount <= 0:
        print("Invalid withdraw amount (must be positive).")
        return

      if amount > self.__balance:
        print(f"Insufficient funds. Current Balance: ${self.__balance}")
        return

      self.__balance -= amount
      print(f"You have withdrawn ${amount}. New Balance: ${self.__balance}")

      file_update.loc[file_update['Username'] == self.Username, 'Balance'] = self.__balance
      file_update.to_csv(FILE, index=False)
    
    @property
    def Check_Balance(self):
      return self.__balance
      
  print(f"Welcome back, {User}")
  user_row = file_update.loc[file_update['Username'] == Username]
  if not user_row.empty:
    balance = user_row.iloc[0]['Balance']
  else:
    balance = 0.0
  
  #Account Management
  while True:
    my_account = Account(User, Pass, PIN, Balance=balance)
    choice = input("""Please choose a number
                    1. Deposit
                    2. Withdraw
                    3. Check Balance
                    4. Exit(full exit out of program)\n""")

    if not choice:
      print("Invalid number try again...")
      time.sleep(1)
      continue
    if choice == "1":
      deposit_amt = float(input("How much would you like to deposit: "))
      my_account.Deposit(deposit_amt)
      continue
    elif choice == "2":
      withdraw_amt = float(input("How much would you like to take out: "))
      my_account.Withdraw(withdraw_amt)
      continue
    elif choice == "3":
      print("$", my_account.Check_Balance)
      continue
    elif choice == "4":
      exit(0)
    else:
      print("Invalid choice, try again...")
      time.sleep(1)
      continue

# Main Init
if __name__ == "__main__":
  new_or_existing_account = input("Enter 1 for new account\n 2 for existing account\n 3 to exit\n ")
  if new_or_existing_account == "1": 
    NewAccount()
  elif new_or_existing_account == "2":
    User = input("Enter Username: ")
    Pass = input("Enter Password: ")
    PIN = input("Enter 6 digit PIN: ")
    Login()
  elif new_or_existing_account == "3":
    print("Exiting...")
    exit(0)
  else:
    print("Invalid user input, returning...")
    time.sleep(1)
    exit(1)