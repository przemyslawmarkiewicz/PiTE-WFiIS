import json


def add_client_to_bank(bank, client):
    bank["clients"].append(client)
    client["has_bank_account"] = True
    client["bank_name"] = bank["name"]


def add_list_of_clients(bank, list_of_clients):
    for client in list_of_clients:
        add_client_to_bank(bank, client)


def delete_bank_account(bank, client):
    bank["clients"].remove(client)
    client["has_bank_account"] = False
    client["bank_name"] = ""


def change_bank(from_bank, to_bank, client):
    delete_bank_account(from_bank, client)
    add_client_to_bank(to_bank, client)


def deposit_money(client, amount):
    if client["has_bank_account"]:
        client["balance"] += amount
    else:
        raise ValueError("This person doesn't have bank account")


def withdraw_money(client, amount):
    balance = client["balance"]
    if client["has_bank_account"] and balance >= amount:
        client["balance"] -= amount
    else:
        if not client["has_bank_account"]:
            raise ValueError("This person doesn't have bank account")
        if balance < amount:
            raise ValueError("Client doesn't have enough money")


def transfer_money_from_to(client_1, client_2, amount):
    withdraw_money(client_1, amount)
    deposit_money(client_2, amount)


if __name__ == "__main__":
    bank_bnp = {
        "name": "BNP",
        "clients": []
    }

    bank_ubs = {
        "name": "UBS",
        "clients": []
    }

    bank_ing = {
        "name": "ING",
        "clients": []
    }

    f = open('clients.json')

    clients = json.load(f)

    tom_smith = clients[0]

    try:
        deposit_money(tom_smith, 231)
    except ValueError as msg:
        print(msg)

    add_list_of_clients(bank_bnp, clients[:4])
    add_list_of_clients(bank_ubs, clients[4:8])
    add_list_of_clients(bank_ing, clients[8:])

    deposit_money(tom_smith, 20553)

    ana_lewis = clients[4]
    print(tom_smith)
    print(ana_lewis)

    try:
        transfer_money_from_to(ana_lewis, tom_smith, 34)
    except ValueError as msg:
        print(msg)

    transfer_money_from_to(tom_smith, ana_lewis, 1234)

    print(tom_smith)
    print(ana_lewis)

    change_bank(bank_ubs, bank_ing, ana_lewis)

    print(ana_lewis)

    withdraw_money(ana_lewis, 234)

    print(ana_lewis)
