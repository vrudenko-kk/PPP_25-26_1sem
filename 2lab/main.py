if __name__ == "__main__":
    pass  # Ваш код здесь

exchange_rate = input().replace(',', '').split()
exchange_request = input().split()
currencies = dict()
for i in range(0, len(exchange_rate), 3):
    key = exchange_rate[i], exchange_rate[i + 1]
    currencies[key] = float(exchange_rate[i + 2])

p = [i for i in currencies.keys()]
for i in range(len(p)):
    for j in range(len(p)):
        if p[i][1] == p[j][0]:
            currencies[(p[i][0], p[j][1])] = currencies[p[i]] * currencies[p[j]]
l = [i for i in currencies.keys()]


start_amount = int(exchange_request[0])
start_currency = exchange_request[1]

print(start_amount, start_currency, end=' -> ')
for i in range(2, len(exchange_request)):
    try:
        print(int(start_amount * currencies[start_currency, exchange_request[i]]), exchange_request[i], end=' ')
    except Exception as e:
        print(f"Возникла ошибка {e}", end='')
    if len(exchange_request) - i > 1:
        print('-> ', end='')
