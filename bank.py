from abc import ABC, abstractmethod  
from datetime import datetime  

class AccountInterface(ABC):  
    @abstractmethod  
    def deposit(self, amount: float) -> None:  
        pass  
    
    @abstractmethod  
    def withdraw(self, amount: float) -> None:  
        pass  

class BancAccount(AccountInterface):  
    def __init__(self, number: str, name: str) -> None:  
        self.__account_number = number  
        self.__owner_name = name  
        self.__balance = 0.0  

    def deposit(self, amount: float) -> None:  
        self.__balance += amount  
        with open("deposits.txt", "a+") as fl:  
            fl.write(f"Ushbu shaxs: {self.__owner_name} ushbu kunda: {datetime.now()} {amount} deposit qildi!\n\n")  

    def withdraw(self, amount: float) -> None:  
        if amount > self.__balance:  
            print("Hisobingizda yetarli mablag' mavjud emas!")  
        else:  
            self.__balance -= amount  
            with open("withdraws.txt", "a+") as fl:  
                fl.write(f"Ushbu shaxs: {self.__owner_name} ushbu kunda: {datetime.now()} {amount} miqdorda pul yechdi!\n\n")  
    
    def get_balance(self) -> float:  
        return self.__balance  
    
    def __str__(self) -> str:  
        return f"No: {self.__account_number}\nName: {self.__owner_name}\nBalance: {self.__balance}"  

class SavingsAccount(BancAccount):  
    def __init__(self, number: str, name: str, interest_rate: float) -> None:  
        super().__init__(number, name)  
        self.__interest_rate = interest_rate  

    def apply_interest(self) -> None:  
        interest = self.get_balance() * (self.__interest_rate / 100)  
        self.deposit(interest)  
        print(f"Hisobga {interest} miqdorida foiz qo'shildi.")  

class BankManager:  
    def __init__(self) -> None:  
        self.accounts = []  

    def create_account(self, account_number: str, owner_name: str, account_type: str, interest_rate: float = 0.0) -> None:  
        if account_type.lower() == "savings":  
            new_account = SavingsAccount(account_number, owner_name, interest_rate)  
        else:  
            new_account = BancAccount(account_number, owner_name)  
        
        self.accounts.append(new_account)  
        print(f"Hisob raqami {account_number} bo'yicha hisob yaratildi.")  

    def list_accounts(self) -> None:  
        if not self.accounts:  
            print("Hisoblar mavjud emas.")  
            return  
        for account in self.accounts:  
            print(account)  

    def find_account(self, account_number: str) -> BancAccount:  
        for account in self.accounts:  
            if account._BancAccount__account_number == account_number:  
                return account  
        print("Hisob topilmadi.")  
        return None  


def main():  
    manager = BankManager()  
    
    while True:  
        print("\nBank Meni:")  
        print("1. Hisob yaratish")  
        print("2. Hisobni ko'rish")  
        print("3. Pul qo'shish")  
        print("4. Pul yechish")  
        print("5. Hisob balansini ko'rish")  
        print("6. Foiz qo'llash")  
        print("7. Chiqish")  
        
        choice = input("Tanlovingizni kiriting (1-7): ")  
        
        if choice == '1':  
            account_number = input("Hisob raqamini kiriting: ")  
            owner_name = input("Egasining ismini kiriting: ")  
            account_type = input("Hisob turini kiriting (Barcha/Nuqul): ")  
            interest_rate = 0.0  
            
            if account_type.lower() == "savings":  
                interest_rate = float(input("Foiz stavkasini kiriting: "))  
            
            manager.create_account(account_number, owner_name, account_type, interest_rate)  
        
        elif choice == '2':  
            manager.list_accounts()  
        
        elif choice == '3':  
            account_number = input("Hisob raqamini kiriting: ")  
            account = manager.find_account(account_number)  
            if account:  
                amount = float(input("Miqdorni kiriting: "))  
                account.deposit(amount)  
        
        elif choice == '4':  
            account_number = input("Hisob raqamini kiriting: ")  
            account = manager.find_account(account_number)  
            if account:  
                amount = float(input("Miqdorni kiriting: "))  
                account.withdraw(amount)  
        
        elif choice == '5':  
            account_number = input("Hisob raqamini kiriting: ")  
            account = manager.find_account(account_number)  
            if account:  
                print(f"Hisob balans: {account.get_balance()}")  
        
        elif choice == '6':  
            account_number = input("Hisob raqamini kiriting: ")  
            account = manager.find_account(account_number)  
            if account and isinstance(account, SavingsAccount):  
                account.apply_interest()  
            else:  
                print("Bu hisobda foiz mavjuda emas yoki hisob topilmadi.")  
        
        elif choice == '7':  
            print("Dasturdan chiqyapsiz...")  
            break  
        
        else:  
            print("Noto'g'ri tanlov, iltimos qayta urinib ko'ring.")  

if __name__ == "__main__":  
    main()