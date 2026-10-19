
import math
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SWINGBY OVER | Mission",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------
# Streamlit 설정 및 선택 정보
# ----------------------------------------
planet = str(st.session_state.get("selected_planet", "지구"))
ship_name = str(st.session_state.get("selected_ship", "ECLIPSE"))

SHIP_DATA = {
    "ECLIPSE": {"speed": 1.00, "control": 1.00, "color": "#72eaff"},
    "VULCAN": {"speed": 1.20, "control": 0.80, "color": "#ff7869"},
    "NOVA": {"speed": 0.90, "control": 1.25, "color": "#c6a0ff"},
}
ship = SHIP_DATA.get(ship_name, SHIP_DATA["ECLIPSE"])

PLANET_DATA = {
    "수성": {"color": "#c4c8d2", "radius": 13},
    "금성": {"color": "#f2c18d", "radius": 19},
    "지구": {"color": "#59aaff", "radius": 21},
    "화성": {"color": "#ff785f", "radius": 16},
    "목성": {"color": "#e4bd8c", "radius": 29},
}
target = PLANET_DATA.get(planet, PLANET_DATA["지구"])

# JS 문자열에 안전하게 넣기 위한 JSON 변환
import json

planet_json = json.dumps(planet, ensure_ascii=False)
ship_json = json.dumps(ship_name, ensure_ascii=False)
color_json = json.dumps(ship["color"])
speed_json = json.dumps(ship["speed"])
control_json = json.dumps(ship["control"])
target_color_json = json.dumps(target["color"])
target_radius_json = json.dumps(target["radius"])

st.markdown(
    """
    <style>
    #MainMenu, footer, header, [data-testid="stSidebar"] {
        display: none !important;
    }
    .block-container {
        max-width: 100% !important;
        padding: 0.5rem 0.7rem 0.2rem 0.7rem !important;
    }
    .stApp {
        background: #050713;
        color: #e9f5ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        text-align:center;
        font-family:Arial,sans-serif;
        padding:0.25rem 0 0.4rem 0;
    ">
        <div style="
            color:#75eaff;
            font-size:0.7rem;
            letter-spacing:0.32rem;
        ">GRAVITY IS YOUR ENGINE</div>
        <div style="
            font-size:clamp(1.5rem,3vw,2.4rem);
            font-weight:900;
            letter-spacing:0.12rem;
            color:#f3f7ff;
        ">SWINGBY OVER</div>
    </div>
    """,
    unsafe_allow_html=True,
)

