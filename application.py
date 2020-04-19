from flask import Flask, make_response, request, render_template
import sys
import os
from werkzeug import secure_filename

# import matplotlib.pyplot as plt
# from sklearn import preprocessing
import handwriting


application = Flask(__name__)
# print(os.path)
UPLOAD_FOLDER = 'static/images'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

print(application.config)


@application.route('/')
def form():
    return render_template("upload.html")



@application.route('/upload', methods=["POST"])
def upload():
    request_file = request.files['data_file']
    if not request_file:
        return "No file"
    
    request_file.save(os.path.join(application.config['UPLOAD_FOLDER'], secure_filename(request_file.filename)))  #important:-        UPLOAD_FOLDER is not any config in flask thats why pass the arguement in file.save(_path,filename)

    # request_file.save(secure_filename(request_file.filename))
    full_filename = os.path.join('/static/images', request_file.filename)
    testData = "."+full_filename
    # print(full_filename)
    # print(os.getcwd())
    predictions = handwriting.predict(testData)
    print(predictions)
    print(type(predictions))
    return render_template('show.html', imgUrl= full_filename, predictions = predictions,length = len(predictions))



@application.route('/predict', methods=["GET"])
def prediction():
    print(request.files)
    return render_template('predictions.html')




application.run(host= os.getenv('IP','0.0.0.0'), port= int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
    application.run()
