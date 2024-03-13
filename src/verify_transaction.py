import sys
from db import conn

def analyze_transaction(transaction_id):
    if conn is not None:
        try:
            cur = conn.cursor()
            query_has_cbk = "SELECT * FROM transactions WHERE transaction_id = %s AND has_cbk = FALSE"
            cur.execute(query_has_cbk, (transaction_id,))
            result_has_cbk = cur.fetchone()
            if result_has_cbk is None:
                return 'Denied: high risk'

            score = 0
            query_device = "SELECT * FROM transactions WHERE transaction_id = %s AND device_id != 'NaN'"
            cur.execute(query_device, (transaction_id,))
            result_device = cur.fetchone()
            if result_device is None:
                score = score + 2
            
            query_transaction_amount = "SELECT * FROM transactions WHERE transaction_id = %s AND transaction_amount < 2000"
            cur.execute(query_transaction_amount, (transaction_id,))
            result_transaction_amount = cur.fetchone()
            if result_transaction_amount is None:
                score = score + 1
            if score > 2:
                return 'Denied: High Risk'

            query_transaction_date = "SELECT * FROM transactions WHERE transaction_id = %s AND EXTRACT(HOUR FROM transaction_date) > 6"
            cur.execute(query_transaction_date, (transaction_id,))
            result_transaction_date = cur.fetchone()
            if result_transaction_date is None:
                score = score + 1
            if score > 2:
                return 'Denied: High Risk'

            query_user_id = "SELECT user_id FROM transactions WHERE transaction_id = %s"
            cur.execute(query_user_id, (transaction_id,))
            result_user_id = cur.fetchone()
            query_total_card_number = "SELECT COUNT(DISTINCT card_number) FROM transactions WHERE user_id = %s GROUP BY user_id;"
            cur.execute(query_total_card_number, (result_user_id,))
            result_total_card_number = cur.fetchone()
            if result_total_card_number[0] > 3:
                score = score + 1
            if result_total_card_number[0] > 10:
                return 'Denied: High Risk'
            if score > 2:
                return 'Denied: High Risk'

            query_card_number = "SELECT card_number FROM transactions WHERE transaction_id = %s"
            cur.execute(query_card_number, (transaction_id,))
            result_card_number = cur.fetchone()
            query_card_number_amount = "SELECT SUM(transaction_amount) FROM transactions WHERE card_number = %s AND transaction_date > (transaction_date - INTERVAL '24 hours')"
            cur.execute(query_card_number_amount, (result_card_number,))
            result_card_number_amount = cur.fetchone()
            if result_card_number_amount[0] > 2000:
                score = score + 1
            if score > 2:
                return 'Denied: High Risk'

            query_merchant_id = "SELECT merchant_id FROM transactions WHERE transaction_id = %s"
            cur.execute(query_merchant_id, (transaction_id,))
            result_merchant_id = cur.fetchone()
            query_user_merchant = "SELECT COUNT(*)FROM transactions WHERE user_id = %s AND merchant_id = %s AND transaction_date > (transaction_date - INTERVAL '24 hours') GROUP BY user_id, merchant_id"
            cur.execute(query_user_merchant, (result_user_id, result_merchant_id))
            result_user_merchant = cur.fetchone()
            if result_user_merchant[0] > 3:
                score = score + 2
            if score > 2:
                return 'Denied: High Risk'

            cur.close()
            conn.close()

            return 'Approved'
        except Exception as e:
            print("Error:", e)
            return None
    else:
        return None

def main():
    if len(sys.argv) < 2:
        print("Please provide a transaction_id.")
        return

    transaction_id = sys.argv[1]
    result = analyze_transaction(transaction_id)
    if result:
        print(result)
    else:
        print("Transaction not found.")

if __name__ == "__main__":
    main()
