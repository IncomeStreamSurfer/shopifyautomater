# Product SEO and Collection Maker System

This repository contains two Python scripts designed to enhance your Shopify store's product listings and collections using AI-powered content generation:

1. **`productseo.py`**: Automatically generates SEO-optimized product titles, descriptions, and tags.
2. **`collectionmaker.py`**: Creates smart collections in your Shopify store based on the generated tags.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setting Up Environment Variables](#setting-up-environment-variables)
- [Usage](#usage)
  - [1. Prepare Your CSV Files](#1-prepare-your-csv-files)
  - [2. Run `productseo.py`](#2-run-productseopy)
  - [3. Run `collectionmaker.py`](#3-run-collectionmakerpy)
- [Environment Variables Template](#environment-variables-template)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Introduction

This system leverages the power of AI to automate the process of optimizing product listings and creating collections in your Shopify store. By using Anthropic's Claude API and the Shopify API, the scripts perform the following tasks:

- **`productseo.py`**:
  - Generates new, SEO-optimized product titles.
  - Creates detailed HTML product descriptions.
  - Generates relevant tags for each product.
  - Outputs an updated CSV file with the new data.

- **`collectionmaker.py`**:
  - Reads the tags generated by `productseo.py`.
  - Generates SEO-friendly titles, handles, and descriptions for collections.
  - Creates smart collections in your Shopify store based on the tags.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7 or higher**
- **Pipenv** or **virtualenv** (recommended for creating a virtual environment)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone [https://github.com/yourusername/your-repo.git](https://github.com/IncomeStreamSurfer/shopifyautomater)
   cd your-repo
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: If a `requirements.txt` file is not provided, you can install the necessary packages individually:

   ```bash
   pip install anthropic python-dotenv requests
   ```

## Setting Up Environment Variables

Create a `.env` file in the root directory of your project to store your API keys and other sensitive information. Use the template provided in the [Environment Variables Template](#environment-variables-template) section.

## Usage

### 1. Prepare Your CSV Files

- **For `productseo.py`**:
  - Ensure you have a `products_export.csv` file containing your product data.
  - The CSV should have headers like `Title`, `Body (HTML)`, `Tags`, `Variant SKU`, etc.

- **For `collectionmaker.py`**:
  - The script reads from a `tags.csv` file containing the unique tags generated by `productseo.py`.
  - Make sure `tags.csv` is available in the same directory.

### 2. Run `productseo.py`

This script generates new product titles, descriptions, and tags.

```bash
python productseo.py
```

- **What it does**:
  - Reads `products_export.csv`.
  - Uses Anthropic's Claude API to generate:
    - New product titles.
    - Detailed product descriptions in HTML format.
    - A list of relevant tags.
  - Writes the updated product data to `updated_products.csv`.
  - Extracts all unique tags and saves them to `unique_tags.csv`.

**Important**: Ensure your Anthropic API key is set in the `.env` file.

### 3. Run `collectionmaker.py`

This script creates smart collections in your Shopify store based on the tags.

```bash
python collectionmaker.py
```

- **What it does**:
  - Reads tags from `unique_tags.csv`.
  - For each tag, it:
    - Generates an SEO-optimized collection title.
    - Creates a handle suitable for URLs.
    - Writes a brief HTML description.
    - Defines rules for the smart collection based on the tag.
  - Uses the Shopify API to create smart collections in your store.

**Important**: Ensure your Shopify API credentials are set in the `.env` file.

## Environment Variables Template

Create a `.env` file in your project's root directory and add the following variables:

```env
# Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Shopify Store Information
SHOPIFY_STORE_URL=https://your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_shopify_access_token
```

- **`ANTHROPIC_API_KEY`**: Your API key for Anthropic's Claude API.
- **`SHOPIFY_STORE_URL`**: Your Shopify store URL (e.g., `https://myshop.myshopify.com`).
- **`SHOPIFY_ACCESS_TOKEN`**: Your Shopify Admin API access token.

**Note**: Keep this file secure and do not commit it to version control.

## Troubleshooting

- **Anthropic API Errors**:
  - Ensure your API key is correct.
  - Check if you've exceeded your API usage limits.
  - Verify that the Anthropic API endpoint and model names are correct.

- **Shopify API Errors**:
  - Double-check your Shopify store URL and access token.
  - Ensure your Shopify API permissions allow for creating smart collections.
  - Verify the API version in the endpoint URL (e.g., `2024-01`).

- **CSV File Issues**:
  - Ensure all required columns are present in your CSV files.
  - Check for encoding issues (use UTF-8 encoding).

- **Dependencies**:
  - If you encounter module import errors, ensure all dependencies are installed.
  - Run `pip install -r requirements.txt` to install missing packages.

## License

This project is licensed under the [MIT License](LICENSE).

---

*For any issues or contributions, feel free to open an issue or a pull request on the repository.*
