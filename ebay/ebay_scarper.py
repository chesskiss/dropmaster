
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import pandas as pd


def search_ebay(results):
    total_pages = int(results.get('paginationOutput').get('totalPages'))
    items_list = results['searchResult']['item']

    i = 2
    while (i <= total_pages):
        payload['paginationInput'] = {'entriesPerPage': 100, 'pageNumber': i}
        results = get_results(payload)
        items_list.extend(results['searchResult']['item'])
        i += 1

    df_items = pd.DataFrame(columns=['itemId', 'title', 'viewItemURL', 'galleryURL', 'location', 'postalCode',
                                     'paymentMethod''listingType', 'bestOfferEnabled', 'buyItNowAvailable',
                                     'currentPrice', 'bidCount', 'sellingState'])

    for item in items_list:
        row = {
            'itemId': item.get('itemId'),
            'title': item.get('title'),
            'viewItemURL': item.get('viewItemURL'),
            'galleryURL': item.get('galleryURL'),
            'location': item.get('location'),
            'postalCode': item.get('postalCode'),
            'paymentMethod': item.get('paymentMethod'),
            'listingType': item.get('listingInfo').get('listingType'),
            'bestOfferEnabled': item.get('listingInfo').get('bestOfferEnabled'),
            'buyItNowAvailable': item.get('listingInfo').get('buyItNowAvailable'),
            'currentPrice': item.get('sellingStatus').get('currentPrice').get('value'),
            'bidCount': item.get('bidCount'),
            'sellingState': item.get('sellingState'),
        }

        df_items = df_items.append(row, ignore_index=True)

    return df_items

try:
    # development key
    api = Finding(domain='svcs.sandbox.ebay.com', appid="AlbertNa-testdrop-SBX-c08db439e-9981daeb", config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'football'})
    results = response.dict()
    df_items = search_ebay(results)
    df_items.head()
    #print(response.dict())
    items = results['searchResult']['item']
    for item in items:
        for key, val in item.items():
            print(f'{key}: {val}')
except ConnectionError as e:
    print(e)
    # print(e.response.dict())