html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }
html, body {
    margin: 0;
    padding: 0;
    background: #050713;
    color: #eaf4ff;
    font-family: Arial, "Noto Sans KR", sans-serif;
    overflow: hidden;
}
#game-wrap {
    width: 100%;
    max-width: 1500px;
    margin: auto;
    border: 1px solid rgba(111, 213, 255, .23);
    border-radius: 14px;
    overflow: hidden;
    background: #050713;
}
#hud {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 10px 14px;
    background: linear-gradient(90deg, #0c1230, #10162c, #090d20);
    border-bottom: 1px solid rgba(111, 213, 255, .2);
}
.hud-label {
    color: #8298c7;
    font-size: 10px;
    letter-spacing: 2px;
}
.hud-value {
    font-size: 13px;
    font-weight: bold;
    margin-top: 4px;
}
#status { color: #76eaff; }
#canvas-wrap {
    position: relative;
    width: 100%;
    background: #050713;
}
canvas {
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 16 / 9;
    cursor: crosshair;
    touch-action: none;
}
#message {
    position: absolute;
    left: 50%;
    top: 15px;
    transform: translateX(-50%);
    max-width: 90%;
    padding: 8px 14px;
    border: 1px solid rgba(119, 226, 255, .35);
    border-radius: 9px;
    background: rgba(5, 10, 28, .85);
    color: #dff8ff;
    font-size: 12px;
    text-align: center;
    pointer-events: none;
    white-space: nowrap;
}
#bottom {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 12px 14px;
    background: #090e20;
    border-top: 1px solid rgba(111, 213, 255, .17);
}
#instructions {
    color: #9eafd3;
    font-size: 12px;
    line-height: 1.8;
}
button {
    border: 1px solid rgba(111, 224, 255, .5);
    border-radius: 8px;
    padding: 9px 14px;
    background: #101e3b;
    color: #e9faff;
    font-weight: bold;
    cursor: pointer;
}
button:hover {
    background: #18365a;
    border-color: #80ecff;
}
#launch {
    color: #07101b;
    background: #7deaff;
    border-color: #7deaff;
}
#launch:hover { background: #b0f5ff; }
#result {
    display: none;
    padding: 12px;
    text-align: center;
    color: #bdefff;
    background: #0c1530;
    font-size: 13px;
}
.legend {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-right: 12px;
}
.dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
}
</style>
</head>
<body>
<div id="game-wrap">
    <div id="hud">
        <div>
            <div class="hud-label">DESTINATION</div>
            <div class="hud-value" id="destination">TARGET</div>
        </div>
        <div>
            <div class="hud-label">SPACECRAFT</div>
            <div class="hud-value" id="craft">ECLIPSE</div>
        </div>
        <div>
            <div class="hud-label">INITIAL SPEED</div>
            <div class="hud-value" id="speed">0.00</div>
        </div>
        <div>
            <div class="hud-label">FLIGHT STATUS</div>
            <div class="hud-value" id="status">READY</div>
        </div>
    </div>

    <div id="canvas-wrap">
        <canvas id="space" width="1200" height="675"></canvas>
        <div id="message">우주선을 뒤로 드래그한 뒤 놓으면 발사됩니다.</div>
    </div>

    <div id="result"></div>

    <div id="bottom">
        <div id="instructions">
            <span class="legend"><span class="dot" style="background:#ff656f"></span>예측 궤도</span>
            <span class="legend"><span class="dot" style="background:#72eaff"></span>중력 영향 범위</span>
            <br>
            ① 우주선에서 뒤쪽으로 드래그하세요.<br>
            ② 당긴 거리가 길수록 초기 속도가 커집니다. 소행성의 중력을 이용해 목적지에 도달하세요.
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button id="reset">↻ 다시 시작</button>
            <button id="launch">발사하기</button>
        </div>
    </div>
</div>

