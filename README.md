Addon for Blender 4.2 following the concept in this video

https://youtu.be/ZdxoIAefQx8?si=CtVG0gqtAaXue8u1

It helps highlight the strokes in the previous keyframe by the order they are drawn,
so that subsequent drawing can follow the same order,
thus making the interpolation tool work correctly.

clicking the highlight button will cycle through strokes in the current layer.

Don't forget to 'Revert All' to revert everything back before moving on.

To also show the stroke direction,
you need to create a 'highight' stroke material with

Line Type = Squares
Style = Texture

and add a small texture file (example : triangle.png in this repo)
this texture need to rotate 90 degrees.
