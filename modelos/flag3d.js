// bandeira dos EUA balançando (textura desenhada e deformada coluna a coluna, com luz e sombra)
function texturaEUA(W,H){const c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d');
 for(let i=0;i<13;i++){g.fillStyle=i%2?'#fff':'#C8202F';g.fillRect(0,i*H/13,W,H/13+1)}
 const cw=W*0.4,ch=H*7/13;g.fillStyle='#1F4AA8';g.fillRect(0,0,cw,ch);g.fillStyle='#fff';
 for(let r=0;r<9;r++){const n=r%2?5:6;for(let k=0;k<n;k++){const x=(k+(r%2?1:0.5))*cw/6.2+cw*0.02,y=(r+0.75)*ch/9.6;
  g.beginPath();for(let p=0;p<10;p++){const a=-Math.PI/2+p*Math.PI/5,rr=p%2?ch*0.018:ch*0.045;g.lineTo(x+rr*Math.cos(a),y+rr*Math.sin(a))}g.fill()}}
 return c}
function desenhaBandeira(cv,t){const W=cv.width,H=cv.height,g=cv.getContext('2d');g.clearRect(0,0,W,H);
 const fh=H/1.3,pad=(H-fh)/2,tex=texturaEUA(W,fh),amp=fh*0.11;
 for(let x=0;x<W;x++){const u=x/W,ph=u*2.2*Math.PI-t*2*Math.PI,dy=Math.sin(ph)*amp*(0.15+0.85*u),sl=Math.cos(ph);
  g.drawImage(tex,x,0,1,fh,x,pad+dy,1.2,fh);
  g.fillStyle=sl>0?`rgba(255,255,255,${0.18*sl*(0.3+u)})`:`rgba(0,0,0,${-0.32*sl*(0.3+u)})`;g.fillRect(x,pad+dy,1.2,fh)}
}
