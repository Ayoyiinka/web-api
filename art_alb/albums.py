from flask import jsonify, request, abort, make_response
from art_alb import app, dict_factory
import sqlite3

@app.route('/api/v1/chinook/album', methods=['POST', 'PUT'])
def album():
    if not request.json:
        abort(400)
    
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    albums = cur.execute('SELECT * FROM albums;').fetchall()
    
    title = request.json.get('Title')
    if request.method == 'POST':
        if not 'Title' in request.json:
            abort(400)
        if not 'Name' in request.json and not 'ArtistId' in request.json:
            abort(400)
        name = request.json.get('Name')
        id_ = request.json.get('ArtistId')
        title = str(title)
        if len(title) > 160:
            abort(400)
        
        album_id = albums[-1]['AlbumId']
        album_id += 1
        
        artists = cur.execute('SELECT * FROM artists;').fetchall()
        if name and id_:
            try:
                id_ = int(id_)
            except:
                abort(400)
            if id_ > len(artists) or id_ < 1:
                abort(400)
            for artist in artists:
                name = str(name)
                if len(name) > 120:
                    abort(400)
                if artist['Name'] == name:
                    artist_id = artist['ArtistId']
                    break
                else:
                    artist_id = None
            if not artist_id:
                abort(404)
            if artist_id == id_:
                cur.execute("INSERT INTO albums VALUES (?, ?, ?)", [album_id, title, artist_id])
            else:
                abort(400)
        elif name:
            for artist in artists:
                if artist['Name'] == name:
                    artist_id = artist['ArtistId']
                    break
                else:
                    artist_id = None
            if not artist_id:
                abort(404)
            cur.execute("INSERT INTO albums VALUES (?, ?, ?)", [album_id, title, artist_id])
        elif id_:
            try:
                id_ = int(id_)
            except:
                abort(400)
            if id_ > len(artists) or id_ < 1:
                abort(400)
            artist_id = id_
            cur.execute("INSERT INTO albums VALUES (?, ?, ?)", [album_id, title, artist_id])
        
        conn.commit()
        conn.close()

        new_album = {
            'AlbumId': album_id,
            'Title': title,
            'ArtistId': artist_id
        }

        albums.append(new_album)
        return jsonify(albums), 201
    
    id_ = request.json.get('AlbumId')
    if request.method == 'PUT':
        if not 'new_title' in request.json and not 'new_artist_id' in request.json:
            abort(400)
        if not 'AlbumId' in request.json and not 'Title' in request.json:
            abort(400)
        
        new_title = request.json.get('new_title')
        new_artist_id = request.json.get('new_artist_id')
        if new_title:
            new_title = str(new_title)
            if len(new_title) > 160:
                abort(400)
            if title and id_:
                try:
                    id_ = int(id_)
                except:
                    abort(400)
                if id_ > len(albums) or id_ < 1:
                    abort(400)
                for album in albums:
                    if album['Title'] == title:
                        album_id = album['AlbumId']
                        break
                    else:
                        album_id = None
                if not album_id:
                    abort(404)
                if album_id == id_:
                    cur.execute("UPDATE albums SET Title = ? where AlbumId = ?", [new_title, album_id])
                else:
                    abort(400)
            elif title:
                for album in albums:
                    if album['Title'] == title:
                        album_id = album['AlbumId']
                        break
                    else:
                        album_id = None
                if not album_id:
                    abort(404)
                cur.execute("UPDATE albums SET Title = ? where AlbumId = ?", [new_title, album_id])
            elif id_:
                try:
                    id_ = int(id_)
                except:
                    abort(400)
                if id_ > len(albums) or id_ < 1:
                    abort(400)
                album_id = id_
                cur.execute("UPDATE albums SET Title = ? where AlbumId = ?", [new_title, album_id])
            albums[album_id-1]['Title'] = new_title
        if new_artist_id:
            if title and id_:
                try:
                    id_ = int(id_)
                except:
                    abort(400)
                if id_ > len(albums) or id_ < 1:
                    abort(400)
                for album in albums:
                    if album['Title'] == title:
                        album_id = album['AlbumId']
                        break
                    else:
                        album_id = None
                if not album_id:
                    abort(404)
                if album_id == id_:
                    cur.execute("UPDATE albums SET ArtistId = ? where AlbumId = ?", [new_artist_id, album_id])
                else:
                    abort(400)
            elif title:
                for album in albums:
                    if album['Title'] == title:
                        album_id = album['AlbumId']
                        break
                    else:
                        album_id = None
                if not album_id:
                    abort(404)
                cur.execute("UPDATE albums SET ArtistId = ? where AlbumId = ?", [new_artist_id, album_id])
            elif id_:
                try:
                    id_ = int(id_)
                except:
                    abort(400)
                if id_ > len(albums) or id_ < 1:
                    abort(400)
                album_id = id_
                cur.execute("UPDATE albums SET ArtistId = ? where AlbumId = ?", [new_artist_id, album_id])
            albums[album_id-1]['ArtistId'] = new_artist_id
                
        conn.commit()
        conn.close()
        
        return jsonify(albums)