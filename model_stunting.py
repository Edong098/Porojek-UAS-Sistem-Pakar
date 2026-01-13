class BayesianNetworkStunting:
    def __init__(self):
        pass

    def get_cpt_penyakit_given_lingkungan(self, lingkungan, penyakit_specific):
        # P(Penyakit Spesifik | Lingkungan)
        cpt = {
            'Baik':   {'Tidak Ada': 0.85, 'Jarang': 0.10, 'Sering Infeksi': 0.04, 'Sering Diare': 0.01}, 
            'Cukup':  {'Tidak Ada': 0.40, 'Jarang': 0.40, 'Sering Infeksi': 0.15, 'Sering Diare': 0.05},
            'Kurang': {'Tidak Ada': 0.05, 'Jarang': 0.15, 'Sering Infeksi': 0.30, 'Sering Diare': 0.50 } 
        }
        return cpt.get(lingkungan, {}).get(penyakit_specific, 0.25)

    def get_cpt_stunting_given_faktor_utama(self, pola_makan, penyakit_specific, stunting):
        # P(Stunting | Pola Makan, Riwayat Penyakit Spesifik)
        key = (pola_makan, penyakit_specific)
        
        cpt = {
            ('Kurang', 'Sering Diare'):   {'Rendah': 0.00, 'Sedang': 0.05, 'Tinggi': 0.95},
            ('Kurang', 'Sering Infeksi'): {'Rendah': 0.05, 'Sedang': 0.10, 'Tinggi': 0.85},
            ('Kurang', 'Jarang'):         {'Rendah': 0.10, 'Sedang': 0.40, 'Tinggi': 0.50},
            ('Kurang', 'Tidak Ada'):      {'Rendah': 0.20, 'Sedang': 0.60, 'Tinggi': 0.20},

            ('Cukup', 'Sering Diare'):    {'Rendah': 0.05, 'Sedang': 0.25, 'Tinggi': 0.70},
            ('Cukup', 'Sering Infeksi'):  {'Rendah': 0.10, 'Sedang': 0.40, 'Tinggi': 0.50},
            ('Cukup', 'Jarang'):          {'Rendah': 0.30, 'Sedang': 0.50, 'Tinggi': 0.20},
            ('Cukup', 'Tidak Ada'):       {'Rendah': 0.60, 'Sedang': 0.35, 'Tinggi': 0.05},

            ('Baik', 'Sering Diare'):     {'Rendah': 0.20, 'Sedang': 0.50, 'Tinggi': 0.30},
            ('Baik', 'Sering Infeksi'):   {'Rendah': 0.40, 'Sedang': 0.40, 'Tinggi': 0.20},
            ('Baik', 'Jarang'):           {'Rendah': 0.70, 'Sedang': 0.25, 'Tinggi': 0.05},
            ('Baik', 'Tidak Ada'):        {'Rendah': 0.98, 'Sedang': 0.02, 'Tinggi': 0.00},
        }
        return cpt.get(key, {'Rendah':0.33, 'Sedang':0.33, 'Tinggi':0.33}).get(stunting, 0)

    def get_cpt_stunting_given_umur(self, umur_bin, stunting):
        # P(Stunting | Umur)
        cpt = {
            '18-21': {'Rendah': 0.20, 'Sedang': 0.30, 'Tinggi': 0.50},
            '22-25': {'Rendah': 0.25, 'Sedang': 0.35, 'Tinggi': 0.40},
            '26-29': {'Rendah': 0.40, 'Sedang': 0.40, 'Tinggi': 0.20},
            '30-33': {'Rendah': 0.50, 'Sedang': 0.40, 'Tinggi': 0.20},
            '34-36': {'Rendah': 0.60, 'Sedang': 0.35, 'Tinggi': 0.05}
        }
        return cpt.get(umur_bin, {'Rendah':0.33, 'Sedang':0.33, 'Tinggi':0.33}).get(stunting, 0)

    def get_age_category(self, months):
        if 18 <= months <= 21: return '18-21'
        elif 22 <= months <= 25: return '22-25'
        elif 26 <= months <= 29: return '26-29'
        elif 30 <= months <= 33: return '30-33'
        elif 34 <= months <= 36: return '34-36'
        else: return '30-33'

    
    def inferensi(self, umur_bulan, pola_makan, riwayat_penyakit, lingkungan):
        riwayat_spec = str(riwayat_penyakit).title()
        
        valid_keys = ["Tidak Ada", "Jarang", "Sering Diare", "Sering Infeksi"]
        if riwayat_spec not in valid_keys:
            if "Diare" in riwayat_spec: riwayat_spec = "Sering Diare"
            elif "Infeksi" in riwayat_spec: riwayat_spec = "Sering Infeksi"
            elif "Jarang" in riwayat_spec: riwayat_spec = "Jarang"
            else: riwayat_spec = "Tidak Ada"

        age_cat = self.get_age_category(umur_bulan)
        scores = {}
        
        for level_stunting in ['Rendah', 'Sedang', 'Tinggi']:
            
            # P(Penyakit Spesifik | Lingkungan)
            prob_penyakit = self.get_cpt_penyakit_given_lingkungan(lingkungan, riwayat_spec)
            
            # P(Stunting | Pola Makan & Penyakit Spesifik)
            prob_utama = self.get_cpt_stunting_given_faktor_utama(pola_makan, riwayat_spec, level_stunting)
            
            # P(Stunting | Umur)
            prob_umur = self.get_cpt_stunting_given_umur(age_cat, level_stunting)
            
            scores[level_stunting] = prob_utama * prob_penyakit * prob_umur

        # Normalisasi
        total_score = sum(scores.values())
        if total_score == 0:
            return {k: 0 for k in scores}, age_cat
            
        for k in scores:
            scores[k] = (scores[k] / total_score) * 100
            
        return scores, age_cat
    
    
