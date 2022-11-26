import official_competition_bar_graph as ocbg

rank_throughPass = 18
rank_lobbedThroughPassTry = 1

rank_possession = 50
rank_pass = 114

rank_longPassTry = 3
rank_shootHeading = 1

rank_goalHeading = 0.16

rank_shootOutPenalty = 2

#메인 실행 함수
def main():
    match_count = 30
    nickname = input("닉네임을 입력하세요 : ")

    #공격 플레이 스타일 분석
    play_style = getPlayStyle(nickname, match_count);

    #결과 출력
    print("[ %s님의 플레이어 분석 ]" %nickname)
    print("- 평균 경기(%d) 득점 수 : %s" %(match_count, str(ocbg.avgoalTotal(match_count, nickname))))
    print("- 주요 득점 방식 : %s" %(getGoalCode(getMaxGoal(match_count, nickname))))
    print("- 플레이 스타일 : %s" %play_style)

#스타일 코드
def getPlayStyleCodeMessage(style_code):
    dict = {
        0 : "침투 플레이",
        1 : "점유율 플레이",
        2 : "타겟맨 플레이",
        3 : "중거리 플레이",
        4 : "밸런스 플레이",
    }
    return dict[style_code]

#스타일 분석해서 코드 반환
def getPlayStyle(nickname, match_count):
    #(0=침투플레이) (1=점유율플레이) (2=타겟맨플레이) (3=중거리플레이) (4=벨런스플레이=>아무것도해당X)
    plyer_throughPass = ocbg.avthroughPassTry(match_count, nickname)
    plyer_lobbedThroughPassTry = ocbg.avlobbedThroughPassTry(match_count, nickname)

    plyer_possession = ocbg.avpossession(match_count, nickname)
    plyer_pass = ocbg.avpassTry(match_count, nickname)

    plyer_longPassTry = ocbg.avlongPassTry(match_count, nickname)
    plyer_shootHeading = ocbg.avshootHeading(match_count, nickname)

    plyer_goalHeading = ocbg.avgoalHeading(match_count, nickname)

    plyer_avshootOutPenalty = ocbg.avshootOutPenalty(match_count, nickname)

    style_code = 4 

    if(plyer_throughPass > rank_throughPass and plyer_lobbedThroughPassTry > rank_lobbedThroughPassTry):
        style_code = 0
    elif(plyer_possession > rank_possession and plyer_pass > rank_pass):
        style_code = 1
    elif(plyer_longPassTry > rank_longPassTry and plyer_goalHeading > rank_goalHeading and plyer_shootHeading > rank_shootHeading):
        style_code = 2
    elif(plyer_avshootOutPenalty > rank_shootOutPenalty):
        style_code = 3
    return getPlayStyleCodeMessage(style_code)


#주요 득점 코드
def getGoalCode(style_code):
    dict = {
        0 : "프리킥 골",
        1 : "패널티 박스 안 골",
        2 : "패널티킥 골",
        3 : "헤딩 골",
        4 : "패널티 박스 바깥 골",
    }
    return dict[style_code]

#가장 많은 득점 패턴 반환
def getMaxGoal(matchCount, nickname):
    dic = {
        "득점수" : 0,
        "패턴" : "없음"
    }
    max = 0

    goal_list = [
        ocbg.avfreeKick(matchCount, nickname),
        ocbg.avgoalInPenalty(matchCount, nickname),
        ocbg.avgoalPenaltyKick(matchCount, nickname),
        ocbg.avgoalHeading(matchCount, nickname),
        ocbg.avgoalOutPenalty(matchCount, nickname)
    ]

    if(goal_list[0] > max):
        max = goal_list[0]
        dic["패턴"] = 0
    if(goal_list[1] > max):
        max = goal_list[1]
        dic["패턴"] = 1
    if(goal_list[2] > max):
        max = goal_list[2]
        dic["패턴"] = 2
    if(goal_list[3] > max):
        max = goal_list[3]
        dic["패턴"] = 3
    if(goal_list[4] > max):
        max = goal_list[4]
        dic["패턴"] = 4

    return dic["패턴"]


#실행
main()
