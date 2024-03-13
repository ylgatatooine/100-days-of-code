import pandas as pd
from collections import defaultdict
from langchain_community.llms import Ollama
import json

# Load your transactions data
def load_transactions_data(file_path):
    return pd.read_csv(file_path)

# Define the prompt template for categorization
prompt_template = """
Given the following transaction description: {description}
And the merchant name: {merchant}
Please categorize this transaction into one of the following categories:
- Food & Dining
- Shopping
- Entertainment
- Travel & Transportation
- Utilities
- Insurance
- Banking
- Health & Wellness
- Education
- Gifts & Donations
- Home & Auto
- Subscriptions & Memberships
- Government Fees
- Parking
- Other

Your response:
"""

# Update the categorize_transaction function to accept both description and merchant
def categorize_transaction(description, merchant):
    # Initialize Llama2 model (adjust parameters as necessary)
    llm = Ollama(model="llama2")

    # Format the prompt with both description and merchant
    formatted_prompt = prompt_template.format(description=description, merchant=merchant)

    # Predict the category using the updated prompt
    response = llm.invoke(formatted_prompt)

    # Debug: Print response type and content to understand its structure
    print("Response type:", type(response))
    print("Response content:", response)

    # Assuming the response structure and extracting category accordingly
    try:
        response_data = json.loads(response)  # Adjust if response is already in the correct format
    except json.JSONDecodeError:
        response_data = {}  # Fallback if parsing fails

    # Extract category from the response structure - adjust this based on actual structure and debugging prints
    category = response_data.get('choices', [{}])[0].get('text', 'Other').strip()

    return category


# Summarize transaction amounts by category
def summarize_transactions(transactions_df):
    category_totals = defaultdict(float)

    for _, row in transactions_df.iterrows():
        print(row['Description'] + row['Merchant'])
        category = categorize_transaction(row['Description'], row['Merchant'])
        amount = row['Amount (USD)']
        category_totals[category] += amount

    return category_totals


# Save the summarized data to a CSV file
def save_to_csv(category_totals, output_file_path):
    category_totals_df = pd.DataFrame(list(category_totals.items()), columns=['Category', 'Total Amount (USD)'])
    category_totals_df.to_csv(output_file_path, index=False)


# Main function to run the program
def main():
    input_csv_path = 'AppleCardTransactions.202402.csv'  # Update this path
    output_csv_path = 'CategoryTotals.202402.csv'  # Update this path

    transactions_df = load_transactions_data(input_csv_path)
    category_totals = summarize_transactions(transactions_df)
    save_to_csv(category_totals, output_csv_path)

    print(f"Analysis completed. Results saved to: {output_csv_path}")


if __name__ == "__main__":
    main()
