from scripts.installation import install
install()

import sys
import subprocess
import argparse
import gradio as gr
from gradio_i18n import Translate, gettext as _

from scripts.advanced_live_portrait_modules.live_portrait.live_portrait_inferencer import LivePortraitInferencer
from scripts.advanced_live_portrait_modules.utils.paths import *
from scripts.advanced_live_portrait_modules.utils.helper import str2bool
from scripts.advanced_live_portrait_modules.utils.constants import *
from modules import scripts, script_callbacks




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

    def create_block(self):
        with self.app as block:
            with self.i18n:
                gr.Markdown(REPO_MARKDOWN, elem_id="md_project")

                with gr.Row():
                    with gr.Column():
                        img_ref = gr.Image(label=_("Reference Image"), height=500)
                with gr.Row():
                    btn_gen = gr.Button("GENERATE", visible=False)
                with gr.Row(equal_height=True):
                    with gr.Column(scale=9):
                        img_out = gr.Image(label=_("Output Image"), height=500)
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
                    outputs=img_out,
                    show_progress="minimal"
                )

                btn_openfolder.click(
                    fn=lambda: self.open_folder(OUTPUTS_DIR), inputs=None, outputs=None
                )

                btn_gen.click(self.inferencer.edit_expression,
                              inputs=params + opt_in_features_params,
                              outputs=img_out)
        return block

    @staticmethod
    def open_folder(folder_path: str):
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
                print(f"The directory path {folder_path} has newly created.")

            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            elif os.name == 'posix':  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.Popen(['open', folder_path])
                elif sys.platform.startswith('linux'):  # Linux
                    subprocess.Popen(['xdg-open', folder_path])
            else:
                os.system(f"start {folder_path}")
        except Exception as e:
            print("Failed to open directory")
            raise

def add_tab():

    app = App()
    block_tab = app.create_block()

    return [(block_tab, "AdvancedLivePortrait", "advanced_live_portrait")]


script_callbacks.on_ui_tabs(add_tab)