<script>
(function () {
"use strict";

const canvas = document.getElementById("space");
const ctx = canvas.getContext("2d");
const W = canvas.width;
const H = canvas.height;

const PLANET = __PLANET__;
const SHIP = __SHIP__;
const SHIP_COLOR = __SHIP_COLOR__;
const SHIP_SPEED = __SHIP_SPEED__;
const SHIP_CONTROL = __SHIP_CONTROL__;
const TARGET_COLOR = __TARGET_COLOR__;
const TARGET_RADIUS = __TARGET_RADIUS__;

document.getElementById("destination").textContent = PLANET.toUpperCase();
document.getElementById("craft").textContent = SHIP;

const stars = [];
for (let i = 0; i < 150; i++) {
    stars.push({
        x: Math.random() * W,
        y: Math.random() * H,
        r: Math.random() * 1.5 + 0.3,
        a: Math.random() * 0.65 + 0.2
    });
}

const start = { x: 95, y: H * 0.51 };
const goal = { x: W - 80, y: H * 0.5 };

// 고정된 소행성. 각각 중력 세기와 영향 범위가 다릅니다.
const asteroids = [
    {x: 300, y: 230, r: 20, g: 4200, range: 115, color:"#b8c2d3", phase:0.3},
    {x: 455, y: 440, r: 29, g: 7600, range: 155, color:"#8b9db5", phase:1.4},
    {x: 600, y: 205, r: 16, g: 2500, range: 88, color:"#c8a98d", phase:2.2},
    {x: 710, y: 430, r: 23, g: 5400, range: 132, color:"#a1a8ba", phase:0.7},
    {x: 820, y: 250, r: 31, g: 9000, range: 170, color:"#9c91a9", phase:2.8},
    {x: 930, y: 455, r: 17, g: 3200, range: 105, color:"#b9b8c5", phase:1.9}
];

let ship = {};
let dragging = false;
let dragPoint = null;
let launched = false;
let finished = false;
let won = false;
let trail = [];
let elapsed = 0;
let animationId = null;
let lastTime = 0;
let messageTimer = null;

function setMessage(text) {
    document.getElementById("message").textContent = text;
}

function resetGame() {
    if (animationId !== null) {
        cancelAnimationFrame(animationId);
    }

    ship = {
        x: start.x,
        y: start.y,
        vx: 0,
        vy: 0,
        r: 8
    };

    dragging = false;
    dragPoint = null;
    launched = false;
    finished = false;
    won = false;
    trail = [];
    elapsed = 0;
    lastTime = 0;

    document.getElementById("speed").textContent = "0.00";
    document.getElementById("status").textContent = "READY";
    document.getElementById("result").style.display = "none";
    document.getElementById("launch").disabled = false;
    setMessage("우주선을 뒤로 드래그한 뒤 놓으면 발사됩니다.");

    animationId = requestAnimationFrame(frame);
}

function getPointer(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: (e.clientX - rect.left) * W / rect.width,
        y: (e.clientY - rect.top) * H / rect.height
    };
}

function speedFromDrag(point) {
    const dx = ship.x - point.x;
    const dy = ship.y - point.y;
    const distance = Math.hypot(dx, dy);
    const magnitude = Math.min(distance * 0.055, 13) * SHIP_SPEED;
    return {
        vx: distance > 0 ? dx / distance * magnitude : 0,
        vy: distance > 0 ? dy / distance * magnitude : 0
    };
}

function applyGravity(body, dt) {
    // 단순화된 중력 모델: 거리 제곱에 따라 중력이 약해집니다.
    // 충돌 판정과 중력 영향 범위는 별도로 계산합니다.
    for (const a of asteroids) {
        const dx = a.x - body.x;
        const dy = a.y - body.y;
        const d2 = dx * dx + dy * dy;
        const d = Math.sqrt(d2);

        if (d < a.range && d > a.r + 2) {
            const softening = 900;
            const acceleration = a.g / (d2 + softening);
            body.vx += dx / d * acceleration * dt * SHIP_CONTROL;
            body.vy += dy / d * acceleration * dt * SHIP_CONTROL;
        }
    }
}

function stepBody(body, dt) {
    applyGravity(body, dt);

    body.x += body.vx * dt;
    body.y += body.vy * dt;
}

function simulatePath(initialVx, initialVy, limit) {
    const b = {
        x: start.x,
        y: start.y,
        vx: initialVx,
        vy: initialVy,
        r: 8
    };

    const points = [];
    const dt = 1.8;
    let hit = false;

    for (let i = 0; i < limit; i++) {
        stepBody(b, dt);

        if (!Number.isFinite(b.x) || !Number.isFinite(b.y)) break;

        points.push({x: b.x, y: b.y});

        if (b.x > goal.x - TARGET_RADIUS && Math.abs(b.y - goal.y) < TARGET_RADIUS + 10) {
            hit = true;
            break;
        }

        let collided = false;
        for (const a of asteroids) {
            if (Math.hypot(b.x - a.x, b.y - a.y) < a.r + b.r) {
                collided = true;
                break;
            }
        }

        if (collided) break;
        if (b.x < -20 || b.x > W + 20 || b.y < -20 || b.y > H + 20) break;
    }

    return {points, hit};
}

function drawBackground() {
    const gradient = ctx.createRadialGradient(
        W * 0.52, H * 0.45, 30,
        W * 0.52, H * 0.45, W * 0.72
    );
    gradient.addColorStop(0, "#111a3a");
    gradient.addColorStop(0.55, "#090d20");
    gradient.addColorStop(1, "#03040a");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    for (const s of stars) {
        ctx.globalAlpha = s.a;
        ctx.fillStyle = "#dcecff";
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.globalAlpha = 1;

    // 희미한 가이드 라인
    ctx.strokeStyle = "rgba(100,145,220,0.06)";
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 75) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, H);
        ctx.stroke();
    }
    for (let y = 0; y < H; y += 75) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(W, y);
        ctx.stroke();
    }
}

