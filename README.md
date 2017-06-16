# convert-mptvserver-recordings-to-tvheadend
Converts recordings made by MediaPortal Tv Server (MPTVServer) to the TVHeadend v4 recording format

Works in Pyton 3.4, probably also other versions.

You must alter the python file to your configuration. 
baseServerDir is the path of the MPTV recording files with xmls. It also looks in subdirs
baseTVHlogDir is the path to the dvr log dir of TVH

The files will be saved in MPimport dir in the baseTVHlogDir. You must copy them manually. If anything goes wrong, you know which files to remove.
After that, restart tvheadend and if all went well, your recordings will show up.
