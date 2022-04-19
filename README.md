# CV Plus

## Provided tools
- Libraries
- Color range selector  
- Camera capture

## How to install

1. Install python  
  minimum reqirement Python 3.8 

2. Upgrade pip  
  **!!!important!!!**  
  When upgrade is not done , the dependented library opencv-python installation nerver finish.  
  Windows  
  ```python -m pip install --upgrade pip```  
  Mac / Linux  
  ```python3 -m pip install --upgrade pip```  

3. Install CVPlus   
3-1. From pypi  
  Windows  
  ```python -m pip install cvplus```  
  Mac / Linux  
  ```python3 -m pip install cvplus```  
3-2. From github  
  Windows  
  ```python -m pip install git+https://github.com/daizyu/cvplus```  
  Mac / Linux  
  ```python3 -m pip install git+https://github.com/daizyu/cvplus``` 

## Libraries  
1.1 Create new image for OpenCV style  
```
from cvplus import cvt
img = cvt.imnew(100,200) 
```

1.2 Save image file with non ascii folder name for OpenCV style.  
```
from cvplus import cvt

img = cvt.imnew(100,200) 
filepath = r'c:\temp\画像ファイル.jpg'  
cvt.imwrite(filepath,img) 
```

1.3 Open image with non ascii folder name for OpenCV style.  
```
from cvplus import cvt
filepath = r'c:\temp\画像ファイル.jpg'  
img = cvt.imread(filepath) 
```


## Gui Tools

[Color range selector](./doc/gui_color_range_selector.md "Color range selector")


### Camera capture

Get picture from camera.  

#### How to use...

Windows  
```python -m cvplus.gui.camera_capture --output-folder c:\image-folder --camera-id 0```  
Mac / Linux  
```python3 -m cvplus.gui.camera_capture --output-folder ~/image-folder --camera-id 0```  

#### Key assignment  

```esc``` : close application  
```s```   : save image file

#### Recommended option  

```--extention...``` : image file extention (.jpg / .png).

```--cap_prop_...``` : camera option.

## img conv (Command line tool)  
Windows  
```
python -m cvplus.cli.imgconv --input-folder c:\In-Images --output-folder c:\Out-Images --recursive True --fixed-height 100 --extension .jpg
```  
Mac / Linux  
```
python3 -m cvplus.cli.imgconv --input-folder ~/In-Images --output-folder ~/Out-Images --recursive True --fixed-height 100 --extension .jpg
``` 

