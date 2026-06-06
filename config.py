# =============================================================
# IBM Watsonx.ai Configuration
# =============================================================
# INSTRUCTIONS:
#   1. Log in to IBM Cloud: https://cloud.ibm.com
#   2. Create or open a Watsonx.ai project
#   3. Copy your Project ID from the project settings
#   4. Generate an API Key from IBM Cloud IAM
#   5. Note the Watsonx endpoint for your region
#   Then paste the values below.
# =============================================================

# Your IBM Watsonx.ai Project ID
# Found at: Watsonx.ai > Your Project > Manage > General > Project ID
PROJECT_ID = "842db10c-beb5-4869-80f6-4ff4797e7989"

# Your IBM Cloud API Key
# Found at: IBM Cloud > Manage > Access (IAM) > API Keys > Create
API_KEY = "Ew8R5yb89Flnh8-2ET3wDwSV4L4Dh4OjlblKdw-ZMUcY"

# Watsonx.ai Endpoint URL (choose based on your IBM Cloud region)
# US South  : https://us-south.ml.cloud.ibm.com
# EU (DE)   : https://eu-de.ml.cloud.ibm.com
# EU (GB)   : https://eu-gb.ml.cloud.ibm.com
# Tokyo     : https://jp-tok.ml.cloud.ibm.com
ENDPOINT_URL = "https://au-syd.ml.cloud.ibm.com"

# IBM Granite model to use via Watsonx.ai
# Granite 13B Instruct v2 is recommended for instruction-following tasks
MODEL_ID = "meta-llama/llama-3-3-70b-instruct"
print("CONFIG LOADED")
print("PROJECT_ID =", PROJECT_ID[:10] if PROJECT_ID else "EMPTY")
print("API_KEY LENGTH =", len(API_KEY))
print("ENDPOINT_URL =", ENDPOINT_URL)