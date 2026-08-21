from db.database import create_tables
from services.market_service import list_prices, save_price


def main():
    create_tables()

    while True:
        print("\n=== Insight Module ===")
        print("1. Add Mandi Price")
        print("2. View Mandi Prices")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            market = input("Mandi ka naam: ")
            commodity = input("Commodity ka naam: ")

            try:
                price = float(input("Price: "))
            except ValueError:
                print("Invalid price. Please enter a number (e.g. 2500 or 2500.50).")
                continue

            save_price(market, commodity, price)
            print("Price saved successfully!")

        elif choice == "2":
            prices = list_prices()

            print("\nMandi Prices:")
            for item in prices:
                print(item)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
