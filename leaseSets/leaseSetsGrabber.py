from html.parser import HTMLParser
import requests
from multiprocessing import Pool

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_slide = False
        self.inside_label = False
        self.current_label = None
        self.data = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ('class', 'slide') in attrs:
            self.inside_slide = True
            self.current_label = None
        elif self.inside_slide and tag == 'label':
            self.inside_label = True

    def handle_data(self, data):
        if self.inside_label:
            self.current_label = data.strip()

    def handle_endtag(self, tag):
        if self.inside_label and tag == 'label':
            self.inside_label = False
        elif self.inside_slide and tag == 'div':
            self.inside_slide = False
            if self.current_label:
                self.data.add(f"{self.current_label}.b32.i2p")

def grab_leasesets(url='http://127.0.0.1:7071/?page=leasesets', out_file_path='./leasesets.txt'):
    response = requests.get(url)

    if response.status_code == 200:
        parser = MyHTMLParser()
        parser.feed(response.text)

        with open(out_file_path, 'a') as file_out:
            for line in parser.data:
                print(line, file=file_out)

    else:
        print(f"Error: Unable to fetch content. Status code: {response.status_code}")

def main():
    # Adjust the number of processes based on your system's capabilities
    num_processes = 4
    urls = [
        'http://127.0.0.1:7071/?page=leasesets',
        'http://127.0.0.1:7070/?page=leasesets',
        # Add more URLs if needed
    ]

    with Pool(processes=num_processes) as pool:
        pool.starmap(grab_leasesets, [(url,) for url in urls])

if __name__ == "__main__":
    main()
