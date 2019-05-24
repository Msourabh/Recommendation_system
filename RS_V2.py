import pandas as pd
import numpy as np
import sys
from itertools import combinations, groupby
from collections import Counter
from IPython.display import display

data = pd.read_csv('market_bucket_analysis/instacart-market-basket-analysis/order_products__prior.csv',chunksize = 100000)
#reader = pd.read_csv('user_logs.csv', chunksize = size, index_col = ['msno'])
for i in range(325):
    data_chunk = next(data)
    if i==0:
        orders = data_chunk.set_index('order_id')['product_id'].rename('item_id')
        print('first_shape: (%s,)'%orders.shape)
    else:
        orders1 = data_chunk.set_index('order_id')['product_id'].rename('item_id')
        print('remaining_shape: (%s,)'%orders1.shape)
        orders = orders.append(orders1)
        del(data_chunk) 
display(orders.head(10))
type(orders)

# Returns generator that yields item pairs, one at a time
def get_item_pairs(order_item):
    order_item = order_item.reset_index().as_matrix()
    for order_id, order_object in groupby(order_item, lambda x: x[0]):
        item_list = [item[1] for item in order_object]
              
        for item_pair in combinations(item_list, 2):
            yield item_pair
            
def freq(iterable):
    if type(iterable) == pd.core.series.Series:
        return iterable.value_counts().rename("freq")
    else: 
        return pd.Series(Counter(iterable)).rename("freq")