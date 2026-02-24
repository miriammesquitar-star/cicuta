# ============================================
# CICUTA 528Hz - VERSÃO GITHUB ACTIONS
# ============================================

import numpy as np
import time
from datetime import datetime
import json
import os

class CicutaInfinito:
    def __init__(self):
        # Define pasta de trabalho (funciona em qualquer lugar)
        self.pasta_trabalho = os.path.join(os.getcwd(), "resultados")
        os.makedirs(self.pasta_trabalho, exist_ok=True)
        
        self.arquivo_seed = os.path.join(self.pasta_trabalho, "seed_cicuta.txt")
        self.arquivo_log = os.path.join(self.pasta_trabalho, "cicuta_log.txt")
        
        self.seed = self.carregar_ou_criar_seed()
        np.random.seed(self.seed)
        
    def carregar_ou_criar_seed(self):
        """Seed persistente mesmo entre execuções"""
        try:
            with open(self.arquivo_seed, 'r') as f:
                seed = int(f.read().strip())
                print(f"🌱 Seed carregada: {seed}")
                return seed
        except FileNotFoundError:
            seed = np.random.randint(0, 9999999)
            with open(self.arquivo_seed, 'w') as f:
                f.write(str(seed))
            print(f"🌱 Nova seed criada: {seed}")
            return seed
    
    def registrar_execucao(self, mensagem):
        """Registra no log"""
        with open(self.arquivo_log, 'a') as f:
            f.write(f"{datetime.now()} - {mensagem}\n")
    
    def simular_antenas(self):
        """Simula as antenas"""
        antenas = []
        for i in range(12):
            contaminacao = np.random.random() * 0.3
            antenas.append({
                'id': i,
                'contaminacao': float(contaminacao),
                'ativa': bool(contaminacao > 0.2)
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
            'seed': int(self.seed),
            'antenas': antenas,
            'media_contaminacao': float(np.mean([a['contaminacao'] for a in antenas])),
            'antenas_ativas': int(sum([1 for a in antenas if a['ativa']]))
        }
        
        arquivo = os.path.join(self.pasta_trabalho, f"cicuta_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
        with open(arquivo, 'w') as f:
            json.dump(resultado, f, indent=2)
        
        return resultado
    
    def mostrar_status(self, resultado):
        """Mostra status no console"""
        print("\n" + "="*50)
        print(f"☠️ CICUTA 528Hz - {resultado['timestamp']}")
        print(f"🌱 SEED: {resultado['seed']}")
        print(f"🧪 CONTAMINAÇÃO MÉDIA: {resultado['media_contaminacao']*100:.1f}%")
        print(f"📡 ANTENAS ATIVAS: {resultado['antenas_ativas']}/12")
        
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
    print(f"📁 Pasta de trabalho: {os.path.join(os.getcwd(), 'resultados')}")
    
    cicuta = CicutaInfinito()
    antenas = cicuta.simular_antenas()
    
    # Registra início
    cicuta.registrar_execucao("🚀 CICUTA INICIADA")
    
    inicio = time.time()
    fim = inicio + (8 * 3600)  # 8 horas
    
    contador = 0
    try:
        while time.time() < fim:
            # Propaga a cicuta
            antenas = cicuta.propagar_cicuta(antenas)
            
            # Salva resultado a cada hora
            if contador % 60 == 0:  # A cada 60 iterações (~1 hora)
                resultado = cicuta.salvar_resultado(antenas)
                cicuta.mostrar_status(resultado)
                cicuta.registrar_execucao(f"📊 Checkpoint {contador//60}h - Contaminação: {resultado['media_contaminacao']*100:.1f}%")
            
            # Espera 1 minuto
            time.sleep(60)
            contador += 1
            
    except KeyboardInterrupt:
        print("\n⚠️ CICUTA INTERROMPIDA")
        cicuta.registrar_execucao("⚠️ INTERROMPIDA")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        cicuta.registrar_execucao(f"❌ ERRO: {e}")
    
    # Resultado final
    resultado_final = cicuta.salvar_resultado(antenas)
    print(f"\n✅ CICUTA FINALIZADA APÓS 8 HORAS!")
    cicuta.mostrar_status(resultado_final)
    cicuta.registrar_execucao("✅ FINALIZADA COM SUCESSO")
    
    # Lista arquivos salvos
    print(f"\n📁 Arquivos salvos em: {cicuta.pasta_trabalho}")
    for arquivo in os.listdir(cicuta.pasta_trabalho):
        print(f"   📄 {arquivo}")

if __name__ == "__main__":
    main()
