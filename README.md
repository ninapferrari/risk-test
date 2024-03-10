# Transaction Verification System

This project is designed to analyze and verify transactions based on various risk factors. It checks transactions against multiple criteria, such as device validity, chargeback occurrences, transaction amounts, and unusual transaction hours, to assign a risk score. Before verifying transactions, the system requires populating the database with transaction data using the `populate_db.py` script.

## Getting Started

These instructions will guide you on how to set up and run the Transaction Verification System on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- Python 3.x
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ninapferrari/risk-test.git

2. **Navigate to the project directory:**

   ```bash
   cd risk-test

3. **Install the required Python packages:**
   ```bash
    pip install -r requirements.txt

4. **Set up your PostgreSQL database:**

- Update the db.py file with your PostgreSQL user information.
- Create a database named risk_analysis.

### Populating the Database
Before verifying any transactions, you need to populate your database with transaction data:

1. **Run the populate_db.py script:**
   ```bash
    python3 populate_db.py

### Verifying Transactions
To verify a transaction, use the 'verify_transaction.py' script, passing the transaction_id as an argument:

1. **Run the verify_transaction.py script:**
   ```bash
    python3 verify_transaction.py <transaction_id>

The system will analyze the specified transaction and output the result, either approving the transaction or denying it with a reason based on the risk score.

### Features
- Device Validation
- Chargeback Check
- Transaction Amount Check
- Transaction Time Check
- User Behavior Analysis
