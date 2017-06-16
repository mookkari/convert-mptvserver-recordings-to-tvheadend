# convert-mptvserver-recordings-to-tvheadend
Converts recordings made by MediaPortal Tv Server (MPTVServer) to the TVHeadend v4 recording format

Works in Pyton 3.4, probably also other versions.

## Configuration
You must alter the python file to your configuration:

* **owner** = one of the usernames in tvheadend
* **baseServerDir** = the path of the MPTV recording files with xmls. It also looks in subdirs
* **baseTVHlogDir** = the path to the dvr log dir of TVH
* **configHash** = one of the hashes found in tvheadend/dvr/config
* **channelHash** = one of the hashes found in tvheadend/dvr/channel/config, it doesn't matter which one, but it should (probably) exist


## Running
Execute `python convertRecordings.py`

The files will be saved in the "MPimport" dir in the "baseTVHlogDir". You must copy them manually to the "baseTVHlogDir". If anything goes wrong, you know which files to remove from the "baseTVHlogDir".
After that, restart tvheadend and if all went well, your recordings will show up.
