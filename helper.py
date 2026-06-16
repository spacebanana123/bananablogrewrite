import os
import libopensonic

def loadEnvironmentVariables():
	if os.path.exists(".env"):
		with open(".env") as dotenv:
			text = dotenv.readlines()
			for line in text:
				if line.startswith("#"):
					continue
				else:
					os.environ[line.split("=")[0].strip()] = line.split("=")[1].strip()


def getPlaylist():
	loadEnvironmentVariables()
	conn = libopensonic.Connection(os.environ["navidromeServer"] , os.environ["User"] , os.environ["bananaBlogPassword"] , port=443)
	playlists = conn.get_playlists()
	reviewedID = ""
	studyID = ""
	for pl in playlists:
		if pl.name == "Reviewed":
			reviewedID = pl.id
		if pl.name == "Study":
			studyID = pl.id

	reviewedPlaylist = "#EXTM3U<br>#PLAYLIST:Reviewed<br>"

	for song in conn.get_playlist(reviewedID).entry:
		reviewedPlaylist += f"#EXTINF: {song.duration},{song.artist} - {song.title}<br>"
		
	songPlaylist = "#EXTM3U<br>#PLAYLIST:Study<br>"

	for song in conn.get_playlist(studyID).entry:
		songPlaylist += f"#EXTINF: {song.duration},{song.artist} - {song.title}<br>"
	
	return (reviewedPlaylist,songPlaylist)
