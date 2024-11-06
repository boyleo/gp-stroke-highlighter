Addon for Blender 4.2 following the concept in this video

https://youtu.be/ZdxoIAefQx8?si=CtVG0gqtAaXue8u1

![Screenshot 2567-11-06 at 21 30 08](https://github.com/user-attachments/assets/3f100b1e-e08c-4947-8729-5f43db6c0a58)


It helps highlight the strokes in the previous keyframe by the order they are drawn,
so that subsequent drawing can follow the same order,
thus making the interpolation tool work correctly.


Clicking the highlight button will cycle through strokes in the current layer.


Don't forget to 'Revert All' to revert everything back before moving on.


To also show the stroke direction,
you need to create a 'highlight' stroke material with


Line Type = Squares

Style = Texture


and add a small texture file (example : triangle.png in this repo)
this texture need to rotate 90 degrees.


* This addon is developed within a few hours with help from ChatGPT and DeepSeek *
