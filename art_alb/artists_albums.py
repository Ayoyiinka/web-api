from flask import jsonify, request, abort
from art_alb import app, dict_factory
import sqlite3

@app.route('/api/v1/chinook/artistsalbums', methods=['GET'])
def get_artists_with_their_albums():
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    artists_dict = cur.execute('SELECT * FROM artists;').fetchall()
    albums_dict = cur.execute('SELECT * FROM albums;').fetchall()
    conn.close()
    for artist in artists_dict:
        artist['AlbumTitle'] = []
        for album in albums_dict:
            if artist['ArtistId'] == album['ArtistId']:
                artist['AlbumTitle'].append(album['Title'])
    
    query_parameters = request.args
    id_ = query_parameters.get('ArtistId')
    name = query_parameters.get('Name')
    if id_ and name:
        if int(id_) <= 0:
            abort(400)
        artists = []
        for artist in artists_dict:
            if artist['Name'] == name:
                artist_id = artist['ArtistId']
                artists.append(artist)
                break
        if len(artists) == 0:
            abort(404)
        if int(id_) == artist_id:
            return jsonify(artists)
        else:
            abort(400)
    elif id_:
        if int(id_) <= 0:
            abort(400)
        artists = []
        if int(id_) > len(artists_dict):
            abort(404)
        artists.append(artists_dict[int(id_) - 1])
        return jsonify(artists)
    elif name:
        artists = []
        for artist in artists_dict:
            if artist['Name'] == name:
                artist_id = artist['ArtistId']
                artists.append(artist)
                break
        if len(artists) == 0:
            abort(404)
        return jsonify(artists)
    return jsonify(artists_dict) 