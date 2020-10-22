#List2Web HTML Playlist Generator for ENCO DAD

import ftplib
import socket
import time
import logging
from configparser import ConfigParser

log = logging.getLogger(__name__)
log_format = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)d] %(funcName)s [%(levelname)s] %(message)s')
console_logger = logging.StreamHandler()
console_logger.setFormatter(log_format)
log.addHandler(console_logger)
log.setLevel(logging.DEBUG)

ini = ConfigParser()

try:
    ini.read('config.ini')
except:
    log.critical('Error finding configuration file. Exiting...')
    exit()

# Read/Validate ip from config.ini
try:
    ip = ini['NETWORK']['IP']
    log.debug(f'IP address, {ip}, read from config.')
except:
    log.error('Error reading IP address from config. Attempting to use 127.0.0.1.')
    ip = '127.0.0.1'
try:
    socket.inet_aton(ip)
    log.debug(f'Successfully validated {ip}.')
except socket.error:
    log.error(f'The IP address in the config, {ip}, is not valid. Attempting to use 127.0.0.1.')
    ip = '127.0.0.1'

# Read / Validate port from config.ini
try:
    port = ini['NETWORK']['Port']
    log.debug(f'UDP port, {port}, read from config.')
except:
    log.error('Error reading port from config. Attempting to use ENCO DCL default 2002.')
    port = 2002
try:
    port = int(port)
    valid_port = port in range(1024, 49151)
    if valid_port:
        log.debug(f'Successfully validated {port}.')
    else:
        log.error(f'The port in the config, {port}, is outside of the allowed range. Attempting to use ENCO DCL default 2002.')
        port = 2002
except:
    log.error(f'The port in the config, {port}, is invalid. Attempting to use ENCO DCL default 2002.')
    port = 2002

# Read DCL command string from config.ini
try:
    dcl_command = ini['NETWORK']['DCLCommand']
    log.debug(f'DCL command string, {dcl_command}, read from config.')
except:
    log.error('Error reading DCL command string from config. Using WebLog default; MAKELOG+HTML.')
    dcl_command = 'MAKELOG+HTML'

# Read / Validate FTP server enable state from config.ini
try:
    ftp_enabled = ini.getboolean('FTP', 'Enable')
    log.debug(f'FTP Uploads {str(ftp_enabled)}')
except:
    ftp_enabled = False
    log.error('Error reading FTP enable state from config. Disabling FTP.')

# Read FTP Server from config.ini
try:
    ftp_host = ini['FTP']['Server']
    log.debug(f'Server URL, {ftp_host}, read from config.')
except:
    ftp_host = 'null'
    ftp_enabled = False
    log.error('Error reading FTP Server URL from config. Disabling FTP.')

# Read FTP Username from config.ini
try:
    ftp_user = ini['FTP']['Username']
    log.debug(f'FTP Username, {ftp_user} read from config.')
except:
    ftp_user = 'null'
    ftp_enabled = False
    log.error('Error reading FTP Username from config. Disabling FTP.')

# Read FTP Password from config.ini
try:
    ftp_password = ini['FTP']['Password']
    log.debug('FTP Password read from config.')
except:
    ftp_password = 'null'
    ftp_enabled = False
    log.error('Error reading FTP Password from config. Disabling FTP.')

# Read input rep file path from config.ini
try:
    input_file = ini['PLAYLIST']['Input']
    log.debug(f'REP Input File, {input_file}, read from config.')
except:
    log.critical('Fatal error reading REP file path from config. Exiting...')
    exit()

# Read output html file path from config.ini
try:
    output_file = ini['PLAYLIST']['Output']
    log.debug(f'HTML output file and path, {output_file}, read from config.')
except:
    log.critical('Fatal error reading HTML output file and path from config. Exiting...')
    exit()

# Read input file parse delimeter from config.ini
try:
    delimeter = ini['PLAYLIST']['Delimeter']
    log.debug(f'Input file delimeter, {delimeter}, read from config.')
except:
    delimeter = ',%,'
    log.error('Error reading input file delimeter from config. Using WebLog default of ,%,')

# Read selected playlist hours from config.ini and create a list of all selected hours
try:
    hours_string = ini['PLAYLIST']['Hours']
    log.debug(f'Playlist hour string, {hours_string}, read from config.')
    hours = hours_string.split(',')
except:
    hours = []
    log.error('Error reading selected hours from config. Unselecting all hours.')

