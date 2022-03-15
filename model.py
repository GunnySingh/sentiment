import numpy as np
import pandas as pd
import pickle


tf_idf=pickle.load(open('Model/TFidf.pkl','rb'))
model_lr=pickle.load(open('Model/lr_Tuned.pkl','rb'))
recommend_system = pickle.load(open('Model/User_Recommendation_System.pkl','rb'))
df = pickle.load(open('Model/df.pkl','rb'))

def model_predict(doc):
    tf_idf_vector = tf_idf.transform(doc)
    output = model_lr.predict(tf_idf_vector)
    return output

def recommend_products(user_name):
    product_list = pd.DataFrame(recommend_system.loc[user_name].sort_values(ascending=False)[0:20])
    output = df[df.name.isin(product_list.index.tolist())][['name','reviews_text']]
    output['prediction'] = model_predict(output['reviews_text'])
    total_products = output.groupby(['name'])['prediction'].mean().sort_values(ascending=False).index[:5]
    return list(total_products)
    
