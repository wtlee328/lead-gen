# n8n Workflow for Prospecting with an Apify Crawler

This document outlines an n8n workflow that leverages an Apify crawler to generate prospect lists based on natural language inputs from a front-end application.

The workflow consists of the following steps:

## 1. Receive Input from Frontend

The workflow is triggered when it receives user-defined criteria for a prospect audience from a front-end interface.

## 2. Convert Input to an Apollo URL using an LLM

An LLM (Large Language Model) node is used to transform the natural language input into a functional Apollo.io search URL.

### LLM Prompt

The prompt engineering for this task is structured as follows:

"""

```
Your task is to take as input a natural language description of a prospect audience, and turn that into an Apollo Search URL. Here's an example of an Apollo Search URL: 
https://app.apollo.io/#/people?page=1&contactEmailStatusV2[]=verified&personTitles[]=project%20manager&personTitles[]=director&personLocations[]=United%20States&organizationIndustryTagIds[]=5567cdd67369643e64020000&organizationNumEmployeesRanges[]=11%2C20&organizationNumEmployeesRanges[]=21%2C50&organizationIndustryTagIds%5B%5D=5567ced173696450cb580000&qOrganizationKeywordTags%5B%5D=Google&includedOrganizationKeywordFields%5B%5D=name&qAndedOrganizationKeywordTags[]=startup&includedAndedOrganizationKeywordFields[]=name&includedAndedOrganizationKeywordFields[]=tags &includedAndedOrganizationKeywordFields[]=social_media_description 
This URL describes a search that people that are: 
1. Email is verified. 
2. Hold the titles: project manager or director. 
3. Are locate in the United States. 
4. Industry: Financial Services. It should be replaced by it's corresponding industry ID in the url. 
5. Company has the number of employees 11-20 or 21-50. 
6. Have a industry related to retail. 
7. Have a company keyword "Google". 
8. Must include companies related to “startup” via keywords in their name, tags, or description.  
	- If a/multiple company name is explicitly mentioned (e.g., “Google”), include: &qOrganizationKeywordTags[]=COMPANY_NAME1 &qOrganizationKeywordTags[]=COMPANY_NAME2 &includedOrganizationKeywordFields[]=name 
	- If a/multiple company-related concept is mentioned (e.g., “startup”, “VC-backed”, “open-source”, “remote-first”), treat it as a required keyword. These describe company identity, structure, or positioning, not names. Use: &qAndedOrganizationKeywordTags[]=KEYWORD1 &qAndedOrganizationKeywordTags[]=KEYWORD2 &includedAndedOrganizationKeywordFields[]=tags &includedAndedOrganizationKeywordFields[]=social_media_description 

You can change those fields (and only those fields).
```

"""

### Industry ID Reference

The following JSON object is provided to the LLM for mapping industries to their corresponding Apollo IDs:

```json
[  
  { "id": "5567cd4773696439b10b0000", "name": "information technology & services" },  
  { "id": "5567cd4773696439dd350000", "name": "construction" },  
  { "id": "5567cd467369644d39040000", "name": "marketing & advertising" },  
  { "id": "5567cddb7369644d250c0000", "name": "health, wellness & fitness" },  
  { "id": "5567e0eb73696410e4bd1200", "name": "pharmaceuticals" },  
  { "id": "5567d08e7369645dbc4b0000", "name": "biotechnology" },  
  { "id": "5567cd477369645401010000", "name": "real estate" },  
  { "id": "5567cdd47369643dbf260000", "name": "management consulting" },  
  { "id": "5567cd4e7369643b70010000", "name": "computer software" },  
  { "id": "5567cd4d736964397e020000", "name": "internet" },  
  { "id": "5567e0d87369640e5aa30c00", "name": "semiconductors" },  
  { "id": "5567ced173696450cb580000", "name": "retail" },  
  { "id": "5567cdd67369643e64020000", "name": "financial services" },  
  { "id": "5567d1127261697f2b1d0000", "name": "consumer services" },  
  { "id": "5567cdde73696439812c0000", "name": "hospital & health care" },  
  { "id": "5567cdf27369644cfd800000", "name": "automotive" },  
  { "id": "5567e0e0736964198de70700", "name": "restaurants" },  
  { "id": "5567ce9e736964540d540000", "name": "education management" },  
  { "id": "5567ce1e7369643b806a0000", "name": "food & beverages" },  
  { "id": "5567cdbc73696439d90b0000", "name": "design" },  
  { "id": "5567cd82736964540d0b0000", "name": "apparel & fashion" },  
  { "id": "5567ce9d7369645430c50000", "name": "import & export" },  
  { "id": "5567ce9d7369643bc19c0000", "name": "hospitality" },  
  { "id": "5567ce1f7369643b78570000", "name": "accounting" },  
  { "id": "5567cd8e7369645409450000", "name": "events services" },  
  { "id": "5567cda97369644cfd3e0000", "name": "luxury goods & jewelry" },  
  { "id": "5567e1ae73696423dc040000", "name": "cosmetics" }, 
  { "id": "5567cd4973696439b9010000", "name": "logistics & supply chain" },  
  { "id": "5567e127736964181e700200", "name": "warehousing" },  
  { "id": "5567e8bb7369641a658f0000", "name": "package/freight delivery" } 
]
```



