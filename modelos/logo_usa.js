// monta o logo Portal USA (linhas da mesma largura; bandeira na altura do "l")
function montaLogos(t){document.querySelectorAll('.lg2').forEach(el=>{const p=el.querySelector('.p'),r2=el.querySelector('.r2'),cv=el.querySelector('canvas'),r1=el.querySelector('.r1');
 r1.style.width=r2.getBoundingClientRect().width+'px';const fs=parseFloat(getComputedStyle(el).fontSize),m=document.createElement('canvas').getContext('2d');m.font='700 '+fs+'px Poppins';
 const asc=m.measureText('l').actualBoundingBoxAscent,pr=p.getBoundingClientRect(),rr=r1.getBoundingClientRect(),h=asc*1.3,pad=(h-asc)/2,base=pr.top-rr.top+0.80*fs;
 cv.style.left=(pr.right-rr.left+0.12*fs)+'px';cv.style.top=(base-asc-pad)+'px';cv.style.height=h+'px';const w=r2.getBoundingClientRect().width-(pr.right-rr.left+0.12*fs);cv.style.width=w+'px';
 cv.width=Math.round(w*2);cv.height=Math.round(h*2);desenhaBandeira(cv,t)})}