function drawGravityField(a) {
    const gradient = ctx.createRadialGradient(
        a.x, a.y, a.r,
        a.x, a.y, a.range
    );
    gradient.addColorStop(0, "rgba(80,190,255,0.10)");
    gradient.addColorStop(0.75, "rgba(80,190,255,0.045)");
    gradient.addColorStop(1, "rgba(80,190,255,0.005)");

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(a.x, a.y, a.range, 0, Math.PI * 2);
    ctx.fill();

    ctx.setLineDash([5, 7]);
    ctx.strokeStyle = "rgba(99,216,255,0.45)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(a.x, a.y, a.range, 0, Math.PI * 2);
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawAsteroid(a) {
    drawGravityField(a);

    const gradient = ctx.createRadialGradient(
        a.x - a.r * 0.35, a.y - a.r * 0.4, 1,
        a.x, a.y, a.r * 1.3
    );
    gradient.addColorStop(0, "#e4e8ef");
    gradient.addColorStop(0.45, a.color);
    gradient.addColorStop(1, "#41495e");

    ctx.save();
    ctx.translate(a.x, a.y);
    ctx.rotate(a.phase);

    ctx.fillStyle = gradient;
    ctx.strokeStyle = "rgba(220,235,255,0.5)";
    ctx.lineWidth = 1.3;
    ctx.beginPath();

    const n = 9;
    for (let i = 0; i < n; i++) {
        const angle = i / n * Math.PI * 2;
        const radius = a.r * (0.82 + 0.18 * Math.sin(i * 4.13 + a.phase));
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }

    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "rgba(35,43,60,0.45)";
    ctx.beginPath();
    ctx.arc(-a.r * 0.2, -a.r * 0.1, a.r * 0.18, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();

    // 중력 세기를 나타내는 작은 표식
    ctx.fillStyle = "#a8c9e9";
    ctx.font = "10px Arial";
    ctx.textAlign = "center";
    ctx.fillText("G " + Math.round(a.g / 1000 * 10) / 10, a.x, a.y + a.r + 15);
}

function drawGoal() {
    const glow = ctx.createRadialGradient(
        goal.x, goal.y, TARGET_RADIUS * 0.3,
        goal.x, goal.y, TARGET_RADIUS * 3
    );
    glow.addColorStop(0, TARGET_COLOR);
    glow.addColorStop(0.2, TARGET_COLOR + "88");
    glow.addColorStop(1, "rgba(80,150,255,0)");

    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(goal.x, goal.y, TARGET_RADIUS * 3, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = TARGET_COLOR;
    ctx.beginPath();
    ctx.arc(goal.x, goal.y, TARGET_RADIUS, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "rgba(255,255,255,0.3)";
    ctx.beginPath();
    ctx.arc(
        goal.x - TARGET_RADIUS * 0.25,
        goal.y - TARGET_RADIUS * 0.25,
        TARGET_RADIUS * 0.45,
        0, Math.PI * 2
    );
    ctx.fill();

    ctx.strokeStyle = "rgba(130,220,255,0.7)";
    ctx.setLineDash([4, 5]);
    ctx.beginPath();
    ctx.arc(goal.x, goal.y, TARGET_RADIUS + 12, 0, Math.PI * 2);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.textAlign = "center";
    ctx.fillStyle = "#e6f5ff";
    ctx.font = "bold 12px Arial";
    ctx.fillText(PLANET.toUpperCase(), goal.x, goal.y + TARGET_RADIUS + 28);
    ctx.fillStyle = "#8199c5";
    ctx.font = "10px Arial";
    ctx.fillText("TARGET", goal.x, goal.y + TARGET_RADIUS + 42);
}

function drawShip() {
    ctx.save();
    ctx.translate(ship.x, ship.y);

    const angle = Math.atan2(ship.vy, ship.vx);
    if (launched && Math.hypot(ship.vx, ship.vy) > 0.1) {
        ctx.rotate(angle);
    }

    ctx.shadowColor = SHIP_COLOR;
    ctx.shadowBlur = 20;
    ctx.fillStyle = SHIP_COLOR;
    ctx.strokeStyle = "#f2fcff";
    ctx.lineWidth = 1.4;

    ctx.beginPath();
    ctx.moveTo(13, 0);
    ctx.lineTo(-8, -7);
    ctx.lineTo(-4, 0);
    ctx.lineTo(-8, 7);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    ctx.shadowBlur = 0;

    if (!launched) {
        ctx.strokeStyle = "rgba(120,230,255,0.35)";
        ctx.beginPath();
        ctx.arc(0, 0, 20, 0, Math.PI * 2);
        ctx.stroke();
    }

    ctx.restore();
}

function drawForecast() {
    if (launched || finished) return;

    let vx = 0;
    let vy = 0;

    if (dragging && dragPoint) {
        const v = speedFromDrag(dragPoint);
        vx = v.vx;
        vy = v.vy;
    } else {
        // 기본 방향의 짧은 예측 궤도
        vx = 3.4 * SHIP_SPEED;
        vy = 0;
    }

    const result = simulatePath(vx, vy, 260);
    const points = result.points;

    if (points.length < 2) return;

    ctx.save();
    ctx.setLineDash([3, 7]);
    ctx.lineWidth = 2;
    ctx.strokeStyle = "#ff6573";
    ctx.shadowColor = "rgba(255,70,100,0.55)";
    ctx.shadowBlur = 7;

    ctx.beginPath();
    ctx.moveTo(ship.x, ship.y);

    for (let i = 0; i < points.length; i++) {
        const p = points[i];
        ctx.lineTo(p.x, p.y);
    }

    ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();

    if (dragging && dragPoint) {
        ctx.strokeStyle = "rgba(255,105,115,0.95)";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(ship.x, ship.y);
        ctx.lineTo(dragPoint.x, dragPoint.y);
        ctx.stroke();

        const v = speedFromDrag(dragPoint);
        ctx.fillStyle = "#ff8b96";
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "left";
        ctx.fillText(
            "v₀ = " + Math.hypot(v.vx, v.vy).toFixed(2),
            ship.x + 15,
            ship.y - 22
        );
    }
}

function drawTrail() {
    if (trail.length < 2) return;

    ctx.beginPath();
    ctx.moveTo(trail[0].x, trail[0].y);

    for (let i = 1; i < trail.length; i++) {
        ctx.lineTo(trail[i].x, trail[i].y);
    }

    ctx.strokeStyle = SHIP_COLOR;
    ctx.lineWidth = 2;
    ctx.shadowColor = SHIP_COLOR;
    ctx.shadowBlur = 9;
    ctx.stroke();
    ctx.shadowBlur = 0;
}

function draw() {
    drawBackground();

    for (const a of asteroids) {
        drawAsteroid(a);
    }

    drawGoal();
    drawForecast();
    drawTrail();
    drawShip();
}

function finish(success, text) {
    finished = true;
    won = success;

    document.getElementById("status").textContent =
        success ? "MISSION COMPLETE" : "MISSION FAILED";

    document.getElementById("result").style.display = "block";
    document.getElementById("result").textContent = text;
    document.getElementById("launch").disabled = true;

    setMessage(success ? "목표 도달 성공!" : "비행 종료. 다시 도전해 보세요.");
}

function update(dt) {
    if (!launched || finished) return;

    // 과도하게 큰 시간 간격을 막아 수치적 불안정을 줄입니다.
    const step = Math.min(dt, 0.04);
    const substeps = 3;
    const subdt = step / substeps;

    for (let i = 0; i < substeps; i++) {
        stepBody(ship, subdt * 60);

        if (!Number.isFinite(ship.x) || !Number.isFinite(ship.y)) {
            finish(false, "계산 가능한 비행 범위를 벗어났습니다. 초기 속도를 조절해 보세요.");
            return;
        }

        for (const a of asteroids) {
            const distance = Math.hypot(ship.x - a.x, ship.y - a.y);

            if (distance < a.r + ship.r) {
                finish(false, "소행성과 충돌했습니다. 중력장을 이용해 궤도를 바꿔 보세요.");
                return;
            }
        }

        const targetDistance = Math.hypot(ship.x - goal.x, ship.y - goal.y);

        if (targetDistance < TARGET_RADIUS + ship.r + 5) {
            finish(true, "축하합니다! " + PLANET + "에 도착했습니다. 중력 스윙바이 임무 성공!");
            return;
        }

        if (
            ship.x < -30 || ship.x > W + 30 ||
            ship.y < -30 || ship.y > H + 30
        ) {
            finish(false, "우주선이 화면을 벗어났습니다. 드래그 방향과 초기 속도를 바꿔 보세요.");
            return;
        }

        elapsed += subdt;
        if (elapsed > 35) {
            finish(false, "비행 시간이 초과되었습니다. 초기 속도와 궤도를 다시 설계해 보세요.");
            return;
        }
    }

    trail.push({x: ship.x, y: ship.y});
    if (trail.length > 1200) trail.shift();

    document.getElementById("speed").textContent =
        Math.hypot(ship.vx, ship.vy).toFixed(2);
}

function frame(timestamp) {
    if (lastTime === 0) lastTime = timestamp;

    const dt = Math.min((timestamp - lastTime) / 1000, 0.04);
    lastTime = timestamp;

    update(dt);
    draw();

    if (!finished) {
        animationId = requestAnimationFrame(frame);
    }
}

function launchShip() {
    if (launched || finished) return;

    let v;

    if (dragging && dragPoint) {
        v = speedFromDrag(dragPoint);
    } else {
        // 버튼으로 발사할 때는 기본 방향과 속도를 사용합니다.
        v = {
            vx: 4.2 * SHIP_SPEED,
            vy: 0
        };
    }

    const magnitude = Math.hypot(v.vx, v.vy);

    if (magnitude < 0.45) {
        setMessage("조금 더 뒤로 당겨 초기 속도를 높여 주세요.");
        return;
    }

    ship.vx = v.vx;
    ship.vy = v.vy;
    launched = true;
    dragging = false;
    dragPoint = null;

    document.getElementById("speed").textContent = magnitude.toFixed(2);
    document.getElementById("status").textContent = "IN FLIGHT";
    document.getElementById("launch").disabled = true;

    setMessage("비행 중! 중력에 의해 궤도가 변화합니다.");
}

canvas.addEventListener("pointerdown", function (e) {
    if (launched || finished) return;

    const p = getPointer(e);
    if (Math.hypot(p.x - ship.x, p.y - ship.y) < 65) {
        dragging = true;
        dragPoint = p;
        canvas.setPointerCapture(e.pointerId);
    }
});

canvas.addEventListener("pointermove", function (e) {
    if (!dragging || launched || finished) return;
    dragPoint = getPointer(e);

    const v = speedFromDrag(dragPoint);
    document.getElementById("speed").textContent =
        Math.hypot(v.vx, v.vy).toFixed(2);
});

canvas.addEventListener("pointerup", function (e) {
    if (!dragging || launched || finished) return;
    dragPoint = getPointer(e);
    launchShip();
});

canvas.addEventListener("pointercancel", function () {
    dragging = false;
    dragPoint = null;
});

document.getElementById("launch").addEventListener("click", launchShip);
document.getElementById("reset").addEventListener("click", resetGame);

resetGame();
})();
</script>
</body>
</html>
"""

html = (
    html.replace("__PLANET__", planet_json)
    .replace("__SHIP__", ship_json)
    .replace("__SHIP_COLOR__", color_json)
    .replace("__SHIP_SPEED__", speed_json)
    .replace("__SHIP_CONTROL__", control_json)
    .replace("__TARGET_COLOR__", target_color_json)
    .replace("__TARGET_RADIUS__", target_radius_json)
)

components.html(html, height=850, scrolling=False)
