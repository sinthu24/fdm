from os import error
from flask import Flask , render_template,request
from flask.sessions import NullSession
import numpy as np
import pandas as pd
from apyori import apriori
import pickle

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


def find(cons):
    store_data = pd.read_csv('GroceryProducts.csv', header=None) 
    df_shape = store_data.shape
    n_of_transactions = df_shape[0]
    n_of_products = df_shape[1]
# Converting our dataframe into a list of lists for Apriori algorithm
    records = []
    for i in range(0, n_of_transactions):
        records.append([])
        for j in range(0, n_of_products):
            if (str(store_data.values[i,j]) != 'nan'):
                records[i].append(str(store_data.values[i,j]))
            else :
                continue
    association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=2, max_length=5)
    association_results = list(association_rules)
    for item in association_results:
        pair = item[0] 
        items = [x for x in pair]
        to_print = "Rule: "
        arrow = " -> "
        for i in range(len(items)):
            to_print += str(items[i]) + arrow
            
    merged = store_data[0]
    for i in range(1,n_of_products):

        merged = merged.append(store_data[i])
    ranking = merged.value_counts(ascending=False)

    ranked_products = list(ranking.index)
    
    Lookup_table = {}
    
    for item in association_results:
        pair = item[0] 

        items = [x for x in pair]

        to_print = "Rule: "

        arrow = " -> "

        for i in range(len(items)):

            to_print += str(items[i]) + arrow  
            if len(items) < 4:

                items_to_append = items

                i = 0

                while len(items) < 4:

                    if ranked_products[i] not in items:

                        items_to_append.append(ranked_products[i])

                    i += 1
            Lookup_table[items_to_append[0]] = items_to_append[1:]
          

    

            
    Lookup_table['default_recommendation'] = ranked_products[:3]
    
    return Lookup_table[cons]
    
    

@app.route('/send',methods=['GET','POST'])
def consequents():
    cons=[]
    if request.method=='POST':
        ant=request.form['product'] 
        if ant=='':
            cons=''
        else:
            cons=find(ant)
    return render_template('index.html',cons=cons)

if __name__ == '__main__':
   app.run(debug=True)


