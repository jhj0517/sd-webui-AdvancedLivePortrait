# AdvancedLivePortrait-WebUI

Extension for [ComfyUI-AdvancedLivePortrait](https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait) in [sd-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) (Works with forge as well). 
<br>You can edit the facial expression from the image.

https://github.com/user-attachments/assets/37a3fded-6e11-48d8-b072-b54438e4bd39

### Dedicated WebUI
If you want to try it in a dedicated webui rather than as an extension:
- https://github.com/jhj0517/AdvancedLivePortrait-WebUI

# Installation
1. Place this extension into `your-webui-path/extension`
```
git clone https://github.com/jhj0517/sd-webui-AdvancedLivePortrait.git
```

## ❤️ Citation and Thanks 
1. LivePortrait paper comes from
```bibtex
@article{guo2024liveportrait,
  title   = {LivePortrait: Efficient Portrait Animation with Stitching and Retargeting Control},
  author  = {Guo, Jianzhu and Zhang, Dingyun and Liu, Xiaoqiang and Zhong, Zhizhou and Zhang, Yuan and Wan, Pengfei and Zhang, Di},
  journal = {arXiv preprint arXiv:2407.03168},
  year    = {2024}
}
```
2. The models are safetensors that have been converted by kijai. : https://github.com/kijai/ComfyUI-LivePortraitKJ
3. [ultralytics](https://github.com/ultralytics/ultralytics) is used to detect the face.
4. This started from [ComfyUI-AdvancedLivePortrait](https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait), various facial expressions like AAA, EEE, Eyebrow, Wink are found by PowerHouseMan.



