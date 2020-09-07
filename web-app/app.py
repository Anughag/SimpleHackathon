from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from forms import DefectPrediction
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
import pandas as pd 
import numpy as np
import os 
import nltk
import decimal
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from IPython.display import IFrame,display,HTML
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    formPredict=DefectPrediction()
    return render_template('index.html', form=form,formPredict=formPredict)

df = pd.read_excel("Final_5_9.xlsx")
Final=df.copy()
df = df['Defect Description']
df = pd.DataFrame({'Desc':df})

@app.route('/defectpredict', methods=('GET', 'POST'))
def defectpredict():
  formPredict=DefectPrediction()
  form = PredictForm()
  if formPredict.submit():
    print(formPredict.plannedCP.data)
    print(formPredict.teamExpertise.data)
    print(formPredict.efforts.data)
    

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDIwMDgyMzE4MzIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDJHTlFKIiwiaWQiOiJJQk1pZC01NTAwMDJHTlFKIiwicmVhbG1pZCI6IklCTWlkIiwiaWRlbnRpZmllciI6IjU1MDAwMkdOUUoiLCJnaXZlbl9uYW1lIjoiTXV0aHUiLCJmYW1pbHlfbmFtZSI6IlN1bmRhcmF2YWRpdmVsIiwibmFtZSI6Ik11dGh1IFN1bmRhcmF2YWRpdmVsIiwiZW1haWwiOiJtdXRodS5zdW5kYXJhdmFkaXZlbEBpbi5pYm0uY29tIiwic3ViIjoibXV0aHUuc3VuZGFyYXZhZGl2ZWxAaW4uaWJtLmNvbSIsImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6ImUzZmQ1Njg2Njc4NjQwYjZhYmUwYmYxMTEzMmMyZTQ4IiwiaW1zX3VzZXJfaWQiOiI4NDA4OTE4IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyMTExODc0In0sImlhdCI6MTU5OTQxMzQzMSwiZXhwIjoxNTk5NDE3MDMxLCJpc3MiOiJodHRwczovL2lhbS5ibHVlbWl4Lm5ldC9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.PV9-vkONx0bPJx9pMrBO1ojYjxpQKzJidqKng_17SXwSUDzylcYdbLUnlfKOsFhueWpELQP-l7qXkH0MlXC4QCiGicBRRj9xx-khQNkvOyYHfuX6X_dNgkLa_QGexLk28Z49wIFlnce2FzPkA67Dn9uyynBkZCsSf_agVRBeKhVqJKea4MS1Zfyu8BQMLLA3XJANIy58rJABw4bhOQ74cFISrQ8778INA2VGztQRWUM4FmaRofJCpYx_Cg4TP-KylBW_BFLSMnVZGnYcCEK1PI72vrOl9B7DkPwNX7aSc5dh4VfzMGSaQqrlTnpf6Ld0DJwkciQHH79-MeMpsAXVpA",
                  'ML-Instance-ID': "91acd4b0-3679-4e9e-9d59-d251f0645d1d"}

        
        
       
    BaseLinedEPCP = decimal.Decimal(1.5)
    TeamExpertise = formPredict.teamExpertise.data 
    Efforts = formPredict.efforts.data
    ActualEPCP = Efforts/formPredict.plannedCP.data
    

        
    global VarianceRiskFactor
    global ComplexityFactor
    VarianceRiskFactor = 0
    if ActualEPCP <= BaseLinedEPCP:
      VarianceRiskFactor = 0
    elif ActualEPCP - BaseLinedEPCP >0 and ActualEPCP - BaseLinedEPCP<=0.5:

      VarianceRiskFactor = 1.25
    elif ActualEPCP - BaseLinedEPCP >0.5 and ActualEPCP - BaseLinedEPCP<=1:
      VarianceRiskFactor = 3
    elif ActualEPCP - BaseLinedEPCP >1 and ActualEPCP - BaseLinedEPCP<=1:
      VarianceRiskFactor = 5
    ComplexityFactor = 0.7 * VarianceRiskFactor + 0.3 * TeamExpertise
    print(ComplexityFactor)
    formPredict.complexityFactor.data=ComplexityFactor
    python_object = [float(formPredict.efforts.data),float(formPredict.plannedCP.data), formPredict.teamExpertise.data,float(formPredict.complexityFactor.data)]
        #Transform python objects to  Json

    userInput = []
    userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        
    payload_scoring = {"input_data": [{"fields": ["efforts", "plannedCP", "teamExpertise","complexityFactor"], "values": userInput }]}

    response_scoring = requests.post('https://private.eu-gb.ml.cloud.ibm.com/ml/v4/deployments/e16087e9-ba37-4642-9e02-3254e38b77cf/predictions', json=payload_scoring, headers=header)

    output = json.loads(response_scoring.text)
    print(output)
        
    formPredict.result=output
    return render_template('index.html', form=form,formPredict=formPredict)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    formPredict=DefectPrediction()
    if form.submit():
      SearchStr=form.num1.data
      print(form.choices.data)
      TOD=form.choices.data
          
    k=0
          
    for a in df.index:

        X=df['Desc'][a]
        # tokenization 


        X_list = word_tokenize(X.lower())  
        Y_list = word_tokenize(SearchStr.lower()) 


      # Fetching all stop words
        sw = stopwords.words('english')  
        V1 =[];V2 =[] 


        # Stop word removal 
        X_set = {lemmatizer.lemmatize(w) for w in X_list if not w in sw}  
        Y_set = {lemmatizer.lemmatize(w) for w in Y_list if not w in sw} 


        UV = X_set.union(Y_set)  
        for w in UV:


            if w in X_set: V1.append(1) 


            else: V1.append(0) 
            if w in Y_set: V2.append(1) 
            else: V2.append(0) 
            c = 0
       
            

            
    # Calculating cosine similarity  
        for i in range(len(UV)): 


          c+= V1[i]*V2[i] 
         
        cosine = c / float((sum(V1)*sum(V2))**0.5) 
        
        
        Final.loc[Final['Defect Description']== X,'Similarity']=cosine
        df_Final=Final.copy()
        

          #sum=form.num1.data+form.num2.data
        df_Final=Final[(Final['Similarity']>0)].sort_values(by='Similarity',ascending=False)
        df_Final = df_Final.drop_duplicates(subset=['Defect Description'], keep='first')
        df_Final = df_Final[['Release Name','Defect ID','Defect Description','RCA']].head(3)
        #print(df_Final)
        #df_Final=pd.DataFrame.to_html(df_Final,columns={'Similarity','Defect_desc'},index=False,classes='data')
        #df_Final=pd.DataFrame.to_records(df_Final,index=False)
        form.pd=df_Final
        #display(HTML(form.abc))
        #print(form.abc)
        
      
        
    return render_template('index.html', form=form,formPredict=formPredict,tables=[df_Final.to_html(classes='data', header="true",index=False)])   


       
       







