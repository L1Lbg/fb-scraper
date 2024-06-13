from bs4 import BeautifulSoup
import urllib.parse

def find_pages(html):
    bs = BeautifulSoup(html, 'html.parser')

    urls = set()
    for a in bs.find_all('a', href=True):
        url = a.get('href')
        # REMOVE USELESS PARAMS
        try:
            if '__tn__' in url:

                parsed_url = urllib.parse.urlparse(url)
        
                # Parse the query parameters into a dictionary
                query_params = urllib.parse.parse_qs(parsed_url.query)
                
                # Filter out only the 'id' parameter
                filtered_query_params = {'id': query_params.get('id')}
                
                # Construct the new query string with only the 'id' parameter
                new_query_string = urllib.parse.urlencode(filtered_query_params, doseq=True)
                
                # Reconstruct the URL with the new query string
                url = urllib.parse.urlunparse(
                    (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment)
                )

        except Exception as e:
            print(f"Could not remove params: {e}")

        # ONLY FACEBOOK INTERNAL URLS
        if 'https://www.facebook.com/' in url or 'https://facebook.com/' in url:
            # IF ITS A FACEBOOK AUTOMATED PAGE
            if '/pages/' not in url:
                # IF ITS NOT AN AD
                if '__cft__[0]' not in url:
                    urls.add(url)

    return urls