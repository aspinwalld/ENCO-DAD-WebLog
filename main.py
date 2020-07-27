#List2Web HTML Playlist Generator for ENCO DAD

import ftplib
import socket
import time

ip = 'YOUR_IP_HERE'
port = 2002

ftp_host = 'YOUR_FTP_SERVER_HERE'
ftp_user = 'YOUR_FTP_USER_HERE'
ftp_password = 'YOUR_FTP_PASSWORD_HERE'

input_file = 'E:\DAD\Files\PLIST.REP'
output_file = 'index.html'

delimeter = ',%,'

def GetPlaylist(output, lines, *args, **kwargs):
    for line in lines:
        line = line.strip().split(delimeter)
        playlist = line[0]
        try:
            if playlist[4] == 'W' and playlist[5] == 'U' and playlist[6] == 'P' and playlist[7] == 'M':
                output.write(f'<br><h3 style="text-align:center"><strong>Playlist: {playlist}</strong>')
        except:
            print('Error in GetPlaylist()')
            pass
        
def GetHour(output, lines, t0, t1, *args, **kwargs):
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
        if at0 == t0 and at1 == t1 and vtdj == 'JEN AUSTIN':
            output.write(f'<tr> <th style="color:#00af00">{airtime}</th> <th style="color:#00af00">{title}</th> <th style="color:#00af00">{artist}</th> <th style="color:#00af00">{intro}</th> <th style="color:#00af00">{length}</th> </tr>')
        elif at0 == t0 and at1 == t1 and vtdj != 'JEN AUSTIN':
            output.write(f'<tr> <th>{airtime}</th> <th>{title}</th> <th>{artist}</th> <th>{intro}</th> <th>{length}</th> </tr>')


def generate_log():
    #Read Log File from ENCO DAD
    infile = open(input_file, 'r')
    lines = infile.readlines()
    infile.close()

    #Create HTML File
    output = open(output_file, 'w')

    output.write('<!DOCTYPE HTML><html><head> <title>MIX 106.9 | Jen Austin</title> <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"> <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script> <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script> </head><body> <div class="row"> <div class="col-md-2"></div><div class="col-md-8"> <div class="well"> <h2 style="text-align:center">MIX 106.9 Playlist Log</h2><h4 style="text-align:center">Jen Austin | 10:00 - 14:00</h4>')

    GetPlaylist(output, lines)

    output.write(f'</div> <table class="table table-striped"> <thead> <tr> <th>Airtime</th> <th>Title</th> <th>Artist</th> <th>Intro</th> <th>Length</th> </tr></thead> <tbody>')

    t0 = '1'
    t1 = '0'
    GetHour(output, lines, t0, t1)

    t1 = '1'
    GetHour(output, lines, t0, t1)


    t1 = '2'
    GetHour(output, lines, t0, t1)


    t1 = '3'
    GetHour(output, lines, t0, t1)

    output.write(' </tbody> </table> <div class="footer"> <h6 style="text-align:center">Created using List2Web for ENCO DAD by D.I. Aspinwall</h6> </div></div><div class="col-md-2"></div><div> </body></html>')
    output.close()

    print('HTML WebLog Generated.')
    upload_log()


def upload_log():
    print(f'Uploading HTML WebLog to {ftp_host}')
    ftp = ftplib.FTP(ftp_host, ftp_user, ftp_password)
    ftp.encoding = 'utf-8'
    with open(output_file, 'rb') as file:
        ftp.storbinary(f'STOR {output_file}', file)
    print('HTML WebLog Uploaded Successfully.')


while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ip, port))

        while True:
            print(f'Listening for DCLs on {ip}:{port}')
            data, address = s.recvfrom(4096)
            dcl = data.decode('utf-8')
            dcl = dcl.upper().strip()
            dcl = dcl[:-1] # Strip garbage character from end of DCL
            print(f'Received DCL: {dcl} from {address}')
            if not data:
                break
            
            if dcl == 'MAKELOG+HTML':
                print('GENERATING HTML WEBLOG...')
                generate_log()
            else:
                print(f'Sorry, don\'t know what to do with that... {dcl} is not a valid List2Web DCL.')
                break
    except:
        print('Something\'s fucked up. Killing myself and trying again...')
        time.sleep(10)
        print('Okay let\'s do this!')
        break