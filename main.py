import prototipe

target_url = 'https://www.youtube.com/watch?v=gHZ73tQ9XAU'
name_video = 'How to Grow a Mechanic Shop Business with Digital Marketing Strategy'
target_url1 = 'https://www.youtube.com/watch?v=0JJTdpKwA28'
name_video1 = 'Meditation Vibes Sounds & Ambience for Relaxation, Sleep, Study and Meditation | Get Some Sleep'
target_url2 = 'https://www.youtube.com/watch?v=nSfU5_hpWbo'
name_video2 = 'Hello Kitty Vs My Melody House Design 🍭💕 | Toca Life World | Toca Tanya'


def main():
    # pr_1 = prototipe.prototipe(url='https://youtube.com', proxy='154.16.243.71:6215:ctimpebr:anssq5y9ocac')
    # pr_2 = prototipe.prototipe(target_url=target_url, proxy='154.16.243.167:6311:ctimpebr:anssq5y9ocac', name_video=name_video)
    # pr_2.go()
    pr_2 = prototipe.prototipe(target_url=target_url1, proxy='154.16.243.167:6311:ctimpebr:anssq5y9ocac', name_video=name_video1)
    pr_2.go()

if __name__ == '__main__':
    main()