# Read selected highlight keyword from config.ini
try:
    highlight_keyword = ini['PLAYLIST']['HighlightKeyword']
    if highlight_keyword == None:
        highlight_keyword = ''
    if highlight_keyword != '':
        log.debug(f'Read highlight keyword, {highlight_keyword}, from config.')
except:
    highlight_keyword = ''
    log.error('Error reading highlight keyword from config.')

# Read playlist title string from config
try:
    title_text = ini['FORMATTING']['Title']
    log.debug(f'Playlist title, {title_text}, read from config.')
except:
    title_text = 'WebLog'
    log.error('Error reading Playlist Title from config.')

# Read playlist subtitle string from config
try:
    subtitle_text = ini['FORMATTING']['Subtitle']
    log.debug(f'Playlist subtitle, {subtitle_text}, read from config.')
except:
    subtitle_text = 'HTML Playlist Creator for ENCO DAD'
    log.error('Error reading Playlist Subtitle from config.')

# Read highlight color for highlight keyword from config
try:
    highlight_color = ini['FORMATTING']['HighlightColor']
    log.debug(f'Read highlight color, {highlight_color}, from config.')
except:
    highlight_color = '000000'
    log.error('Error reading highlight color from config. Using black.')



def GetPlaylist(output, lines, *args, **kwargs):
    line = lines[0]
    line = line.strip().split(delimeter)
    playlist = line[0]
    try:            
        output.write(f"""
        <br>
        <h3 style="text-align:center"><strong>Playlist: {playlist}</strong></h3>
        """)
    except:
        log.error('Error getting playlist name from input file line 0, index 0.')

        
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
        if at0 == t0 and at1 == t1 and vtdj == highlight_keyword:
            output.write(f"""
            <tr>
             <th style="color:#{highlight_color}">{airtime}</th>
             <th style="color:#{highlight_color}">{title}</th>
             <th style="color:#{highlight_color}">{artist}</th>
             <th style="color:#{highlight_color}">{intro}</th>
             <th style="color:#{highlight_color}">{length}</th>
             </tr>
             """)
        elif at0 == t0 and at1 == t1 and vtdj != highlight_keyword:
            output.write(f"""
            <tr>
             <th>{airtime}</th>
             <th>{title}</th>
             <th>{artist}</th>
             <th>{intro}</th>
             <th>{length}</th>
             </tr>
             """)


def generate_log():
    #Read Log File from ENCO DAD
    infile = open(input_file, 'r')
    lines = infile.readlines()
    infile.close()

    #Create HTML File
    output = open(output_file, 'w')

    output.write(f"""
    <!DOCTYPE HTML>
    <html>
    <head>
     <title>{title}}</title>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
      <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" 
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" 
        integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
      <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" 
        integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </head>
    <body>
     <div class="row">
      <div class="col-md-2"></div>
      <div class="col-md-8">
       <div class="well">
        <h3 style="text-align:center">{subtitle_text}</h3>
    """)

    GetPlaylist(output, lines)

    output.write("""
    </div>
     <table class="table table-striped">
      <thead>
       <tr>
        <th>Airtime</th>
        <th>Title</th>
        <th>Artist</th>
        <th>Intro</th>
        <th>Length</th>
        </tr>
      </thead>
      <tbody>""")

    t0 = '1'
    t1 = '0'
    GetHour(output, lines, t0, t1)

    t1 = '1'
    GetHour(output, lines, t0, t1)

    t1 = '2'
    GetHour(output, lines, t0, t1)

    t1 = '3'
    GetHour(output, lines, t0, t1)

    output.write("""
          </tbody>
        </table>
        <div class="footer">
          <h6 style="text-align:center">Created using List2Web for ENCO DAD by D.I. Aspinwall</h6>
        </div>
        </div>
          <div class="col-md-2"></div>
        </div>
      </body>
    </html>
    """)
    output.close()

    print('HTML WebLog Generated.')
    if ftp_enabled:
        upload_log()


def upload_log():
    print(f'Uploading WebLog to {ftp_host}')
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
            
            if dcl == dcl_command:
                print('GENERATING WEBLOG...')
                generate_log()
            else:
                print(f'Invalid DCL Command sent to WebLog. Ignoring it...')
                break
    except:
        print('An error has occurred. Attempting to recover...')
        time.sleep(10)
        break