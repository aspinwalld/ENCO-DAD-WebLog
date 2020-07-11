# WebLOG HTML Log Generator
# By D.I. Aspinwall

inputfile = 'plist.txt'
outputfile = 'log\index.html'
callLetters = 'WUPM'
jockName = 'JEN AUSTIN'
delimeter = ',%,'

def GetPlaylist():
    global callLetters
    for line in lines:
        line = line.strip().split(delimeter)
        playlist = line[0]
        try:
            if playlist[4] == callLetters[0] and playlist[5] == callLetters[1] and playlist[6] == callLetters[2] and playlist[7] == callLetters[3]:
                output.write(f'<br><h3 style="text-align:center"><strong>Playlist: {playlist}</strong>')
        except:
            print('Error in GetPlaylist()')
            pass
        
def GetHour():
    global jockName
    for line in lines:
        line = line.strip().split(delimeter)
        airtime = line[0]
        try:
            at0 = airtime[0]
            at1 = airtime[1]
        except:
            at0 = 'null'
            at1 = 'null'
        title = line[1]
        artist = line[2]
        vtdj = artist.strip()
        intro = line[3]
        length = line[4]
        if at0 == t0 and at1 == t1 and vtdj == jockName:
            output.write(f'<tr> <th style="color:#00af00">{airtime}</th> <th style="color:#00af00">{title}</th> <th style="color:#00af00">{artist}</th> <th style="color:#00af00">{intro}</th> <th style="color:#00af00">{length}</th> </tr>')
        elif at0 == t0 and at1 == t1 and vtdj != jockName:
            output.write(f'<tr> <th>{airtime}</th> <th>{title}</th> <th>{artist}</th> <th>{intro}</th> <th>{length}</th> </tr>')
            
#Read Log File from ENCO DAD
infile = open(inputfile, 'r')
lines = infile.readlines()
infile.close()

#Render HTML Document
output = open(outputfile, 'w')

output.write(f'<!DOCTYPE HTML><html><head> <title>{callLetters} WebLOG</title> <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"> <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script> <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script> </head><body> <div class="row"> <div class="col-md-2"></div><div class="col-md-8"> <div class="well"> <h2 style="text-align:center">{callLetters} Playlist Log</h2><h4 style="text-align:center">{jockName}</h4>')

GetPlaylist()

output.write(f'</div> <table class="table table-striped"> <thead> <tr> <th>Airtime</th> <th>Title</th> <th>Artist</th> <th>Intro</th> <th>Length</th> </tr></thead> <tbody>')

t0 = '1'
t1 = '0'
GetHour()

t1 = '1'
GetHour()

t1 = '2'
GetHour()

t1 = '3'
GetHour()

output.write(' </tbody> </table> <div class="footer"> <h6 style="text-align:center">Created using WebLOG HTML Log Generator by D.I. Aspinwall</h6> </div></div><div class="col-md-2"></div><div> </body></html>')
output.close()