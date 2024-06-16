from elasticsearch import Elasticsearch
import pages.util.user as user
# Connect to Elasticsearch

def get_laptops(prompt):
    es = Elasticsearch(['http://localhost:9200'])
    result=""
    # Query for the best match for multiple criteria and sort by price
    query = user.ask_prompt(prompt)
    print(query)


    # Search the index
    response = es.search(index='computers-999', body=query)

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