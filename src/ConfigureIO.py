import json
import io

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

def writeSettingFile(data):
    with io.open('Config.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))

def readSettingFile():
    with open('Config.json') as data_file:
        data_loaded = json.load(data_file)
    return data_loaded

if __name__ == "__main__":
    # Sample
    cfgData = {'General': {'Recent': '3'},
            'Account': {'Username': '',
                        'Password': ''},
            'Organizer': {'Organize': 'True',
                          'Copy': '/.../',
                          'Sort': 'True',
                          'Rename': 'True'},
            'Watched': ['/Test1/', '/Test2/', '/Test3'],
            'Proxy': {'Type': '',
                      'Server': '',
                      'Port': '',
                      'Username': '',
                      'Password': ''}
            }
    writeSettingFile(cfgData)
    rec = readSettingFile()
    print(rec)
