from experiments.order_model import Order
from experiments.order_book import OrderBook


def print_book(book, title):
    snapshot = book.get_snapshot()

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("\nBIDS")
    if not snapshot["bids"]:
        print("No resting bids")
    else:
        for level in snapshot["bids"]:
            print(f"Price: {level['price']:.2f} | Total quantity: {level['quantity']}")
            for order in level["orders"]:
                print(
                    f"  {order['order_id']} | "
                    f"Remaining quantity: {order['quantity']}"
                )

    print("\nASKS")
    if not snapshot["asks"]:
        print("No resting asks")
    else:
        for level in snapshot["asks"]:
            print(f"Price: {level['price']:.2f} | Total quantity: {level['quantity']}")
            for order in level["orders"]:
                print(
                    f"  {order['order_id']} | "
                    f"Remaining quantity: {order['quantity']}"
                )

    print("\nMarket summary")
    print("Best bid:", snapshot["best_bid"])
    print("Best ask:", snapshot["best_ask"])
    print("Spread:", snapshot["spread"])


def print_trades(book):
    print("\n" + "=" * 60)
    print("EXECUTION RECORDS")
    print("=" * 60)

    if not book.trades:
        print("No trades executed")
        return

    for trade in book.trades:
        print(
            f"{trade.trade_id} | "
            f"Buyer: {trade.buy_order_id} | "
            f"Seller: {trade.sell_order_id} | "
            f"Price: {trade.price:.2f} | "
            f"Quantity: {trade.quantity} | "
            f"Timestamp: {trade.timestamp}"
        )


def main():
    book = OrderBook()

    print("PHASE 1: LIMIT ORDER BOOK DEMONSTRATION")
    print("Continuous double auction with price-time priority")

    # Add resting buy orders
    book.add_resting_order(
        Order("B001", "BUY", 100.00, 40, 40, 1)
    )
    book.add_resting_order(
        Order("B002", "BUY", 99.00, 30, 30, 2)
    )
    book.add_resting_order(
        Order("B003", "BUY", 100.00, 20, 20, 3)
    )

    # Add resting sell orders
    book.add_resting_order(
        Order("S001", "SELL", 102.00, 30, 30, 4)
    )
    book.add_resting_order(
        Order("S002", "SELL", 103.00, 50, 50, 5)
    )

    print_book(book, "INITIAL ORDER BOOK")

    # Submit an incoming buy order that crosses the spread
    incoming_order = Order(
        "B004",
        "BUY",
        103.00,
        65,
        65,
        6
    )

    print("\n" + "=" * 60)
    print("INCOMING ORDER")
    print("=" * 60)
    print("Order ID:", incoming_order.order_id)
    print("Side:", incoming_order.side)
    print("Limit price:", incoming_order.price)
    print("Quantity:", incoming_order.original_quantity)

    print("\nSubmitting order to the matching engine...")

    book.process_order(incoming_order)

    print_trades(book)

    print_book(book, "FINAL ORDER BOOK")

    print("\n" + "=" * 60)
    print("QUANTITY ACCOUNTING")
    print("=" * 60)

    accounting = book.get_quantity_accounting()

    for side, values in accounting.items():
        print(f"\n{side.upper()}")
        print("Submitted:", values["submitted"])
        print("Executed:", values["executed"])
        print("Cancelled:", values["cancelled"])
        print("Resting:", values["resting"])

    print("\nQuantity conservation:", book.check_quantity_conservation())
    print("\nDemonstration completed.")


if __name__ == "__main__":
    main()