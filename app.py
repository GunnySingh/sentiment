
from flask import Flask,render_template,request
import model

app = Flask('__name__')



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend_top5():
    user_name = request.form['User Name']
    
    top_products = model.recommend_products(user_name)
    # return render_template('index.html',column_names=top5_products.columns.values, row_data=list(top5_products.values.tolist()), zip=zip,text='Recommended products')
    return render_template('index.html',text = top_products[0])

    
if __name__ == '__main__':
    app.debug=False

    app.run()
