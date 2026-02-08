# PICO — AI Prediksi Postpartum Hemorrhage (PPH)

## Pertanyaan Klinis
Pada pasien persalinan SC/partus dengan risiko sedang–tinggi PPH, apakah model AI gabungan (video + data anestesi/vital + lab) dibandingkan penilaian klinis standar dengan EBL manual dapat meningkatkan deteksi dini PPH dan memperbaiki luaran klinis?

## Populasi (P)
- Ibu bersalin (SC atau pervaginam) dengan risiko sedang–tinggi PPH.
- Contoh faktor risiko: riwayat PPH, plasenta previa/akreta, atonia uteri, kehamilan ganda, preeklampsia, anemia, SC emergensi.

## Intervensi (I)
Model AI multimodal real-time yang menggabungkan:
- Data vital dan anestesi (tekanan darah, nadi, SpO2, obat anestesi, uterotonik).
- Data laboratorium (Hb, hematokrit, koagulasi, laktat bila tersedia).
- Estimasi perdarahan berbasis kamera/video (computer vision).

Output model:
- Skor risiko PPH dinamis per interval waktu.
- Alarm dini saat probabilitas melewati ambang klinis.

## Komparator (C)
- Penilaian klinis rutin oleh tim obstetri/anestesi.
- Estimasi blood loss manual (EBL manual) sesuai praktik saat ini.

## Outcomes (O)
### Outcome primer
- Waktu ke deteksi PPH (menit dari onset perdarahan bermakna).
- Sensitivitas deteksi dini PPH sebelum diagnosis klinis rutin.

### Outcome sekunder
- Akurasi estimasi blood loss (dibanding referensi terstandar rumah sakit).
- Kebutuhan transfusi darah.
- Penggunaan uterotonik tambahan dan/atau balloon tamponade.
- Kejadian histerektomi obstetrik.
- Kebutuhan perawatan ICU.
- Lama rawat inap maternal.
- Luaran keamanan: false alarm rate dan alarm fatigue.

## Definisi Operasional yang Disarankan
- PPH: kehilangan darah ≥1000 mL atau disertai tanda hipovolemia dalam 24 jam postpartum (sesuaikan guideline lokal).
- Deteksi dini: alarm AI muncul lebih awal dibanding penilaian klinis rutin dengan lead-time bermakna (mis. ≥10–15 menit).

## Rancangan Evaluasi (ringkas)
- Desain: kohort prospektif atau uji pragmatik bertahap (stepped-wedge) di ruang bersalin/OK.
- Analitik utama:
  - AUC-ROC, AUC-PR, sensitivitas, spesifisitas, PPV, NPV.
  - Time-to-event/lead-time analysis.
  - Decision-curve analysis untuk manfaat klinis bersih.
- Analisis dampak klinis:
  - Perubahan waktu intervensi (transfusi/uterotonik/balloon).
  - Perubahan angka komplikasi berat (histerektomi/ICU).

## Ringkasan Hipotesis
Implementasi model AI multimodal untuk prediksi PPH memungkinkan deteksi lebih dini dibanding penilaian klinis + EBL manual, sehingga mempercepat intervensi dan berpotensi menurunkan luaran berat maternal.
