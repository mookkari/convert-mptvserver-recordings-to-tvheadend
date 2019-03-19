import xml.etree.ElementTree as ET
import datetime, time
import json
import os
import hashlib


owner = "admin" #one of the usernames in tvheadend
baseServerDir = "/srv/ZFSDisk/Opnames/" #where your MP recordings are
baseTVHlogDir = "/home/hts/.hts/tvheadend/dvr/log"
configHash = "3d6a906a6b6ad5ca25867270db2f192e" #one of the hashes found in tvheadend/dvr/config
channelHash = "3af7cb4eae5dfa8c2f0e03d0c641ef49" #pick one, it doesn't matter which one, but it should (probably) exist


def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            _, file_extension = os.path.splitext(filename)
            if file_extension == '.xml':
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# get the all xml recording files
xmlFiles = get_filepaths(baseServerDir)



print('Found ' + str(len(xmlFiles)) + ' recording files...')

for recXmlFile in xmlFiles:
    print('Read:\t' + recXmlFile)

    recFile = recXmlFile.replace('xml', 'ts').replace('\\', '/')

    #read data from MediaPortal xml
    tree = ET.parse(recXmlFile)
    root = tree.getroot()
    #print(root.findAll('SimpleTag'))
    tags = tree.findall(".//SimpleTag")

    data = {}
    for i in tags: 
        name = i.find('name').text
        value = i.find('value').text

        if name == 'STARTTIME' or name == 'ENDTIME':
            value = int(time.mktime(datetime.datetime.strptime(value, '%Y-%m-%d %H:%M').timetuple()))
        elif name == 'COMMENT':
            value = value.split('. ')
            subtitle = value[0]
            del value[0]
            description = '. '.join(value)
            data['SUBTITLE'] = subtitle
            data['DESCRIPTION'] = description
        else:
            value = value.replace('\n      ', '')
        data[name] = value

    #make json for tvheadend
    jd = {}

    jd["enabled"] = True
    jd["start"] = data.get('STARTTIME', int(os.stat(recXmlFile)[-2]))
    jd["start_extra"] = 0
    jd["stop"] = data.get('ENDTIME', int(os.stat(recXmlFile)[-2])+300)
    jd["stop_extra"] = 0
    jd["channel"] = channelHash
    jd["channelname"] = data.get('CHANNEL_NAME', 'N/A')
    jd["title"] = {}
    jd["title"]["dut"] = data.get('TITLE')
    jd["subtitle"] = {}
    jd["subtitle"]["dut"] = data.get('SUBTITLE')
    jd["description"] = {}
    jd["description"]["dut"] = data.get('DESCRIPTION')
    jd["pri"] = 2
    jd["retention"] = 0
    jd["removal"] = 0
    jd["playposition"] = 0
    jd["playcount"] = 2
    jd["config_name"] = configHash
    jd["owner"] = owner
    jd["creator"] = owner
    jd["errorcode"] = 0
    jd["errors"] = 0
    jd["data_errors"] = 0
    jd["dvb_eid"] = 0
    jd["noresched"] = True
    jd["norerecord"] = False
    jd["fileremoved"] = 0
    jd["autorec"] = ""
    jd["timerec"] = ""
    jd["parent"] = ""
    jd["child"] = ""
    jd["content_type"] = 1
    jd["broadcast"] = 0
    jd["comment"] = "Imported from MediaPortal"
    jd["files"] = [{}]
    jd["files"][0]["filename"] = recFile
    jd["files"][0]["start"] = data.get('STARTTIME', int(os.stat(recXmlFile)[-2]))-300
    jd["files"][0]["stop"] = data.get('ENDTIME', int(os.stat(recXmlFile)[-2]))+300

    jsonString = json.dumps(jd, sort_keys=True, indent="\t").encode('utf-8');

    #calculate filename hash
    md5name = hashlib.md5(jsonString).hexdigest()

    #write to file
    writePath = baseTVHlogDir + '/MPimport/'
    print('Write:\t' + writePath+md5name)
    if not os.path.exists(writePath):
        os.mkdir(writePath)

    with open(writePath + md5name, 'w') as outfile:
        json.dump(jd, outfile)
