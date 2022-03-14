from flask import Flask,render_template,request
import model

app = Flask('__name__')

@app.route('/')
def home():
    return render_template('Templates/index.html')

@app.route('/recommend',methods=['POST'])
def recommend_top5():
    user_name = request.form['User Name']
    
    top20_products = model.recommend_product(user_name)
    top5_products = model.Top_Products(top20_products)
    
    return render_template('Template/index.html',column_names=top5_products.columns.values, row_data=list(top5_products.values.tolist()), zip=zip,text='Recommended products')
    

if __name__ == '__main__':
    app.debug=False

    app.run()
