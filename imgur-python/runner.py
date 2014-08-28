from client import ImgurClient

if __name__ == '__main__':
    img = ImgurClient(client_id='3aa9b7ef8d192ea')
    print img.make_request('GET', 'account/jasdev')