from manim import *

class CreateCircle(Scene):
    def construct(self):
        # Create the shape of a heart using a Polygon
        circle_left = Circle(radius=1.5, color=RED).shift(LEFT)
        circle_right = Circle(radius=1.5, color=RED).shift(RIGHT)
        # Fill circle_left and circle_right with RED color
        circle_left.set_fill(RED, opacity=1)
        circle_right.set_fill(RED, opacity=1)
        triangle = Polygon([-2, -1, 0], [2, -1, 0], [0, -3, 0], color=RED).set_fill(RED, opacity=1)

        # Group the shapes to form the heart
        heart = VGroup(circle_left, circle_right, triangle)
        

        heart.move_to(ORIGIN)
        heart.scale(0.1)
        # Animate the heart
        self.play(GrowFromCenter(heart))
        self.wait(1)

        # Display "Made with heart using Manim"
        text_left = Text("Made with").next_to(heart, LEFT)
        text_right = Text("using Manim").next_to(heart, RIGHT)
        self.play(Write(text_left), Write(text_right))