import requests
import json
import os
from config import WPP_API_URL, SESSION_NAME

ADVERTENCIAS_FILE = "advertencias.json"

def cargar_advertencias():
    if not os.path.exists(ADVERTENCIAS_FILE):
        return {}
    with open(ADVERTENCIAS_FILE, "r") as f:
        return json.load(f)

def guardar_advertencias(data):
    with open(ADVERTENCIAS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def enviar_mensaje(numero, mensaje):
    url = f"{WPP_API_URL}/{SESSION_NAME}/send-message"
    payload = {
        "number": numero,
        "message": mensaje
    }
    try:
        requests.post(url, json=payload)
    except:
        print("❌ Error enviando mensaje.")

def procesar_comando(numero, mensaje):
    advertencias = cargar_advertencias()
    partes = mensaje.strip().split()
    comando = partes[0].lower()

    if comando == ".menu":
        texto = (
            "✨ *Menú del Bot* ✨\n\n"
            "📌 .advertencia @usuario — Dar advertencia\n"
            "📋 .advertencias — Ver advertencias\n"
            "🧹 .resetadvertencias — Borrar advertencias\n"
            "🔊 .mencionar — Mencionar a todos\n"
            "❌ .echar @usuario — Expulsar usuario (solo texto)\n"
        )
        enviar_mensaje(numero, texto)

    elif comando == ".advertencia":
        if len(partes) < 2:
            enviar_mensaje(numero, "❗ Usa: .advertencia @usuario")
            return
        usuario = partes[1]
        advertencias[usuario] = advertencias.get(usuario, 0) + 1
        guardar_advertencias(advertencias)
        enviar_mensaje(numero, f"🚫 {usuario} tiene {advertencias[usuario]} advertencia(s).")

    elif comando == ".advertencias":
        if not advertencias:
            enviar_mensaje(numero, "✅ No hay advertencias registradas.")
            return
        texto = "📋 *Advertencias:*\n"
        for user, count in advertencias.items():
            texto += f"• {user}: {count}\n"
        enviar_mensaje(numero, texto)

    elif comando == ".resetadvertencias":
        guardar_advertencias({})
        enviar_mensaje(numero, "🧹 Advertencias reiniciadas.")

    elif comando == ".mencionar":
        enviar_mensaje(numero, "👥 [Mención simulada] Hola a todos.")

    elif comando == ".echar":
        if len(partes) < 2:
            enviar_mensaje(numero, "❗ Usa: .echar @usuario")
            return
        usuario = partes[1]
        enviar_mensaje(numero, f"👢 {usuario} fue *expulsado* (solo texto, no real).")

    else:
        enviar_mensaje(numero, "❌ Comando no reconocido. Usa .menu")

if __name__ == "__main__":
    print("📥 Simulando recepción de comandos.")
    while True:
        numero = input("📱 Número (ej: 5511999999999@c.us): ")
        mensaje = input("💬 Mensaje recibido: ")
        procesar_comando(numero, mensaje)
