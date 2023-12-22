import cv2
import pynput
import math
#需要下载两个资料，一个是mediapipe手势识别的，调用就可以，还有一个是pynput，控制鼠标的
#右手暂时没有开发，其实和左手原理近似，只要把左手的代码复制下去，修改一些即可
ctr = pynput.mouse.Controller()
from HANDUTILS import HandDetector
camera = cv2.VideoCapture(0)

camera.set(3, 7000)
camera.set(4, 7000)
hand_detector = HandDetector()
flag=1
num=0
while True:
    success, img = camera.read()
    if success:
        img = cv2.flip(img,1)#屏幕反转
        hand_detector.process(img)
        position = hand_detector.find_position(img)
        #print(hand_detector.find_eight_x)  # 下方控制器
        #左手，中指无名指小指合上，鼠标不再动，食指和大拇指缩小一厘米处，鼠标单机且不松开，可以拖拽，食指和大拇指完全合并，双击
        hand_L= 'Left'
        #left_fingers =hand_detector.fingers_count('Left')#子函数
        tips = [4, 8 , 12, 16, 20]
        tip_data = {4: 0, 8: 0, 12: 0, 16: 0, 20: 0}

        for tip in tips:
            ltp1 = position[hand_L].get(tip, None)  # 左手显示关节坐标
            ltp2 = position[hand_L].get(tip - 2, None)
            ltp_8 = position[hand_L].get(8, None)
            ltp_4 = position[hand_L].get(4, None)
            ltp_0 = position[hand_L].get(0, None)

            if ltp1 and ltp2:

                cv2.circle(img, (ltp_8[0], ltp_8[1]), 7, (255, 255, 0), cv2.FILLED)  # 食指
                #cv2.circle(img, (ltp_12[0], ltp_12[1]), 7, (0, 255, 255), cv2.FILLED)  # 中指
                cv2.line(img, (ltp_8[0], ltp_8[1]),(ltp_4[0], ltp_4[1]),  (255, 255, 255),3)  # 食指中指之间的线

                t_1=int ((ltp_4[0]+ltp_8[0])/2)
                t_2=int ((ltp_4[1]+ltp_8[1])/2)
                cv2.circle(img, (t_1, t_2), 7, (255, 0, 255), cv2.FILLED)  # 食指和中指中间的点


                print(ltp_4[1]-ltp_8[1])
                if (flag==1)and(ltp_4[1] - ltp_8[1]) <= 20:
                    ctr.click(pynput.mouse.Button.left, 2)
                    flag = 0
                if (flag==1) and (ltp_4[1]-ltp_8[1])<=50and(ltp_4[1]-ltp_8[1])>=30:
                    #pyautogui.click()
                    ctr.press(pynput.mouse.Button.left)
                    flag=0

                if (flag==0) and (ltp_4[1]-ltp_8[1])>50:
                    ctr.release(pynput.mouse.Button.left)
                    flag=1
                cv2.circle(img, (ltp1[0], ltp1[1]), 7, (255, 255, 0), cv2.FILLED)  # end,可以去掉
                cv2.circle(img, (ltp2[0], ltp2[1]), 5, (255, 100, 0), cv2.FILLED)  # end,可以去掉
                if tip == 4:
                    if ltp1[0] > ltp2[0]:  # ltp[i]，i=1的时候，是y坐标，i=0的时候，是x坐标
                        tip_data[tip] = 1
                    else:
                        tip_data[tip] = 0
                else:
                    if ltp1[1] > ltp2[1]:
                        tip_data[tip] = 0
                    else:
                        tip_data[tip] = 1
                if int(list(tip_data.values()).count(1)) > 2:
                    ctr.position = ((ltp_0[0] - 300) * 3, (ltp_0[1] - 400) * 3)




        # print(list(tip_data.values()).count(1))  # 把tip_data里面的1，提取出来，计算一共有几个
        #print('左手',list(tip_data.values()).count(1))
        #cv2.putText(img,str(list(tip_data.values()).count(1)),(100,100),cv2.FONT_HERSHEY_TRIPLEX,3,(255, 0, 0))


       #右手，暂时没有开发
       # cv2.line(img,ltp_lzhongzhi,(200,200),(0,255,0),3)#绿色，3个像素宽度
        hand_R = 'Right'
        # left_fingers =hand_detector.fingers_count('Left')#子函数
        tips = [4, 8, 12, 16, 20]
        tip_data = {4: 0, 8: 0, 12: 0, 16: 0, 20: 0}
        ltp_0_0 = 0
        ltp_4_0 = 0
        for tip in tips:
            ltp1 = position[hand_R].get(tip, None)  # 右手显示关节坐标
            ltp2 = position[hand_R].get(tip - 2, None)
            ltp_8 = position[hand_R].get(8, None)
            ltp_4 = position[hand_R].get(4, None)
            ltp_0 = position[hand_R].get(0, None)


            if ltp1 and ltp2:

                cv2.circle(img, (ltp_8[0], ltp_8[1]), 7, (0, 255, 255), cv2.FILLED)  # 食指
                # cv2.circle(img, (ltp_12[0], ltp_12[1]), 7, (0, 255, 255), cv2.FILLED)  # 中指
                cv2.line(img, (ltp_8[0], ltp_8[1]), (ltp_4[0], ltp_4[1]), (255, 255, 255), 3)  # 食指中指之间的线

                t_1 = int((ltp_4[0] + ltp_8[0]) / 2)
                t_2 = int((ltp_4[1] + ltp_8[1]) / 2)
                cv2.circle(img, (t_1, t_2), 7, (15, 180, 15), cv2.FILLED)  # 食指和中指中间的点

                print(ltp_4[1] - ltp_8[1])
                if (flag == 1) and (ltp_4[1] - ltp_8[1]) <= 20:
                    ctr.click(pynput.mouse.Button.left, 2)
                    flag = 0
                if (flag == 1) and (ltp_4[1] - ltp_8[1]) <= 50 and (ltp_4[1] - ltp_8[1]) >= 30:
                    # pyautogui.click()
                    ctr.press(pynput.mouse.Button.left)
                    flag = 0

                if (flag == 0) and (ltp_4[1] - ltp_8[1]) > 50:
                    ctr.release(pynput.mouse.Button.left)
                    flag = 1

                cv2.circle(img, (ltp1[0], ltp1[1]), 7, (0, 255, 255), cv2.FILLED)  # end,可以去掉
                cv2.circle(img, (ltp2[0], ltp2[1]), 5, (255, 0, 255), cv2.FILLED)  # end,可以去掉
                if tip == 4:
                    if ltp1[0] < ltp2[0]:  # ltp[i]，i=1的时候，是y坐标，i=0的时候，是x坐标
                        tip_data[tip] = 1
                    else:
                        tip_data[tip] = 0
                else:
                    if ltp1[1] > ltp2[1]:
                        tip_data[tip] = 0
                    else:
                        tip_data[tip] = 1
                if int(list(tip_data.values()).count(1)):
                    ctr.position = ((ltp_0[0] - 600) * 3, (ltp_0[1] - 400) * 3)

        # print(list(tip_data.values()).count(1))  # 把tip_data里面的1，提取出来，计算一共有几个
        #print('右手',list(tip_data.values()).count(1))
        #cv2.putText(img, str(list(tip_data.values()).count(1)), (450, 100), cv2.FONT_HERSHEY_TRIPLEX,3, (255, 0, 255))




        cv2.imshow('Video',img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

