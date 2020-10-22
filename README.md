# WebLog for ENCO DAD

#### WebLog generates a HTML file based on an ENCO .REP file and uploads the html file via ftp.

## Configuration

Various WebLog settings can be controlled through a *config.ini* file associated with WebLog.

### NETWORK

WebLog can be triggered via ENCO DCL Commands.

**IP**: The IP address of the computer the WebLog server will run on (this is required as many machines running WebLog may have multiple NICs).

**Port**: The UDP port for listening for incoming DCLs from the ENCO system. ENCO uses UDP port 2002 for DCL commands, and this port should not be changed under normal circumstances.

### FTP_UPLOAD

WebLog can automatically upload the generated HTML file to a FTP server.

**Server**: IP address or URL of FTP server.

**Username**: Username credential for FTP server.

**Password**: Password credential for FTP server.

### PLAYLIST

**Input**: Path to the PLIST.REP or PLIST2.REP report files on the ENCO. (Note these files must be formatted as notated in the *Playlist Report Formatting* section).

> Example: *E:\DAD\Files\PLIST.REP*

**Output**: Path and filename of the generated html file.

> Example: *C:\WebLog\Playlist.html*

**Delimeter**: String used as a delimeter value in the Plist.rpg file. For more information, refer to the *Playlist Report Formatting* section.

**Hours**: Hours of the day to include in the html playlist report. Comma seperated values, 24 hour clock, leading zeros.

> Example: ***09, 10, 11, 12, 13*** *would output the 9:00am, 10:00am, 11:00am, 12:00pm, and 1:00pm hours.*

## Playlist RPG Formatting

ENCO reports are generated based on RPG template files. In order for WebLog to properly function, use the included Plist.rpg template.

*Note that this template assumes your library is called "CUTS". If your library has a different name, it can be changed in the RPG file.*