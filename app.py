from flask import Flask,render_template, request,jsonify
import pickle


app=Flask("placement_prediction")
model=pickle.load(open('placement_model.pkl','rb'))
@app.route('/',methods=['GET'])
def ping():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])

def predict():
    if request.method=='POST':
        ssc_p=int(request.form['ssc_p'])
        hsc_p=int(request.form['hsc_p'])
        degree_p=int(request.form['degree_p'])
        etest_p=int(request.form['etest_p'])

        gender=request.form['gender']
        if(gender=='M'):
            gender=1
        else:
            gender=0

        ssc_b_Others=request.form['ssc_b_Others']
        if(ssc_b_Others=='Others'):
            ssc_b_Others=1
        else:
            ssc_b_Others=0

        hsc_b_Others = request.form['hsc_b_Others']
        if (hsc_b_Others == 'Others'):
            hsc_b_Others = 1
        else:
            hsc_b_Others = 0
        hsc_s_Commerce=0
        hsc_s_Science=request.form['hsc_s_Science']
        if (hsc_s_Science=='Science'):
            hsc_s_Science=1
            hsc_s_Commerce=0

        elif(hsc_s_Science=='Commerce'):
            hsc_s_Science=0
            hsc_s_Commerce=1

        else:
            hsc_s_Science=0
            hsc_s_Commerce=0

        degree_t_Others=0

        degree_t_Sci=request.form['degree_t_Sci&Tech']
        if(degree_t_Sci=='Sci&Tech'):
            degree_t_Sci=1
            degree_t_Others=0

        elif(degree_t_Sci=='Others'):
            degree_t_Sci=0
            degree_t_Others=1

        else:
            degree_t_Sci=0
            degree_t_Others=0

        workex=request.form['workex']
        if(workex=='Yes'):
            workex=1
        else:
            workex=0

        prediction=model.predict_proba([[gender,ssc_p,hsc_p,degree_p,etest_p,ssc_b_Others,hsc_b_Others,hsc_s_Commerce,hsc_s_Science,
                                   degree_t_Others,degree_t_Sci,workex]])

        output =prediction[:,1]*100

        return render_template('home.html',prediction_text="The chance of placement is {} %".format(round(output,2)))





if __name__=='__main__':
    app.run(debug=True)
