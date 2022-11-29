import yaml, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__)))

CONFIG = 'config.yaml'


def DbConnect(segment=None, topics='database'):
    with open(CONFIG) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if topics in data:
            if segment in data[topics]:
                return data[topics][segment]
            else:
                return "Connection String is not available"
        else:
            return "Connection String is not available"
