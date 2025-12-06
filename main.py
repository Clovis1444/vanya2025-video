from manim import *
from datetime import datetime
import calendar

def get_calendar_table_month(year, month, h_day = None, scale_factor = 0.5):
        cal = calendar.monthcalendar(year, month)
        # Prepare data (replace 0 with empty string)
        table_data = []
        for week in cal:
            row = []
            for day in week:
                row.append(str(day) if day != 0 else "")
            table_data.append(row)

        h_index_prev = (2, 1)
        h_index = None
        for i in table_data:
            for j in i:
                if j == str(h_day):
                    h_index = (table_data.index(i) + 2, i.index(j) + 1)
                if h_index == None: h_index_prev = (table_data.index(i) + 2, i.index(j) + 1)

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        # Create table
        calendar_table = Table(
            table_data,
            col_labels=[Text(day, font_size=20) for day in days_of_week],
            include_outer_lines=True,
        ).scale(scale_factor)

        return calendar_table, h_index, h_index_prev


class main(MovingCameraScene):
    def construct(self):
        # Def camera frame
        cam_state = self.camera.frame.copy()

        # Init calendar
        cal_y, cal_m = (2025, 12)
        cal_title = Text("{} {}".format(calendar.month_name[cal_m], cal_y))
        cal, cal_h_i, cal_h_i_prev = get_calendar_table_month(cal_y, cal_m, 12)
        cal_title.next_to(cal, UP)
        cal_el = cal.get_cell(cal_h_i_prev)
        cal_el_new = cal.get_cell(cal_h_i)
        cal_g = Group(cal, cal_title, cal_el)

        # [Init]
        self.play(Create(cal), Write(cal_title))
        self.play(cal_el.animate.set_color(RED))
        self.wait(2)
        # [Move selector]
        self.play(cal_el.animate.move_to(cal_el_new))
        self.wait(2)
        # [Zoom in selector]
        self.play(self.camera.frame.animate.move_to(cal_el).scale(0.15))
        self.wait(2)
        # [Hide calendar]
        self.play(FadeOut(cal_g))
        # Restore camera
        self.camera.frame.become(cam_state)

        self.wait(1)

        # [Wonder text]
        text_wonder = Text("Hmmm...")
        text_ah = Text("Ah!")
        text_isee = Text("I see!")
        self.play(Write(text_wonder))
        self.wait(2)
        self.play(Transform(text_wonder, text_ah))
        self.wait(0.5)
        self.play(Transform(text_wonder, text_isee))
        self.wait(2)
        self.play(FadeOut(text_wonder))

        # [Emoji text]
        date1 = Text("12.12.2025")
        equal_text = Text("=")
        date1.next_to(equal_text, UP)
        emoji_p1 = ImageMobject("./resources/party-popper-emoji.png")
        emoji_p1.height = 1
        emoji_p1.next_to(equal_text, DOWN)
        emoji_p2 = emoji_p1.copy()
        emoji_p2.next_to(emoji_p1, LEFT)
        emoji_p3 = emoji_p1.copy()
        emoji_p3.next_to(emoji_p1, RIGHT)
        emoji_g = Group(date1, equal_text, emoji_p1, emoji_p2, emoji_p3)
        self.play(Write(date1), Write(equal_text))
        self.wait(2)
        self.play(FadeIn(emoji_p1), FadeIn(emoji_p2), FadeIn(emoji_p3), run_time = 2)
        self.wait(2)
        self.play(FadeOut(emoji_g))

        # [Wait text]
        wait_text = Text("But wait...")
        another_text = Text("There was another one!")
        self.play(Write(wait_text))
        self.wait(2)
        self.play(Transform(wait_text, another_text))
        self.wait(2)
        self.play(FadeOut(wait_text))
        self.wait(2)

        # [Date merge section]
        rect1 = RoundedRectangle()
        date1.move_to(rect1)
        date1_g = Group(rect1, date1)
        rect2 = RoundedRectangle()
        date2 = Text("12.12.2024")
        date2.move_to(rect2)
        date2_g = Group(rect2, date2)
        # creation
        self.play(Create(date1), Create(rect1))
        self.wait(0.5)
        self.play(date1_g.animate.shift(2.5*DOWN))
        self.play(Create(date2), Create(rect2))
        self.wait(0.5)
        self.play(date2_g.animate.shift(2.5*UP))
        self.wait(2)
        # merging
        rect3 = RoundedRectangle()
        date3 = Text("")
        date3.move_to(rect3)
        date3_g = Group(rect3, date3)
        self.play(Rotate(date1_g, angle=4*PI, about_point=ORIGIN), Rotate(date2_g, angle=4*PI, about_point=ORIGIN), run_time=3)
        self.play(date1_g.animate.shift(ORIGIN), date2_g.animate.shift(ORIGIN),
                  Transform(date1_g, date3_g), Transform(date2_g, date3_g),
                  Rotate(date1_g, angle=-4*PI, about_point=ORIGIN), Rotate(date2_g, angle=-4*PI, about_point=ORIGIN),
                  self.camera.frame.animate.move_to(ORIGIN).scale(0.15).set_run_time(50),
                  run_time=3)
        # Restore camera
        self.camera.frame.become(cam_state)
        self.remove(date1_g, date2_g, date3_g)
