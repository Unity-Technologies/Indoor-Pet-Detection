### Experiment Results



<table>
<tr>
  <td>Pre-training</td>
  <td>Fine tune(real data)</td>
  <td>AP</td>
  <td>Data generation time(mins)</td>
</tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_0k_synthetic.pth">ImageNet + no synthetic</a>
  </td><td>1200</td><td>51.16</td><td>---</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_5k_synthetic.pth">ImageNet + 5k synthetic </a>
    </td><td>1200</td><td>57.18</td><td>33</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_10k_synthetic.pth">ImageNet + 10k synthetic </a>
  </td><td>1200</td><td>58.42</td><td>35</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_40k_synthetic.pth">ImageNet + 40k synthetic </a>
  </td><td>1200</td><td>63.03</td><td>50</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_100k_synthetic.pth">ImageNet + 100k synthetic </a>
  </td><td>1200</td><td>65.4</td><td>84</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_0k.pth">Scratch + no synthetic </a>
  </td><td>1200</td><td>23.16</td><td>---</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_5k.pth">Scratch + 5k  synthetic </a>
  </td><td>1200</td><td>36.16</td><td>33</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_10k.pth">Scratch + 10k synthetic </a>
  </td><td>1200</td><td>36.97</td><td>35</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_40k.pth">Scratch + 40k synthetic </a>
  </td><td>1200</td><td>47.3</td><td>50</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_100k.pth">Scratch + 100k synthetic </a>
  </td><td>1200</td><td>53.78</td><td>84</td></tr>
</table>
