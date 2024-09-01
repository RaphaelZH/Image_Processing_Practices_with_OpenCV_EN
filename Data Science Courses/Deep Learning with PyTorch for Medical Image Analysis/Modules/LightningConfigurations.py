from lightning.pytorch.callbacks import RichProgressBar
from lightning.pytorch.callbacks.progress.rich_progress import RichProgressBarTheme

from .CustomColors import *


class CustomProgressBar(RichProgressBar):
    def __init__(self):
        super().__init__()
        self.enable = True

        def custom_gradient_colors(colors, color_index):
            color_list = gradient_dark_generator(colors[color_index], 3)
            color_list.append(colors[color_index])
            color_list.remove(color_list[0])
            return color_list

        self.colors = calm_color_generator(2)
        self.color_group_1 = custom_gradient_colors(self.colors, 0)
        self.color_group_2 = custom_gradient_colors(self.colors, 1)

        self.theme = RichProgressBarTheme(
            description=self.color_group_1[2],
            progress_bar=self.color_group_1[0],
            progress_bar_finished=self.color_group_1[1],
            progress_bar_pulse=self.color_group_1[1],
            batch_progress=self.color_group_1[2],
            time=self.color_group_2[1],
            processing_speed=self.color_group_2[0],
            metrics=self.color_group_2[2],
            metrics_text_delimiter="\n",
            metrics_format="<.5f",
        )
        self.leave = (False,)

    def disable(self):
        self.enable = False

    def get_metrics(self, trainer, model):
        items = super().get_metrics(trainer, model)
        items.pop("v_num", None)
        return items
