
from flask import Flask,render_template,request
import model_final


app = Flask('__name__')



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend_top5():
    user_name = request.form['User Name']
    
    top_products = model_final.recommend_products(user_name)
    
    return render_template('index.html', row_data=top_products,text='Recommended products')
    # return render_template('index.html',text = top_products)

    
if __name__ == '__main__':
    app.debug=False

    app.run()