### Expected Output Format

The LLM is instructed to return the generated URL in a JSON object without quotations:

```json
{"searchUrl":"Search URL goes here"}
```



## 3. Retrieve Prospects with Apify Crawler

The URL generated by the LLM is then passed to an Apify crawler to retrieve the prospect data.

### Apify API Client Code

The following Python script demonstrates how to use the Apify API client to run the crawler. The Apify API token is stored in a .env.local file in the root folder.

```python
from apify_client import ApifyClient 
# Initialize the Apify
Client with your API token client = ApifyClient("<YOUR_API_TOKEN>") 
# Prepare the Actor 
input run_input = {    "url":"https://app.apollo.io/#/peoplefinderViewId=5b8050d050a3893c382e9360&personLocations[]=Germany&page=1&sortByField=recommendations_score&organizationNumEmployeesRanges[]=5000%2C5200&organizationIndustryTagIds[]=5567e0bf7369641d115f0200&organizationIndustryTagIds[]=5567e3f3736964395d7a0000",    
 "totalRecords": 50,    
 "fileName": "Apollo Prospects", 
} 
# Run the Actor and wait for it to finish 
run = client.actor("jljBwyyQakqrL1wae").call(run_input=run_input) 
# Fetch and print Actor results from the run's dataset (if there are any) 
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
	print(item)
```



### Apify API Endpoint Reference

Here are some of the relevant API endpoints for the Apify Actor:

- **Run Actor**
  - **Description**: Runs the Actor asynchronously.
  - **Method**: POST
  - **URL**: https://api.apify.com/v2/acts/code_crafter~apollo-io-scraper/runs?token=***
- **Run Actor Synchronously**
  - **Description**: Runs the Actor and waits for it to finish.
  - **Method**: POST
  - **URL**: https://api.apify.com/v2/acts/code_crafter~apollo-io-scraper/run-sync?token=***
- **Run Actor Synchronously and Get Dataset Items**
  - **Description**: Runs the Actor, waits for it to finish, and returns the dataset items in the response.
  - **Method**: POST
  - **URL**: https://api.apify.com/v2/acts/code_crafter~apollo-io-scraper/run-sync-get-dataset-items?token=***
- **Get Actor**
  - **Description**: Returns the settings of the Actor.
  - **Method**: GET
  - **URL**: https://api.apify.com/v2/acts/code_crafter~apollo-io-scraper?token=***
- **Get List of Actor Versions**
  - **Description**: Returns a list of all versions of the Actor.
  - **Method**: GET
  - **URL**: https://api.apify.com/v2/acts/code_crafter~apollo-io-scraper/versions?token=***
- **Get Last Run**
  - **Description**: Returns the last run of the Actor. Add status=SUCCEEDED to get the last successful run.
  - **Method**: GET
  - **URL**: https://api.apify.com/v2/acts/code_crafter~apollo-io-scraper/runs/last?token=***
- **Get Last Run Dataset Items**
  - **Description**: Returns data from the default dataset of the last run.
  - **Method**: GET
  - **URL**: https://api.apify.com/v2/acts/code_crafter~apollo-io-scraper/runs/last/dataset/items?token=***

## 4. Display Results on Frontend

Finally, the results retrieved from the Apify crawler are sent to the front-end to be displayed to the user.