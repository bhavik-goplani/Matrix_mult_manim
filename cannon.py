from manim import *

class CannonScene(Scene):
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        self.A = self.createSquareMatrix(3, "A", BLUE, 0.8)
        self.B = self.createSquareMatrix(3, "B", GREEN, 0.8)
        self.P = self.createSquareMatrix(3, "P", RED, 0.8)

    def construct(self):
        title = Text("Cannon's Algorithm", color=WHITE).to_edge(UP + LEFT).scale(0.8)

        # show the matrices on screen
        self.play(Write(title))
        self.animateInitial()

        self.wait(2)

    def createSquareMatrix(self, size, label, color, scale):
        matrix = VGroup()
        for x in range(size):
            row = VGroup()
            for y in range(size):
                cell = Square(side_length=1*scale, fill_color=color, fill_opacity=0.5) 
                cell_label = MathTex(label + "_{" + str(x) + str(y) + "}", color=WHITE).scale(cell.get_height())
                cell.add(cell_label)
                row.add(cell)
            matrix.add(row.arrange(RIGHT, buff=0.1*scale))
        matrix.arrange(DOWN, buff=0.1*scale)  
        return matrix
    
    def animateInitial(self):
        A = self.A
        B = self.B
        P = self.P
        # position the matrices on the screen
        A.move_to(LEFT * 4)
        B.move_to(ORIGIN)
        P.move_to(RIGHT * 4)

        A_text = Text("A (3x3)", color=WHITE).next_to(A, UP).scale(0.5)
        B_text = Text("B (3x3)", color=WHITE).next_to(B, UP).scale(0.5)
        P_text = Text("P (3x3)", color=WHITE).next_to(P, UP).scale(0.5)

        steps_text = MathTex(r"\text{Algorithm works in } \sqrt{P} \text{ steps} = \sqrt{9} = 3 \text{ steps}", color=WHITE).next_to(B, DOWN, buff=1).scale(0.8)

        self.play(Create(A), Create(B), Create(P))
        self.play(Write(A_text), Write(B_text), Write(P_text))
        self.play(Write(steps_text))
        self.wait(2)

        self.play(FadeOut(A, B, P))
        self.play(FadeOut(A_text, B_text, P_text))
        self.play(FadeOut(steps_text))


        pass

    def animateStep0(self):
        pass

