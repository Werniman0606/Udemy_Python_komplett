cart_prices = [20, 3.5, 6.49, 8.99, 9.99, 14.98]


def list_sum(l):
    total = 0
    for i in l:
        total = total + i
    print(total)


list_sum(cart_prices)
