import os
import sys
import argparse
from fastapi import FastAPI

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)
sys.path.insert(0, os.path.dirname(APP_DIR))
sys.path.insert(0, os.path.abspath(os.path.join(APP_DIR, "..", "..")))

from db.database import create_tables
from services.market_service import list_prices, save_price
from api.market import router as market_router
from api.buyers import router as buyers_router
from api.logistics import router as logistics_router

# FastAPI application instance
app = FastAPI(title="Harvest Nexus - Insight Module")

app.include_router(market_router)
app.include_router(buyers_router)
app.include_router(logistics_router)

@app.get("/")
def home():
    return {"status": "running", "message": "Insight Module API is operational"}


def main_cli():
    create_tables()

    while True:
        print("\n=== Insight Module ===")
        print("1. Add Mandi Price")
        print("2. View Mandi Prices")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            region = input("Region/Mandi: ")
            crop_type = input("Crop/Commodity: ")

            try:
                price = float(input("Price per quintal: "))
            except ValueError:
                print("Invalid price. Please enter a number (e.g. 2500 or 2500.50).")
                continue

            save_price(crop_type, region, price)
            print("Price saved successfully!")

        elif choice == "2":
            prices = list_prices()

            print("\nMandi Prices:")
            for item in prices:
                print(f"Crop: {item[0]}, Region: {item[1]}, Price: {item[2]} per quintal, Date: {item[3]}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Harvest Nexus - Insight Module")
    parser.add_argument("--api", action="store_true", help="Start the FastAPI API Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the API on")
    args = parser.parse_args()

    if args.api:
        import uvicorn
        print("Starting FastAPI app...")
        uvicorn.run("main:app", host="0.0.0.0", port=args.port, reload=True)
    else:
        main_cli()
