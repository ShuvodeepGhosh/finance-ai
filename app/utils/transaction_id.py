import hashlib


def generate_transaction_id(row):

    base_string = f"{row['date']}_{row['description']}_{row['amount']}"

    txn_hash = hashlib.md5(base_string.encode()).hexdigest()

    return txn_hash[:10]