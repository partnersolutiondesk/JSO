from PythonPackage.AppInit import app
import json
#import PythonPackage.AppInit
#import PythonPackage.Models
from PythonPackage.api import UserLogin
config_file_path = "serverConfig.json"
def read_config(file_path):
    try:
        with open(file_path, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print(f"Config file '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

config = read_config(config_file_path)
print(config)
if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'],debug=True)
    #app.run(debug=True)