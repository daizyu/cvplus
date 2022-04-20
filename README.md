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
[cvt](./doc/lib_cvt.md "CVT Module")  
- cvt.imnew  
Create nwe OpenCV image
- cvt.imread  
Read OpenCV image (non-ascii code enable)
- cvt.imwrite  
Write OpenCV image (non-ascii code enable)
- cvt.from_pil  
Convert image format from PIL image to OpenCV image
- cvt.to_pil  
Convert image format from OpenCV image to PIL image

[draw](./doc/lib_draw.md "DRAW Module")

## Gui Tools

[Color range selector](./doc/gui_color_range_selector.md "Color range selector")  

[Camera capture](./doc/gui_color_range_selector.md "Camera capture")  


## Cui Tool  

[Image converter](./doc/cli_img_conv.md "Image converter")

