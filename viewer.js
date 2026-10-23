import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const state=window.ROVER_DATA;const d=state.design;const test=state.mode==='drive';const host=document.getElementById('scene');
const scene=new THREE.Scene(); scene.background=new THREE.Color('#261c1c');scene.fog=new THREE.Fog('#261c1c',20,85);
const camera=new THREE.PerspectiveCamera(45,host.clientWidth/host.clientHeight,.05,200);camera.position.set(4.8,3.4,6.4);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setSize(host.clientWidth,host.clientHeight);renderer.shadowMap.enabled=true;host.appendChild(renderer.domElement);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;orbit.target.set(0,.65,0);orbit.maxPolarAngle=Math.PI*.48;
scene.add(new THREE.HemisphereLight('#ffe1c0','#4d2720',2.1));const sun=new THREE.DirectionalLight('#fff0dc',3);sun.position.set(-5,12,5);sun.castShadow=true;scene.add(sun);
const sand=new THREE.MeshStandardMaterial({color:0x92513a,roughness:1});const metal=new THREE.MeshStandardMaterial({color:0xb9bfc3,metalness:.62,roughness:.45});const dark=new THREE.MeshStandardMaterial({color:0x242a30,metalness:.2,roughness:.85});const accent=new THREE.MeshStandardMaterial({color:0xe5a66b,metalness:.4,roughness:.5});
const groundGeom=new THREE.PlaneGeometry(130,130,90,90);groundGeom.rotateX(-Math.PI/2);
const p=groundGeom.attributes.position;function groundHeight(x,z){return .095*Math.sin(x*.6)*Math.cos(z*.8)+.045*Math.sin(x*2.7+z*.7)+.035*Math.cos(z*3.1-x*.5)}
for(let i=0;i<p.count;i++){const x=p.getX(i),z=p.getZ(i);p.setY(i,groundHeight(x,z)-.16)}groundGeom.computeVertexNormals();let ground=new THREE.Mesh(groundGeom,sand);ground.receiveShadow=true;scene.add(ground);
const rng=(i)=>((Math.sin(i*12.9898)*43758.5453)%1+1)%1;
for(let i=0;i<100;i++){const x=(rng(i+5)-.5)*65,z=(rng(i+200)-.5)*65;if(Math.abs(x)<2&&Math.abs(z)<3)continue;let s=.08+rng(i+400)*.6;const rock=new THREE.Mesh(new THREE.DodecahedronGeometry(s,0),new THREE.MeshStandardMaterial({color:new THREE.Color().setHSL(.04,.27,.23+rng(i+66)*.13),roughness:1}));rock.position.set(x,groundHeight(x,z)-.08+s*.5,z);rock.rotation.set(rng(i)*2,rng(i+25)*3,rng(i+51));rock.castShadow=true;scene.add(rock)}
const rover=new THREE.Group();scene.add(rover);
function cube(w,h,l,mat,parent,x,y,z){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,l),mat);o.position.set(x,y,z);o.castShadow=true;parent.add(o);return o}
function bar(a,b,r=.025,mat=metal){const aa=new THREE.Vector3(...a),bb=new THREE.Vector3(...b);const delta=bb.clone().sub(aa);const o=new THREE.Mesh(new THREE.CylinderGeometry(r,r,delta.length(),8),mat);o.position.copy(aa.add(bb).multiplyScalar(.5));o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),delta.normalize());rover.add(o);return o}
const h=d.clearance+d.radius*.45;cube(d.body_width,.22,d.body_length,metal,rover,0,h+.20,0);cube(d.body_width*.82,.075,d.body_length*.9,accent,rover,0,h+.345,0);cube(d.body_width*.4,.22,.38,dark,rover,0,h+.48,-.15);bar([0,h+.55,-.25],[0,h+1.05,-.25],.038);cube(.30,.14,.16,dark,rover,0,h+1.1,-.25);
const wheels=[];for(const sx of [-1,1])for(const z of [-d.body_length*.48,0,d.body_length*.48]){
 const xx=sx*(d.body_width/2+d.width*.57+.075);const wy=d.radius-.03;
 const wheelGroup=new THREE.Group();wheelGroup.position.set(xx,wy,z);rover.add(wheelGroup);
 const tyre=new THREE.Mesh(new THREE.CylinderGeometry(d.radius,d.radius,d.width,32),dark);tyre.rotation.z=Math.PI/2;tyre.castShadow=true;wheelGroup.add(tyre);
 const hub=new THREE.Mesh(new THREE.CylinderGeometry(d.radius*.38,d.radius*.38,d.width+.015,18),accent);hub.rotation.z=Math.PI/2;wheelGroup.add(hub);
 for(let k=0;k<d.grousers;k++){const angle=k*2*Math.PI/d.grousers;const lug=cube(d.width*.92,.022,.055,metal,wheelGroup,0,0,0);lug.rotation.x=angle;lug.position.set(0,Math.cos(angle)*(d.radius+.015),Math.sin(angle)*(d.radius+.015))}
 bar([sx*d.body_width*.43,h+.12,z*.58],[xx,wy,z],.035);wheels.push(wheelGroup)
}
const clock=new THREE.Clock();let distance=0;let stopped=false;function animate(){requestAnimationFrame(animate);const dt=Math.min(clock.getDelta(),.05);if(test&&!stopped){const speed=state.success?.9:.56;const move=speed*dt;distance+=move;rover.position.z-=move;for(const w of wheels)w.rotation.x-=move/d.radius;rover.position.y=.018*Math.sin(distance*6);if(distance> (state.success?18:8)){stopped=true;document.getElementById('status').textContent=state.success?'● TEST COMPLETE · CHECK RESULTS':'● MOBILITY LIMIT REACHED · CHECK RESULTS'}}orbit.update();renderer.render(scene,camera)}animate();
if(test){camera.position.set(3.6,2.8,5.4);orbit.target.set(0,.8,-1)}
new ResizeObserver(()=>{const w=host.clientWidth,h=host.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h)}).observe(host);
