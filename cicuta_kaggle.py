# ============================================
# CICUTA 528Hz - VERSÃO KAGGLE
# ============================================

import numpy as np
import time
from datetime import datetime
import json
import os

class CicutaKaggle:
    def __init__(self):
        self.seed = self.carregar_ou_criar_seed()
        np.random.seed(self.seed)
        
    def carregar_ou_criar_seed(self):
        """Seed persistente mesmo entre execuções"""
        arquivo_seed = "/kaggle/working/seed_cicuta.txt"
        try:
            with open(arquivo_seed, 'r') as f:
                return int(f.read().strip())
        except:
            seed = np.random.randint(0, 9999999)
            with open(arquivo_seed, 'w') as f:
                f.write(str(seed))
            return seed
    
    def simular_antenas(self):
        """Simula as antenas (versão texto)"""
        antenas = []
        for i in range(12):
            contaminacao = np.random.random() * 0.3
            antenas.append({
                'id': i,
                'contaminacao': contaminacao,
                'ativa': contaminacao > 0.2
            })
        return antenas
    
    def propagar_cicuta(self, antenas):
        """Propaga a contaminação"""
        for i in range(len(antenas)):
            if antenas[i]['ativa']:
                antenas[i]['contaminacao'] = min(1.0, antenas[i]['contaminacao'] + 0.01)
                # Espalha pras vizinhas
                if i > 0:
                    antenas[i-1]['contaminacao'] = min(1.0, antenas[i-1]['contaminacao'] + 0.005)
                if i < len(antenas)-1:
                    antenas[i+1]['contaminacao'] = min(1.0, antenas[i+1]['contaminacao'] + 0.005)
        return antenas
    
    def salvar_resultado(self, antenas):
        """Salva estado atual"""
        resultado = {
            'timestamp': str(datetime.now()),
            'seed': self.seed,
            'antenas': antenas,
            'media_contaminacao': float(np.mean([a['contaminacao'] for a in antenas]))
        }
        
        arquivo = f"/kaggle/working/resultados/cicuta_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        os.makedirs("/kaggle/working/resultados", exist_ok=True)
        with open(arquivo, 'w') as f:
            json.dump(resultado, f, indent=2)
        
        return resultado
    
    def mostrar_status(self, resultado):
        """Mostra status bonitinho"""
        print("\n" + "="*50)
        print(f"☠️ CICUTA 528Hz - {resultado['timestamp']}")
        print(f"🌱 SEED: {resultado['seed']}")
        print(f"🧪 CONTAMINAÇÃO MÉDIA: {resultado['media_contaminacao']*100:.1f}%")
        print(f"📡 ANTENAS ATIVAS: {sum([1 for a in resultado['antenas'] if a['ativa']])}/12")
        
        # Barra de progresso
        barra = "█" * int(resultado['media_contaminacao'] * 20)
        barra += "░" * (20 - len(barra))
        print(f"📊 {barra}")
        print("="*50)

# ============================================
# MAIN - RODA POR 8 HORAS
# ============================================

def main():
    print("🚀 INICIANDO CICUTA NO GITHUB ACTIONS")
    
    cicuta = CicutaKaggle()
    antenas = cicuta.simular_antenas()
    
    inicio = time.time()
    fim = inicio + (8 * 3600)  # 8 horas
    
    contador = 0
    while time.time() < fim:
        # Propaga a cicuta
        antenas = cicuta.propagar_cicuta(antenas)
        
        # Salva resultado a cada hora
        if contador % 60 == 0:  # A cada 60 iterações (~1 hora)
            resultado = cicuta.salvar_resultado(antenas)
            cicuta.mostrar_status(resultado)
        
        # Espera 1 minuto
        time.sleep(60)
        contador += 1
    
    # Resultado final
    resultado_final = cicuta.salvar_resultado(antenas)
    print(f"\n✅ CICUTA FINALIZADA APÓS 8 HORAS!")
    cicuta.mostrar_status(resultado_final)

if __name__ == "__main__":
    main()
