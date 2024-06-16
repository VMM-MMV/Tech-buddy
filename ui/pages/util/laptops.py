from elasticsearch import Elasticsearch
import pages.util.user as user
# Connect to Elasticsearch

def get_laptops(prompt,mode):
    es = Elasticsearch(['https://1637-81-180-73-68.ngrok-free.app'])
    result=""
    # Query for the best match for multiple criteria and sort by price
    query = user.ask_prompt(prompt)
    print(query)

    index="computers" if mode == "light" else "computers-999"
    print(index)
    # Search the index
    response = es.search(index=index, body=query)

    # Print search results
    print("Search Results:")
    for hit in response['hits']['hits'][:5]:
        result+=f"\nName: {hit['_source']['name']}, Price: {hit['_source']['price']}"
        print(result)
        # Access additional specifications if needed
        additional_specs = hit['_source'].get('additional_specs', {})
        if additional_specs:
            result+="\nAdditional Specifications:"
            for key, value in additional_specs.items():
                result+=f"\n{key}: {value}"
        # Access store name
        store_name = hit['_source'].get('store_name', '')
        if store_name:
            result+=f"\nStore: {store_name}\n"
        print(result)
        print()
    return result