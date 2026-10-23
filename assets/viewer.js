import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const root=document.getElementById('app');
const d=window.ROVER_STATE.design;const ter=window.ROVER_STATE.terrain;
const scene=new THREE.Scene();scene.background=new THREE.Color('#1a202d');scene.fog=new THREE.FogExp2(0x362926,0.004);
const camera=new THREE.PerspectiveCamera(48,root.clientWidth/root.clientHeight,.02,1600);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setSize(root.clientWidth,root.clientHeight);renderer.shadowMap.enabled=true;renderer.outputColorSpace=THREE.SRGBColorSpace;root.appendChild(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xdbe7ff,0x8c3925,2.3));const sun=new THREE.DirectionalLight(0xffd9b5,3);sun.position.set(-8,14,8);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);scene.add(sun);
const ctrl=new OrbitControls(camera,renderer.domElement);ctrl.enableDamping=true;ctrl.dampingFactor=.07;ctrl.maxPolarAngle=Math.PI*.49;
let worldWidth=ter?85000:13;
function material(color,metalness=0,roughness=.8){return new THREE.MeshStandardMaterial({color,metalness,roughness});}
const rust=material('#92523a'),dark=material('#262f36'),metal=material('#8f9aa5',.65,.34),gold=material('#c8944f',.45,.45),wheelMat=material('#34383c',.22,.7);
function box(x,y,z,w,h,l,mat,parent=scene){const ob=new THREE.Mesh(new THREE.BoxGeometry(w,h,l),mat);ob.position.set(x,y,z);ob.castShadow=true;ob.receiveShadow=true;parent.add(ob);return ob;}
function link(A,B,rad=.036,mat=metal,parent=scene){const va=new THREE.Vector3(...A),vb=new THREE.Vector3(...B);let delta=vb.clone().sub(va);const part=new THREE.Mesh(new THREE.CylinderGeometry(rad,rad,delta.length(),10),mat);part.position.copy(va.add(vb).multiplyScalar(.5));part.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),delta.normalize());part.castShadow=true;parent.add(part);}
// Units of rover are metres, independent of the visual-only world scale of a MOLA patch.
function createRover(){const rover=new THREE.Group();scene.add(rover);const R=d.radius,W=d.width;
 const half=d.body_width/2,bodyY=R+d.clearance+.13;
 box(0,bodyY,0,d.body_width,.24,d.body_length,dark,rover);
 box(0,bodyY+.17,0,d.body_width*.8,.12,d.body_length*.72,gold,rover);
 // wheel axes along X; three axle positions each side
 const axle=[-d.body_length*.57,0,d.body_length*.57];
 for (const side of [-1,1]){
   const x=side*(half+W*.6+.08);
   for (let i=0;i<3;i++){
     const z=axle[i],center=[x,R,z];
     const wheel=new THREE.Mesh(new THREE.CylinderGeometry(R,R,W,40),wheelMat);
     wheel.rotation.z=Math.PI/2;wheel.position.set(...center);wheel.castShadow=true;wheel.receiveShadow=true;rover.add(wheel);
     const hub=new THREE.Mesh(new THREE.CylinderGeometry(R*.32,R*.32,W+.015,22),gold);hub.rotation.z=Math.PI/2;hub.position.set(...center);rover.add(hub);
     // grousers placed on circumference
     for(let j=0;j<d.grousers;j++){
       const a=j*2*Math.PI/d.grousers;
       const tread=box(x,R+(R+d.grouser_height*.36)*Math.sin(a),z+(R+d.grouser_height*.36)*Math.cos(a),W+.013,d.grouser_height*.7,R*.19,metal,rover);
       tread.rotation.x=-a;
     }
   }
   const base=[side*(half-.07),bodyY-.07,0];
   if(d.suspension==='Rocker-bogie'){
     const mid=[x,R+.22,0];const bogie=[x,R+.15,axle[1]*.5+axle[2]*.5];
     link(base,mid,.045,metal,rover);link(mid,[x,R,axle[0]],.048,metal,rover);link(mid,bogie,.05,metal,rover);
     link(bogie,[x,R,axle[1]],.042,metal,rover);link(bogie,[x,R,axle[2]],.042,metal,rover);
   } else {for(const z of axle)link([base[0],base[1],z],[x,R,z],.055,metal,rover);}
 }
 link([0,bodyY+.2,-.35],[0,bodyY+.65,-.35],.032,metal,rover);box(0,bodyY+.71,-.35,.31,.16,.19,dark,rover);
 const cog=new THREE.Mesh(new THREE.SphereGeometry(.07,15,12),new THREE.MeshBasicMaterial({color:0xff5555}));cog.position.set(0,d.cg,0);rover.add(cog);
 return rover;}
let rover=createRover();
const N=ter?ter.heights.length:90;
let world,heights;
if(ter){
  heights=ter.heights;let min=Infinity,max=-Infinity;for(const row of heights)for(const v of row){min=Math.min(min,v);max=Math.max(max,v)}
  // exaggerate for readability; slope test uses separate assumed ramp, NOT rescaled slope.
  let relief=Math.max(1,max-min);worldWidth=85000;
  const geometry=new THREE.PlaneGeometry(worldWidth,worldWidth,N-1,N-1);geometry.rotateX(-Math.PI/2);
  const positions=geometry.attributes.position;
  for(let i=0;i<N;i++)for(let j=0;j<N;j++){
    const p=i*N+j;positions.setY(p,(heights[i][j]-heights[Math.floor(N/2)][Math.floor(N/2)])*13);
  }
  geometry.computeVertexNormals();
  world=new THREE.Mesh(geometry,new THREE.MeshStandardMaterial({color:ter.real?0xae5c3a:0x946452,wireframe:false,flatShading:true,roughness:1,side:THREE.DoubleSide}));
  world.receiveShadow=true;scene.add(world);
  // Rover deliberately displayed at an illustrative scale so it's visible in the huge MOLA area.
  rover.scale.setScalar(1100);rover.position.y=40;
  camera.position.set(18000,13000,17500);ctrl.target.set(0,0,0);
}else{
  const geo=new THREE.PlaneGeometry(14,14,85,85);geo.rotateX(-Math.PI/2);let p=geo.attributes.position;
  for(let i=0;i<p.count;i++){let x=p.getX(i),z=p.getZ(i);const ridge=.18*Math.sin(x*1.4)*Math.cos(z*1.2);p.setY(i,-.04+ridge*Math.min(1,Math.max(0,(Math.hypot(x,z)-2)/2)));}
  geo.computeVertexNormals();world=new THREE.Mesh(geo,rust);world.receiveShadow=true;scene.add(world);
  camera.position.set(4.4,2.9,4.7);ctrl.target.set(0,.65,0);
}
ctrl.update();
const legend=document.createElement('div');legend.id='legend';legend.textContent='마우스 드래그: 회전  ·  휠: 확대 / 축소';root.appendChild(legend);
const label=document.createElement('div');label.id='label';label.innerHTML=ter?`<b>MARS TERRAIN / MOLA</b><br>${ter.source}<br>중심 ${ter.lat}°N ${ter.lon}°E / ±${ter.span_deg/2}°<br><small>지형 높이 13배 강조 · 로버 크기 과장</small>`:`<b>ROVER WORKSHOP</b><br>6-WHEEL CONFIGURATION<br>Wheel Ø ${(d.radius*2).toFixed(2)} m · ${d.mass} kg`;root.appendChild(label);
function resize(){const w=root.clientWidth,h=root.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h);}
window.addEventListener('resize',resize);
function render(){requestAnimationFrame(render);ctrl.update();renderer.render(scene,camera)}render();
