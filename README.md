# Smart Garage Door
opens automatically when it sees your plate number
<p></p>

## Table of contents  
- [How it works](#how-it-works)
- [Prerequisites](#prerequisites)

<p></p>

## How it works
1. Wait for the car.
1. Take a picture.
1. Send it to [Open ALPR](https://www.openalpr.com/) API.
1. Get plate numbers guess from the API.
1. check if they exist in our database.
1. If yes, open the door
1. wait for a new car and repeat.
<p></p>



## Prerequisites
##### 1. Enable Camera module:
> sudo raspi-config

then go to interfaces and __enable camera module__

> reboot

##### 2. Installing Python Libraries:
> sudo pip3 install picamera

> sudo pip3 install requests

##### 3. Get your sk (secret_key)
1. [Register in OpenALPR](https://cloud.openalpr.com/account/register)
1. [Get your secret key](https://cloud.openalpr.com/cloudapi/)
<p align="center">
  <img width="800" height="512" src="https://github.com/AlphaArslan/Smart_Garage_Door/blob/master/secret_key.png">
</p>
1. add your key here

```python
  secret_Key  = "sk_d1f041eXXXXXXXXXXXXXXXX"
```
