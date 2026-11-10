// "E se o Sol sumisse?": a luz e a gravidade andam juntas, na mesma velocidade.
// - antes do Sol sumir: um feixe de luz do Sol até a Terra;
// - depois: a última luz (um ponto) sai do lugar vazio e o feixe encolhe atrás dela até a Terra;
// - a gravidade é um anel no plano da órbita que cresce exatamente com a última luz;
// - no trecho de "filme" (a Terra disparando) e no rebobinar, a luz e o anel ficam parados;
// - quando a última luz passa, a Terra apaga; quando a fala diz "apaga", a Lua apaga.
//   O estilo pinta o lado da noite de azul e não tem como desligar a luz, então uma esfera
//   preta semitransparente cobre cada corpo (o gelo e a água ficam por fora dela).
import { linhaGorda } from '../../linhas.js';

export function montar({ THREE, scene, W, H, OBJ, tempo, posDe, registrar, PLANO }) {
  const F = PLANO.frente;
  const S = new THREE.Vector3(0, 0, 0);
  // a última luz chega na superfície da Terra voltada para o lugar do Sol (não no centro, senão some dentro dela)
  const rTerra = (OBJ.terra && OBJ.terra.raio) || 1;
  const C = new THREE.Vector3(...F.chegada).multiplyScalar(1 - rTerra / F.R);
  const RC = C.length();
  const tS = tempo(F.t.some), tF0 = tempo(F.t.voo), tR1 = tempo(F.t.volta), tG = tempo(F.t.grav), tC = tempo(F.t.chega), tL = tempo(F.t.lua);
  const pausa = tR1 - tF0;
  const efetivo = (t) => (t < tF0 ? t : t < tR1 ? tF0 : t - pausa);
  const clamp = (x) => Math.min(1, Math.max(0, x));
  const suave = (x) => x * x * (3 - 2 * x);
  const fracao = (t) => clamp((efetivo(t) - tS) / (tC - pausa - tS));

  // brilho redondo (sprite) feito aqui mesmo
  const cv = document.createElement('canvas'); cv.width = cv.height = 128;
  const g = cv.getContext('2d'); const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,240,200,0.85)'); gr.addColorStop(1, 'rgba(255,220,150,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  const tex = new THREE.CanvasTexture(cv);
  const ponto = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, color: new THREE.Color('#FFE7A3'), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
  scene.add(ponto);

  const feixe = linhaGorda([new THREE.Vector3(), new THREE.Vector3(0, 0.001, 0)], { cor: '#FFE7A3', largura: 7, opacidade: 0.38, aditiva: true, W, H });
  scene.add(feixe);

  const anelMat = new THREE.MeshBasicMaterial({ color: new THREE.Color('#9FD0FF'), transparent: true, opacity: 0.8, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false });
  const anel = new THREE.Mesh(new THREE.RingGeometry(0.993, 1.007, 256), anelMat);
  const brumaMat = anelMat.clone(); brumaMat.opacity = 0.22;
  const bruma = new THREE.Mesh(new THREE.RingGeometry(0.972, 1.0, 256), brumaMat);
  for (const m of [anel, bruma]) { m.rotation.x = -Math.PI / 2; scene.add(m); }

  const sombra = (nome) => {
    const mat = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0, depthWrite: false });
    const m = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 32), mat); m.visible = false; scene.add(m);
    return { m, mat, r: (OBJ[nome] && OBJ[nome].raio) || 1 };
  };
  const sombraTerra = sombra('terra'), sombraLua = sombra('lua');
  const apagar = (s, nome, t, t0, forca) => {
    const k = forca * suave(clamp((t - t0) / 0.5));
    s.m.visible = k > 0.01;
    if (s.m.visible) { s.m.position.copy(posDe(nome, t)); s.m.scale.setScalar(s.r * 1.012); s.mat.opacity = k; }
  };

  return {
    desenhar(t) {
      const filme = t >= tF0 && t < tR1;
      const terra = posDe('terra', t);
      const f = fracao(t);
      const p = S.clone().lerp(C, f);
      // feixe: do Sol (ou da última luz) até a Terra, enquanto ainda chega luz
      const temFeixe = !filme && t < tC;
      feixe.visible = temFeixe;
      if (temFeixe) feixe.userData.definir([t < tS ? S.clone() : p.clone(), terra.clone()]);
      // a última luz
      const temPonto = t >= tS && !filme && t < tC + 0.3;
      ponto.visible = temPonto;
      if (temPonto) {
        ponto.position.copy(p);
        ponto.scale.setScalar(1.3 * (1 + 0.08 * Math.sin(t * 18)));
        ponto.material.opacity = 1 - suave(clamp((t - tC) / 0.3));
        registrar('luz', p, 0.4, true);
      }
      // a gravidade: um anel que cresce junto com a última luz
      const temAnel = t >= tG && !filme && t < tC + 0.6;
      anel.visible = bruma.visible = temAnel;
      if (temAnel) {
        const depois = Math.max(0, t - tC);
        const r = Math.max(0.3, f * RC + depois * 6);
        const k = suave(clamp((t - tG) / 0.25)) * (1 - suave(clamp(depois / 0.6)));
        for (const m of [anel, bruma]) { m.position.copy(S); m.scale.setScalar(r); }
        anelMat.opacity = 0.85 * k; brumaMat.opacity = 0.25 * k;
        registrar('gravidade', S, r, true);
      }
      // a Terra e a Lua apagam
      apagar(sombraTerra, 'terra', t, tC, 0.8);
      apagar(sombraLua, 'lua', t, tL, 0.88);
    },
  };
}
