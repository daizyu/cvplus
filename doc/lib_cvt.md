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
from PIL
from cvplus import cvt
pil_img = Image.open('1.png')
img = cvt.from_pil(pil_img)
cvt.imwrite('2.png',img) 
```

## to_html_img_tag  
Convert image to HTML img tag (Base64 encoding)   
``` python
from cvplus import cvt
img = cvt.imread("test.jpg")
img_tag = cvt.to_html_img_tag(img ,{'alt': 'test alt', 'title': 'test title'})
with codecs.open("test.html", "w+", "utf8") as f:
    f.write(f"<html>{img_tag}</html>")
```

tag  
```
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAJ8CAIAAADh/4cWAAAgAElEQVR4AaTBAZZkx5Vl13Oe/R9B
               :
               :
XHEdFRKYWYSPiIiPwHwf2saqiIOfK/kAAAAAElFTkSuQmCC
" alt="test alt" title="test title">
```
