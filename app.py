import json
import os
import random
import string

import pandas
from flask import Flask, Response, request, jsonify

from analysis import Analysis
from preprocess import Preprocess

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/handle/")
def cleaning_handler():
    try:
        file_name = request.args.get('filename')
        username = request.args.get('username')
        workspace = request.args.get('workspace')
    except:
        return Response({'message': "input error"}, status=400)

    current_path = os.getcwd()
    save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    dataframe = pandas.read_csv(save_path)
    preprocess = Preprocess(dataframe=dataframe)

    if request.args.get('missing') == '1':
        if request.args.get('columns_missing') != '':
            col = request.args.get('columns_missing').split(",")
            preprocess.data_null_handler(col)
        else:
            preprocess.data_null_handler()

    if request.args.get('duplication') == '1':
        if request.args.get('columns_duplication') != '':
            col = request.args.get('columns_duplication').split(",")
            preprocess.data_duplication_handler(col)
        else:
            preprocess.data_duplication_handler()

    # handle ordinal encoding
    if request.args.get('ordinal_encoding') == '1':
        if request.args.get('columns_ordinal_encoding') != '':
            col = request.args.get('columns_ordinal_encoding').split(",")
            col_ranks = request.args.get('ranks_ordinal_encoding').split(";")
            
            list_ranks = []
            for ranks in col_ranks :
                ranks.split(",")
                multi_ranks = {}
                i = 0
                for key in ranks :
                    multi_ranks[key] = i
                    i+=1
                list_ranks.append(multi_ranks)
                
            result_dict = dict(zip(col, multi_ranks))
            preprocess.data_ordinal_encoding(result_dict)
        else:
            preprocess.data_ordinal_encoding()
    
    # handle encoding
    if request.args.get('encoding') == '1':
        if request.args.get('columns_encoding') != '':
            col = request.args.get('columns_encoding').split(",")
            preprocess.data_encoding(col)
        else:
            preprocess.data_encoding()

    # if request.args.get('outlier') == '1':
    #     preprocess.data_outlier_handler()

    # generate new file name
    new_file_name = generate_file_name(file_name)

    # save cleaned dataset to csv
    save_path = f'{current_path}/directory/{username}/{workspace}/{new_file_name}'
    if os.path.isfile(save_path):
        return Response({'errcode': "input error", 'message': "file name must unique"},
                        status=400)
    preprocess.dataframe.to_csv(save_path)

    # create new file model with serializer
    file_size = round(os.path.getsize(save_path) / (1024 * 1024), 2)

    # check and collect columns type
    columns_type = preprocess.get_all_column_type()
    numeric_type = []
    non_numeric_type = []
    for k, v in columns_type.items():
        if v in ['Numerical']:
            numeric_type.append(k)
        else:
            non_numeric_type.append(k)
    numeric = ''
    non_numeric = ''
    if len(numeric_type) != 0:
        numeric = ','.join(numeric_type)
    if len(non_numeric_type) != 0:
        non_numeric_type = ','.join(non_numeric_type)

    '''
    The following lines are commented out because it requires interaction with the database.
    This service strictly preprocess and returns the result. Any interaction with the database 
    should be handled by the main controller.
    '''

    # payload = {
    #     'file': new_file_name,
    #     'size': file_size,
    #     'username': username,
    #     'workspace': workspace,
    #     'numeric': numeric,
    #     'non_numeric': non_numeric,
    # }

    # file_serializer = FileSerializer(data=payload)
    # if not file_serializer.is_valid():
    #     os.remove(save_path)
    #     return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # save file model to database
    # file_serializer.save()

    return jsonify(preprocess.dataframe.head(10).to_json()), 200


##masih gayakin sama scaler
@app.route("/standardscaler/")
def standard_scaler():
    try:
        file_name = request.args.get('filename')
        username = request.args.get('username')
        workspace = request.args.get('workspace')
    except:
        return Response({'message': "input error"}, status=400)

    current_path = os.getcwd()
    save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    dataframe = pandas.read_csv(save_path)
    preprocess = Preprocess(dataframe=dataframe)
    result = preprocess.data_standardization()
    return jsonify(result), 200

@app.route("/minmaxscaler/")
def minmax_scaler():
    try:
        file_name = request.args.get('filename')
        username = request.args.get('username')
        workspace = request.args.get('workspace')
    except:
        return Response({'message': "input error"}, status=400)

    current_path = os.getcwd()
    save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    dataframe = pandas.read_csv(save_path)
    preprocess = Preprocess(dataframe=dataframe)
    result = preprocess.data_normalization()
    return jsonify(result), 200

@app.route("/null/")
def null_check():
    try:
        file_name = request.args.get('filename')
        username = request.args.get('username')
        workspace = request.args.get('workspace')
    except:
        return Response({'message': "input error"}, status=400)

    current_path = os.getcwd()
    save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    dataframe = pandas.read_csv(save_path)
    preprocess = Preprocess(dataframe=dataframe)
    result = preprocess.data_null_check()
    return jsonify(result), 200


@app.route("/duplication/")
def duplication_check():
    try:
        file_name = request.args.get('filename')
        username = request.args.get('username')
        workspace = request.args.get('workspace')
    except:
        return Response({'message': "input error"}, status=400)

    current_path = os.getcwd()
    save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    dataframe = pandas.read_csv(save_path)
    preprocess = Preprocess(dataframe=dataframe)
    result = preprocess.data_duplication_check()
    return jsonify(result), 200

@app.route("/encode/")
def encoding_check():
    try:
        file_name = request.args.get('filename')
        username = request.args.get('username')
        workspace = request.args.get('workspace')
    except:
        return Response({'message': "input error"}, status=400)

    current_path = os.getcwd()
    save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    dataframe = pandas.read_csv(save_path)
    preprocess = Preprocess(dataframe=dataframe)
    result = preprocess.data_encode_check()
    return jsonify(result), 200

# @app.route("/outlier/")
# def outlier_check():
#     try:
#         file_name = request.args.get('filename')
#         username = request.args.get('username')
#         workspace = request.args.get('workspace')
#     except:
#         return Response({'message': "input error"}, status=400)

#     current_path = os.getcwd()
#     save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
#     dataframe = pandas.read_csv(save_path)
#     preprocess = Preprocess(dataframe=dataframe)
#     result = preprocess.data_outlier_check()
#     return jsonify(result), 200


# @app.route("/boxplot/")
# def get_boxplot():
#     try:
#         file_name = request.args.get('filename')
#         username = request.args.get('username')
#         workspace = request.args.get('workspace')
#     except:
#         return Response({'message': "input error"}, status=400)

#     current_path = os.getcwd()
#     save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
#     dataframe = pandas.read_csv(save_path)
#     analysis = Analysis(dataframe=dataframe)
#     result = json.loads(analysis.get_box_plot_data())
#     return jsonify(result), 200




def generate_file_name(file_name):
    _file, ext = os.path.splitext(file_name)
    new_file_name = _file + "_" + random_string() + ext
    return new_file_name


def random_string(length=4):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
