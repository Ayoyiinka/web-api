from flask import jsonify, request, abort
from art_alb import app, dict_factory
import sqlite3

@app.route('/api/v1/chinook/artist', methods=['POST', 'PUT'])
def artist():
    if not request.json:
        abort(400)
        
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    artists = cur.execute('SELECT * FROM artists;').fetchall()
    
    name = request.json.get('Name')
    if request.method == 'POST':
        if not 'Name' in request.json:
            abort(400)
    
        artist_id = artists[-1]['ArtistId']
        artist_id += 1
        name = str(name)
        if len(name) > 120:
            abort(400)

        cur.execute("INSERT INTO artists VALUES (?, ?)", [artist_id, name])
        conn.commit()
        conn.close()

        new_artist = {
            'ArtistId': artist_id,
            'Name': name
        }
    
        artists.append(new_artist)
        return jsonify(artists), 201
    
    id_ = request.json.get('ArtistId')
    if request.method == 'PUT':
        if not 'Name' in request.json and not 'ArtistId' in request.json:
            abort(400)
        if not 'new_name' in request.json:
            abort(400)
            
        new_name = str(request.json.get('new_name'))
        if len(new_name) > 120:
            abort(400)
            
        if name and id_:
            try:
                id_ = int(id_)
            except:
                abort(400)
            if id_ > len(artists) or id_ < 1:
                abort(400)
            name = str(name)
            if len(name) > 120:
                abort(400)
            for artist in artists:
                if artist['Name'] == name:
                    artist_id = artist['ArtistId']
                    break
                else:
                    artist_id = None
            if not artist_id:
                abort(404)
            if artist_id == id_:
                cur.execute("UPDATE artists SET Name = ? where ArtistId = ?", [new_name, artist_id])
            else:
                abort(400)
        elif name:
            name = str(name)
            if len(name) > 120:
                abort(400)
            for artist in artists:
                if artist['Name'] == name:
                    artist_id = artist['ArtistId']
                    break
                else:
                    artist_id = None
            if not artist_id:
                abort(404)
            cur.execute("UPDATE artists SET Name = ? where ArtistId = ?", [new_name, artist_id])
        elif id_:
            try:
                id_ = int(id_)
            except:
                abort(400)
            if id_ > len(artists) or id_ < 1:
                abort(400)
            artist_id = id_
            cur.execute("UPDATE artists SET Name = ? where ArtistId = ?", [new_name, artist_id])

        conn.commit()
        conn.close()
        artists[artist_id-1]['Name'] = new_name
        return jsonify(artists)
