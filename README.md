<h1>Description</h1>
Addon for Blender 4.2 following the concept in this video<br>


https://youtu.be/ZdxoIAefQx8?si=CtVG0gqtAaXue8u1

![Screenshot 2567-11-06 at 21 30 08](https://github.com/user-attachments/assets/3f100b1e-e08c-4947-8729-5f43db6c0a58)


It helps highlight the strokes in the previous keyframe by the order they are drawn,<br>
so that subsequent drawing can follow the same order,<br>
thus making the interpolation tool work correctly.<br>


Clicking the highlight button will cycle through strokes in the current layer.<br>


Don't forget to 'Revert All' to revert everything back before moving on.<br>

<h2>Showing Stroke Direction</h2>

To also show the stroke direction,<br>
you need to create a 'highlight' stroke material with<br>


Line Type = Squares<br>
Style = Texture<br>


and add a small texture file (triangle.png in this repo)<br>
this texture need to rotate 90 degrees.<br>

![Screenshot 2567-11-06 at 21 41 58](https://github.com/user-attachments/assets/29c11395-d465-4fb6-a435-344996c0a228)


<h2>Installation</h2>

Download and extract in your addon folder.<br>
Enable the addon in Blender preferences.<br>

<h2>Disclaimer</h2>
This addon has not been tested with other version of Blender.
It has not been thoroughly tested in 4.2, neither.

* This addon was developed within a few hours with help from ChatGPT and DeepSeek *
