import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
 
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
 
detector = HandDetector(maxHands=1)
 
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
 
while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()
 
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]
 
    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw
 
    if startGame:
 
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
 
            if timer > 3:
                stateResult = True
                timer = 0
 
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0] or fingers == [1, 0, 0, 0, 0] or fingers == [1, 0, 0, 0, 1]:
                        playerMove = 1
                    elif fingers == [1, 1, 1, 1, 1] or fingers == [0, 1, 1, 1, 1]:
                        playerMove = 2
                    elif fingers == [0, 1, 1, 0, 0] or fingers == [1, 1, 1, 0, 0]:
                        playerMove = 3
                    else:
                        # player move is unknown
                        playerMove = 4
                    
                    # always beat the player if the player's move is known
                    if playerMove == 4 or None:
                        aiMove = random.randint(1, 3)
                    elif playerMove == 1:
                        aiMove = 2
                    elif playerMove == 2:
                        aiMove = 3
                    elif playerMove == 3:
                        aiMove = 1

                imgAI = cv2.imread(f'Resources/{aiMove}.png', cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                # Player Wins
                if playerMove == 4:
                    scores[1] += 1
                elif (playerMove == 1 and aiMove == 3) or \
                        (playerMove == 2 and aiMove == 1) or \
                        (playerMove == 3 and aiMove == 2):
                    scores[1] += 1

                # AI Wins
                elif (playerMove == 3 and aiMove == 1) or \
                        (playerMove == 1 and aiMove == 2) or \
                        (playerMove == 2 and aiMove == 3):
                    scores[0] += 1
                print(scores)
 
    imgBG[234:654, 795:1195] = imgScaled
 
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
 
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
 
    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgScaled)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    elif key == ord('q'):
        break
cv2.destroyAllWindows()
