# DRAW module  

## arrow
Draw arrow    
``` python
from cvplus import cvt, draw
img = cvt.imnew(200,80)
draw.arrow(img,(20,10),(180,70),(255,255,0),2)
cvt.imwrite('sample.jpg', img)
```  
![lib draw arrow](img/lib_draw_001.jpg)
