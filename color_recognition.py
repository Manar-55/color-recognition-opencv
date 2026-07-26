import cv2
import numpy as np

image = cv2.imread("colors.jpg")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

colors = {
    "Orange":   ([8, 100, 150], [18, 255, 255], (0, 140, 255)),
    "Gold":     ([18, 150, 150], [28, 255, 255], (0, 215, 255)),
    "Maroon":   ([165, 100, 60], [179, 255, 180], (50, 0, 130)),
    "Olive":    ([25, 100, 100], [40, 255, 200], (0, 128, 128)),
    "Teal":     ([85, 80, 120], [100, 200, 220], (180, 130, 70)),
    "Blue":     ([100, 80, 120], [115, 200, 220], (180, 70, 0)),
    "Pink":     ([160, 30, 180], [175, 90, 255], (200, 180, 240)),
    "Rose":     ([165, 60, 130], [178, 150, 220], (120, 100, 200)),
    "Lavender": ([120, 30, 150], [140, 90, 230], (220, 160, 180)),
}


def draw_rounded_rect(img, top_left, bottom_right, color, radius=4, thickness=-1):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)


for color_name, (lower, upper, box_color) in colors.items():
    lower = np.array(lower)
    upper = np.array(upper)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), box_color, 2)

            text = color_name
            font_scale = 0.5
            thickness_text = 1
            (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness_text)

            pad_x = 6
            pad_y = 4
            label_x1, label_y1 = x + 6, y + 6
            label_x2, label_y2 = label_x1 + text_w + pad_x * 2, label_y1 + text_h + pad_y * 2

            draw_rounded_rect(image, (label_x1, label_y1), (label_x2, label_y2),
                               (255, 255, 255), radius=4, thickness=-1)

            cv2.putText(image, text, (label_x1 + pad_x, label_y2 - pad_y),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, box_color, thickness_text)

cv2.imshow("Color Recognition", image)
cv2.waitKey(0)
cv2.destroyAllWindows()