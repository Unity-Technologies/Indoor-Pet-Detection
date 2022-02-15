### Experiment Results



<table>
<tr>
  <td>Pre-training</td>
  <td>Fine tune(real data)</td>
  <td>AP</td>
  <td>Data generation time(mins)</td>
</tr>
<tr><td>ImageNet + no synthetic</td><td>1200</td><td>51.16</td><td>---</td></tr>
<tr><td>ImageNet + 5k synthetic</td><td>1200</td><td>57.18</td><td>33</td></tr>
<tr><td>ImageNet + 10k synthetic</td><td>1200</td><td>58.42</td><td>35</td></tr>
<tr><td>ImageNet + 40k synthetic</td><td>1200</td><td>63.03</td><td>50</td></tr>
<tr><td>ImageNet + 100k synthetic</td><td>1200</td><td>65.4</td><td>84</td></tr>
<tr><td>Scratch + no synthetic</td><td>1200</td><td>23.16</td><td>---</td></tr>
<tr><td>Scratch + 5k  synthetic</td><td>1200</td><td>36.16</td><td>33</td></tr>
<tr><td>Scratch + 10k synthetic</td><td>1200</td><td>36.97</td><td>35</td></tr>
<tr><td>Scratch + 40k synthetic</td><td>1200</td><td>47.3</td><td>50</td></tr>
<tr><td>Scratch + 100k synthetic</td><td>1200</td><td>53.78</td><td>84</td></tr>
</table>