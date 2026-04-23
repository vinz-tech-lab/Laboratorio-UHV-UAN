import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="UHV Virtual Lab - UAN", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #1f77b4; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;}
    .report-card { background-color: #ffffff; padding: 30px; border-radius: 10px; border: 2px solid #1f77b4; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); text-align: center;}
    </style>
""", unsafe_allow_html=True)

# --- VARIABLES DE SESIÓN (MEMORIA DEL JUGADOR) ---
if 'registered' not in st.session_state: st.session_state.registered = False
if 'student_name' not in st.session_state: st.session_state.student_name = ""
if 'student_id' not in st.session_state: st.session_state.student_id = ""
if 'exam_score' not in st.session_state: st.session_state.exam_score = 0
if 'exam_taken' not in st.session_state: st.session_state.exam_taken = False
if 'q_evac_correct' not in st.session_state: st.session_state.q_evac_correct = None
if 'q_plasma_correct' not in st.session_state: st.session_state.q_plasma_correct = None

# ==========================================
# PANTALLA DE INICIO: EXPLICACIÓN Y REGISTRO
# ==========================================
if not st.session_state.registered:
    st.title("🔬 Laboratorio Virtual de Tecnología de Vacío - UAN")
    
    st.markdown("""
    ### Bienvenido al Simulador de Ultra Alto Vacío (UHV)
    
    Este entorno virtual interactivo te permite operar un sistema de vacío profesional y realizar procesos de inyección de gas, sin los riesgos físicos o costos de los equipos reales.
    
    **Tus objetivos en este seminario son:**
    1. **📝 Certificación Teórica:** Aprobar el examen de conocimientos sobre bombas y sensores. Necesitas 13/15 puntos.
    2. **🚀 Evacuación Dinámica:** Encender las bombas en el orden correcto para evacuar la cámara y responder la pregunta de control.
    3. **⚛️ Control de Proceso:** Utilizar controladores de flujo másico para estabilizar la presión, encender un plasma y responder la pregunta de control.
    
    *Por favor, regístrate para comenzar la simulación.*
    """)
    
    st.divider()
    
    with st.form("registro_form"):
        st.subheader("Registro del Operador")
        nombre = st.text_input("Nombre Completo:")
        codigo = st.text_input("Código de Estudiante:")
        submitted = st.form_submit_button("Ingresar al Laboratorio", type="primary")
        
        if submitted:
            if nombre.strip() == "" or codigo.strip() == "":
                st.error("Por favor, ingresa tu nombre y código para continuar.")
            else:
                st.session_state.student_name = nombre
                st.session_state.student_id = codigo
                st.session_state.registered = True
                st.rerun()

# ==========================================
# SIMULADOR PRINCIPAL
# ==========================================
else:
    st.title(f"🔬 Laboratorio UHV | Operador: {st.session_state.student_name}")

    t1, t2, t3, t4 = st.tabs([
        "📝 Certificación Teórica", 
        "🚀 Simulador de Evacuación Dinámica", 
        "⚛️ Control de Proceso Avanzado (Mezcla y Plasma)",
        "📊 Reporte de Resultados"
    ])

    # ==========================================
    # PESTAÑA 1: TEORÍA Y CERTIFICACIÓN
    # ==========================================
    with t1:
        st.header("Examen de Certificación de Operador UHV")
        st.write("Demuestra tus conocimientos teóricos antes de operar los equipos de alto vacío del laboratorio. Debes obtener al menos 13/15 para aprobar.")
        
        preguntas = [
            {
                "q": "¿Cuál es el rango de presión límite típico que puede alcanzar una bomba mecánica rotativa de paletas de doble etapa?", 
                "o": ["100 mbar", "1e-3 mbar", "1e-9 mbar", "Presión atmosférica únicamente"], 
                "a": "1e-3 mbar",
                "feedback": "Las bombas rotativas de aceite están limitadas por la presión de vapor de su propio aceite y el volumen muerto (espacio nocivo) en la cámara de compresión. Típicamente alcanzan un límite de $10^{-3}$ mbar, también conocido como vacío primario."
            },
            {
                "q": "¿Por qué una bomba turbomolecular no puede descargar el gas directamente a la presión atmosférica?", 
                "o": ["Porque funciona con aceite y se evaporaría.", "Por su baja relación de compresión a altas presiones, requiriendo una bomba de respaldo (mecánica).", "Porque el gas se congelaría en los álabes."], 
                "a": "Por su baja relación de compresión a altas presiones, requiriendo una bomba de respaldo (mecánica).",
                "feedback": "La relación de compresión de una bomba turbo depende del régimen molecular. A presiones atmosféricas, el flujo es viscoso y las moléculas chocan entre sí, anulando el impulso direccional de los álabes. Siempre requiere que una bomba mecánica le mantenga el escape a $\\approx 10^{-2}$ mbar."
            },
            {
                "q": "¿Qué sucede de forma catastrófica si la presión de la cámara sube bruscamente mientras la bomba turbo gira a máxima velocidad?", 
                "o": ["Falla de los álabes debido a la extrema fricción viscosa contra el aire denso.", "La bomba simplemente se apaga sin daños.", "El campo magnético interno colapsa."], 
                "a": "Falla de los álabes debido a la extrema fricción viscosa contra el aire denso.",
                "feedback": "El rotor gira entre 30,000 y 90,000 RPM. Si la presión sube, el gas entra en régimen de flujo viscoso. La fricción aerodinámica masiva sobrecalienta y dobla los álabes, haciéndolos chocar contra el estator y destruyendo la bomba instantáneamente (Crash)."
            },
            {
                "q": "¿Cuál es el principio de funcionamiento principal de una bomba de difusión?", 
                "o": ["Usa aspas giratorias a gran velocidad.", "Atrapa gases en paneles criogénicos.", "Arrastra las moléculas de gas mediante chorros de vapor de aceite supersónicos descendentes."], 
                "a": "Arrastra las moléculas de gas mediante chorros de vapor de aceite supersónicos descendentes.",
                "feedback": "La bomba calienta un aceite especial; su vapor asciende y es expulsado hacia abajo a velocidad supersónica por toberas. Las moléculas de gas que deambulan por la entrada chocan con este vapor y reciben momento hacia el fondo, donde son extraídas por la bomba de respaldo."
            },
            {
                "q": "¿Qué componente es obligatorio colocar sobre una bomba de difusión para evitar el 'backstreaming' (contaminación de la cámara)?", 
                "o": ["Un sensor Pirani de alta precisión.", "Una trampa fría o bafle ópticamente ciego.", "Una válvula de aguja micrométrica."], 
                "a": "Una trampa fría o bafle ópticamente ciego.",
                "feedback": "El 'backstreaming' es la migración de moléculas de vapor de aceite hacia la cámara principal. Un bafle refrigerado (usualmente con agua o nitrógeno líquido) condensa este vapor y lo hace gotear de regreso a la caldera antes de que pueda contaminar tu muestra o sistema óptico."
            },
            {
                "q": "¿Qué principio físico permite a una bomba iónica (Sputter Ion Pump) extraer gas?", 
                "o": ["Fuerza centrífuga y rotación electromagnética.", "Ioniza el gas y lo acelera magnéticamente contra cátodos de titanio, atrapándolo química y físicamente.", "Condensación de gases en superficies refrigeradas por nitrógeno líquido."], 
                "a": "Ioniza el gas y lo acelera magnéticamente contra cátodos de titanio, atrapándolo química y físicamente.",
                "feedback": "Utiliza un alto voltaje y un campo magnético para mantener un plasma (descarga Penning). Los iones bombardean un cátodo de titanio (Sputtering), recubriendo las paredes con titanio fresco. Los gases reactivos se unen químicamente a este titanio (Gettering), y los gases inertes quedan enterrados debajo de él."
            },
            {
                "q": "¿A qué presión de seguridad (crossover) se debe encender una bomba iónica estándar para evitar un arco eléctrico destructivo?", 
                "o": ["A presión atmosférica (1013 mbar).", "Debajo de 1e-1 mbar.", "Debajo de 1e-5 mbar."], 
                "a": "Debajo de 1e-5 mbar.",
                "feedback": "Si se enciende a presiones mayores (ej. $10^{-3}$ mbar), la alta densidad de gas provocaría una avalancha electrónica masiva, generando un arco voltaico continuo que fundiría los electrodos de titanio y destruiría la fuente de alta tensión."
            },
            {
                "q": "¿Cómo se comporta una bomba iónica estándar tipo diodo frente a los gases nobles (ej. Argón)?", 
                "o": ["Los bombea de manera extremadamente eficiente.", "Los bombea muy lentamente porque no reaccionan químicamente con el titanio.", "No los bombea en absoluto."], 
                "a": "Los bombea muy lentamente porque no reaccionan químicamente con el titanio.",
                "feedback": "Los gases inertes o nobles no hacen reacciones químicas (no hay 'Gettering'). La única forma en que la bomba iónica los extrae es bombardeándolos contra la pared para que queden físicamente 'enterrados' por capas posteriores de titanio, un proceso que tiene solo un 10% de la eficiencia comparado con el nitrógeno."
            },
            {
                "q": "¿Cuál es la función principal del filamento en una bomba de sublimación de titanio (TSP)?", 
                "o": ["Medir la temperatura del vacío.", "Calentarse para emitir luz ultravioleta desinfectante.", "Sublimar titanio puro sobre las paredes para crear una película 'getter' que reaccione con gases activos."], 
                "a": "Sublimar titanio puro sobre las paredes para crear una película 'getter' que reaccione con gases activos.",
                "feedback": "Al pasar alta corriente por el filamento, el titanio cambia de estado sólido a gaseoso (sublimación) y se condensa en las paredes frías circundantes. Esta nueva capa metálica es altamente reactiva y actúa como una 'esponja' química para gases como $O_2$, $N_2$ y $H_2$."
            },
            {
                "q": "¿Qué gas NO es bombeado de manera efectiva por una bomba de sublimación de titanio (TSP)?", 
                "o": ["Oxígeno (O2).", "Monóxido de carbono (CO).", "Metano (CH4) y gases nobles."], 
                "a": "Metano (CH4) y gases nobles.",
                "feedback": "La bomba TSP es puramente química (Gettering). Los gases nobles (Helio, Argón) no reaccionan. El Metano ($CH_4$) es químicamente demasiado estable a temperatura ambiente para disociarse en la superficie del titanio, por lo que su velocidad de bombeo es prácticamente nula."
            },
            {
                "q": "¿En qué fenómeno físico se basa el funcionamiento de un sensor de vacío tipo Pirani?", 
                "o": ["En el cambio de conductividad térmica del gas; mide el enfriamiento de un filamento caliente.", "En la emisión de fotones de un cátodo.", "En la desviación de partículas alfa."], 
                "a": "En el cambio de conductividad térmica del gas; mide el enfriamiento de un filamento caliente.",
                "feedback": "Un alambre muy fino (ej. tungsteno) se calienta eléctricamente. Las moléculas de gas que chocan contra él le roban calor. Si la presión baja, hay menos moléculas, el filamento retiene más calor, su temperatura sube y, en consecuencia, cambia su resistencia eléctrica."
            },
            {
                "q": "¿En qué rango de presión es preciso y confiable un medidor Pirani estándar?", 
                "o": ["De 1013 mbar a 1e-4 mbar.", "De 1e-3 mbar a 1e-11 mbar.", "Únicamente en el rango de Ultra Alto Vacío."], 
                "a": "De 1013 mbar a 1e-4 mbar.",
                "feedback": "Por debajo de $10^{-4}$ mbar, el gas está tan enrarecido que la principal pérdida de calor del filamento deja de ser por conducción del gas y pasa a ser por radiación infrarroja y conducción térmica por los soportes. En ese punto, el sensor se vuelve 'ciego' a la presión."
            },
            {
                "q": "¿Cómo mide la presión un sensor de cátodo frío (ej. tipo Penning o Magnetrón Invertido)?", 
                "o": ["Midiendo la resistencia eléctrica de un hilo de tungsteno.", "Midiendo la deformación de un diafragma de cerámica.", "Midiendo la corriente eléctrica generada por la ionización del gas en un campo magnético y eléctrico cruzado."], 
                "a": "Midiendo la corriente eléctrica generada por la ionización del gas en un campo magnético y eléctrico cruzado.",
                "feedback": "Utiliza campos magnéticos para obligar a los electrones libres a viajar en espiral. Esto alarga su trayectoria y aumenta la probabilidad de que choquen y colisionen con las pocas moléculas de gas restantes (ionización). La corriente de iones medida es directamente proporcional a la presión del gas."
            },
            {
                "q": "¿Por qué NUNCA se debe encender un sensor de cátodo frío a presión atmosférica?", 
                "o": ["Porque gastaría mucha electricidad.", "Porque la alta densidad de gas causaría una corriente excesiva, chisporroteo y contaminación/destrucción de los electrodos.", "Porque mediría una presión negativa."], 
                "a": "Porque la alta densidad de gas causaría una corriente excesiva, chisporroteo y contaminación/destrucción de los electrodos.",
                "feedback": "A presiones mayores de $10^{-2}$ mbar, encender los altos voltajes ($>2000V$) del cátodo frío genera un arco eléctrico masivo y sputtering incontrolado que contamina los aislantes cerámicos y destruye el ánodo internamente."
            },
            {
                "q": "¿Qué combinación de equipos forma un sistema de bombeo '100% libre de aceite' (Dry system) ideal para Ultra Alto Vacío puro?", 
                "o": ["Bomba mecánica rotativa de paletas + Bomba de difusión.", "Bomba scroll seca + Bomba turbomolecular de rodamientos magnéticos.", "Bomba de diafragma + Bomba rotativa húmeda."], 
                "a": "Bomba scroll seca + Bomba turbomolecular de rodamientos magnéticos.",
                "feedback": "La bomba Scroll utiliza espirales recubiertas de PTFE para comprimir gas mecánicamente sin lubricantes líquidos. Acoplada a una Turbo de levitación magnética (que no requiere grasa en sus rodamientos), garantiza que no haya moléculas de hidrocarburos contaminando la cámara UHV."
            }
        ]

        with st.form("examen_form"):
            respuestas_usuario = []
            for i, p in enumerate(preguntas):
                st.markdown(f"**{i+1}. {p['q']}**")
                resp = st.radio("Selecciona una opción:", p['o'], key=f"q_{i}", index=None, label_visibility="collapsed")
                respuestas_usuario.append(resp)
                st.markdown("---")
                
            submit_btn = st.form_submit_button("Calificar Examen")
            
            if submit_btn:
                puntaje = 0
                for i, (resp, p) in enumerate(zip(respuestas_usuario, preguntas)):
                    if resp == p['a']: 
                        puntaje += 1
                    elif resp is None: 
                        st.warning(f"⚠️ Pregunta {i+1} sin responder.")
                    else: 
                        st.error(f"❌ **Pregunta {i+1} incorrecta.** La respuesta correcta es:\n\n*{p['a']}*")
                        st.info(f"💡 **Fundamento Físico:** {p['feedback']}")
                
                st.session_state.exam_score = puntaje
                st.session_state.exam_taken = True
                st.subheader(f"Puntuación Final: {puntaje} / 15")
                
                if puntaje >= 13:
                    st.success("🎉 ¡EXCELENTE! Has aprobado la certificación teórica y estás listo para operar el sistema UHV.")
                    st.balloons()
                else:
                    st.error("🛑 Examen no aprobado. Revisa los fundamentos teóricos proporcionados arriba y vuelve a intentarlo.")

    # ==========================================
    # PESTAÑA 2: SIMULADOR DE EVACUACIÓN
    # ==========================================
    with t2:
        st.header("Simulador de Evacuación Dinámica")
        st.markdown("Esquema reactivo con **simulación de partículas en tiempo real**. Abre las válvulas en el orden correcto.")
        
        # PREGUNTA DE CONTROL
        with st.expander("📝 Pregunta de Control: Evacuación (Requerida para el reporte)", expanded=True):
            with st.form("form_evac"):
                st.write("**Durante la evacuación dinámica, ¿por qué es crítico esperar a que la presión descienda al régimen de vacío primario (crossover) antes de abrir la válvula de la bomba Turbomolecular?**")
                ans_evac = st.radio("Opciones:", [
                    "Para ahorrar energía eléctrica.",
                    "Para evitar la destrucción de los álabes por fricción viscosa a alta presión.",
                    "Para permitir que el sensor Pirani se caliente."
                ], index=None, label_visibility="collapsed")
                
                if st.form_submit_button("Guardar Respuesta"):
                    if ans_evac == "Para evitar la destrucción de los álabes por fricción viscosa a alta presión.":
                        st.session_state.q_evac_correct = True
                        st.success("¡Correcto! Operar la Turbo en flujo molecular es esencial. Respuesta guardada para el reporte.")
                    else:
                        st.session_state.q_evac_correct = False
                        st.error("❌ Incorrecto.")
                        st.info("💡 **Fundamento Físico:** La bomba turbomolecular opera en el régimen de flujo molecular, donde el camino libre medio ($\lambda$) es mayor que el espacio entre los álabes. Si se expone a alta presión (flujo viscoso), las densas colisiones moleculares generan una fricción aerodinámica masiva que calienta y rompe el rotor de aleación, el cual gira a más de 30,000 RPM.")

        html_evac = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background: #ffffff; color: #333; margin: 0; padding: 10px; }
                .grid-container { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; }
                .panel { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; }
                .control-group { margin-bottom: 15px; }
                .control-group h4 { margin: 0 0 10px 0; color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 5px;}
                label { display: block; margin-bottom: 5px; cursor: pointer; font-weight: bold;}
                input[type="checkbox"] { transform: scale(1.2); margin-right: 8px; cursor: pointer; }
                .display-presion { font-size: 2em; font-family: monospace; color: #d62728; font-weight: bold; background: #fff; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #ccc;}
                .alert { background: #ffeded; color: #d62728; padding: 15px; border-radius: 5px; font-weight: bold; display: none; margin-top: 15px; border-left: 5px solid #d62728;}
                .success { background: #edffef; color: #2ca02c; padding: 15px; border-radius: 5px; font-weight: bold; display: none; margin-top: 15px; border-left: 5px solid #2ca02c;}
                button { background: #1f77b4; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold; font-size: 1.1em;}
                button:hover { background: #155a8a; }
                canvas { background: white; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 100%; }
            </style>
        </head>
        <body>
        <div class="grid-container">
            <div class="panel">
                <div class="display-presion" id="p-disp">1.0e+3 mbar</div>
                <div id="c-disp" style="text-align:center; margin-bottom: 15px; color: #666;">Cátodo: APAGADO</div>
                
                <div class="control-group">
                    <h4>Sensores</h4>
                    <label><input type="checkbox" id="scat"> Encender Cátodo Frío</label>
                </div>
                <div class="control-group">
                    <h4>Válvulas</h4>
                    <label><input type="checkbox" id="vmec"> Válvula Mecánica</label>
                    <label><input type="checkbox" id="vtur"> Válvula Turbo</label>
                    <label><input type="checkbox" id="vion"> Válvula Iónica</label>
                </div>
                <div class="control-group">
                    <h4>Bombas</h4>
                    <label><input type="checkbox" id="bmec"> Bomba Mecánica</label>
                    <label><input type="checkbox" id="btur"> Bomba Turbo</label>
                    <label><input type="checkbox" id="bion"> Bomba Iónica</label>
                    <label><input type="checkbox" id="btsp"> Bomba TSP</label>
                </div>
                
                <button onclick="resetSim()">🔄 Reiniciar Sistema</button>
                <div id="alert-box" class="alert"></div>
                <div id="success-box" class="success">🏆 ¡UHV ALCANZADO (1.0e-11 mbar)!</div>
            </div>
            <div>
                <canvas id="schemaCanvas" width="600" height="250" style="margin-bottom: 15px;"></canvas>
                <canvas id="chartCanvas" width="600" height="250"></canvas>
            </div>
        </div>
        <script>
            let P = 1013.0, t = 0, state = "OK";
            let hX = [0], hY = [1013.0];
            
            const els = {
                scat: document.getElementById('scat'), vmec: document.getElementById('vmec'), vtur: document.getElementById('vtur'), vion: document.getElementById('vion'),
                bmec: document.getElementById('bmec'), btur: document.getElementById('btur'), bion: document.getElementById('bion'), btsp: document.getElementById('btsp'),
                pD: document.getElementById('p-disp'), cD: document.getElementById('c-disp'), aB: document.getElementById('alert-box'), sB: document.getElementById('success-box')
            };

            const ctxChart = document.getElementById('chartCanvas').getContext('2d');
            const chart = new Chart(ctxChart, {
                type: 'line', data: { labels: hX, datasets: [{ label: 'Presión (mbar)', data: hY, borderColor: '#1f77b4', borderWidth: 2, pointRadius: 0, tension: 0.1 }] },
                options: { animation: false, scales: { x: { title: { display: true, text: 'Tiempo (s)' } }, y: { type: 'logarithmic', min: 1e-12, max: 2000, ticks: { callback: v => v.toExponential(1) } } } }
            });

            let particles = [];
            for(let i = 0; i < 200; i++) particles.push({ x: 210 + Math.random()*180, y: 50 + Math.random()*70, vx: (Math.random()-0.5)*3, vy: (Math.random()-0.5)*3 });

            function drawValve(ctx, x, y, isOpen) {
                ctx.fillStyle = isOpen ? '#00e5ff' : '#d62728';
                ctx.beginPath(); ctx.moveTo(x-10, y-10); ctx.lineTo(x+10, y+10); ctx.lineTo(x+10, y-10); ctx.lineTo(x-10, y+10); ctx.closePath(); ctx.fill();
            }

            const ctxSchema = document.getElementById('schemaCanvas').getContext('2d');
            function renderLoop() {
                ctxSchema.clearRect(0, 0, 600, 250);
                let fM = els.bmec.checked && els.vmec.checked, fT = els.btur.checked && els.vtur.checked, fI = els.bion.checked && els.vion.checked;

                ctxSchema.textAlign = 'center';
                ctxSchema.lineWidth = 6; ctxSchema.strokeStyle = fM ? '#00e5ff' : '#999'; ctxSchema.beginPath(); ctxSchema.moveTo(300, 100); ctxSchema.lineTo(100, 100); ctxSchema.stroke();
                ctxSchema.lineWidth = 10; ctxSchema.strokeStyle = fT ? '#00e5ff' : '#999'; ctxSchema.beginPath(); ctxSchema.moveTo(300, 130); ctxSchema.lineTo(300, 200); ctxSchema.stroke();
                ctxSchema.lineWidth = 6; ctxSchema.strokeStyle = fI ? '#00e5ff' : '#999'; ctxSchema.beginPath(); ctxSchema.moveTo(300, 100); ctxSchema.lineTo(500, 100); ctxSchema.stroke();

                drawValve(ctxSchema, 200, 100, els.vmec.checked); drawValve(ctxSchema, 300, 160, els.vtur.checked); drawValve(ctxSchema, 400, 100, els.vion.checked);

                ctxSchema.lineWidth = 3; ctxSchema.strokeStyle = '#333'; ctxSchema.strokeRect(200, 40, 200, 90);
                ctxSchema.fillStyle = '#333'; ctxSchema.font = 'bold 16px Arial'; ctxSchema.fillText("CÁMARA", 300, 30);

                let logP = Math.log10(P); let targetP = Math.max(0, Math.floor(((logP + 12) / 15) * 200));
                ctxSchema.fillStyle = '#1f77b4';
                for(let i = 0; i < targetP; i++) {
                    let p = particles[i]; p.x += p.vx; p.y += p.vy;
                    if(p.x <= 205 || p.x >= 395) p.vx *= -1; if(p.y <= 45 || p.y >= 125) p.vy *= -1;
                    ctxSchema.beginPath(); ctxSchema.arc(p.x, p.y, 2.5, 0, Math.PI*2); ctxSchema.fill();
                }

                ctxSchema.fillStyle = '#1f77b4'; ctxSchema.fillRect(40, 70, 60, 60); ctxSchema.fillStyle = '#fff'; ctxSchema.font = '14px Arial'; ctxSchema.fillText("MEC", 70, 105);
                ctxSchema.fillStyle = '#2ca02c'; ctxSchema.fillRect(260, 200, 80, 40); ctxSchema.fillStyle = '#fff'; ctxSchema.fillText("TURBO", 300, 225);
                ctxSchema.fillStyle = '#9467bd'; ctxSchema.fillRect(500, 70, 60, 60); ctxSchema.fillStyle = '#fff'; ctxSchema.fillText("IÓNICA", 530, 105);
                ctxSchema.fillStyle = '#ff7f0e'; ctxSchema.fillRect(400, -5, 40, 45); ctxSchema.fillStyle = '#fff'; ctxSchema.font = '12px Arial'; ctxSchema.fillText("TSP", 420, 20);

                ctxSchema.fillStyle = '#d62728'; ctxSchema.beginPath(); ctxSchema.arc(230, 40, 10, 0, 2*Math.PI); ctxSchema.fill(); ctxSchema.fillStyle = '#333'; ctxSchema.fillText("Pirani", 230, 20);
                ctxSchema.fillStyle = els.scat.checked ? '#9467bd' : '#d62728'; ctxSchema.beginPath(); ctxSchema.arc(370, 40, 10, 0, 2*Math.PI); ctxSchema.fill(); ctxSchema.fillStyle = '#333'; ctxSchema.fillText("Cátodo", 370, 20);

                requestAnimationFrame(renderLoop);
            }

            function fail(msg) { state = "FAIL"; els.aB.innerHTML = msg; els.aB.style.display = "block"; Object.values(els).forEach(el => { if(el.type === 'checkbox') el.disabled = true; }); }
            
            function resetSim() {
                P = 1013.0; t = 0; state = "OK"; hX.length = 0; hY.length = 0; hX.push(0); hY.push(1013.0);
                els.aB.style.display = "none"; els.sB.style.display = "none";
                Object.values(els).forEach(el => { if(el.type === 'checkbox') { el.checked = false; el.disabled = false; }});
                updateDisplays(); chart.update();
            }

            function updateDisplays() {
                let pStr = P.toExponential(1);
                els.pD.innerHTML = (P >= 1e-4) ? pStr + " mbar" : "< 1.0e-4 mbar"; els.pD.style.color = (P >= 1e-4) ? "#333" : "#ccc";
                els.cD.innerHTML = (els.scat.checked && state !== "FAIL") ? "Cátodo Frío: <strong style='color:#9467bd'>" + pStr + " mbar</strong>" : "Cátodo Frío: APAGADO";
            }

            Object.values(els).forEach(el => { if(el && el.type === 'checkbox') el.addEventListener('change', updateDisplays); });

            setInterval(() => {
                if (state !== "OK") return;
                let pP = P;
                if (els.scat.checked && pP > 1e-2) return fail("💥 SENSOR QUEMADO: Cátodo frío a presión alta.");
                if (els.btur.checked && els.vtur.checked && pP > 1e-1) return fail("💥 TURBO DESTRUIDA: Fricción viscosa.");
                if (els.bion.checked && els.vion.checked && pP > 1e-5) return fail("💥 IÓNICA QUEMADA: Arco eléctrico.");
                if (els.btsp.checked && pP > 1e-7) return fail("💥 TSP FUNDIDA: Oxidación.");

                let Seff = 0; let Pobj = 1013.0;
                if (els.btsp.checked) { Seff = 500; Pobj = 1e-11; } else if (els.bion.checked && els.vion.checked) { Seff = 50; Pobj = 1e-10; } else if (els.btur.checked && els.vtur.checked) { Seff = 200; Pobj = 1e-9; } else if (els.bmec.checked && els.vmec.checked) { Seff = 5; Pobj = 1e-3; }
                if (Seff === 0 && P < 1013.0) { Seff = -0.1; Pobj = 1013.0; }

                let dt = 0.5;
                if (Math.abs(P - Pobj) > Pobj * 0.01) {
                    P = Math.max(1e-12, Math.min(Pobj + (P - Pobj) * Math.exp(-(Seff/50)*dt), 1013.0));
                    t += dt; hX.push(t.toFixed(1)); hY.push(P);
                    if(hX.length > 100) { hX.shift(); hY.shift(); }
                    chart.update(); updateDisplays();
                    if (P <= 1.01e-11 && els.sB.style.display !== "block") els.sB.style.display = "block";
                }
            }, 100);

            requestAnimationFrame(renderLoop);
        </script>
        </body>
        </html>
        """
        components.html(html_evac, height=750)

    # ==========================================
    # PESTAÑA 3: PROCESO AVANZADO (MEZCLA Y PLASMA)
    # ==========================================
    with t3:
        st.header("Laboratorio de Mezcla de Gases y Plasma Multicomponente")
        st.markdown("Experimenta con **Argón, Nitrógeno, Oxígeno e Hidrógeno**. Observa cómo la adición de Hidrógeno desestabiliza la presión rápidamente. Mantén la presión entre **1.0e-3 y 1.0e-2 mbar** para encender el plasma.")

        # PREGUNTA DE CONTROL
        with st.expander("📝 Pregunta de Control: Dinámica de Gases (Requerida para el reporte)", expanded=True):
            with st.form("form_plasma"):
                st.write("**Al inyectar Hidrógeno ($H_2$) en la cámara, notarás que la presión se desestabiliza mucho más rápido que con el Argón. ¿A qué se debe este fenómeno físico?**")
                ans_plasma = st.radio("Opciones:", [
                    "El Hidrógeno reacciona químicamente con las paredes de la cámara instantáneamente.",
                    "El Hidrógeno tiene una masa molecular mucho menor, lo que le confiere una altísima movilidad térmica (difusividad).",
                    "El Hidrógeno congela la bomba turbomolecular."
                ], index=None, label_visibility="collapsed")
                
                if st.form_submit_button("Guardar Respuesta"):
                    if ans_plasma == "El Hidrógeno tiene una masa molecular mucho menor, lo que le confiere una altísima movilidad térmica (difusividad).":
                        st.session_state.q_plasma_correct = True
                        st.success("¡Correcto! Respuesta guardada para el reporte.")
                    else:
                        st.session_state.q_plasma_correct = False
                        st.error("❌ Incorrecto.")
                        st.info("💡 **Fundamento Físico:** Según la teoría cinética de los gases, la velocidad térmica media de una molécula es inversamente proporcional a la raíz cuadrada de su masa molecular ($v_{rms} \propto 1/\sqrt{M}$). El Hidrógeno ($H_2$) tiene una masa de $\\approx 2$ g/mol, mientras que el Argón ($Ar$) pesa $\\approx 40$ g/mol. Por lo tanto, las moléculas de hidrógeno se mueven mucho más rápido, difundiéndose y cambiando la presión de la cámara casi instantáneamente, lo que hace que estabilizar su flujo sea un reto en el control PID de la vida real.")

        html_mezcla = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: 'Segoe UI', sans-serif; padding: 10px; background: #fff; margin: 0;}
                .grid { display: grid; grid-template-columns: 350px 1fr; gap: 20px; }
                .controls { background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #ddd; }
                .display { font-size: 2em; font-family: monospace; text-align: center; color: #333; margin-bottom: 10px; background: #fff; padding: 10px; border-radius: 5px; border: 1px solid #ccc;}
                .slider-group { margin-bottom: 10px; padding: 8px; background: #fff; border-radius: 5px; border: 1px solid #eee; border-left: 4px solid #ccc;}
                .slider-group.ar { border-left-color: #9467bd; } .slider-group.n2 { border-left-color: #ff6432; } .slider-group.o2 { border-left-color: #64c8ff; } .slider-group.h2 { border-left-color: #e682ff; }
                .slider-label { display: flex; justify-content: space-between; font-weight: bold; font-size: 0.9em; margin-bottom: 5px;}
                input[type=range] { width: 100%; cursor: pointer; }
                .chamber { height: 250px; border: 4px solid #333; border-radius: 10px; position: relative; background: #111; margin-bottom: 15px; overflow: hidden;}
                .plasma { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; mix-blend-mode: screen; }
                .btn { padding: 15px; border-radius: 5px; border: none; width: 100%; font-weight: bold; color: white; background: #666; cursor: not-allowed; transition: 0.3s;}
                .btn.ready { background: #2ca02c; cursor: pointer; box-shadow: 0 0 10px #2ca02c;} .btn.active { background: #d62728; cursor: pointer; box-shadow: 0 0 15px #d62728;}
                .alert { color: #d62728; font-weight: bold; text-align: center; margin-top: 10px; min-height: 20px;}
            </style>
        </head>
        <body>
        <div class="grid">
            <div class="controls">
                <div class="display" id="p-text">1.0e-8 mbar</div>
                <div class="slider-group ar"><div class="slider-label"><span style="color:#9467bd">Argón (Ar)</span> <span id="v-ar">0 sccm</span></div><input type="range" id="q-ar" min="0" max="100" value="0"></div>
                <div class="slider-group n2"><div class="slider-label"><span style="color:#ff6432">Nitrógeno (N2)</span> <span id="v-n2">0 sccm</span></div><input type="range" id="q-n2" min="0" max="100" value="0"></div>
                <div class="slider-group o2"><div class="slider-label"><span style="color:#64c8ff">Oxígeno (O2)</span> <span id="v-o2">0 sccm</span></div><input type="range" id="q-o2" min="0" max="100" value="0"></div>
                <div class="slider-group h2"><div class="slider-label"><span style="color:#e682ff">Hidrógeno (H2)</span> <span id="v-h2">0 sccm</span></div><input type="range" id="q-h2" min="0" max="100" value="0"></div>
                <hr>
                <div class="slider-label"><span>Bomba Turbo (S)</span> <span id="v-pump">250 L/s</span></div><input type="range" id="s-pump" min="10" max="500" value="250">
                <button id="ignite" class="btn" style="margin-top: 15px;">PLASMA APAGADO</button>
                <div id="alert-msg" class="alert"></div>
            </div>
            <div>
                <div class="chamber">
                    <canvas id="particleCanvas" width="800" height="250" style="position:absolute; top:0; left:0; width:100%; height:100%;"></canvas>
                    <div id="plasma-glow" class="plasma"></div>
                </div>
                <canvas id="live-chart" height="200" style="width:100%; background:#fff; border-radius:5px; border:1px solid #ccc;"></canvas>
            </div>
        </div>
        <script>
            let P = 1.0e-8, t = 0, isPlasmaOn = false, hX = [0], hY = [1e-8];
            const inputs = { Ar: document.getElementById('q-ar'), N2: document.getElementById('q-n2'), O2: document.getElementById('q-o2'), H2: document.getElementById('q-h2'), Pump: document.getElementById('s-pump') };
            const pText = document.getElementById('p-text'), btnIgnite = document.getElementById('ignite'), alertMsg = document.getElementById('alert-msg'), plasmaGlow = document.getElementById('plasma-glow');
            const colors = { Ar: [148, 103, 189], N2: [255, 100, 50], O2: [100, 200, 255], H2: [230, 130, 255] };

            const ctxChart = document.getElementById('live-chart').getContext('2d');
            const chart = new Chart(ctxChart, {
                type: 'line', data: { labels: hX, datasets: [{ label: 'Presión Dinámica (mbar)', data: hY, borderColor: '#333', backgroundColor: 'rgba(0,0,0,0.1)', fill: true, pointRadius: 0, tension: 0.1 }] },
                options: { animation: false, scales: { x: { title: {display: true, text: 'Tiempo'} }, y: { type: 'logarithmic', min: 1e-9, max: 1e-1, ticks: { callback: v => v.toExponential(1) } } },
                    plugins: { annotation: { annotations: { box1: { type: 'box', yMin: 1e-3, yMax: 1e-2, backgroundColor: 'rgba(44, 160, 44, 0.1)', borderWidth: 0 } } } } }
            });

            const pCtx = document.getElementById('particleCanvas').getContext('2d');
            let particles = [];
            
            function updateParticles(targetCount, gasFractions) {
                while(particles.length < targetCount) particles.push({ x: Math.random()*800, y: Math.random()*250, vx: (Math.random()-0.5)*4, vy: (Math.random()-0.5)*4, gas: 'Ar' });
                while(particles.length > targetCount) particles.pop();
                let idx = 0;
                for(let gas in gasFractions) {
                    let count = Math.round(targetCount * gasFractions[gas]);
                    for(let i=0; i<count && idx < particles.length; i++) { particles[idx].gas = gas; idx++; }
                }
            }

            function drawParticles() {
                pCtx.clearRect(0, 0, 800, 250);
                for(let i=0; i<particles.length; i++) {
                    let p = particles[i]; p.x += p.vx; p.y += p.vy;
                    let speedMult = (p.gas === 'H2') ? 2.5 : 1.0;
                    p.x += p.vx * speedMult * 0.5; p.y += p.vy * speedMult * 0.5;
                    if(p.x < 0 || p.x > 800) p.vx *= -1; if(p.y < 0 || p.y > 250) p.vy *= -1;
                    let c = colors[p.gas]; pCtx.fillStyle = `rgba(${c[0]}, ${c[1]}, ${c[2]}, 0.8)`;
                    pCtx.beginPath(); pCtx.arc(p.x, p.y, 3, 0, Math.PI*2); pCtx.fill();
                }
                requestAnimationFrame(drawParticles);
            }
            drawParticles();

            setInterval(() => {
                let qAr = parseInt(inputs.Ar.value), qN2 = parseInt(inputs.N2.value), qO2 = parseInt(inputs.O2.value), qH2 = parseInt(inputs.H2.value), S = parseInt(inputs.Pump.value);
                document.getElementById('v-ar').innerText = qAr + " sccm"; document.getElementById('v-n2').innerText = qN2 + " sccm"; document.getElementById('v-o2').innerText = qO2 + " sccm"; document.getElementById('v-h2').innerText = qH2 + " sccm"; document.getElementById('v-pump').innerText = S + " L/s";

                let totalSccm = qAr + qN2 + qO2 + qH2;
                let targetP = 1.0e-8 + ((totalSccm * 0.0166) / S);
                let fractionH2 = totalSccm > 0 ? (qH2 / totalSccm) : 0;
                P = P + (targetP - P) * (0.1 + (fractionH2 * 0.15));
                pText.innerText = P.toExponential(1) + " mbar";

                let inRange = (P >= 1e-3 && P <= 1e-2);
                if (isPlasmaOn) {
                    if (!inRange) {
                        isPlasmaOn = false; plasmaGlow.style.display = "none";
                        alertMsg.innerText = P > 1e-2 ? "⚠️ Plasma Extinguido: Exceso de presión." : "⚠️ Plasma Extinguido: Falta de gas.";
                        btnIgnite.className = "btn"; btnIgnite.innerText = "PLASMA APAGADO";
                    } else {
                        let r=0, g=0, b=0;
                        if(totalSccm > 0) {
                            r = (qAr*colors.Ar[0] + qN2*colors.N2[0] + qO2*colors.O2[0] + qH2*colors.H2[0]) / totalSccm;
                            g = (qAr*colors.Ar[1] + qN2*colors.N2[1] + qO2*colors.O2[1] + qH2*colors.H2[1]) / totalSccm;
                            b = (qAr*colors.Ar[2] + qN2*colors.N2[2] + qO2*colors.O2[2] + qH2*colors.H2[2]) / totalSccm;
                        }
                        plasmaGlow.style.background = `radial-gradient(circle, rgba(${r},${g},${b}, 0.9) 0%, rgba(${r},${g},${b}, 0) 70%)`;
                    }
                } else {
                    if (inRange && totalSccm > 0) { btnIgnite.className = "btn ready"; btnIgnite.innerText = "INICIAR PLASMA"; alertMsg.innerText = "✓ Condiciones óptimas"; }
                    else { btnIgnite.className = "btn"; btnIgnite.innerText = "FUERA DE RANGO"; if(!inRange && totalSccm > 0) alertMsg.innerText = ""; }
                }

                btnIgnite.onclick = () => {
                    if (inRange && !isPlasmaOn) { isPlasmaOn = true; plasmaGlow.style.display = "block"; btnIgnite.className = "btn active"; btnIgnite.innerText = "APAGAR PLASMA"; alertMsg.innerText = "🔥 Plasma Estable"; }
                    else if (isPlasmaOn) { isPlasmaOn = false; plasmaGlow.style.display = "none"; btnIgnite.className = "btn ready"; btnIgnite.innerText = "INICIAR PLASMA"; alertMsg.innerText = "Plasma apagado."; }
                };

                t += 0.5; hX.push(t.toFixed(1)); hY.push(P);
                if(hX.length > 80) { hX.shift(); hY.shift(); }
                chart.update();

                let logP = Math.log10(P); let pCount = Math.max(0, Math.floor(((logP + 8) / 7) * 300));
                updateParticles(pCount, { Ar: totalSccm > 0 ? qAr/totalSccm : 0, N2: totalSccm > 0 ? qN2/totalSccm : 0, O2: totalSccm > 0 ? qO2/totalSccm : 0, H2: totalSccm > 0 ? qH2/totalSccm : 0 });

            }, 100);
        </script>
        </body>
        </html>
        """
        components.html(html_mezcla, height=650)

    # ==========================================
    # PESTAÑA 4: REPORTE FINAL ACTUALIZADO
    # ==========================================
    with t4:
        st.header("📊 Reporte de Resultados del Seminario")
        st.write("Boletín de evaluación oficial para la Universidad Antonio Nariño.")
        
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2>UNIVERSIDAD ANTONIO NARIÑO</h2>", unsafe_allow_html=True)
        st.markdown(f"### Certificación en Tecnología de Vacío")
        st.divider()
        st.markdown(f"**Operador / Estudiante:** {st.session_state.student_name}")
        st.markdown(f"**Código ID:** {st.session_state.student_id}")
        
        st.divider()
        st.markdown("### 1. Desempeño Teórico")
        if st.session_state.exam_taken:
            st.markdown(f"**Calificación del Examen:** {st.session_state.exam_score} / 15")
        else:
            st.warning("⚠️ Examen teórico pendiente (Pestaña 1).")

        st.markdown("### 2. Evaluaciones Prácticas")
        
        # Evaluar pregunta de evacuación
        if st.session_state.q_evac_correct is True:
            st.success("✅ **Simulador Evacuación:** Pregunta de control respondida correctamente.")
        elif st.session_state.q_evac_correct is False:
            st.error("❌ **Simulador Evacuación:** Pregunta de control respondida incorrectamente.")
        else:
            st.warning("⚠️ **Simulador Evacuación:** Pregunta de control pendiente (Pestaña 2).")
            
        # Evaluar pregunta de plasma
        if st.session_state.q_plasma_correct is True:
            st.success("✅ **Simulador Plasma:** Pregunta de control respondida correctamente.")
        elif st.session_state.q_plasma_correct is False:
            st.error("❌ **Simulador Plasma:** Pregunta de control respondida incorrectamente.")
        else:
            st.warning("⚠️ **Simulador Plasma:** Pregunta de control pendiente (Pestaña 3).")

        st.divider()
        
        # LÓGICA DE APROBACIÓN FINAL
        if st.session_state.exam_taken and st.session_state.exam_score >= 13 and st.session_state.q_evac_correct and st.session_state.q_plasma_correct:
            st.success("ESTADO: **APROBADO PARA OPERACIÓN UHV** ✅")
            st.markdown("El estudiante superó la evaluación teórica y demostró comprensión de los fenómenos físicos en los simuladores dinámicos.")
        else:
            st.error("ESTADO: **NO CERTIFICADO (REPROBADO/INCOMPLETO)** ❌")
            st.markdown("Para aprobar, el estudiante debe obtener al menos 13/15 en el examen teórico y responder correctamente ambas preguntas de control en los simuladores.")
            
        st.divider()
        st.caption("Documento generado por el Simulador UHV | 2026")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Cerrar Sesión", use_container_width=True):
            # Reiniciar todas las variables
            st.session_state.registered = False
            st.session_state.student_name = ""
            st.session_state.student_id = ""
            st.session_state.exam_score = 0
            st.session_state.exam_taken = False
            st.session_state.q_evac_correct = None
            st.session_state.q_plasma_correct = None
            st.rerun()