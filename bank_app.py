import requests, csv, os
from flask import Flask, render_template, request, redirect

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(THIS_FOLDER, 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'sekretnyklucz'

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0]['rates']
code_l = [rates[i]['code'] for i,j in enumerate(rates)]
actual_date = data[0]['effectiveDate']

def export_data_to_csv():
    with open('bank_data_{}.csv'.format(actual_date), 'w', newline='') as csvfile:
        bank_data = csv.writer(csvfile, delimiter=';')
        bank_data.writerow(['currency','code','bid','ask'])
        for i,j in enumerate(rates):
            cur = rates[i]['currency']
            cod = rates[i]['code']
            bid = rates[i]['bid']
            ask = rates[i]['ask']
            bank_data.writerow([cur, cod, bid, ask])
        print("Succesfully saved")

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("bank_form.html", code_l=code_l)   
    elif request.method == 'POST':
        code = request.form.get("code")
        amount = float(request.form.get("amount"))
        for i,j in enumerate(rates):
            if code == rates[i]['code']:
                currency = rates[i]['currency']
                ask = float(rates[i]['ask'])
        result = amount * ask            
        return render_template('bank_result.html', code=code, amount=amount, currency=currency, ask=ask, result=result)

if __name__ == "__main__":
    export_data_to_csv()