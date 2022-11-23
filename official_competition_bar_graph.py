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

#승률 그래프 함수
def winningRate(matchCount, nickname):
    #승무패 변수와 그래프 관련 변수
    x = np.arange(3)
    result = ["Win", "Draw", "Lose"] 
    resultCount = [0, 0, 0] #승, 무, 패 순서

    #매치 아이디 조회
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)

    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기

        #매치 정보 조회
        match_result = matchInfoFind(match_id)["matchInfo"][0]["matchDetail"]["matchResult"]; #승무패 변수

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

#매치 정보 조회
def matchInfoFind(match_id):
    match_info_url = 'https://api.nexon.co.kr/fifaonline4/v1.0/matches/'+match_id 
    match_info_url_req = requests.get(match_info_url, headers = headers)
    match_info_data = match_info_url_req.json()
    return match_info_data

#매치 아이디 조회
def matchIdFind(matchtype, offset, limit, nickname):
    match_info = {'matchtype' : matchtype, 'offset' : offset, 'limit' : limit}
    match_url = 'https://api.nexon.co.kr/fifaonline4/v1.0/users/'+ userIdFind(nickname) + '/matches?'
    match_url_req = requests.get(match_url,params=match_info, headers = headers)
    match_url_data = match_url_req.json()
    #매치 정보, 매치 데이터(json) 반환
    return match_info, match_url_data

#사용자 id 조회
def userIdFind(nickname):
    user_url = "https://api.nexon.co.kr/fifaonline4/v1.0/users?"
    player_nick = {'nickname' : nickname}
    user_response = requests.get(user_url, params=player_nick, headers = headers)
    user_json = user_response.json()
    user_id = user_json['accessId']
    return user_id

#평균 쓰루 패스 시도 수
def avthroughPassTry(matchCount, nickname):
    av_result = 0 
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["pass"]["throughPassTry"]; 
        av_result = av_result + int(match_result)
    return int(av_result/matchCount);
    
#평균 로빙 쓰루 패스 시도 수
def avlobbedThroughPassTry(matchCount, nickname):
    av_result = 0 
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["pass"]["lobbedThroughPassTry"]; 
        av_result = av_result + int(match_result)
    return int(av_result/matchCount);

#평균 점유율 (%단위로 반환)
def avpossession(matchCount, nickname):
    av_possession = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["matchDetail"]["possession"]; 
        av_possession = av_possession + int(match_result)
    return int(av_possession/matchCount)

#평균 패스 시도 수
def avpassTry(matchCount, nickname):
    av_passTry = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["pass"]["passTry"]; 
        av_passTry = av_passTry + int(match_result)
    return int(av_passTry/matchCount)


#평균 롱패스 시도 수
def avlongPassTry(matchCount, nickname):
    av_longPassTry = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["pass"]["longPassTry"]; 
        av_longPassTry = av_longPassTry + int(match_result)
    return int(av_longPassTry/matchCount)

#평균 경기 전체 골 수
def avgoalTotal(matchCount, nickname):
    av_goalTotal = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["shoot"]["goalTotal"]; 
        av_goalTotal = av_goalTotal + int(match_result)
    return int(av_goalTotal/matchCount)

#평균 헤딩 슛 수
def avshootHeading(matchCount, nickname):
    av_shootHeading = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["shoot"]["shootHeading"]; 
        av_shootHeading = av_shootHeading + int(match_result)
    return int(av_shootHeading/matchCount)


#평균 인패널티 슛 수
def avshootInPenalty(matchCount, nickname):
    av_shootInPenalty = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["shoot"]["shootInPenalty"]; 
        av_shootInPenalty = av_shootInPenalty + int(match_result)
    return int(av_shootInPenalty/matchCount)

#평균 아웃패널티 슛 수
def avshootOutPenalty(matchCount, nickname):
    av_shootOutPenalty = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["shoot"]["shootOutPenalty"]; 
        av_shootOutPenalty = av_shootOutPenalty + int(match_result)
    return int(av_shootOutPenalty/matchCount)

#평균 헤딩 골 수
def avgoalHeading(matchCount, nickname):
    av_goalHeading = 0
    match_info, match_url_data = matchIdFind(40, 0, matchCount, nickname)
    for i in range(0, match_info['limit'], 1): #매치를 하나씩 검사해서 승무패 카운트 올리기
        match_id = match_url_data[i]; #리스트로 특정 매치 불러오기
        match_result = matchInfoFind(match_id)["matchInfo"][0]["shoot"]["goalHeading"]; 
        av_goalHeading = av_goalHeading + int(match_result)
    return float(av_goalHeading/matchCount)




