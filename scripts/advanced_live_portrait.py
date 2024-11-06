from scripts.advanced_live_portrait_modules.installation import *
install_sam()
from scripts.layer_divider_modules import sam2
from scripts.layer_divider_modules.ui_utils import *
from scripts.layer_divider_modules.html_constants import *
from scripts.layer_divider_modules.video_utils import get_frames_from_dir
from scripts.layer_divider_modules.default_hparams import DEFAULT_HPARAMS
from scripts.layer_divider_modules.model_downloader import DEFAULT_MODEL_TYPE
from scripts.layer_divider_modules.paths import (SAM2_CONFIGS_DIR, TEMP_DIR, TEMP_OUT_DIR, OUTPUT_DIR,
                                                 OUTPUT_FILTER_DIR, OUTPUT_PSD_DIR, init_paths)
from scripts.layer_divider_modules.constants import (AUTOMATIC_MODE, BOX_PROMPT_MODE, COLOR_FILTER, PIXELIZE_FILTER,
                                                     IMAGE_FILE_EXT, VIDEO_FILE_EXT, DEFAULT_COLOR, DEFAULT_PIXEL_SIZE)

import gradio as gr
from gradio_image_prompter import ImagePrompter
import os
import yaml
from typing import Dict, Optional

from advanced_live_portrait_modules import scripts, script_callbacks

sam_inf = sam2.SamInference()


class App:
    def __init__(self,
                 args=None):
        self.args = args
        self.app = gr.Blocks(css=GRADIO_CSS)
        self.i18n = Translate(I18N_YAML_PATH)
        self.inferencer = LivePortraitInferencer(
            model_dir=args.model_dir if args else MODELS_DIR,
            output_dir=args.output_dir if args else OUTPUTS_DIR
        )

    @staticmethod
    def create_parameters():
        return [
            gr.Dropdown(label=_("Model Type"), visible=False, interactive=False,
                        choices=[item.value for item in ModelType], value=ModelType.HUMAN.value),
            gr.Slider(label=_("Rotate Pitch"), minimum=-20, maximum=20, step=0.5, value=0),
            gr.Slider(label=_("Rotate Yaw"), minimum=-20, maximum=20, step=0.5, value=0),
            gr.Slider(label=_("Rotate Roll"), minimum=-20, maximum=20, step=0.5, value=0),
            gr.Slider(label=_("Blink"), minimum=-20, maximum=20, step=0.5, value=0),
            gr.Slider(label=_("Eyebrow"), minimum=-20, maximum=20, step=0.5, value=0),
            gr.Slider(label=_("Wink"), minimum=0, maximum=25, step=0.5, value=0),
            gr.Slider(label=_("Pupil X"), minimum=-20, maximum=20, step=0.5, value=0),
            gr.Slider(label=_("Pupil Y"), minimum=-20, maximum=20, step=0.5, value=0),
            gr.Slider(label=_("AAA"), minimum=-30, maximum=120, step=1, value=0),
            gr.Slider(label=_("EEE"), minimum=-20, maximum=20, step=0.2, value=0),
            gr.Slider(label=_("WOO"), minimum=-20, maximum=20, step=0.2, value=0),
            gr.Slider(label=_("Smile"), minimum=-2.0, maximum=2.0, step=0.01, value=0),
            gr.Slider(label=_("Source Ratio"), minimum=0, maximum=1, step=0.01, value=1),
            gr.Slider(label=_("Sample Ratio"), minimum=-0.2, maximum=1.2, step=0.01, value=1),
            gr.Dropdown(label=_("Sample Parts"),
                        choices=[part.value for part in SamplePart], value=SamplePart.ALL.value),
            gr.Slider(label=_("Crop Factor"), minimum=1.5, maximum=2.5, step=0.1, value=1.7)
        ]

    def launch(self):
        with self.app:
            with self.i18n:
                gr.Markdown(REPO_MARKDOWN, elem_id="md_project")

                with gr.Row():
                    with gr.Column():
                        img_ref = gr.Image(label=_("Reference Image"))
                with gr.Row():
                    btn_gen = gr.Button("GENERATE", visible=False)
                with gr.Row(equal_height=True):
                    with gr.Column(scale=9):
                        img_out = gr.Image(label=_("Output Image"))
                    with gr.Column(scale=1):
                        expression_parameters = self.create_parameters()
                        btn_openfolder = gr.Button('📂')
                        with gr.Accordion("Opt in features", visible=False):
                            img_sample = gr.Image()
                            img_motion_link = gr.Image()
                            tb_exp = gr.Textbox()

                params = expression_parameters + [img_ref]
                opt_in_features_params = [img_sample, img_motion_link, tb_exp]

                gr.on(
                    triggers=[param.change for param in params],
                    fn=self.inferencer.edit_expression,
                    inputs=params + opt_in_features_params,
                    outputs=img_out
                )

                btn_openfolder.click(
                    fn=lambda: self.open_folder(self.args.output_dir), inputs=None, outputs=None
                )

                btn_gen.click(self.inferencer.edit_expression,
                              inputs=params + opt_in_features_params,
                              outputs=img_out)

            gradio_launch_args = {
                "inbrowser": self.args.inbrowser,
                "share": self.args.share,
                "server_name": self.args.server_name,
                "server_port": self.args.server_port,
                "root_path": self.args.root_path,
                "auth": (self.args.username, self.args.password) if self.args.username and self.args.password else None,
            }
            self.app.queue().launch(**gradio_launch_args)

    @staticmethod
    def open_folder(folder_path: str):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            print(f"The directory path {folder_path} has newly created.")
        os.system(f"start {folder_path}")

def add_tab():
    global sam_inf

    init_paths()


    return [(block_tab, "AdvancedLivePortrait", "advanced_live_portrait")]


def on_unload():
    global sam_inf
    sam_inf = None


script_callbacks.on_ui_tabs(add_tab)
script_callbacks.on_script_unloaded(on_unload)
