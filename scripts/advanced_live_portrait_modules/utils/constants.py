from enum import Enum
from gradio_i18n import Translate, gettext as _


class ModelType(Enum):
    HUMAN = _("Human")
    ANIMAL = _("Animal")


class SamplePart(Enum):
    ONLY_EXPRESSION = _("OnlyExpression")
    ONLY_ROTATION = _("OnlyRotation")
    ONLY_MOUTH = _("OnlyMouth")
    ONLY_EYES = _("OnlyEyes")
    ALL = _("All")


REPO_MARKDOWN = """
## [sd-webui-AdvancedLivePortrait](https://https://github.com/jhj0517/sd-webui-AdvancedLivePortrait)
"""

GRADIO_CSS = """
#md_project a {
  color: black;
  text-decoration: none;
}
#md_project a:hover {
  text-decoration: underline;
}
"""