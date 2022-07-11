from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
import requests

url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data?end_date=2022-07-08&start_date=2021-07-08#panel', headers = { 'User-Agent': 'Popular browser\'s user-agent', })
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped text-sm text-lg-normal'})
date_row = table.find_all('th', attrs={'class':'font-semibold text-center'})

date_row_length = len(date_row)

temp = [] #initiating a list 

for i in range(0, date_row_length):

    # scrapping process
    # get date
    date = table.find_all('th', attrs={'class':'font-semibold text-center'})[i].text
    # get volume
    # clean the ' ', '\n', ',', and '$' while at it 
    vol = table.find_all('td', attrs={'class':'text-center'})[(i*4)+1].text.replace("\n","").replace(",","").replace("$","").replace(" ","")
    temp.append((date,vol)) 
    
temp[:10] 

#change into dataframe
eth = pd.DataFrame(temp, columns = ('Date','Volume'))

#insert data wrangling here
eth = eth.astype({"Date": "datetime64", 
                  "Volume":"int64"})
eth = eth.set_index('Date')



#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{eth["Volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = eth.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)