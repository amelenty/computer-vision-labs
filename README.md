# Computer Vision Labs
Practice tasks for the Computer Vision course at Kyiv Polytechnic Institute

## Lab 1: Дві вежі
### Порівняння дескрипторів
(це замість гуглдоки)

#### Ключові точки
Ключових точок згенеровано:

|        | SIFT | BRISK |
|--------|------|-------|
|Пепсі   |  160 |  295  |
|Ведмедик|  113 |  179  |

Бачимо, що BRISK їх генерує приблизно в півтора рази більше, ніж SIFT.

Це BRISK:

![Pepsi BRISK](lab1/output/ada/brisk/base_key_points_rich.jpg)

Це SIFT:

![Pepsi SIFT](lab1/output/ada/sift/base_key_points_rich.jpg)

Це BRISK:

![Teddy BRISK](lab1/output/vlada/brisk/base_key_points_rich.jpg)

Це SIFT:

![Teddy SIFT](lab1/output/vlada/sift/base_key_points_rich.jpg)

Незважаючи на більшу кількість ключових точок, BRISK в цьому плані видається надійнішим: точки зосереджено по краях, майже немає зайвих точок. Чого не скажеш про SIFT.

Загалом для бляшанки Пепсі обидва алгоритми закономірно вважають ключовими лого та підпис (BRISK — ще й металічні краї), а для ведмедика — кінцівки, морду та талію.

## Lab 0: A toe into madness

- Read an image from webcam
- Display the image
- Write the image to disk
- Load the image from disk
- Convert the image to grayscale
- Draw a line on the image
- Draw a rectangle on the image
- Display it again and write it to disk again (why not?)

### Example

![Colorful raccoon](lab0/example/img/img_from_webcam.png)

![Colorless raccoon](lab0/example/img/img_grayscale.png)