# =================================================================
# PENJELASAN UNTUK  WEB 
# =================================================================

"""

Catatan :
terdapat 4 value
umur
lingkungan: 'Baik', 'Cukup', 'Kurang'
pola_makan: 'Baik', 'Cukup', 'Kurang'
riwayat_penyakit: 'Tidak Ada', 'Jarang', 'Sering Diare', 'Sering Infeksi'

dibagi 2 penyebab stunting :
penyebab tidak langsung : umur,lingkungan
penyebab langsung : pola_makan,riwayat_penyakit

rumus CHAIN RULE BAYESIAN NETWORK :
P(Total) = P(Stunting|Utama) * P(Penyakit|Lingkungan) * P(Stunting|Umur)



1. Import class ini ke file utama web :
   from model_stunting import BayesianNetworkStunting

2. Buat object modelnya:
   model = BayesianNetworkStunting()

3. Siapkan data input dari form user :
   - Umur: Integer 
   - Pola Makan: String persis "Baik", "Cukup", atau "Kurang" 
   - Riwayat Penyakit: String "Tidak Ada", "Jarang", "Sering Diare", atau "Sering Infeksi"
   - Lingkungan: String persis "Baik", "Cukup", atau "Kurang"

4. Panggil fungsi prediksi:
    contoh
    hasil_diagnosa, kategori_umur = model.inferensi(24, "Kurang", "Sering Diare", "Kurang")

5. Contoh Output 'hasil_diagnosa' yang akan kamu terima:
   {'Rendah': 1.5, 'Sedang': 8.5, 'Tinggi': 90.0}

6. Cara menampilkan di Web:
   Ambil nilai terbesar dari dictionary tersebut untuk menentukan label akhir.
   Contoh logic tampilan:
   
   tertinggi = max(hasil_diagnosa, key=hasil_diagnosa.get)
   if tertinggi == 'Tinggi':
       tampilkan_alert_merah("BAHAYA! Risiko Stunting Tinggi")
"""
