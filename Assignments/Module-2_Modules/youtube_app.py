from pytubefix import YouTube

url="https://www.youtube.com/watch?v=gLptmcuCx6Q"

YouTube(url).streams.first().download()