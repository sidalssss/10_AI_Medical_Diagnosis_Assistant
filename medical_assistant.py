import numpy as np
from datetime import datetime

class AIMedicalAssistant:
    """
    Kapsamlı Tıbbi Teşhis Destek Sistemi.
    Belirti analizi ve Görüntüleme bulgularını birleştirerek olasılıksal rapor üretir.
    """
    def __init__(self):
        self.knowledge_base = {
            "belirtiler": {
                "öksürük": {"olasilik": 0.4, "hastaliklar": ["Bronşit", "Pnömoni", "Grip"]},
                "ateş": {"olasilik": 0.6, "hastaliklar": ["Enfeksiyon", "Grip", "Sıtma"]},
                "nefes_darlığı": {"olasilik": 0.8, "hastaliklar": ["Pnömoni", "KOAH", "Kalp Yetmezliği"]}
            }
        }
        self.report_id = 0

    def analyze_symptoms(self, symptom_list):
        """Belirtilere göre olası hastalıkları skorlar."""
        scores = {}
        for s in symptom_list:
            if s in self.knowledge_base["belirtiler"]:
                data = self.knowledge_base["belirtiler"][s]
                for h in data["hastaliklar"]:
                    scores[h] = scores.get(h, 0) + data["olasilik"]
        
        # Skorları normalize et (0-100 arası)
        total = sum(scores.values()) if scores else 1
        sorted_results = sorted(
            [(k, round((v/total)*100, 2)) for k, v in scores.items()], 
            key=lambda x: x[1], 
            reverse=True
        )
        return sorted_results

    def generate_report(self, patient_name, symptoms, imaging_results=None):
        """Profesyonel tıbbi analiz raporu oluşturur."""
        self.report_id += 1
        diagnoses = self.analyze_symptoms(symptoms)
        
        report = f"""
        ============================================================
        SIDAL AI MEDICAL DIAGNOSIS REPORT #{self.report_id}
        ============================================================
        Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Hasta Adı: {patient_name.upper()}
        Bildirilen Belirtiler: {", ".join(symptoms)}
        
        ANALİZ SONUÇLARI (OLASILIK SIRALAMASI):
        ------------------------------------------------------------
        """
        for rank, (disease, prob) in enumerate(diagnoses, 1):
            report += f"{rank}. {disease}: %{prob}
"
        
        report += "
ÖNERİ: Lütfen sonuçları kesin tanı için bir uzman doktor ile paylaşın."
        report += "
============================================================
"
        return report

if __name__ == "__main__":
    print("Sidal AI - Medical Assistant Modülü Başlatılıyor...")
    assistant = AIMedicalAssistant()
    
    # Simülasyon Senaryosu
    patient = "Sidal Sınırtaş"
    reported_symptoms = ["öksürük", "ateş", "nefes_darlığı"]
    
    final_report = assistant.generate_report(patient, reported_symptoms)
    print(final_report)
