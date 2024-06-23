from flask import Flask, jsonify
import os

app = Flask(__name__)
data_storage = []

def read_data_from_files():
    global data_storage
    directory = "mock/mock_files/request"

    conteudo_pasta = os.listdir(directory)
    
    # Itera sobre os itens na pasta
    for item in conteudo_pasta:
        print(item)

    for filename in sorted(os.listdir(directory)):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                data_dict = {
                    "timestamp": parts[0],
                    "type": parts[1],
                    "content": parts[2],
                    "extra_1": parts[3],
                    "extra_2": parts[4],
                }
                data_storage.append(data_dict)
        os.remove(filepath)  # Remove file after reading

@app.route('/data', methods=['GET'])
def get_data():
    read_data_from_files()
    return jsonify(data_storage)

if __name__ == '__main__':
    app.run(port=5000)
