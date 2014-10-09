from imgurpython import ImgurClient

if __name__ == "__main__":
    c = ImgurClient('d678b0301ba0dad', 'f2a1b2e3d9310a2f9f1d5a0a078a782c0d94e6b7')
    print(c.gallery())