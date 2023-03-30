import socket
import time
import math

# 닉네임을 사용자에 맞게 변경해 주세요.
NICKNAME = 'SEOUL1_KOHYEONGJIN'

# 일타싸피 프로그램을 로컬에서 실행할 경우 변경하지 않습니다.
HOST = '127.0.0.1'

# 일타싸피 프로그램과 통신할 때 사용하는 코드값으로 변경하지 않습니다.
PORT = 1447
CODE_SEND = 9901
CODE_REQUEST = 9902
SIGNAL_ORDER = 9908
SIGNAL_CLOSE = 9909

# 게임 환경에 대한 상수입니다.
TABLE_WIDTH = 254
TABLE_HEIGHT = 127
NUMBER_OF_BALLS = 6
HOLES = [[0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127]]

order = 0
balls = [[0, 0] for i in range(NUMBER_OF_BALLS)]

sock = socket.socket()
print('Trying to Connect: %s:%d' % (HOST, PORT))
sock.connect((HOST, PORT))
print('Connected: %s:%d' % (HOST, PORT))

send_data = '%d/%s' % (CODE_SEND, NICKNAME)
sock.send(send_data.encode('utf-8'))
print('Ready to play!\n--------------------')
turn = 1
while True:

    # Receive Data
    recv_data = (sock.recv(1024)).decode()
    print('Data Received: %s' % recv_data)

    # Read Game Data
    split_data = recv_data.split('/')
    idx = 0
    try:
        for i in range(NUMBER_OF_BALLS):
            for j in range(2):
                balls[i][j] = float(split_data[idx])
                idx += 1
    except:
        send_data = '%d/%s' % (CODE_REQUEST, NICKNAME)
        print("Received Data has been currupted, Resend Requested.")
        continue

    # Check Signal for Player Order or Close Connection
    if balls[0][0] == SIGNAL_ORDER:
        order = int(balls[0][1])
        print('\n* You will be the %s player. *\n' % ('first' if order == 1 else 'second'))
        continue
    elif balls[0][0] == SIGNAL_CLOSE:
        break

    # Show Balls' Position
    print('====== Arrays ======')
    for i in range(NUMBER_OF_BALLS):
        print('Ball %d: %f, %f' % (i, balls[i][0], balls[i][1]))
    print('====================')

    angle = 0.0
    power = 0.0

    ##############################
    # 이 위는 일타싸피와 통신하여 데이터를 주고 받기 위해 작성된 부분이므로 수정하면 안됩니다.
    #
    # 모든 수신값은 변수, 배열에서 확인할 수 있습니다.
    #   - order: 1인 경우 선공, 2인 경우 후공을 의미
    #   - balls[][]: 일타싸피 정보를 수신해서 각 공의 좌표를 배열로 저장
    #     예) balls[0][0]: 흰 공의 X좌표
    #         balls[0][1]: 흰 공의 Y좌표
    #         balls[1][0]: 1번 공의 X좌표
    #         balls[4][0]: 4번 공의 X좌표
    #         balls[5][0]: 마지막 번호(8번) 공의 X좌표

    # 여기서부터 코드를 작성하세요.
    # 아래에 있는 것은 샘플로 작성된 코드이므로 자유롭게 변경할 수 있습니다.

    # whiteBall_x, whiteBall_y: 흰 공의 X, Y좌표를 나타내기 위해 사용한 변수
    p = 0
    whiteBall_x = balls[0][0]
    whiteBall_y = balls[0][1]

    # targetBall_x, targetBall_y: 목적구의 X, Y좌표를 나타내기 위해 사용한 변수
    # if balls[5] == [198, 64]:
    #     print('1')
    #     targetBall_x = balls[5][0]
    #     targetBall_y = balls[5][1]

    if order == 1 and turn == 1:
        targetBall_x = balls[3][0]
        targetBall_y = balls[3][1]
    else:
        for k in range(order, 5, 2):
            if balls[k][0] != -1.0:
                targetBall_x = balls[k][0]
                targetBall_y = balls[k][1]
                break
        else:
            targetBall_x = balls[5][0]
            targetBall_y = balls[5][1]

    # 목적구와 흰색공의 위치 관계
    positon = 0
    if whiteBall_x < targetBall_x and whiteBall_y < targetBall_y:
        positon = 1
    elif whiteBall_x > targetBall_x and whiteBall_y < targetBall_y:
        positon = 2
    elif whiteBall_x > targetBall_x and whiteBall_y > targetBall_y:
        positon = 3
    elif whiteBall_x < targetBall_x and whiteBall_y > targetBall_y:
        positon = 4

    if positon == 4:
        if targetBall_x < 127:
            target_hole_x, target_hole_y = HOLES[1][0], HOLES[1][1] + p
        else:
            target_hole_x, target_hole_y = HOLES[2][0] - p, HOLES[2][1] + p
    elif positon == 3:
        if targetBall_x > 127:
            target_hole_x, target_hole_y = HOLES[1][0], HOLES[1][1] + p
        else:
            target_hole_x, target_hole_y = HOLES[0][0] + p, HOLES[0][1] + p
    elif positon == 2:
        if targetBall_x > 127:
            target_hole_x, target_hole_y = HOLES[4][0], HOLES[4][1] - p
        else:
            target_hole_x, target_hole_y = HOLES[3][0] + p, HOLES[3][1] - p
    else:
        if targetBall_x < 127:
            target_hole_x, target_hole_y = HOLES[4][0], HOLES[4][1] - p
        else:
            target_hole_x, target_hole_y = HOLES[5][0] - p, HOLES[5][1] - p

    hole_distance = math.sqrt(abs(targetBall_x - target_hole_x) ** 2 + abs(targetBall_y - target_hole_y) ** 2)

    target_x = targetBall_x + 5.6 * (targetBall_x - target_hole_x) / hole_distance
    target_y = targetBall_y + 5.6 * (targetBall_y - target_hole_y) / hole_distance
    print('타겟 볼 좌표', targetBall_x, targetBall_y)
    print('타겟 홀 좌표', target_hole_x, target_hole_y)
    print('타겟 할 곳 좌표', target_x, target_y, (targetBall_x - target_hole_x), hole_distance)
    # width, height: 목적구와 흰 공의 X좌표 간의 거리, Y좌표 간의 거리
    width = abs(target_x - whiteBall_x)
    height = abs(target_y - whiteBall_y)

    # radian: width와 height를 두 변으로 하는 직각삼각형의 각도를 구한 결과
    #   - 1radian = 180 / PI (도)
    #   - 1도 = PI / 180 (radian)
    # angle: 아크탄젠트로 얻은 각도 radian을 degree로 환산한 결과
    radian = math.atan(width / height) if height > 0 else 0
    angle = 180 / math.pi * radian

    # 목적구가 흰 공과 상하좌우로 일직선상에 위치했을 때 각도 입력
    if whiteBall_x == targetBall_x:
        if whiteBall_y < targetBall_y:
            angle = 0
        else:
            angle = 180
    elif whiteBall_y == targetBall_y:
        if whiteBall_x < targetBall_x:
            angle = 90
        else:
            angle = 270

    # 목적구가 흰 공을 중심으로 3사분면에 위치했을 때 각도를 재계산
    if whiteBall_x > target_x and whiteBall_y > target_y:
        radian = math.atan(width / height)
        angle = (180 / math.pi * radian) + 180

    # 목적구가 흰 공을 중심으로 4사분면에 위치했을 때 각도를 재계산
    elif whiteBall_x < target_x and whiteBall_y > target_y:
        radian = math.atan(height / width)
        angle = (180 / math.pi * radian) + 90

    # 목적구가 흰 공을 중심으로 2사분면에 위치했을 때 각도를 재계산
    elif whiteBall_x > target_x and whiteBall_y < target_y:
        radian = math.atan(height / width)
        angle = (180 / math.pi * radian) + 270
        print(True)

    print(width, height)
    print('각도', angle)
    # distance: 두 점(좌표) 사이의 거리를 계산
    distance = math.sqrt(abs(whiteBall_x - target_hole_x) ** 2 + abs(whiteBall_y - target_hole_y) ** 2)

    # power: 거리 distance에 따른 힘의 세기를 계산
    power = distance * 0.21

    # 주어진 데이터(공의 좌표)를 활용하여 두 개의 값을 최종 결정하고 나면,
    # 나머지 코드에서 일타싸피로 값을 보내 자동으로 플레이를 진행하게 합니다.
    #   - angle: 흰 공을 때려서 보낼 방향(각도)
    #   - power: 흰 공을 때릴 힘의 세기
    #
    # 이 때 주의할 점은 power는 100을 초과할 수 없으며,
    # power = 0인 경우 힘이 제로(0)이므로 아무런 반응이 나타나지 않습니다.
    #
    # 아래는 일타싸피와 통신하는 나머지 부분이므로 수정하면 안됩니다.
    ##############################

    merged_data = '%f/%f/' % (angle, power)
    sock.send(merged_data.encode('utf-8'))
    print('Data Sent: %s' % merged_data)
    turn += 1
sock.close()
print('Connection Closed.\n--------------------')

"""
1. 타겟공을 판별합니다.
2. 흰색공과 목적구의 위치 정보에 따라 넣을 타겟홀의 좌표 target_hole_x, target_hole_y를 정합니다.
3. 타겟홀과 목적구의 위치에 따라서 타겟할 타겟좌표 target_x와 target_y를 정합니다.
   목적구와 타겟홀의 각도에 따라서 흰색공을 타겟좌표에 도달하게 하면 목적구가 타겟홀로 향하게끔 타겟좌표를 정합니다.
4. 타겟좌표와 흰색공의 위치 관계에 따라서 각도를 변경합니다.
5. 흰색공과 타겟홀의 거리에 따라서 세기를 조절합니다.
6. 계산된 세기와 각도를 이용해 시행합니다.
"""
