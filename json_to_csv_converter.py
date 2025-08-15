import json
import csv

# --- Paste your JSON data inside the triple quotes below ---
json_data_string = """
[
  {
    "leads_data": [
      {
        "first_name": "Wang",
        "last_name": "Lucy",
        "name": "Wang Lucy",
        "job_title": "Marketing Manager",
        "company_name": "Phoenix Medical Taiwan Co., Ltd",
        "company_size": "2",
        "industry": [
          "cosmetics"
        ],
        "location": "Taiwan",
        "email": "lucy.wang@phoenixtaiwan.com",
        "phone": "+886227015157",
        "linkedIn_url": "http://www.linkedin.com/in/wang-lucy-64652047",
        "keywords": [
          "atopic dermatitis",
          "rheumotology",
          "eczema",
          "psoriasis"
        ],
        "source_query_criteria": {
          "mainQuery": "I'm looking for the contact information of CEOs, CMOs, Marketing managers at cosmetics companies based in Taiwan",
          "filters": {
            "jobTitle": "",
            "industry": "",
            "location": "",
            "companySize": "",
            "companyNames": [],
            "keywords": []
          }
        },
        "icebreaker": null
      },
      {
        "first_name": "Steven",
        "last_name": "Ko",
        "name": "Steven Ko",
        "job_title": "Founder CEO ",
        "company_name": "O'right",
        "company_size": "54",
        "industry": [
          "cosmetics"
        ],
        "location": "Taoyuan City, Taiwan",
        "email": "steven_ko@oright.com.tw",
        "phone": "+88634116789",
        "linkedIn_url": "http://www.linkedin.com/in/stevenko%e8%91%9b%e6%9c%9b%e5%b9%b3",
        "keywords": [
          "first carbon neutral shampoo in the world",
          "first carbon footprint wave member for taiwan",
          "first company to achieve carbon trading in taiwan",
          "pas 2050",
          "pas 2060",
          "katerva award environmental finalist",
          "sustainability",
          "green beauty",
          "hair care",
          "skin care",
          "zero carbon",
          "zero impact",
          "carbon footprint",
          "sdgs",
          "esg",
          "sdg",
          "sustainable",
          "natural",
          "green",
          "cosmetic",
          "sustainable beauty",
          "clean products",
          "natural ingredients",
          "environmental protection",
          "green philosophy",
          "eco-friendly",
          "carbon neutral",
          "biodegradable packaging",
          "sustainable packaging",
          "herbal skincare",
          "hair care products",
          "private label",
          "green certifications",
          "sustainability report",
          "green building",
          "climate action",
          "sustainable business",
          "plant-based ingredients",
          "wild rose oil",
          "caffeine shampoo",
          "moisturizing conditioner",
          "hair styling products",
          "body wash",
          "personal care",
          "fragrance",
          "beauty lifestyle",
          "scalp care",
          "recyclable materials",
          "award-winning design",
          "tree in a bottle",
          "coffee extract",
          "biodegradable materials",
          "green charity",
          "eco-conscious",
          "renewable energy",
          "climate change initiatives",
          "forest preservation",
          "beach cleanup",
          "carbon footprint management",
          "green awards",
          "community involvement",
          "social responsibility",
          "earth hour",
          "plant a tree program",
          "environmental education",
          "circular economy",
          "innovation in beauty",
          "nature-inspired products",
          "environmental services",
          "renewables & environment",
          "clean energy & technology"
        ],
        "source_query_criteria": {
          "mainQuery": "I'm looking for the contact information of CEOs, CMOs, Marketing managers at cosmetics companies based in Taiwan",
          "filters": {
            "jobTitle": "",
            "industry": "",
            "location": "",
            "companySize": "",
            "companyNames": [],
            "keywords": []
          }
        },
        "icebreaker": null
      },
      {
        "first_name": "Louise",
        "last_name": "Robertson",
        "name": "Louise Robertson",
        "job_title": "Founder and CEO",
        "company_name": "De Ce Jour",
        "company_size": "1",
        "industry": [
          "cosmetics"
        ],
        "location": "Taipei, Taiwan",
        "email": "louise@decejour.com.tw",
        "phone": null,
        "linkedIn_url": "http://www.linkedin.com/in/robertson-louise",
        "keywords": [],
        "source_query_criteria": {
          "mainQuery": "I'm looking for the contact information of CEOs, CMOs, Marketing managers at cosmetics companies based in Taiwan",
          "filters": {
            "jobTitle": "",
            "industry": "",
            "location": "",
            "companySize": "",
            "companyNames": [],
            "keywords": []
          }
        },
        "icebreaker": null
      },
      {
        "first_name": "Erin",
        "last_name": "Lo",
        "name": "Erin Lo",
        "job_title": "Assistant Trade Marketing Manager",
        "company_name": "ELEMIS",
        "company_size": "780",
        "industry": [
          "cosmetics"
        ],
        "location": "Taiwan",
        "email": "erin.lo@elemis.com",
        "phone": null,
        "linkedIn_url": "http://www.linkedin.com/in/erin-lo-57b65819a",
        "keywords": [
          "skincare",
          "anti-aging",
          "moisturizer",
          "cleanser",
          "exfoliator",
          "serum",
          "facial",
          "spa treatments",
          "natural ingredients",
          "sensitive skin",
          "hydrate",
          "nourish",
          "rejuvenate",
          "luxury skincare",
          "eye cream",
          "face mask",
          "acne treatment",
          "sun protection",
          "cleansing balm",
          "body care",
          "men's grooming",
          "aromatherapy",
          "professional skincare",
          "retinol",
          "facial oils",
          "skin brightening",
          "hydrating mist",
          "anti-wrinkle",
          "toner",
          "skin repair",
          "pore refining",
          "extraction tools",
          "beauty tools",
          "essence",
          "skin therapy",
          "whitening products",
          "self-care",
          "wellness products",
          "cosmetic formulations",
          "vegan skincare",
          "cruelty-free",
          "professional treatments",
          "skin analysis",
          "moisture boost",
          "therapeutic",
          "premium ingredients",
          "skincare routine",
          "holistic approach",
          "anti-aging solutions",
          "clinical trials",
          "sustainable practices",
          "biodiversity",
          "environmental responsibility",
          "skincare innovation",
          "b corp certified",
          "pro-collagen range",
          "superfood products",
          "cleansing balms",
          "moisturizers",
          "wellness brand",
          "personal care products",
          "spa & wellness services",
          "online shopping",
          "beauty community",
          "influencer marketing",
          "target demographic",
          "female audience",
          "age 25-34",
          "global presence",
          "award-winning brand",
          "customer satisfaction",
          "skincare efficacy",
          "luxury beauty",
          "eco-friendly packaging",
          "skincare technology",
          "premium skincare",
          "skincare routines",
          "rejuvenating treatments",
          "skincare education",
          "social impact initiatives",
          "health care",
          "health, wellness & fitness",
          "hospital & health care",
          "e-commerce",
          "consumer internet",
          "consumers",
          "internet",
          "information technology & services"
        ],
        "source_query_criteria": {
          "mainQuery": "I'm looking for the contact information of CEOs, CMOs, Marketing managers at cosmetics companies based in Taiwan",
          "filters": {
            "jobTitle": "",
            "industry": "",
            "location": "",
            "companySize": "",
            "companyNames": [],
            "keywords": []
          }
        },
        "icebreaker": null
      },
      {
        "first_name": "Kaitlin",
        "last_name": "Lin",
        "name": "Kaitlin Lin",
        "job_title": "PA to CEO",
        "company_name": "O'right",
        "company_size": "54",
        "industry": [
          "cosmetics"
        ],
        "location": "Taipei, Taiwan",
        "email": "kaitlin.lin@oright.inc",
        "phone": "+88634116789",
        "linkedIn_url": "http://www.linkedin.com/in/marketerkaitlin",
        "keywords": [
          "first carbon neutral shampoo in the world",
          "first carbon footprint wave member for taiwan",
          "first company to achieve carbon trading in taiwan",
          "pas 2050",
          "pas 2060",
          "katerva award environmental finalist",
          "sustainability",
          "green beauty",
          "hair care",
          "skin care",
          "zero carbon",
          "zero impact",
          "carbon footprint",
          "sdgs",
          "esg",
          "sdg",
          "sustainable",
          "natural",
          "green",
          "cosmetic",
          "sustainable beauty",
          "clean products",
          "natural ingredients",
          "environmental protection",
          "green philosophy",
          "eco-friendly",
          "carbon neutral",
          "biodegradable packaging",
          "sustainable packaging",
          "herbal skincare",
          "hair care products",
          "private label",
          "green certifications",
          "sustainability report",
          "green building",
          "climate action",
          "sustainable business",
          "plant-based ingredients",
          "wild rose oil",
          "caffeine shampoo",
          "moisturizing conditioner",
          "hair styling products",
          "body wash",
          "personal care",
          "fragrance",
          "beauty lifestyle",
          "scalp care",
          "recyclable materials",
          "award-winning design",
          "tree in a bottle",
          "coffee extract",
          "biodegradable materials",
          "green charity",
          "eco-conscious",
          "renewable energy",
          "climate change initiatives",
          "forest preservation",
          "beach cleanup",
          "carbon footprint management",
          "green awards",
          "community involvement",
          "social responsibility",
          "earth hour",
          "plant a tree program",
          "environmental education",
          "circular economy",
          "innovation in beauty",
          "nature-inspired products",
          "environmental services",
          "renewables & environment",
          "clean energy & technology"
        ],
        "source_query_criteria": {
          "mainQuery": "I'm looking for the contact information of CEOs, CMOs, Marketing managers at cosmetics companies based in Taiwan",
          "filters": {
            "jobTitle": "",
            "industry": "",
            "location": "",
            "companySize": "",
            "companyNames": [],
            "keywords": []
          }
        },
        "icebreaker": null
      },
      {
        "first_name": "Ya-Yen",
        "last_name": "Chin",
        "name": "Ya-Yen Chin",
        "job_title": "Senior Marketing Manager",
        "company_name": "Memebox Corporation",
        "company_size": "230",
        "industry": [
          "cosmetics"
        ],
        "location": "Taiwan",
        "email": "roxanne.chin@memebox.com",
        "phone": "+18312108688",
        "linkedIn_url": "http://www.linkedin.com/in/ya-yen-chin-3b36a735",
        "keywords": [
          "ecommerce",
          "beauty & cosmetics",
          "social media marketing",
          "e-commerce",
          "mobile commerce",
          "beauty",
          "consumer internet",
          "internet",
          "information technology",
          "multi-use",
          "base",
          "eye",
          "lip",
          "tool",
          "event",
          "self-expression",
          "empower",
          "global shipping",
          "black friday",
          "fun",
          "individuality",
          "makeup",
          "k-beauty",
          "lips",
          "eyes",
          "owner empowerment",
          "beauty tools",
          "self representation",
          "color",
          "palette",
          "cosmetic products",
          "fashion",
          "mainstream",
          "creative",
          "unique",
          "reminder",
          "self-identity",
          "inclusive beauty",
          "skincare",
          "affordable makeup",
          "high quality",
          "new arrivals",
          "product range",
          "trending",
          "versatile",
          "easy application",
          "makeup essentials",
          "beauty supply",
          "discounts",
          "online shopping",
          "price reduction",
          "brand loyalty",
          "social media",
          "customer engagement",
          "beauty tips",
          "community building",
          "international delivery",
          "beauty products",
          "innovative beauty solutions",
          "data-driven innovation",
          "sustainability",
          "vegan products",
          "global presence",
          "subscription model",
          "influencer marketing",
          "beauty enthusiasts",
          "diverse brand portfolio",
          "customer-centric",
          "inclusivity",
          "personal expression",
          "online retail",
          "partnerships",
          "retail distribution",
          "beauty trends",
          "youthful demographic",
          "product curation",
          "private label",
          "beauty experience",
          "market expansion",
          "beauty community",
          "eco-friendly products",
          "beauty sampling",
          "niche market",
          "consumers",
          "information technology & services",
          "marketing & advertising",
          "environmental services",
          "renewables & environment"
        ],
        "source_query_criteria": {
          "mainQuery": "I'm looking for the contact information of CEOs, CMOs, Marketing managers at cosmetics companies based in Taiwan",
          "filters": {
            "jobTitle": "",
            "industry": "",
            "location": "",
            "companySize": "",
            "companyNames": [],
            "keywords": []
          }
        },
        "icebreaker": null
      }
    ]
  }
]
"""

