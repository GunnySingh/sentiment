import numpy as np
import pandas as pd
import re
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

tf_idf=pickle.load(open('TFidf.pkl','rb'))
model_lr=pickle.load(open('lr_Tuned.pkl','rb'))
recommend_system = pickle.load(open('User_Recommendation_System.pkl','rb'))


df = pd.read_csv('Data/sample30.csv')



def preprocess(doc):
    
    # Converting text into lowercase
    doc=doc.lower()
    
    # Removing Punctuations and special characters
    doc=re.sub('[^A-Za-z0-9\s]'," ",doc)
    
    # Removing Stop Words
    words=word_tokenize(doc)
    words=[word for word in words if word not in stopwords.words('english')]
    
    # Lemmatizing words 
    wordnet_lemmatizer = WordNetLemmatizer()
    words = [wordnet_lemmatizer.lemmatize(word, pos='v') for word in words]
    
    doc=" ".join(words)
    return doc


# Predicting sentiment 
def model_predict(doc):
    tf_idf_vector = tf_idf.transform(doc)
    output = model_lr.predict(tf_idf_vector)
    return output

# Recommending top 20 products
def recommend_product(user_name):
    product_list = pd.DataFrame(recommend_system.loc[user_name].sort_values(ascending=False)[0:20])
    output = df[df.name.isin(product_list.index.tolist())][['name','reviews_text']]
    output['lemma'] = output['reviews_text'].map(lambda x : preprocess(x))
    output['prediction'] = model_predict(output['lemma'])
    return output


# Recommending top 5 products using sentiment analysis
def Top_Products(x):
    total_product=x.groupby(['name']).agg('count')
    df2 = x.groupby(['name','prediction']).agg('count')
    df2=df2.reset_index()
    merge_df = pd.merge(df2,total_product['reviews_text'],on='name')
    merge_df['percentage'] = (merge_df['reviews_text_x']/merge_df['reviews_text_y'])*100
    merge_df=merge_df.sort_values(ascending=False,by='percentage')
    output_products = pd.DataFrame(merge_df['name'][merge_df['prediction'] ==  1][:5])
    return output_products

