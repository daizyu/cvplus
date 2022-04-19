# CVT module  

## imnew
Create new image for OpenCV style  
``` python
from cvplus import cvt
img = cvt.imnew(100,200) 
```  

## imwrite  
Save image file with non ascii folder name for OpenCV style.  
``` python
from cvplus import cvt

img = cvt.imnew(100,200) 
filepath = r'c:\temp\画像ファイル.jpg'  
cvt.imwrite(filepath,img) 
```  

## imread  
Open image with non ascii folder name for OpenCV style.  
``` python
from cvplus import cvt
filepath = r'c:\temp\画像ファイル.jpg'  
img = cvt.imread(filepath) 
```

## to_pil  
Convert from OpenCV Image to Pil Image.  
``` python
from cvplus import cvt
img = cvt.imnew(100,100)
pil_img = cvt.to_pil(img)
```
## from_pil  
Convert from Pil Image to OpenCV Image.  
``` python
from PIL import Image                                            
from cvplus import cvt
pil_img = Image.open('1.png')
img = cvt.from_pil(pil_img)
cvt.imwrite('2.png', img) 
```  

## to_pil  
Convert to PulImage from OpenCV Image.  
``` python
from PIL import Image                                            
from cvplus import cvt
pil_img = Image.open('1.png')
img = cvt.from_pil(pil_img)
cvt.imwrite('2.png',img) 
```