def convert_json_to_csv(json_string, output_filename="leads.csv"):
    """
    Parses a JSON string, extracts lead data, and writes it to a CSV file.

    Args:
        json_string (str): The string containing the JSON data.
        output_filename (str): The name of the output CSV file.
    """
    print("Processing JSON data...")

    # 1. Parse the JSON string into a Python object
    try:
        data = json.loads(json_string)
        # Access the nested list of leads
        leads_list = data[0]['leads_data']
    except (json.JSONDecodeError, IndexError, KeyError) as e:
        print(f"Error parsing or accessing JSON data: {e}")
        return

    if not leads_list:
        print("No leads found in the JSON data.")
        return

    # 2. Define the headers for the CSV file
    # We add 'source_query' to replace the complex 'source_query_criteria' object
    headers = [
        'first_name', 'last_name', 'name', 'job_title', 'company_name',
        'company_size', 'industry', 'location', 'email', 'phone',
        'linkedIn_url', 'keywords', 'source_query', 'icebreaker'
    ]

    processed_rows = []
    # 3. Process each lead record to flatten complex fields
    for lead in leads_list:
        row = {}
        for header in headers:
            # Handle the special cases first
            if header == 'keywords' or header == 'industry':
                # Join list items into a single string, handle None
                value = lead.get(header)
                row[header] = '; '.join(value) if isinstance(value, list) else ''
            elif header == 'source_query':
                # Extract the nested 'mainQuery' value safely
                row[header] = lead.get('source_query_criteria', {}).get('mainQuery', '')
            else:
                # For all other fields, get the value and handle None
                value = lead.get(header)
                row[header] = '' if value is None else value
        processed_rows.append(row)

    # 4. Write the processed data to a CSV file
    print(f"Writing data to {output_filename}...")
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # DictWriter maps dictionaries to CSV rows automatically
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            
            # Write the header row
            writer.writeheader()
            
            # Write all the processed rows
            writer.writerows(processed_rows)
        print(f"\nSuccessfully converted JSON to {output_filename}!")
    except IOError as e:
        print(f"Error writing to file: {e}")

# --- Run the conversion ---
# (I've truncated your JSON for this example, but you can paste the full data)
convert_json_to_csv(json_data_string)