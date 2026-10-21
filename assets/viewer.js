const scenes = new WeakMap();
const THREE_URL = 'https://esm.sh/three@0.164.1';
const ORBIT_URL = 'https://esm.sh/three@0.164.1/examples/jsm/controls/OrbitControls.js';

export default function({ parentElement, data }) {
  const viewport = parentElement.querySelector('#rover-viewport');
  if (!viewport) return;
  let state = scenes.get(viewport);
  if (state) {
    state.update(data?.params || {});
    return;
  }
  // Modules are cached by the browser. This avoids reinitializing WebGL on
  // routine Streamlit reruns; only parametric rover meshes are rebuilt.
  Promise.all([import(THREE_URL), import(ORBIT_URL)]).then(([THREE, orbit]) => {
    if (!viewport.isConnected) return;
    if (scenes.has(viewport)) { scenes.get(viewport).update(data?.params || {}); return; }
    const { OrbitControls } = orbit;
    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x172131, 16, 42);
    const camera = new THREE.PerspectiveCamera(43, 1, .04, 100);
    camera.position.set(3.9, 2.8, 4.7);
    const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio||1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    viewport.innerHTML = '';
    viewport.appendChild(renderer.domElement);
    const label = document.createElement('div'); label.className='viewer-label'; label.textContent='ROVER // DESIGN STUDIO'; viewport.appendChild(label);
    const corner = document.createElement('div'); corner.className='viewer-corner'; corner.textContent='MARS GRAVITY  ·  3.71 m/s²'; viewport.appendChild(corner);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; controls.dampingFactor=.06;
    controls.maxPolarAngle = Math.PI*.49; controls.minDistance=1.8;controls.maxDistance=13;
    controls.target.set(0,.5,0);
    scene.add(new THREE.HemisphereLight(0xbad5ff, 0x543021, 2.1));
    const sun = new THREE.DirectionalLight(0xffd9ae,3.2);
    sun.position.set(-3,8,5); sun.castShadow=true;
    sun.shadow.mapSize.set(1024,1024);
    scene.add(sun);
    const groundMat = new THREE.MeshStandardMaterial({color:0x906047,roughness:1});
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(70,70),groundMat);
    ground.rotation.x=-Math.PI/2;ground.position.y=-.016;ground.receiveShadow=true;scene.add(ground);
    const grid = new THREE.GridHelper(24,48,0x6a5144,0x664c3d);
    grid.position.y=.006;grid.material.opacity=.28;grid.material.transparent=true;scene.add(grid);
    const rover = new THREE.Group(); scene.add(rover);
    const mat=(color,metalness=.25,roughness=.65)=>new THREE.MeshStandardMaterial({color,metalness,roughness});
    const metal=mat(0xc8d4d9,.72,.32), dark=mat(0x232f3d,.52,.51), orange=mat(0xef9139,.32,.5), tire=mat(0x666d75,.56,.6), gold=mat(0xb4945c,.58,.43);
    function box(group,w,h,d,x,y,z,material){
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
      mesh.position.set(x,y,z);mesh.castShadow=true;mesh.receiveShadow=true;group.add(mesh);return mesh;
    }
    function link(group, a,b,r,material){
      const av=new THREE.Vector3(...a),bv=new THREE.Vector3(...b),delta=bv.clone().sub(av);
      const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r,r,delta.length(),10),material);
      mesh.position.copy(av).add(bv).multiplyScalar(.5);
      mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),delta.normalize());
      mesh.castShadow=true;group.add(mesh);
    }
    function wheel(group,x,y,z,p){
      const r=p.wheel_radius,w=p.wheel_width;
      const tireMesh=new THREE.Mesh(new THREE.CylinderGeometry(r,r,w,40), tire);
      tireMesh.rotation.x=Math.PI/2;tireMesh.position.set(x,y,z);tireMesh.castShadow=true;group.add(tireMesh);
      for(const sign of [-1,1]){
        const hub=new THREE.Mesh(new THREE.CylinderGeometry(r*.48,r*.48,.012,28),metal);
        hub.rotation.x=Math.PI/2;hub.position.set(x,y,z+sign*(w*.5+.006));group.add(hub);
        const axle=new THREE.Mesh(new THREE.CylinderGeometry(r*.16,r*.16,.025,20),orange);
        axle.rotation.x=Math.PI/2; axle.position.set(x,y,z+sign*(w*.5+.02));group.add(axle);
      }
      if(p.wheel_style !== '평활 휠') {
        const count=p.wheel_style==='격자형 휠'?24:p.grouser_count;
        const ht=p.wheel_style==='격자형 휠'?.012:p.grouser_height;
        for(let i=0;i<count;i++){
          const a=i*2*Math.PI/count;
          const cleat=new THREE.Mesh(new THREE.BoxGeometry(.022+ht,w*.94,.018+ht),gold);
          // Box geometry initially extends in y; rotate around wheel's z axis.
          cleat.position.set(x+(r+ht*.45)*Math.sin(a),y+(r+ht*.45)*Math.cos(a),z);
          cleat.rotation.z=-a;cleat.castShadow=true;group.add(cleat);
        }
      }
    }
    function clearGroup(g){
      while(g.children.length){const m=g.children[0];g.remove(m);m.traverse(o=>{if(o.geometry)o.geometry.dispose();});}
    }
    function update(p){
      if(!p.wheel_radius)return;
      clearGroup(rover);
      const r=p.wheel_radius;
      const lift=Math.max(p.clearance,r*.85);
      const top=lift+.23;
      const spread=p.body_width*.5+p.wheel_width*.53+.09;
      const front=p.body_length*.6,mid=0,back=-p.body_length*.6;
      box(rover,p.body_length,.26,p.body_width,0,top,0,orange);
      box(rover,p.body_length*.92,.07,p.body_width*.9,0,top+.165,0,metal);
      box(rover,p.body_length*.42,.14,p.body_width*.58,-.12,top+.27,0,dark);
      box(rover,.15,.13,.20,front*.55,top+.34,0,metal);
      link(rover,[front*.55,top+.35,0],[front*.55,top+.76,0],.034,dark);
      box(rover,.24,.17,.24,front*.55,top+.78,0,metal);
      for(const sign of [-1,1]){
        const z=sign*spread;
        [front,mid,back].forEach(x=>wheel(rover,x,r,z,p));
        if(p.suspension.startsWith('6륜 로커')){
          link(rover,[-.1,top-.12,sign*p.body_width*.47],[front,r,z],.044,metal);
          link(rover,[-.1,top-.12,sign*p.body_width*.47],[back*.54,r+.11,z],.047,metal);
          link(rover,[back*.54,r+.11,z],[mid,r,z],.035,dark);
          link(rover,[back*.54,r+.11,z],[back,r,z],.035,dark);
        }else{
          for(const x of [front,mid,back]) link(rover,[x*.9,top-.13,sign*p.body_width*.45],[x,r,z],.043,metal);
        }
      }
      // Visualization-only CG marker: does not imply a solved mass distribution.
      const cg = new THREE.Mesh(new THREE.SphereGeometry(.065,16,10),mat(0x48d4da,.1,.3));
      cg.position.set(0, p.clearance+.2+p.cg_extra,0);rover.add(cg);
    }
    const ro=new ResizeObserver(()=>{
      const w=Math.max(1,viewport.clientWidth),h=Math.max(1,viewport.clientHeight);
      renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
    });ro.observe(viewport);
    let alive=true;
    function tick(){ if(!alive)return;controls.update();renderer.render(scene,camera);requestAnimationFrame(tick); }
    tick();
    const current={update,dispose(){alive=false;ro.disconnect();controls.dispose();renderer.dispose();clearGroup(rover);}};
    scenes.set(viewport,current);
    update(data?.params||{});
  }).catch(error=>{viewport.innerHTML='<div class="viewport-loading">3D 라이브러리를 불러오지 못했습니다. 인터넷 연결 또는 브라우저 콘솔을 확인하세요.</div>'; console.error(error);});
}
