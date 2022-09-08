# name : officialCompetition
# author : 이정진
# date : 2022-09-07

import requests
import matplotlib.pyplot as plt
import numpy as np

#사용자 키 (넥슨에서 발급)
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLUFwcC1SYXRlLUxpbWl0IjoiNTAwOjEwIiwiYWNjb3VudF9pZCI6IjEzNDMwOTAzNzgiLCJhdXRoX2lkIjoiMiIsImV4cCI6MTY3ODAwOTAyNSwiaWF0IjoxNjYyNDU3MDI1LCJuYmYiOjE2NjI0NTcwMjUsInNlcnZpY2VfaWQiOiI0MzAwMTE0ODEiLCJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4ifQ.tS9ocmoEg2BK-UzoGT60178omldYyIQhmsJ01fs_ErU"

#헤더
headers = {'Authorization' : api_key}

#메인 실행 함수
def main():
    #승무패 변수와 그래프 관련 변수
    x = np.arange(3)
    result = ["Win", "Draw", "Lose"] 
    resultCount = [0, 0, 0] #승, 무, 패 순서

    #닉네임 입력받기
    nickname = str(input("NickName : "))

    #매치 아이디 조회
    match_info = {'matchtype' : 40, 'offset' : 0, 'limit' : 100}
    match_url = 'https://api.nexon.co.kr/fifaonline4/v1.0/users/'+ userIdFind(nickname) + '/matches?'
    match_url_req = requests.get(match_url,params=match_info, headers = headers)
    match_url_data = match_url_req.json()

    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
    
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        # print(match_id) 

        #매치 정보 조회
        match_info_url = 'https://api.nexon.co.kr/fifaonline4/v1.0/matches/'+match_id 
        match_info_url_req = requests.get(match_info_url, headers = headers)
        match_info_data = match_info_url_req.json()
        # print(match_info_data["matchInfo"][0]["matchDetail"]["matchResult"]) #승무패

        match_result = match_info_data["matchInfo"][0]["matchDetail"]["matchResult"]; #승무패 변수

        if match_result == "승":
            resultCount[0] = resultCount[0] + 1
        elif match_result == "무":
            resultCount[1] = resultCount[1] + 1
        elif match_result == "패":
            resultCount[2] = resultCount[2] + 1

    result[0] = "Win(" + str(resultCount[0]) + "%)"
    result[1] = "Draw(" + str(resultCount[1]) + "%)"
    result[2] = "Lose(" + str(resultCount[2]) + "%)"

    plt.bar(x, resultCount, width=0.5)
    plt.xticks(x, result)
    plt.title("1 to 1 official match")
    plt.show()


#사용자 id 조회
def userIdFind(nickname):
    user_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?"
    player_nick = {'nickname' : nickname}
    user_response = requests.get(user_url, params=player_nick, headers = headers)
    user_json = user_response.json()
    user_id = user_json['accessId']
    return user_id


#실행
main()