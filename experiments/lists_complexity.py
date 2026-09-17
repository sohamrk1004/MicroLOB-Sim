#SectionA
orders = [
    "BUY001",
    "SELL001",
    "BUY002",
]

for order in orders:
    print(order)
    print(orders[0])
    print(orders[2])
orders.append("SELL002")
print(orders)
removed_order = orders.pop()
print(removed_order)
print("BUY001" in orders)
print("BUY999" in orders)


#SectionB
orders2 = [
    "BUY001",
    "SELL001",
    "BUY002",
    "SELL002",
    "BUY003",
    "SELL003",
]

for order in orders2:
    print(order)
#SectionC
quantities = [25, 40, 15, 60, 30, 70]

print(len(orders2))
print(quantities[0])
print(quantities[5])
print(quantities[0] + quantities[1] + quantities[2] + quantities[3]+ quantities[4] + quantities[5])
print(40 in quantities)
removed_order2 = orders2.pop()
print(removed_order2)


#SectionD
# orders[0] is O(1) because it is direct indexing
#orders.append("BUY999") is O(1) amortised because most appends take constant time, although occasional resizing can require more work.
#orders.pop() is O(1) because it removes the final element without requiring all the preceding elements to shift.
#orders.pop(0) is O(n) because python needs the remaining elements to shift.
#"BUY999" in orders is O(n) because python needs to examine every element of list to find.
#for order in orders:print(order) is O(n) too because python needs to print every element.

