(function(){
 function g(x,m,s){return Math.exp(-0.5*Math.pow((x-m)/s,2))}
 function noise(t,seed,amp){return amp*(0.52*Math.sin(t*5.17+seed*1.13)+0.28*Math.sin(t*11.73+seed*.47)+0.13*Math.sin(t*23.1+seed*2.01)+0.07*Math.sin(t*37.7+seed*.23))}
 function artifact(t,amp){return amp*(-g(t,.17,.026)+.72*g(t,.25,.035)-.18*g(t,.36,.055))}
 function motorUnit(t,onset,width,amp,skew){const x=t-onset;if(x<0)return 0;const envelope=1-Math.exp(-x/Math.max(.025,width*.08));return envelope*amp*(-g(x,width*.48,width*.23)+(.68+skew*.08)*g(x,width*1.12,width*.34)-.18*g(x,width*1.9,width*.46))}
 function cmap(t,o){let v=0;const n=o.units||18,spread=o.spread||.55;for(let i=0;i<n;i++){const q=i/(n-1),j=i===0?0:.10*(.5+.5*Math.sin((i+1)*7.31+(o.seed||1)));const onset=o.latency+spread*(q+j);const width=(o.unitWidth||1.05)*(1+.22*Math.sin(i*2.17));const weight=(1-.34*q)*(1+.12*Math.sin(i*4.7));v+=motorUnit(t,onset,width,(o.amplitude??1)*weight/n,o.skew||0)}return v*(o.gain||2.55)}
 function snap(t,o){const x=t-o.latency;if(x<0)return 0;const a=o.amplitude??10,w=o.width||.18,negPeak=w*1.2,cross=w*2.4,posPeak=w*3.3,end=w*5.0;if(x<=negPeak)return -.56*a*Math.sin(Math.PI*x/(2*negPeak));if(x<=cross)return -.56*a*Math.cos(Math.PI*(x-negPeak)/(2*(cross-negPeak)));if(x<=posPeak)return .44*a*Math.sin(Math.PI*(x-cross)/(2*(posPeak-cross)));if(x<=end)return .44*a*Math.cos(Math.PI*(x-posPeak)/(2*(end-posPeak)));return 0}
 function fwave(t,o){if(o.latency==null||t<o.latency)return 0;const x=t-o.latency,envelope=1-Math.exp(-x/.08);let v=0;const phases=o.phases||4;for(let i=0;i<phases;i++){const sign=i%2===0?-1:1;const center=.25+i*(o.spacing||.68)+.06*(1+Math.sin(i*3.1+(o.seed||1)));const width=.20+.05*i;v+=sign*(o.amplitude||.25)*(1-.13*i)*g(x,center,width)}return envelope*v}
 function hwave(t,o){if(!o.amplitude||t<o.latency)return 0;const x=t-o.latency,w=o.width||1.0,a=o.amplitude,envelope=1-Math.exp(-x/Math.max(.05,w*.08));return envelope*a*(-g(x,.25*w,.34*w)+.76*g(x,1.05*w,.44*w)-.22*g(x,2.15*w,.62*w))}
 window.NCSWave={g,noise,artifact,motorUnit,cmap,snap,fwave,hwave};
})();
