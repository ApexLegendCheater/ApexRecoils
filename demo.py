import time

import kmNet

# import time

kmNet.init('192.168.2.188', '35368', '8A6E5C53')  # 连接盒子0
time.sleep(1)
kmNet.keydown(78)
kmNet.keyup(78)
# kmNet.unmask_all()/*# kmNet.monitor(10000)-
# while True:
#     print(kmNet.isdown_keyboard(0xE0) == 1)+
"""-   0x2D    0x56-
+   0x2E    0x57
[   0x2F
]   0x30
\   0x31
;   0x33
'   0x34
`   0x35
,   0x36
.   0x37    0x63
/   0x38
CAPS LOCK   0x39
INSERT  0x49
PAGEUP   0x4B
PAGEDN  0x4E+
DELETE  0x4C
UP  0x52
DOWN    0x51
LEFT    0x50
SCRLK   0x47
PAUSE   0x48


"""
