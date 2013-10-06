#Spinitron Abnormalities
WMFO - Tufts Freeform Radio  
ops@wmfo.org  
For copyrights and licensing, see COPYING.  

A simple Python script that detects when automation is on while a DJ is on-air.

It expects a csv file that can be obtained from Spinitron by admins. Export a playlist with only the time field, csv format, with headings for playlist, no columns headings, DJ real names optional, for reading by a computer.

Pass the file in as an argument, or use the name `spin-data.csv`. Offendings DJs will have their names printed. Specifically, these DJs played two songs within 10 minutes of each other, and during that window Rick Deckard also logged a song.

The script is far from perfect but is more likely to have false negatives than false positives.

One avenue for expansion is to detect other abnormalities, such as playlists more than 3ish hours long.

##Changelog
###09/17/13
Initial version. - Max Goldstein

###10/6/13
Show how many times Rick Deckard logged between human-logged songs. - Max Goldstein
