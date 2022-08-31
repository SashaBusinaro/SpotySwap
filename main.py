def main():
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    import os

    """
    Inserct here your API credentials
    """
    SOURCE_USER_ID = ""
    SOURCE_USER_SECRET = ""

    DESTINATION_USER_ID = ""
    DESTINATION_USER_SECRET = ""

    """
    Extracts the list of tracks from the source account
    """
    
    # Source Account, Scope: Read
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SOURCE_USER_ID, client_secret=SOURCE_USER_SECRET, redirect_uri="http://localhost:8000", scope="user-library-read"))

    track_list = []
    offset = 0 # defines the point from which to start extracting tracks, 0 = beginning 
    run = True
    
    while run == True:
        # Extract all the tracks in the library
        extracted_library = sp.current_user_saved_tracks(limit=50, offset=offset)

        tracks_number = extracted_library["total"]
        print('Total library tracks:', tracks_number)

        # Generates a list containing chunks of 50 track ids each
        track_list.append([extracted_library['items'][i]['track']['id'] for i in range(len(extracted_library['items']))])

        # Calculate the remaining songs to be included in the track list
        remaining = len(track_list[-1]) + offset

        if remaining == tracks_number:
            run = False

        # Adjust the offset
        offset += 50

    """
    Filters the track list to obtain only songs not already present in the target library
    """

    # Clearing the access cache allows logging in with the target account
    os.remove('.cache')

    # Destination Account, Scope: Read
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=DESTINATION_USER_ID, client_secret=DESTINATION_USER_SECRET, redirect_uri="http://localhost:8000", scope="user-library-read"))

    only_new_tracks = []

    # Filter each chunk to obtain only new tracks
    for chunk in track_list:
        # Query the target library
        chuncked_results = sp.current_user_saved_tracks_contains(tracks=chunk)
        
        # Only includes songs in the list that are not already in the target library (False)
        only_new_tracks.extend([chunk[i] for i in range(len(chunk)) if chuncked_results[i] == False])

    # Sort the result into sublists containing a maximum of 50 tracks each
    def chunk_list(only_new_tracks):
        sorted_result = []

        chunk_size = 50 # maximum ids per sublist

        i = 0 # increment for the function

        remaining = len(only_new_tracks) # tracks remaining to be sorted

        # Repeat the process until all tracks have been sorted
        while remaining > 0:
            i_start = i*chunk_size
            i_stop = i*chunk_size + chunk_size
            sorted_result.append(only_new_tracks[i_start:i_stop])

            i += 1
            remaining -= chunk_size
        return sorted_result, i, remaining

    sorted_result, i , remaining = chunk_list(only_new_tracks)
    new_tracks_found = ((i-1)*50) + (50+remaining)

    print(new_tracks_found, "New tracks found")

    """
    Only imports into the target library tracks that are not already present
    """

    # Destination Account, Scope: Modify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=DESTINATION_USER_ID, client_secret=DESTINATION_USER_SECRET, redirect_uri="http://localhost:8000", scope="user-library-modify"))

    for chunk in sorted_result:
        sp.current_user_saved_tracks_add(tracks=chunk)
    
    print(f"Successfully transferred {new_tracks_found} new tracks")
    
    # Init cache
    os.remove('.cache')

if __name__ == '__main__':
    main()