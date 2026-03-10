import numpy as np
import logging
from typing import Dict, List, Tuple
from datetime import datetime

# Enterprise Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MedicalAssistant")

class BayesianDiagnosticEngine:
    """
    Bayesian çıkarım mantığına dayalı akıllı tıbbi teşhis asistanı.
    Belirtiler (Evidence) ve Hastalıklar (Hypotheses) arasındaki olasılıksal ilişkiyi analiz eder.
    """
    def __init__(self):
        # Olasılıksal Bilgi Tabanı (P(Belirti | Hastalık))
        self.priors = {
            "Grip": 0.15,
            "Pnömoni": 0.05,
            "Bronşit": 0.08,
            "KOAH": 0.04,
            "Sıtma": 0.02
        }
        self.likelihoods = {
            "ateş": {"Grip": 0.85, "Pnömoni": 0.9, "Bronşit": 0.4, "KOAH": 0.2, "Sıtma": 0.95},
            "öksürük": {"Grip": 0.7, "Pnömoni": 0.85, "Bronşit": 0.9, "KOAH": 0.9, "Sıtma": 0.2},
            "nefes_darlığı": {"Grip": 0.1, "Pnömoni": 0.9, "Bronşit": 0.6, "KOAH": 0.95, "Sıtma": 0.3}
        }

    def infer_diagnosis(self, symptoms: List[str]) -> List[Tuple[str, float]]:
        """Bayes Teoremini kullanarak sonsal olasılıkları (Posterior) hesaplar."""
        posteriors = self.priors.copy()
        
        for symptom in symptoms:
            if symptom in self.likelihoods:
                # P(H | E) = P(E | H) * P(H) / P(E) -> Basitleştirilmiş Normalize Edilmiş Form
                for disease in posteriors:
                    posteriors[disease] *= self.likelihoods[symptom].get(disease, 0.01)
        
        # Normalizasyon
        total = sum(posteriors.values())
        if total == 0: return []
        
        normalized = [(d, round((v / total) * 100, 2)) for d, v in posteriors.items()]
        return sorted(normalized, key=lambda x: x[1], reverse=True)

class MedicalReportGenerator:
    """Analiz sonuçlarını profesyonel tıbbi rapor formatına dönüştürür."""
    @staticmethod
    def create_report(patient_name: str, symptoms: List[str], diagnoses: List[Tuple[str, float]]) -> str:
        report = f"""
        ============================================================
        SIDAL AI - ENTERPRISE MEDICAL ANALYSIS REPORT
        ============================================================
        Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Hasta Bilgisi: {patient_name.upper()}
        Belirtiler: {", ".join(symptoms).title()}
        
        OLASILIKSAL TEŞHİS ANALİZİ:
        ------------------------------------------------------------
        """
        for i, (disease, prob) in enumerate(diagnoses, 1):
            bar = "█" * int(prob // 5)
            report += f"{i}. {disease:<15} | %{prob:>5} | {bar}\n"
        
        report += "\nKRİTİK UYARI: Bu rapor yapay zeka tarafından desteklenen bir karar yardımcısıdır."
        report += "\nKesin teşhis için radyolojik bulgular ve doktor onayı zorunludur."
        report += "\n============================================================\n"
        return report

if __name__ == "__main__":
    logger.info("Medical Diagnostic Engine v3.0 [READY]")
    engine = BayesianDiagnosticEngine()
    
    # Simülasyon Senaryosu
    p_name = "Sidal Sınırtaş"
    s_list = ["ateş", "öksürük", "nefes_darlığı"]
    
    results = engine.infer_diagnosis(s_list)
    print(MedicalReportGenerator.create_report(p_name, s_list, results))
