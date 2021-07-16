from flickrapi import FlickrAPI
import json
import urllib
import os 

# Constants
SIZE = 'url_s'
IMG_LIMIT = 4000
WRITE_FILE = 'urls.json'

# Retrieve API Key and Secret
f = open('tokens.json')

tokens = json.load(f)
API_KEY = tokens['api_key']
SECRET = tokens['secret']

f.close()

# Initialize FlickrAPI
flickr = FlickrAPI(API_KEY, SECRET, format='parsed-json')

# States to search images on 
states = ['Alabama', 'Alaska', 'Arkansas', 'Arizona', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 
'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
 'West Virginia', 'Wisconsin', 'Wyoming']
states_test = ['Alabama']

def retreive_urls(states, limit):
    url_dict = {state: [] for state in states}

    for state in states:
        photos = flickr.photos.search(tags=state, sort='relevance', privacy_filter=1, extras=SIZE, per_page=500, page=8, geo_context=2)

        count = 0
        # Insert Urls into url_dict for ease of access 
        for photo in photos['photos']['photo']:     
            if SIZE in photo.keys():
                print(photo)
                break
                url_dict[state].append(photo[SIZE])
                count += 1

                # Check if within the image limit
                if count == limit:
                    break
        
        print('Image count for {}: {}'.format(state, count))
        
    return url_dict

def manage_dir(state):
    cwd = os.getcwd()
    path = os.path.join(cwd, state)

    existing_dir = os.path.exists(path)

    if existing_dir:
        pass
    else:
        os.mkdir(path)

    return 1

def save_imgs(urls, states):
    for state in states:
        state_urls = urls[state]
        
        # Retreive data on current state's directory status
        count = manage_dir(state)

        # Save each file uniquely
        count = 1
        for url in state_urls:
            urllib.request.urlretrieve(url, './' + state + '/' + state + str(count) + '.png')
            count += 1

def write_to_json(url_dict, file):
    with open(file, 'w') as outfile:
        json.dump(url_dict, outfile)

    outfile.close()


def main():
    url_dict = retreive_urls(states, IMG_LIMIT)
    save_imgs(url_dict, states)
    write_to_json(url_dict, WRITE_FILE)

if __name__ == "__main__":
    main()
