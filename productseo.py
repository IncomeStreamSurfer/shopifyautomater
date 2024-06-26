import csv
import anthropic
import concurrent.futures
from collections import Counter

# Set up Anthropic API key
anthropic.api_key = "X"

def generate_tags(title, body, current_tags):
    prompt = f"You are writing for Supplies For Pets. DO NOT SAY NEW TAGS: DO NOT CHAT BACK. Only generate what is needed and nothing else. Also include the current tags in the list. When tagging please consider what piece of pet accessories you are assigning. A tag means it will appear in a product category, so make them accurate. The more tags the better. Make sure they're very relevant to the product. Please answer in this format: tag1,tag2,tag3,tag4,tag5,etc. Generate as many relevant tags as possible for an Online Pet Accessory shop with the following title, description, and current tags:\nTitle: {title}\nDescription: {body}\nCurrent Tags: {current_tags}\nNew Tags:"
    try:
        client = anthropic.Anthropic(api_key=anthropic.api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        generated_tags = response.content[0].text.strip()
        print(f"Generated tags for '{title}': {generated_tags}")
        return generated_tags
    except Exception as e:
        error_message = f"Error generating tags for '{title}': {str(e)}"
        print(error_message)
        return error_message

def generate_title(title, body):
    prompt = f"You are writing for Supplies for Pets. This is going directly onto a websit eso DO NOT WRITE NEW TITLE: DO NOT CHAT BACK. Only generate what is needed and nothing else. Generate a new SEO title pet's accessories Online. with the following existing title and description:\nExisting Title: {title}\nDescription: {body}\nNew Title: Please include what the product is at and if it has a brand and any other important distinguishing factors."
    try:
        client = anthropic.Anthropic(api_key=anthropic.api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=100,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        generated_title = response.content[0].text.strip()
        print(f"Generated title for '{title}': {generated_title}")
        return generated_title
    except Exception as e:
        error_message = f"Error generating title for '{title}': {str(e)}"
        print(error_message)
        return error_message

def generate_description(title, body):
    prompt = f"You are writing for Supplies for Pets. DO NOT WRITE NEW DESCRIPTION: DO NOT CHAT BACK. Only generate what is needed and nothing else. Respond in HTML but only with inside <p> tags, do not give unecessary <div> <html> and other tags. Lists and tables are good Generate a new, detailed description for a Pet's Accessory Online Shop. with the following title and existing description:\nTitle: {title}\nExisting Description: {body}\nNew Description:"
    try:
        client = anthropic.Anthropic(api_key=anthropic.api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        generated_description = response.content[0].text.strip()
        print(f"Generated description for '{title}': {generated_description}")
        return generated_description
    except Exception as e:
        error_message = f"Error generating description for '{title}': {str(e)}"
        print(error_message)
        return error_message

def process_products(products_csv, output_csv, max_concurrent_calls=5):
    with open(products_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        products = list(reader)
        fieldnames = reader.fieldnames + ['new_tags', 'new_title', 'new_description']

    processed_skus = set()
    all_tags = []

    with open(output_csv, mode='w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_calls) as executor:
            futures = {}
            for product in products:
                if product['Variant SKU'] not in processed_skus and product['Title'].strip():  # Check if Title is not empty
                    processed_skus.add(product['Variant SKU'])
                    futures[product['Variant SKU']] = (
                        product,
                        executor.submit(generate_title, product['Title'], product.get('Body (HTML)', '')),
                        executor.submit(generate_description, product['Title'], product.get('Body (HTML)', '')),
                        executor.submit(generate_tags, product['Title'], product.get('Body (HTML)', ''), product.get('Tags', ''))
                    )

            for product in products:
                if product['Variant SKU'] in futures:
                    original_product, title_future, description_future, tags_future = futures[product['Variant SKU']]
                    original_product['new_title'] = title_future.result()
                    original_product['new_description'] = description_future.result()
                    original_product['new_tags'] = tags_future.result()
                    writer.writerow(original_product)
                    output_file.flush()  # Flush the buffer to write the row immediately
                    
                    # Collect all tags
                    all_tags.extend([tag.strip() for tag in original_product['new_tags'].split(',')])
                else:
                    # Write the original row without changes if it was skipped
                    writer.writerow(product)
                    output_file.flush()

    return all_tags

def write_unique_tags(tags, output_file):
    unique_tags = sorted(set(tags))
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        f.write(','.join(unique_tags))

if __name__ == "__main__":
    all_tags = process_products('products_export.csv', 'updated_products33piamargot.csv', max_concurrent_calls=5)
    write_unique_tags(all_tags, 'unique_tags.csv')
    print("Process completed. Unique tags have been written to 'unique_tags.csv'.")