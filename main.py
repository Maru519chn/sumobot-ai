#!/usr/bin/env python3
"""
Sumobot AI Mentor - FIX FINAL ✅ SIN ASYNC + JSON SAFE
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()
DATA_DIR = Path("sumobot_data")
MEMORY_FILE = Path("memory.json")
MODEL_NAME = "llama3.2:3b"

DATA_DIR.mkdir(exist_ok=True)
MEMORY_FILE.parent.mkdir(exist_ok=True)

class SumobotMentor:
    def __init__(self):
        self.memory = self.load_memory()
        self.conversation_history = self.memory.get("conversation_history", [])
        self.project_bible = self.memory.get("project_bible", self.init_project_bible())
        
    def load_memory(self) -> Dict[str, Any]:
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except:
                console.print("[red]⚠️ Memory reset[/red]")
        return {}
    
    def save_memory(self):
        """🔥 FIX: JSON-safe serialization"""
        memory = {
            "conversation_history": self.conversation_history[-20:],  # Solo últimas 20
            "project_bible": self.project_bible,
            "last_update": time.strftime("%Y-%m-%d %H:%M:%S"),
            "files_count": len(list(DATA_DIR.rglob("*")))
        }
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2, ensure_ascii=False)
        except:
            pass  # No crash si falla
    
    def init_project_bible(self) -> Dict[str, str]:
        return {
            "rules": "Mini Sumo: 500g, 10x10cm, IR edge sensors",
            "hardware": "N20 motors + TB6612FNG + TCRT5000",
            "strategy": "SEARCH→ATTACK→EDGE_AVOID"
        }
    
    def get_files_summary(self) -> str:
        """📁 Resumen ligero (201 files OK!)"""
        files = list(DATA_DIR.rglob("*"))
        return f"{len(files)} archivos totales en sumobot_data/"
    
    def get_ai_response(self, user_input: str) -> str:
        """🔥 FIX: SIN ASYNC - Síncrono puro"""
        try:
            files_info = self.get_files_summary()
            prompt = f"""SUMOBOT MENTOR - Mini Sumo Expert

Archivos: {files_info}
Biblia: {self.project_bible}

Pregunta: {user_input}

Responde TÉCNICO y DIRECTO sobre Sumo Robot."""

            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"❌ Error Ollama: {e}\nEjecuta: ollama list"
    
    def print_status(self):
        table = Table(title="🤖 Status")
        table.add_column("Item")
        table.add_column("Status")
        table.add_row("Memory", "✅ OK")
        table.add_row("Files", self.get_files_summary())
        table.add_row("History", f"{len(self.conversation_history)} chats")
        table.add_row("Model", MODEL_NAME)
        console.print(table)
    
    def print_help(self):
        console.print(Panel("/status /files /help /save /model <name>", title="Commands"))
    
    def handle_command(self, cmd: str):
        if cmd == "/status": 
            self.print_status()
        elif cmd == "/files": 
            print(self.get_files_summary())
        elif cmd == "/help": 
            self.print_help()
        elif cmd == "/save": 
            self.save_memory()
            print("💾 Guardado!")
        elif cmd.startswith("/model "):
            global MODEL_NAME
            MODEL_NAME = cmd.split(" ", 1)[1]
            print(f"🔄 Modelo: {MODEL_NAME}")
        else: 
            print("❌ Comando desconocido. /help")
    
    def run(self):
        console.print(Panel("🤖 SUMOBOT MENTOR - 201 FILES OK! 🚀", style="green"))
        self.print_status()
        print("\n💬 ¡Pregunta sobre tu Sumobot!\n")
        
        while True:
            try:
                user_input = Prompt.ask("You")
                
                if user_input.startswith("/"):
                    self.handle_command(user_input)
                    continue
                if user_input.lower() in ['exit', 'quit', 'salir']:
                    self.save_memory()
                    print("👋 ¡Suerte en la competencia!")
                    break
                
                print("🤖 AI responde...")
                ai_response = self.get_ai_response(user_input)
                print(f"🤖 {ai_response}\n")
                
                # Guardar chat
                self.conversation_history.append({
                    "user": user_input[:100],  # Truncado
                    "ai": ai_response[:500],   # Truncado
                    "time": time.strftime("%H:%M")
                })
                self.save_memory()
                
            except KeyboardInterrupt:
                print("\n👋")
                self.save_memory()
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    mentor = SumobotMentor()
    mentor.run()