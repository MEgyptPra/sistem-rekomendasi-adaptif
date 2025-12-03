PENGEMBANGAN SISTEM REKOMENDASI ADAPTIF *REAL-TIME* UNTUK DESTINASI
WISATA: OPTIMALISASI KEBERAGAMAN DAN CAKUPAN GUNA MENDORONG PEMERATAAN
DISTRIBUSI PARIWISATA

TESIS

Karya tulis sebagai salah satu syarat

untuk memperoleh gelar Magister dari

Institut Teknologi Bandung

Oleh

M EGYPT PRATAMA

NIM: 23523311

(Program Studi Magister Informatika)

![Description: GAJAHPT](media/image1.png){width="0.9251968503937008in"
height="1.3779527559055118in"}

INSTITUT TEKNOLOGI BANDUNG\
November 2025

# ABSTRAK

PENGEMBANGAN SISTEM REKOMENDASI ADAPTIF *REAL-TIME* UNTUK DESTINASI
WISATA: OPTIMALISASI KEBERAGAMAN DAN CAKUPAN GUNA MENDORONG PEMERATAAN
DISTRIBUSI PARIWISATA

Oleh

M Egypt Pratama

NIM: 23523311

(Program Studi Magister Informatika)

Transformasi digital dalam industri pariwisata telah menciptakan
paradoks fundamental di mana sistem rekomendasi konvensional justru
memperburuk ketimpangan distribusi kunjungan melalui fenomena popularity
bias. Secara global, 10 destinasi teratas menampung 40% kedatangan
wisatawan, menciptakan konsentrasi yang tidak berkelanjutan dan
mengabaikan potensi destinasi alternatif. Di Kabupaten Sumedang, dari 77
destinasi terdaftar, 72,4% total kunjungan terpusat pada hanya 10
destinasi populer, sementara 67 destinasi potensial lainnya mengalami
marjinalisasi sistematis. Sistem rekomendasi berbasis *Collaborative
Filtering* tradisional memperparah masalah ini karena cenderung
memperkuat preferensi mayoritas, menciptakan siklus
\"*rich-get-richer*\" di mana kurang dari 3% item dapat mendominasi
hingga 100% rekomendasi.

Meskipun teknik diversifikasi seperti *Maximal Marginal Relevance* (MMR)
telah terbukti meningkatkan keberagaman rekomendasi, pendekatan existing
menggunakan parameter λ statis yang gagal beradaptasi terhadap
karakteristik dinamis domain pariwisata. Faktor kontekstual seperti
cuaca, waktu, dan kepadatan wisatawan sangat memengaruhi keputusan
wisatawan, namun sistem tradisional tidak mampu merespons perubahan ini
secara adaptif. Lebih penting lagi, tidak ada penelitian yang secara
sistematis mengeksplorasi optimasi parameter diversifikasi secara
dinamis untuk mencapai keseimbangan optimal antara akurasi dan
keberagaman dalam konteks pariwisata dengan *data sparsity* ekstrem.
Penelitian ini bertujuan mengembangkan sistem rekomendasi adaptif yang
mampu menyeimbangkan akurasi dan keberagaman melalui optimasi parameter
dinamis, serta memvalidasi dampaknya terhadap pemerataan distribusi dan
eksposur destinasi *long-tail*. Pendekatan ini diperlukan untuk
memberikan bukti empiris bahwa intervensi algoritmik dapat memitigasi
*popularity bias* sambil mempertahankan kepuasan pengguna.

Penelitian menggunakan *Design Science Research Methodology* (DSRM)
dengan arsitektur hibrida yang mengintegrasikan *Collaborative
Filtering*, *Content-Based Filtering*, dan komponen *Context-Aware* yang
memproses data cuaca dan kalender secara *real-time* melalui API, serta
model simulasi untuk lalu lintas dan tren media sosial. Mekanisme inti
adalah *Multi-Armed Bandit* dengan algoritma *Upper Confidence Bound*
yang memilih parameter λ secara adaptif dari 5 arms diskrit (0.0, 0.3,
0.5, 0.7, 1.0) berdasarkan fungsi *composite reward* yang
mengombinasikan 50% akurasi, 30% keberagaman, dan 20% kebaruan. Evaluasi
komprehensif pada dataset 36.992 interaksi dari 224 destinasi Sumedang
(*sparsity* 0,602%) dan pengujian pengguna (n=30) dilakukan untuk
memvalidasi performa sistem.

Model MAB-MMR mencapai akurasi setara baseline Hybrid (NDCG@10=0,0237,
p=0,20) dengan peningkatan *Diversity* sebesar +3,5% dibanding baseline
tersebut (dari 0,5801 menjadi 0,6003, p\<0,001, Cohen\'s d=0,33) dan
*Long-Tail Coverage* tertinggi (69,64%). Sistem berhasil memberikan
boost eksposur signifikan pada destinasi long-tail berkualitas tinggi,
seperti Curug Pasirwangi yang meningkat +52,78% dan Curug Cirengganis
+33,77%. Evaluasi pengguna (n=30) menunjukkan usability kategori
\"Baik\" (SUS 79,1, percentile rank ke-85) dengan tingkat penemuan
destinasi baru yang sangat tinggi (96,7%) dan persepsi keberagaman yang
positif (4,3/5,0). Keterbatasan meliputi evaluasi terbatas pada satu
kabupaten dan penggunaan data simulasi untuk sebagian konteks (lalu
lintas, tren media sosial).

Penelitian ini menunjukkan bahwa pendekatan adaptif *Multi-Armed Bandit*
untuk optimasi parameter *Maximal Marginal Relevance* dapat secara
efektif memitigasi popularity bias, meningkatkan visibilitas destinasi
long-tail, dan mendukung pemerataan distribusi pariwisata tanpa
mengorbankan akurasi prediksi maupun kepuasan pengguna. Temuan ini
memberikan panduan praktis bagi pengelola destinasi wisata, pelaku UKM
lokal, dan pembuat kebijakan dalam meningkatkan visibilitas destinasi
berkualitas yang selama ini terabaikan.

Kata Kunci: Sistem Rekomendasi Adaptif, *Multi-Armed Bandit, Maximal
Marginal Relevance, Popularity Bias*, Pariwisata Berkelanjutan,
*Distribusi Long-Tail*.

# ABSTRACT

***DEVELOPMENT OF AN ADAPTIVE REAL-TIME RECOMMENDATION SYSTEM FOR
TOURIST DESTINATIONS: OPTIMIZING DIVERSITY AND COVERAGE TO PROMOTE
EQUITABLE TOURISM DISTRIBUTION***

*By*

M Egypt Pratama

NIM: 23523311

(*Master's Program in Informatics*)

The digital transformation of the tourism industry has created a
fundamental paradox where conventional recommender systems exacerbate
visitation inequality through popularity bias phenomena. Globally, the
top 10 destinations attract 40% of tourist arrivals, creating
unsustainable concentration while neglecting the potential of
alternative destinations. In Sumedang Regency, out of 77 registered
destinations, 72.4% of total visits are concentrated in only 10 popular
destinations, while 67 other potential destinations experience
systematic marginalization. Traditional Collaborative Filtering-based
recommender systems worsen this problem by reinforcing majority
preferences, creating a \"rich-get-richer\" cycle where less than 3% of
items can dominate up to 100% of recommendations.

Although diversification techniques such as Maximal Marginal Relevance
(MMR) have proven to increase recommendation diversity, existing
approaches use static λ parameters that fail to adapt to the dynamic
characteristics of the tourism domain. Contextual factors such as
weather, time, and tourist density significantly influence tourist
decisions, yet traditional systems cannot respond adaptively to these
changes. More importantly, no research has systematically explored
dynamic diversification parameter optimization to achieve optimal
balance between accuracy and diversity in tourism contexts with extreme
data sparsity. This research aims to develop an adaptive recommender
system capable of balancing accuracy and diversity through dynamic
parameter optimization, and validate its impact on distribution equity
and long-tail destination exposure. This approach is necessary to
provide empirical evidence that algorithmic interventions can mitigate
popularity bias while maintaining user satisfaction.

The research employs Design Science Research Methodology (DSRM) with a
hybrid architecture integrating Collaborative Filtering, Content-Based
Filtering, and Context-Aware components that process weather and
calendar data in real-time via APIs, along with simulation models for
traffic and social media trends. The core mechanism is a Multi-Armed
Bandit with Upper Confidence Bound algorithm that adaptively selects λ
parameter from 5 discrete arms (0.0, 0.3, 0.5, 0.7, 1.0) based on a
composite reward function combining 50% accuracy, 30% diversity, and 20%
novelty. Comprehensive evaluation on a dataset of 36,992 interactions
from 224 Sumedang destinations (0.602% sparsity) and user testing (n=30)
was conducted to validate system performance.

The MAB-MMR model achieves accuracy equivalent to the Hybrid baseline
(NDCG@10=0.0237, p=0.20) with a +3.5% increase in Diversity compared to
that baseline (from 0.5801 to 0.6003, p\<0.001, Cohen\'s d=0.33) and the
highest Long-Tail Coverage (69.64%). The system successfully provides
significant exposure boosts to high-quality long-tail destinations, such
as Curug Pasirwangi which increased by +52.78% and Curug Cirengganis by
+33.77%. User evaluation (n=30) demonstrates \"Good\" category usability
(SUS 79.1, 85th percentile rank) with a remarkably high discovery rate
of novel destinations (96.7%) and positive perceived diversity
(4.3/5.0). Limitations include evaluation restricted to one regency and
use of simulated data for partial context (traffic, social media
trends).

This research demonstrates that the adaptive Multi-Armed Bandit approach
for optimizing Maximal Marginal Relevance parameters can effectively
mitigate popularity bias, enhance long-tail destination visibility, and
support equitable tourism distribution without compromising prediction
accuracy or user satisfaction. These findings provide practical guidance
for destination managers, local SME operators, and policymakers in
increasing the visibility of quality destinations that have been
previously overlooked.

Keywords: Adaptive Recommender System, Multi-Armed Bandit, Maximal
Marginal Relevance, Popularity Bias, Sustainable Tourism, Long-Tail
Distribution.

PENGEMBANGAN SISTEM REKOMENDASI ADAPTIF *REAL-TIME* UNTUK DESTINASI
WISATA: OPTIMALISASI KEBERAGAMAN DAN CAKUPAN GUNA MENDORONG PEMERATAAN
DISTRIBUSI PARIWISATA

# HALAMAN PENGESAHAN

Oleh

M Egypt Pratama

NIM: 23523311

(Program Studi Magister Informatika)

Institut Teknologi Bandung

Menyetujui

Tim Pembimbing

Tanggal November 2025

Pembimbing I

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Dr. Ir. Arry Akhmad Arman, M.T.

# PEDOMAN PENGGUNAAN TESIS

Tesis Magister yang tidak dipublikasikan terdaftar dan tersedia di
Perpustakaan Institut Teknologi Bandung, dan terbuka untuk umum dengan
ketentuan bahwa hak cipta ada pada penulis dengan mengikuti aturan HaKI
yang berlaku di Institut Teknologi Bandung. Referensi kepustakaan
diperkenankan dicatat, tetapi pengutipan atau peringkasan hanya dapat
dilakukan seizin penulis dan harus disertai dengan kaidah ilmiah untuk
menyebutkan sumbernya.

Sitasi hasil penelitian Tesis ini dapat di tulis dalam bahasa Indonesia
sebagai berikut:

Pratama, M. E. 2025: *Pengembangan Sistem Rekomendasi Adaptif Real-time
untuk Destinasi Wisata: Optimalisasi Keberagaman dan Cakupan guna
Mendorong Pemerataan Distribusi Pariwisata*, Tesis Program Magister,
Institut Teknologi Bandung.

dan dalam bahasa Inggris sebagai berikut:

Pratama, M. E. 2025: *Development of an Adaptive Real-Time
Recommendation System for Tourist Destinations: Optimizing Diversity and
Coverage to Promote Equitable Tourism Distribution*, Master's Thesis,
Institut Teknologi Bandung.

Memperbanyak atau menerbitkan sebagian atau seluruh tesis haruslah
seizin Dekan Sekolah Pascasarjana, Institut Teknologi Bandung.

# HALAMAN PERUNTUKAN

Dipersembahkan kepada istriku tercinta Efa Nur Asyiah, anaku Mysha
Shazna Hadeeqa, orang tua terkasih, adik kakak, mertua serta keluarga
besarku tercinta yang senantiasa mendukung lahir dan batin.

# **KATA PENGANTAR**

Puji syukur ke hadirat Allah SWT karena atas rahmat dan karunia-Nya
penulis menyelesaikan Tesis ini yang berjudul "Pengembangan Sistem
Rekomendasi Adaptif Real-time untuk Destinasi Wisata: Optimalisasi
Keberagaman dan Cakupan guna Mendorong Pemerataan Distribusi
Pariwisata". Tesis ini tidak dapat diselesaikan tanpa bantuan dan
dukungan dari berbagai pihak. Pada kesempatan ini, penulis ingin
mengucapkan terima kasih kepada:

1.  Bapak Dr. Ir. Arry Akhmad Arman, M.T. selaku dosen pembimbing yang
    telah membimbing dan memberikan masukan dan saran kepada penulis
    dalam menyelesaikan penelitian Tesis,

2.  Ibu Dr. Fetty Fitriyanti Lubis, S.T., M.T. selaku dosen wali yang
    telah memberikan arahan, nasehat, dan dukungan selama berkuliah di
    program studi Magister Informatika ITB,

3.  Seluruh dosen Informatika ITB, atas ilmu dan inspirasi yang
    diberikan kepada penulis,

4.  Kepada Kementerian Komunikasi dan Digital selaku lembaga pemberi
    beasiswa yang memberikan bantuan secara finansial untuk melaksanakan
    studi,

5.  Orang tua dan keluarga yang selalu memberikan semangat dan doa
    kepada penulis,

6.  Teman-teman Magister Informatika 2024 khususnya teman-teman Smart-X
    (Sistem Cerdas) yang telah memberikan pengalaman belajar yang
    menyenangkan selama proses perkuliahan,

7.  Pihak-pihak lain yang tidak dapat disebutkan satu per satu yang
    turut serta untuk membantu penulis untuk menyelesaikan Tesis.

Bandung, November 2025

Penulis

# **DAFTAR ISI**

[ABSTRAK [i](#abstrak)](#abstrak)

[ABSTRACT [iii](#abstract)](#abstract)

[HALAMAN PENGESAHAN [v](#halaman-pengesahan)](#halaman-pengesahan)

[PEDOMAN PENGGUNAAN TESIS
[vi](#pedoman-penggunaan-tesis)](#pedoman-penggunaan-tesis)

[HALAMAN PERUNTUKAN [vii](#halaman-peruntukan)](#halaman-peruntukan)

[KATA PENGANTAR [viii](#kata-pengantar)](#kata-pengantar)

[DAFTAR ISI [ix](#daftar-isi)](#daftar-isi)

[DAFTAR LAMPIRAN [i](#daftar-lampiran)](#daftar-lampiran)

[DAFTAR GAMBAR DAN ILUSTRASI
[ii](#daftar-gambar-dan-ilustrasi)](#daftar-gambar-dan-ilustrasi)

[DAFTAR TABEL [iii](#daftar-tabel)](#daftar-tabel)

[DAFTAR SINGKATAN DAN LAMBANG
[iv](#daftar-singkatan-dan-lambang)](#daftar-singkatan-dan-lambang)

[BAB I. Pendahuluan [1](#pendahuluan)](#pendahuluan)

[I.1 Latar Belakang [1](#latar-belakang)](#latar-belakang)

[I.2 Rumusan Masalah [5](#rumusan-masalah)](#rumusan-masalah)

[I.3 Tujuan Penelitian [5](#tujuan-penelitian)](#tujuan-penelitian)

[I.4 Ruang Lingkup Masalah
[6](#ruang-lingkup-masalah)](#ruang-lingkup-masalah)

[I.5 Kontribusi Keilmuan
[7](#kontribusi-keilmuan)](#kontribusi-keilmuan)

[I.6 Hipotesis [7](#hipotesis)](#hipotesis)

[I.7 Sistematika Penulisan
[8](#sistematika-penulisan)](#sistematika-penulisan)

[BAB II. Tinjauan Pustaka [9](#tinjauan-pustaka)](#tinjauan-pustaka)

[II.1 Sistem Rekomendasi dalam Ekosistem Pariwisata Digital
[9](#sistem-rekomendasi-dalam-ekosistem-pariwisata-digital)](#sistem-rekomendasi-dalam-ekosistem-pariwisata-digital)

[II.2 Tantangan Sistem Rekomendasi Konvensional: *Popularity Bias*
[11](#tantangan-sistem-rekomendasi-konvensional-popularity-bias)](#tantangan-sistem-rekomendasi-konvensional-popularity-bias)

[II.3 *Collaborative Filtering* dalam Sistem Rekomendasi Sektor
Pariwisata
[13](#collaborative-filtering-dalam-sistem-rekomendasi-sektor-pariwisata)](#collaborative-filtering-dalam-sistem-rekomendasi-sektor-pariwisata)

[II.4 *Context-Aware Recommendations* dalam Domain Pariwisata
[14](#context-aware-recommendations-dalam-domain-pariwisata)](#context-aware-recommendations-dalam-domain-pariwisata)

[II.4.1 Kategori Konteks dalam Pariwisata
[15](#kategori-konteks-dalam-pariwisata)](#kategori-konteks-dalam-pariwisata)

[II.4.2 Pendekatan Integrasi Konteks
[15](#pendekatan-integrasi-konteks)](#pendekatan-integrasi-konteks)

[II.5 Pendekatan Hibrida untuk Personalisasi
[16](#pendekatan-hibrida-untuk-personalisasi)](#pendekatan-hibrida-untuk-personalisasi)

[II.6 Keberagaman dan Cakupan
[18](#keberagaman-dan-cakupan)](#keberagaman-dan-cakupan)

[II.7 *Maximal Marginal Relevance* dan *Multi-Armed Bandit*
[21](#maximal-marginal-relevance-dan-multi-armed-bandit)](#maximal-marginal-relevance-dan-multi-armed-bandit)

[II.8 Sistem Adaptif: Keterbatasan Pendekatan Statis
[23](#sistem-adaptif-keterbatasan-pendekatan-statis)](#sistem-adaptif-keterbatasan-pendekatan-statis)

[II.9 Rangkuman Tinjauan Pustaka dan Posisi Penelitian
[26](#rangkuman-tinjauan-pustaka-dan-posisi-penelitian)](#rangkuman-tinjauan-pustaka-dan-posisi-penelitian)

[BAB III. Metodologi Penelitian
[29](#metodologi-penelitian)](#metodologi-penelitian)

[III.1 Metode Penelitian DSRM
[29](#metode-penelitian-dsrm)](#metode-penelitian-dsrm)

[III.2 Identifikasi Masalah dan Motivasi
[31](#identifikasi-masalah-dan-motivasi)](#identifikasi-masalah-dan-motivasi)

[III.2.1 Analisis Permasalahan
[31](#analisis-permasalahan)](#analisis-permasalahan)

[III.3 Menentukan Solusi dari Tujuan
[33](#menentukan-solusi-dari-tujuan)](#menentukan-solusi-dari-tujuan)

[III.3.1 Analisis Solusi [34](#analisis-solusi)](#analisis-solusi)

[III.3.2 Rancangan Solusi dan Justifikasi
[44](#rancangan-solusi-dan-justifikasi)](#rancangan-solusi-dan-justifikasi)

[III.4 Perancangan dan Pengembangan
[45](#perancangan-dan-pengembangan)](#perancangan-dan-pengembangan)

[III.4.1 Spesifikasi Kebutuhan Sistem
[45](#spesifikasi-kebutuhan-sistem)](#spesifikasi-kebutuhan-sistem)

[III.4.2 Integrasi Data dan API
[47](#integrasi-data-dan-api)](#integrasi-data-dan-api)

[III.4.3 Dataset Penelitian
[48](#dataset-penelitian)](#dataset-penelitian)

[III.4.4 Desain Model *Machine Learning* (MAB-MMR)
[48](#desain-model-machine-learning-mab-mmr)](#desain-model-machine-learning-mab-mmr)

[III.4.5 Arsitektur Aliran Data
[52](#arsitektur-aliran-data)](#arsitektur-aliran-data)

[III.4.6 Alur Interaksi Sistem (*Sequence Diagram*)
[54](#alur-interaksi-sistem-sequence-diagram)](#alur-interaksi-sistem-sequence-diagram)

[III.4.7 Desain Basis Data (ERD)
[56](#desain-basis-data-erd)](#desain-basis-data-erd)

[III.4.8 Strategi Menangani *Cold Start*
[59](#strategi-menangani-cold-start)](#strategi-menangani-cold-start)

[III.5 Demonstrasi [60](#demonstrasi)](#demonstrasi)

[III.5.1 Skenario Demonstrasi
[60](#skenario-demonstrasi)](#skenario-demonstrasi)

[III.6 Evaluasi [61](#evaluasi)](#evaluasi)

[III.6.1 Evaluasi Kuantitatif
[62](#evaluasi-kuantitatif)](#evaluasi-kuantitatif)

[III.6.2 Evaluasi Kualitatif
[65](#evaluasi-kualitatif)](#evaluasi-kualitatif)

[III.6.3 Protokol Pengujian
[67](#protokol-pengujian)](#protokol-pengujian)

[III.7 Komunikasi [69](#komunikasi)](#komunikasi)

[BAB IV. Implementasi dan Hasil Penelitian
[70](#implementasi-dan-hasil-penelitian)](#implementasi-dan-hasil-penelitian)

[IV.1 Lingkungan Implementasi
[70](#lingkungan-implementasi)](#lingkungan-implementasi)

[IV.1.1 Stack Teknologi [70](#stack-teknologi)](#stack-teknologi)

[IV.1.2 Spesifikasi Sistem
[71](#spesifikasi-sistem)](#spesifikasi-sistem)

[IV.2 Implementasi Sistem
[71](#implementasi-sistem)](#implementasi-sistem)

[IV.2.1 Arsitektur Sistem [72](#arsitektur-sistem)](#arsitektur-sistem)

[IV.2.2 Deskripsi Dataset dan Eksperimen
[73](#deskripsi-dataset-dan-eksperimen)](#deskripsi-dataset-dan-eksperimen)

[IV.2.3 Implementasi Backend dan Model
[75](#implementasi-backend-dan-model)](#implementasi-backend-dan-model)

[IV.2.4 Implementasi Antarmuka Pengguna
[77](#implementasi-antarmuka-pengguna)](#implementasi-antarmuka-pengguna)

[IV.3 Hasil Evaluasi Kuantitatif
[78](#hasil-evaluasi-kuantitatif)](#hasil-evaluasi-kuantitatif)

[IV.3.1 Performa Model Baseline Non-Diversified (CF, CB, Hybrid)
[78](#performa-model-baseline-non-diversified-cf-cb-hybrid)](#performa-model-baseline-non-diversified-cf-cb-hybrid)

[IV.3.2 Performa Model Diversifikasi (MMR Statis vs. MAB-MMR)
[83](#performa-model-diversifikasi-mmr-statis-vs.-mab-mmr)](#performa-model-diversifikasi-mmr-statis-vs.-mab-mmr)

[IV.3.3 *Statistical Validation* Kontribusi MAB
[87](#statistical-validation-kontribusi-mab)](#statistical-validation-kontribusi-mab)

[IV.3.4 Pareto frontier analysis & *trade-off* interpretation
[91](#pareto-frontier-analysis-trade-off-interpretation)](#pareto-frontier-analysis-trade-off-interpretation)

[IV.3.5 Validasi Strategi *Cold-Start* Melalui\
Stratifikasi Pengguna
[93](#validasi-strategi-cold-start-melalui-stratifikasi-pengguna)](#validasi-strategi-cold-start-melalui-stratifikasi-pengguna)

[IV.3.6 Analisis Distribusi dan *Long-Tail*
[94](#analisis-distribusi-dan-long-tail)](#analisis-distribusi-dan-long-tail)

[IV.3.7 Analisis *Novelty* [97](#analisis-novelty)](#analisis-novelty)

[IV.3.8 Rangkuman Validasi Tujuan Penelitian
[99](#rangkuman-validasi-tujuan-penelitian)](#rangkuman-validasi-tujuan-penelitian)

[IV.3.9 Evaluasi Performa Sistem (*Latency Analysis*)
[100](#evaluasi-performa-sistem-latency-analysis)](#evaluasi-performa-sistem-latency-analysis)

[IV.3.10 Demonstrasi Adaptabilitas Skenario (*Case Studies*)
[101](#demonstrasi-adaptabilitas-skenario-case-studies)](#demonstrasi-adaptabilitas-skenario-case-studies)

[IV.4 Hasil Evaluasi Kualitatif
[103](#hasil-evaluasi-kualitatif)](#hasil-evaluasi-kualitatif)

[IV.4.1 Hasil SUS (*System Usability Scale*)
[103](#hasil-sus-system-usability-scale)](#hasil-sus-system-usability-scale)

[IV.4.2 Triangulasi Kualitatif-Kuantitatif
[105](#triangulasi-kualitatif-kuantitatif)](#triangulasi-kualitatif-kuantitatif)

[IV.4.3 Kesimpulan Evaluasi Kualitatif
[106](#kesimpulan-evaluasi-kualitatif)](#kesimpulan-evaluasi-kualitatif)

[IV.5 Diskusi dan Implikasi
[107](#diskusi-dan-implikasi)](#diskusi-dan-implikasi)

[IV.5.1 Interpretasi Temuan Utama
[107](#interpretasi-temuan-utama)](#interpretasi-temuan-utama)

[IV.5.2 Kontribusi terhadap *Body of Knowledge*
[109](#kontribusi-terhadap-body-of-knowledge)](#kontribusi-terhadap-body-of-knowledge)

[IV.5.3 Implikasi Praktis [109](#implikasi-praktis)](#implikasi-praktis)

[IV.5.4 Keterbatasan Penelitian
[110](#keterbatasan-penelitian)](#keterbatasan-penelitian)

[IV.6 Rangkuman Bab [111](#rangkuman-bab)](#rangkuman-bab)

[BAB V. Kesimpulan dan Saran
[113](#kesimpulan-dan-saran)](#kesimpulan-dan-saran)

[V.1 Kesimpulan [113](#kesimpulan)](#kesimpulan)

[V.2 Saran [115](#saran)](#saran)

[DAFTAR PUSTAKA [116](#daftar-pustaka)](#daftar-pustaka)

[LAMPIRAN [120](#lampiran)](#lampiran)

# DAFTAR LAMPIRAN

[Lampiran A: Detail Implementasi Teknis
[121](#_Toc214880879)](#_Toc214880879)

[A.1 Snippet Kode Komponen Utama [121](#_Toc214880880)](#_Toc214880880)

[A.2 Detail Aturan Kontekstual Aditif
[123](#_Toc214880881)](#_Toc214880881)

# DAFTAR GAMBAR DAN ILUSTRASI

[Gambar II.1 Alur Konseptual Penelitian
[28](#_Toc214882431)](#_Toc214882431)

[Gambar III.1 Kerangka Kerja DSRM berdasarkan Peffers dkk (2007)
[29](#_Toc214882432)](#_Toc214882432)

[Gambar III.2 Kerangka Penelitian [30](#_Toc214882433)](#_Toc214882433)

[Gambar III.4 Arsitektur Aliran Data
[52](#_Toc214882434)](#_Toc214882434)

[Gambar III.5 Tahap 1: Permintaan Rekomendasi
[54](#_Toc214882435)](#_Toc214882435)

[Gambar III.6 Tahap 6-7: Interaksi & Pembelajaran
[55](#_Toc214882436)](#_Toc214882436)

[Gambar III.7 *Entity-Relationship Diagram* (ERD)
[56](#_Toc214882437)](#_Toc214882437)

[Gambar IV.1 Arsitektur Pipeline Rekomendasi MAB-MMR
[73](#_Toc214882438)](#_Toc214882438)

[Gambar IV.2 Distribusi Interaksi Pengguna Asli (*Long-Tail*) pada
Dataset\
Pariwisata Sumedang [74](#_Toc214882439)](#_Toc214882439)

[Gambar IV.3 Tampilan Halaman Utama
[77](#_Toc214882440)](#_Toc214882440)

[Gambar IV.4 Perbandingan Rata-rata Metrik Model Baseline
*Non-Diversified* [82](#_Toc214882441)](#_Toc214882441)

[Gambar IV.5 Kurva Pembelajaran MAB: Peningkatan Rata-rata Reward
Seiring\
Waktu [90](#_Toc214882442)](#_Toc214882442)

[Gambar IV.6 *Trade-off* Akurasi (NDCG@10) vs. Keberagaman\
(*Diversity*) [91](#_Toc214882443)](#_Toc214882443)

[Gambar IV.7 Visualisasi metrik *long-tail*: (a) Jangkauan (*Coverage*)
per segmen,\
(b) Rasio *Head-Tail*, (c) *Aggregate Diversity* (Jangkauan Katalog),\
dan (d) *Expected Popularity Complement* (EPC)
[96](#_Toc214882444)](#_Toc214882444)

[Gambar IV.8 Stabilitas *Novelty* seiring waktu: (a) Skor *Novelty*
dengan 50-episode\
moving average, dan (b) Rata-rata Novelty per boks episode
[98](#_Toc214882445)](#_Toc214882445)

[Gambar IV.9 *Heatmap* Korelasi Metrik MAB-MMR
[99](#_Toc214882446)](#_Toc214882446)

# DAFTAR TABEL

[Tabel III.1 Solusi Alternatif Mengurangi *Popularity Bias*
[34](#_Toc214880948)](#_Toc214880948)

[Tabel III.2 Solusi Alternatif Mengatasi Kurangnya *Context-Awareness*
[36](#_Toc214880949)](#_Toc214880949)

[Tabel III.3 Solusi Alternatif Meningkatkan *Diversity & Coverage*
[38](#_Toc214880950)](#_Toc214880950)

[Tabel III.4 Solusi Alternatif Mengatasi *Cold-Start Problem*
[40](#_Toc214880951)](#_Toc214880951)

[Tabel III.5 Solusi Alternatif Menangani *Concept Drift*
[42](#_Toc214880952)](#_Toc214880952)

[Tabel III.6 Kebutuhan Fungsional Sistem
[45](#_Toc214880953)](#_Toc214880953)

[Tabel III.7 Kebutuhan *Non-Fungsional* Sistem
[46](#_Toc214880954)](#_Toc214880954)

[Tabel III.8 Spesifikasi Integrasi Data dan API
[47](#_Toc214880955)](#_Toc214880955)

[Tabel III.9 Struktur Tabel User [57](#_Toc214880956)](#_Toc214880956)

[Tabel III.10 Struktur Tabel rating
[57](#_Toc214880957)](#_Toc214880957)

[Tabel III.11 Struktur Tabel Destination
[58](#_Toc214880958)](#_Toc214880958)

[Tabel III.12 Struktur Tabel destination_categories
[58](#_Toc214880959)](#_Toc214880959)

[Tabel III.13 Struktur Tabel Categories
[58](#_Toc214880960)](#_Toc214880960)

[Tabel III.14 Struktur Tabel review
[59](#_Toc214880961)](#_Toc214880961)

[Tabel III.15 Daftar Pernyataan *System Usability Scale*
[66](#_Toc214880962)](#_Toc214880962)

[Tabel IV.1 Stack Teknologi Penelitian
[70](#_Toc214880963)](#_Toc214880963)

[Tabel IV.2 Perbandingan Kinerja Model *Baseline Non-Diversified*
[78](#_Toc214880964)](#_Toc214880964)

[Tabel IV.3 Performa MMR dengan Berbagai Nilai λ Statis
[83](#_Toc214880965)](#_Toc214880965)

[Tabel IV.4 Perbandingan MAB-MMR (Adaptif) vs MMR- λ =0.5 (Statis)
[85](#_Toc214880966)](#_Toc214880966)

[Tabel IV.5 Distribusi Pemilihan Parameter λ oleh MAB-MMR
[86](#_Toc214880967)](#_Toc214880967)

[Tabel IV.6 Hasil Uji Statistik (*Paired t-test*, N=1714 *users*)
[87](#_Toc214880968)](#_Toc214880968)

[Tabel IV.7 Performa Model (NDCG@10) per Strata Pengguna
[93](#_Toc214880969)](#_Toc214880969)

[Tabel IV.8 Perbandingan *Gini Coefficient* (Pemerataan Frekuensi)
[94](#_Toc214880970)](#_Toc214880970)

[Tabel IV.9 Analisis *Coverage* dan *Long-Tail*
[95](#_Toc214880971)](#_Toc214880971)

[Tabel IV.10 Top 5 Destinasi *Long-Tail* dengan Boost Tertinggi\
(MAB vs. Hybrid) [96](#_Toc214880972)](#_Toc214880972)

[Tabel IV.11 Perbandingan Skor *Novelty*
[97](#_Toc214880973)](#_Toc214880973)

[Tabel IV.12 Demonstrasi Perubahan Rekomendasi pada Berbagai\
Skenario Konteks [101](#_Toc214880974)](#_Toc214880974)

[Tabel IV.13 Analisis Per-Item *System Usability Scale* (MAB-MMR, n=30)
[103](#_Toc214880975)](#_Toc214880975)

[Tabel A.2.1 Aturan Kontekstual - Tipe Hari
[123](#_Toc214880976)](#_Toc214880976)

[Tabel A.2.2 Aturan Kontekstual -- Cuaca
[124](#_Toc214880977)](#_Toc214880977)

[Tabel A.2.3 Aturan Kontekstual - Waktu & Musim
[124](#_Toc214880978)](#_Toc214880978)

[Tabel A.2.4 Aturan Kontekstual - Event, Tren, & Kepadatan
[125](#_Toc214880979)](#_Toc214880979)

# DAFTAR SINGKATAN DAN LAMBANG

  ----------------------------------------------------------------------
  SINGKATAN        Nama                                      Pemakaian
                                                             pertama
                                                             kali pada
                                                             halaman
  ---------------- ----------------------------------------- -----------
  API              Application Programming Interface         Hal. 31

  DSRM             Design Science Research Methodology       Hal. 25

  MAB              Multi-Armed Bandit                        Hal. 4

  ML               Machine Learning                          Hal. 32

  MMR              Maximal Marginal Relevance                Hal. 3

  NDCG             Normalized Discounted Cumulative Gain     Hal. 5

  ODTW             Objek Daya Tarik Wisata                   Hal. 31

  RS               Recommender Systems                       Hal. 7
  ----------------------------------------------------------------------

  -----------------------------------------------------------------------
  LAMBANG          Deskripsi                                 Halaman
  ---------------- ----------------------------------------- ------------
                                                             

  λ                hyperparameter yang mengontrol            Hal. 39
                   keseimbangan antara akurasi               
                   (Scoreprediksi) dan keberagaman           

  γ                bobot yang mengontrol intensitas fungsi   Hal. 39
                   koreksi bias.                             

  μ                global mean rating                        Hal. 35

  bu               user                                      Hal. 35

  bi               item biases                               Hal. 35

  c                parameter eksplorasi.                     Hal. 38

  μ̂(t,k)           estimated reward mean                     Hal. 38

  N(t,k)           number of times arm k dipilih             Hal. 38

  pop(i)           popularity score dari item i              Hal. 44

  qiTpu            latent factor vectors                     Hal. 35

  S                set rekomendasi                           Hal. 44

  sim(i,j)         similarity antara item i dan j.           Hal. 44

  W                learned weights untuk masing-masing       Hal. 36
                   kategori *contextual features*            
  -----------------------------------------------------------------------

# Pendahuluan

Bab ini menjelaskan dasar-dasar yang membantu dalam melakukan penelitian
ini. Dasar pemikiran didasarkan pada fenomena masalah yang muncul dan
dibahas dalam penelitian setelah membaca sumber referensi yang tersedia.

## Latar Belakang

Ekosistem pariwisata digital saat ini dihadapkan pada paradoks
fundamental yang mengancam esensi eksplorasi wisata. Meskipun teknologi
informasi membuka akses ke ribuan destinasi yang beragam dan otentik,
sistem rekomendasi konvensional justru menghasilkan konsentrasi
wisatawan yang tidak berkelanjutan pada segelintir destinasi populer
Pencarelli, (2020) dan Ricci dkk., (2022) menggarisbawahi fenomena ini.
Dampak dari paradoks tersebut tidak hanya mengikis autentisitas
pengalaman wisata, tetapi juga menimbulkan distorsi ekonomi yang
sistematis dalam ekosistem pariwisata global.

Konsentrasi wisatawan memicu ketidakseimbangan ekonomi yang merugikan.
Menurut UNWTO (2021), 10 destinasi teratas menampung 40% kedatangan
wisatawan global dan 10 negara dengan penerimaan tertinggi menguasai
hampir 50% pendapatan pariwisata dunia, dengan Amerika Serikat sendiri
mencapai USD 214 miliar. Ketergantungan berlebih ini membuat wilayah
tertentu sangat rentan, misalnya Makau di mana pariwisata menyumbang 48%
PDB, serta Spanyol dan Kroasia lebih dari 10% PDB. Sebaliknya, potensi
daerah lain kerap terabaikan, sehingga pemerintah beberapa negara,
seperti Belanda, mendorong kebijakan penyebaran wisatawan ke luar kota
besar (Hu dkk., 2020). Dalam konteks digital, bias algoritma yang lebih
sering merekomendasikan destinasi populer (*popularity bias*)
(Abdollahpouri dkk., 2021) memperparah ketimpangan ini, sekaligus
menyulitkan UKM lokal di destinasi alternatif untuk bersaing (Massimo
dan Ricci, 2022).

Secara sosial, konsentrasi wisatawan yang tidak merata menciptakan
gesekan di lokasi populer dan mengabaikan potensi pengembangan komunitas
di tempat lain (Hoarau-Heemstra dkk., 2023). Di destinasi *mainstream*,
kepadatan berlebih atau *overtourism* menurunkan kualitas pengalaman
turis dan mengganggu kehidupan penduduk lokal melalui kemacetan,
kebisingan, dan beban infrastruktur yang berat (Hoarau-Heemstra dkk.,
2023). Fenomena *overtourism* ini juga mengarah pada penurunan kualitas
pengalaman wisatawan akibat kepadatan berlebih dan terbatasnya daya
dukung kawasan (Foronda-Robles dkk., 2025). Investasi pun cenderung
terpusat di wilayah populer, meninggalkan destinasi potensial lainnya
dengan fasilitas yang kurang memadai (Hoarau-Heemstra dkk., 2023). Lebih
jauh lagi, komersialisasi pariwisata massal berisiko mengikis keaslian
budaya lokal di destinasi populer, sehingga menimbulkan ketegangan
antara kebutuhan ekonomi dan pelestarian warisan (Siyamiyan Gorji dkk.,
2026). Sementara itu, destinasi alternatif yang kurang dikunjungi
kehilangan peluang untuk mengembangkan interaksi budaya yang lebih
berkelanjutan (Hoarau-Heemstra dkk., 2023). Oleh karena itu, distribusi
wisatawan yang tidak merata tidak hanya memperburuk beban sosial di
destinasi utama, tetapi juga menghambat potensi pembangunan komunitas di
wilayah lain (Hoarau-Heemstra dkk., 2023).

Fenomena global tersebut terkonfirmasi oleh data empiris dari Kabupaten
Sumedang, DISPARBUDPORA (2024) melaporkan distribusi kunjungan yang
sangat timpang: dari 77 destinasi terdaftar, 72,4% total kunjungan
terpusat pada hanya 10 destinasi populer (13% dari total destinasi),
menghasilkan distribusi Pareto yang jauh lebih ekstrem dibandingkan
rasio klasik 80/20.

Dominasi destinasi *mainstream* menunjukkan pola yang konsisten dengan
temuan tentang *popularity bias*, di mana item-item populer cenderung
direkomendasikan secara berlebihan bahkan kepada pengguna yang minatnya
lebih ke arah item *niche* atau kurang populer (Abdollahpouri dkk.,
2021). Fenomena ini menyebabkan item-item populer mendominasi
rekomendasi yang diberikan kepada semua pengguna (Abdollahpouri dkk.,
2021). Menara Kujang Sapasang menerima 306.333 kunjungan (18,2% dari
total kunjungan kabupaten), sementara OW Janspark mencatat 249.579
kunjungan (14,8%). Kontras yang mencolok terlihat pada destinasi
berpotensi tinggi namun terabaikan: Kampung Adat Cikondang hanya
menerima 8.450 kunjungan (0,5%), meskipun menawarkan *authentic cultural
experience* yang unik. Museum Prabu Geusan Ulun, yang memiliki nilai
historis tinggi, hanya dikunjungi 14.232 wisatawan (0,8% dari total).

Fenomena *\'popularity bias\'* menjadi akar permasalahan dalam algoritma
rekomendasi konvensional. Sistem berbasis *Collaborative Filtering*
cenderung memperkuat preferensi mayoritas sehingga menciptakan siklus
"yang kaya semakin kaya", di mana destinasi populer mendapat visibilitas
berlebih sementara destinasi bernilai tinggi namun kurang terekspos
terpinggirkan hal ini dijelaskan oleh Abdollahpouri dkk., (2021).
Menurut temuan Abdollahpouri dkk., (2021) kurang dari 3% item dapat
mendominasi 100% rekomendasi pada sistem *Item-Collaborative Filtering*,
dan dominasi mencapai 99% pada *User-Collaborative Filtering*.

Konsekuensi bias algoritmik melampaui masalah teknis semata. Dalam ruang
pariwisata Barykin dkk., (2021) serta Solano-Barliza dkk., (2024)
menunjukkan bagaimana *popularity bias* berkontribusi pada *overtourism*
yang merusak destinasi populer secara paralel. Ricci dkk., (2022)
menyoroti munculnya "gurun ekonomi" pada destinasi potensial yang
terabaikan. Konsentrasi wisatawan yang tidak berkelanjutan mengikis
autentisitas budaya lokal dan menciptakan ketimpangan ekonomi regional
operator pariwisata skala kecil seringkali kehilangan akses pasar akibat
*algorithmic invisibility*.

Upaya mitigasi *popularity bias* melalui teknik diversifikasi
memperlihatkan hasil yang menjanjikan. Yalcin dan Bilge, (2021)
misalnya, melaporkan bahwa *Maximal Marginal Relevance* (MMR) mampu
meningkatkan keberagaman rekomendasi dengan mengoptimalisasi *trade-off*
antara relevansi dan dissimilarity, dalam kerangka MMR, parameter lambda
(λ ∈ \[0,1\]) mengatur keseimbangan tersebut λ=0 menekankan relevansi
murni dan λ=1 memaksimalkan keberagaman tanpa mempertimbangkan
relevansi. Namun, pendekatan dengan parameter λ statis memiliki
keterbatasan signifikan dalam merespons dinamika pariwisata. Optimalitas
λ bersifat kontekstual dan dapat berubah secara drastis berdasarkan
kondisi *real-time*.

Perubahan konteks seperti perubahan cuaca, kepadatan pengunjung, atau
viral trends pada media sosial memengaruhi preferensi relevansi versus
diversitas, Shi dkk., (2023) dan Yoon dan Choi, (2023) menyoroti
dinamika konteks semacam ini. Ketika cuaca beralih dari cerah menjadi
hujan lebat, misalnya, sistem harus meningkatkan prioritas relevansi (λ
tinggi) untuk destinasi indoor dan mengurangi diversitas agar tidak
merekomendasikan destinasi outdoor yang tidak layak kondisi seperti ini
menuntut mekanisme adaptif yang mampu menyesuaikan λ secara *real-time*.

*Multi-Armed Bandit* (MAB) menawarkan solusi untuk masalah adaptasi
parameter λ secara otomatis. MAB bekerja dengan mencoba berbagai nilai λ
(misalnya 0.0, 0.3, 0.5, 0.7, 1.0) dan secara bertahap belajar nilai
mana yang paling efektif untuk setiap kondisi konteks. Dengan menerima
feedback dari interaksi pengguna (klik, rating), sistem dapat terus
menyesuaikan pilihan λ optimal berdasarkan perubahan cuaca, lalu lintas,
atau tren viral secara berkelanjutan (Shi dkk., 2023).

Meskipun potensi integrasi MAB dengan teknik diversifikasi seperti
*Maximal Marginal Relevance* (MMR) telah diidentifikasi, implementasi
sistematis untuk optimasi parameter dinamis dalam lingkungan pemrosesan
kontekstual *real-time* data multimodal pariwisata belum dieksplorasi
secara komprehensif. Kesenjangan (gap) penelitian ini mengindikasikan
urgensi pengembangan sistem rekomendasi pariwisata adaptif yang dapat
menjawab tantangan distribusi tidak merata sekaligus mempertahankan
kualitas rekomendasi.

## Rumusan Masalah

Berdasarkan identifikasi masalah tersebut, rumusan masalah penelitian
ini adalah:

1.  Bagaimana optimasi dinamis parameter λ pada MMR menggunakan
    *Multi-Armed Bandit* dapat meningkatkan keberagaman dan cakupan
    rekomendasi tanpa mengorbankan akurasi?

2.  Seberapa besar pengaruh integrasi data kontekstual (cuaca dan
    kalender secara *real-time*, serta simulasi lalu lintas dan tren
    media sosial) dalam mendorong pemerataan distribusi kunjungan
    pariwisata, diukur melalui pengurangan koefisien Gini dan
    peningkatan *Coverage@K*?

3.  Sejauh mana sistem rekomendasi adaptif dapat meningkatkan eksposur
    destinasi kurang populer dibandingkan sistem konvensional, diukur
    melalui metrik *Novelty, long-tail coverage,* dan evaluasi kepuasan
    pengguna (*user acceptance*)?

## Tujuan Penelitian

Tujuan utama penelitian ini adalah pengembangan sistem rekomendasi
pariwisata adaptif dengan optimasi parameter *Multi-Armed Bandit* pada
*Maximal Marginal Relevance* yang menyeimbangkan *trade-off* antara
akurasi (Precision@K, NDCG) dan keberagaman (*Intra-List Diversity*),
serta memvalidasi dampaknya terhadap pemerataan distribusi rekomendasi
(*Gini coefficient*), peningkatan *catalog coverage*, dan eksposur
destinasi kurang populer melalui evaluasi offline. Secara spesifik,
tujuan penelitian meliputi:

1.  Mengembangkan mekanisme parameter tuning adaptif berbasis
    *Multi-Armed Bandit* pada *Maximal Marginal Relevance* untuk
    mengoptimalkan keseimbangan antara akurasi (NDCG@10) dan keberagaman
    (*Intra-List Diversity*), serta memvalidasi dampaknya terhadap
    distribusi rekomendasi yang lebih merata (*Gini coefficient*) dan
    eksposur item yang lebih luas (Coverage@K).

2.  Mengintegrasikan data kontekstual dinamis (cuaca dan kalender secara
    *real-time* melalui API, serta model simulasi lalu lintas dan tren
    media sosial) dalam sistem rekomendasi untuk meningkatkan relevansi
    rekomendasi dan memperluas eksposur destinasi, serta memvalidasi
    dampaknya terhadap pemerataan distribusi rekomendasi (*Gini
    coefficient*) dan peningkatan *catalog coverage*.

3.  Merancang dan menguji sistem rekomendasi adaptif melalui evaluasi
    hybrid: (a) *offline evaluation* komprehensif menggunakan metrik
    akurasi (Precision@K, Recall@K, NDCG@K), metrik keberagaman
    (*Intra-List Diversity*), metrik distribusi (Gini coefficient,
    Coverage@K), dan (b) *online user testing* dengan *prototype* web
    menggunakan *System Usability Scale* (SUS), guna menilai dampaknya
    terhadap eksposur destinasi kurang populer secara komprehensif.

## Ruang Lingkup Masalah

Agar penelitian lebih terarah, ruang lingkup masalah dibatasi pada
aspek-aspek berikut:

1.  Penggunaan data kontekstual dinamis meliputi cuaca dan kalender
    secara *real-time* melalui API (*OpenWeatherMap* dan
    *Calendarific*), serta model simulasi untuk kondisi lalu lintas dan
    tren media sosial guna validasi logika adaptasi algoritma.

2.  Penelitian difokuskan pada destinasi wisata di Kabupaten Sumedang.

3.  Analisis dilakukan terhadap tingkat keberagaman dan cakupan
    rekomendasi destinasi.

4.  Evaluasi performa sistem mencakup metrik *Precision@K, NDCG, Gini
    Coefficient, Intra-List Diversity, Coverage@K,* dan *Novelty.*

5.  Evaluasi berbasis pengguna dilakukan melalui user testing dengan
    pengamatan langsung terhadap interaksi pengguna.

6.  Evaluasi sistem dilakukan dalam dua tahap: (1) *offline evaluation*
    untuk validasi metrik kuantitatif, dan (2) online *user testing*
    dengan *prototype web* terbatas untuk validasi *usability* dan *user
    acceptance*.

7.  Evaluasi terbatas pada rekomendasi destinasi wisata (tidak termasuk
    akomodasi).

## Kontribusi Keilmuan

Kontribusi utama penelitian ini terletak pada pengembangan mekanisme
optimasi parameter adaptif untuk *Maximal Marginal Relevance* (MMR)
menggunakan algoritma *Multi-Armed Bandit* (MAB). Penelitian ini mengisi
celah pada literatur sistem rekomendasi pariwisata yang sebelumnya
didominasi oleh pendekatan parameter statis, dengan menawarkan solusi
dinamis untuk menyeimbangkan trade-off antara akurasi dan keberagaman
secara otomatis. Pendekatan ini terbukti memberikan kontribusi empiris
dalam memitigasi *popularity bias* dan meningkatkan eksposur destinasi
long-tail tanpa mengorbankan relevansi, khususnya pada kondisi data
dengan tingkat kelangkaan (sparsity) tinggi.

## Hipotesis

Pada penelitian ini terdapat beberapa premis yang menjadi dasar
pemikiran untuk memperoleh hasil sesuai tujuan yang telah dirancang.
Beberapa premis tersebut adalah sebagai berikut:

1.  Model optimasi dinamis (seperti MAB/RL) mampu menyeimbangkan tujuan
    yang saling bertentangan (misalnya, relevansi dan keberagaman)
    secara adaptif (Shi dkk., 2023). Hal ini mengatasi keterbatasan
    *trade-off* kaku pada MMR berparameter statis, yang cenderung
    mengorbankan akurasi untuk meningkatkan keberagaman (Shi dkk.,
    2023).

2.  *Popularity bias* dominasi item populer yang diukur metrik seperti
    *Coverage* dan Koefisien Gini memerlukan mitigasi (Yalcin dan Bilge,
    2021). Dalam domain pariwisata, integrasi data kontekstual
    *real-time* (misalnya, waktu, lokasi) melalui *contextual bandit*
    krusial untuk personalisasi yang adaptif (Qassimi dan Rakrak, 2025).

3.  Kerangka kerja adaptif dirancang untuk memitigasi *popularity bias*
    (Shi dkk., 2023). Pendekatan ini terbukti meningkatkan *novelty* dan
    *Diversity* sehingga mempromosikan eksposur *long-tail* sembari
    mempertahankan akurasi yang memadai dibandingkan model statis (Shi
    dkk., 2023).

Dari beberapa premis tersebut, didapat hipotesis yang mencerminkan fokus
utama penelitian ini, yaitu: \"Implementasi *Multi-Armed Bandit* untuk
optimasi parameter dinamis pada *Maximal Marginal Relevance* yang
dikombinasikan dengan pemrosesan kontekstual *real-time* dapat secara
efektif mengatasi *popularity bias*, meningkatkan keberagaman dan
cakupan destinasi, serta mempertahankan akurasi prediktif dalam sistem
rekomendasi pariwisata adaptif.\"

## Sistematika Penulisan

Dalam penyusunan tesis ini, penelitian ini terbagi menjadi lima bab
dengan penjabaran untuk masing-masing bab sebagai berikut.

BAB I Pendahuluan

> Bab ini membahas mengenai latar belakang masalah, rumusan masalah,
> maksud dan tujuan, batasan masalah, metodologi penelitian, dan
> sistematika penulisan yang digunakan.

BAB II Tinjauan Pustaka

> Bab ini membahas mengenai konsep dasar serta teori-teori yang
> berkaitan dengan topik penelitian dan hal-hal yang berguna dalam
> proses analisis permasalahan.

BAB III Metodologi Penelitian

> Bab ini berisi tentang metodologi penelitian yang digunakan dalam
> melakukan penelitian serta dijelaskan metode yang dilakukan setiap
> tahapan mulai dari awal sampai dengan akhir.

BAB IV Implementasi dan Hasil Penelitian

> Bab ini menyajikan dokumentasi implementasi sistem, *statistical
> analysis*, dan *interpretation of results* dalam konteks *research
> questions* yang telah diformulasikan.

BAB V Kesimpulan dan Saran

> Bab ini merangkum kesimpulan utama yang menjawab rumusan masalah.
> *acknowledge limitations*, dan menyajikan *future research directions*
> yang spesifik dan *actionable*.

# Tinjauan Pustaka

Tinjauan pustaka dalam penelitian ini membahas teori-teori yang
mendasari pengembangan sistem rekomendasi pariwisata adaptif. Bagian ini
mencakup kajian teori, penelitian terdahulu, serta kerangka pemikiran
yang menjadi dasar dalam perancangan sistem.

## Sistem Rekomendasi dalam Ekosistem Pariwisata Digital

Industri pariwisata telah mengalami transformasi digital fundamental
yang dipercepat oleh peristiwa global (Barykin dkk., 2021). Studi
tersebut menekankan bahwa solusi teknologi menjadi krusial agar industri
ini dapat tumbuh lebih tangguh dan berkelanjutan. Sebagai
konsekuensinya, para pelaku industri dituntut untuk meningkatkan
kehadiran *e-commerce*, menawarkan pengalaman digital yang inovatif, dan
mengoptimalkan strategi pemasaran destinasi mereka (Barykin dkk., 2021).

Pertumbuhan data eksponensial di internet (*information overload*)
(Huang dkk., 2020 dan Alfaifi, 2024) menciptakan paradoks kelebihan
informasi (*information overload*) (Kumar dkk., 2024 dan Sachi Nandan
Mohanty, 2020). Paradoks ini secara fundamental menghambat kemampuan
pengguna untuk mengakses konten yang relevan dengan cepat (Huang dkk.,
2020) dan menjadikan pencarian rekomendasi yang benar-benar sesuai
sebagai sebuah tantangan kompleks (Kumar dkk., 2024). Oleh karena itu,
sistem rekomendasi hadir sebagai alat mitigasi yang krusial, dirancang
khusus untuk mengelola surplus informasi ini dan memfasilitasi
pengambilan keputusan yang lebih optimal bagi pengguna (Gotthardt dan
Mezhuyev, 2022).

Dengan demikian, peran strategis Sistem Rekomendasi melampaui sekadar
mekanisme penyelesaian masalah kelebihan informasi (Shuvo dan Islam,
2024). Lebih dari itu, SR berfungsi sebagai pendorong pergeseran
paradigma dalam perilaku wisatawan dari pemrosesan informasi yang
reaktif menuju kurasi pengalaman yang proaktif. Kemampuan SR untuk
menyediakan rekomendasi yang personal dan relevan, seperti yang
ditekankan oleh Javadian Sabet dkk., (2022) dan Ricci dkk., (2022) serta
beradaptasi sesuai situasi waktu nyata (Yoon dan Choi, 2023), secara
signifikan mengurangi beban kognitif wisatawan (Shambour dkk., 2024).
Hal ini membebaskan kapasitas mental mereka untuk fokus pada aspirasi
yang lebih mendalam: mencari pengalaman yang otentik (Shafqat dan Byun,
2020), meningkatkan kepuasan, dan memperkaya pengalaman perjalanan (Choi
dkk., 2021), bahkan mendukung pencapaian tujuan pariwisata berkelanjutan
(Yoon dan Choi, 2023).

Pergeseran menuju pencarian pengalaman ini diperkuat oleh data empiris
yang kuat. Temuan bahwa 78% wisatawan global merasa \'lebih hidup\' saat
berlibur dan 68% merasa menjadi versi terbaik dari diri mereka
Booking.com, (2023) mengindikasikan bahwa perjalanan telah berevolusi
menjadi sebuah medium aktualisasi diri. Fenomena ini sejalan dengan
konsep \"Paradigma Pariwisata 2.0\" yang, menurut Yoon dan Choi, (2023)
mengedepankan pengalaman budaya partisipatif daripada sekadar konsumsi.

Dalam konteks ini, kemampuan SR untuk menyaring dan mengarahkan pengguna
ke item-item baru yang relevan (Ricci dkk., 2022) menjadi instrumen
strategis (Gotthardt dan Mezhuyev, 2022) untuk menerjemahkan aspirasi
wisatawan menjadi rekomendasi yang otentik dan personal (Shambour dkk.,
2024). Kemampuan SR untuk menawarkan atraksi yang dipersonalisasi
berdasarkan analisis pola perjalanan dan preferensi, seperti yang
dijelaskan oleh Choi dkk., (2021) secara fundamental meningkatkan
pengalaman wisatawan dan menjadikan perjalanan sebagai jalur yang lebih
bermakna menuju pengembangan pribadi, sebuah tren yang sejalan dengan
pantauan (World Tourism Organization, 2024).

Oleh karena itu, sistem rekomendasi berfungsi tidak hanya sebagai
instrumen teknis untuk mengatasi *information overload*, melainkan juga
sebagai fasilitator transformasi fundamental dalam cara wisatawan
merencanakan dan mengalami perjalanan mereka. Kemampuan SR untuk
menyeimbangkan personalisasi dengan penemuan pengalaman otentik menjadi
titik tolak bagi penelitian ini dalam mengembangkan sistem yang tidak
hanya relevan tetapi juga mendorong diversifikasi destinasi wisata.

## Tantangan Sistem Rekomendasi Konvensional: *Popularity Bias*

Dalam lanskap sistem rekomendasi yang terus berkembang (Alfaifi, 2024),
*popularity bias* menjadi sebuah fenomena sistemik yang signifikan. Bias
ini menyebabkan item-item populer direkomendasikan secara tidak
proporsional dibandingkan item *long-tail*. Seperti yang diidentifikasi
oleh Yalcin dan Bilge, (2021) dan Abdollahpouri dkk., (2021), *item
niche* tersebut mungkin sangat relevan bagi preferensi pengguna namun
terabaikan. Kecenderungan intrinsik ini menghasilkan efek \"yang kaya
semakin kaya\" (*the rich get richer*), di mana item-item populer secara
sistematis diuntungkan (Abdollahpouri dkk., 2021). Akibatnya, konten
populer mendapatkan visibilitas berlebihan yang kemudian meningkatkan
konsumsinya secara eksponensial. Kondisi ini, menurut Abdollahpouri,
(2019) dan Ricci dkk., (2022), menyebabkan marjinalisasi terhadap
item-item niche, terutama yang baru, meskipun memiliki potensi relevansi
yang tinggi.

Akar dari bias algoritmik ini terletak pada karakteristik fundamental
algoritma itu sendiri, yang dilatih berdasarkan pola preferensi pengguna
yang tidak terdistribusi secara merata (Yalcin dan Bilge, 2021 dan
Abdollahpouri dkk., 2020). Sebagian besar pengguna cenderung
mengevaluasi item-item tertentu saja, sementara item lainnya hanya
menerima sedikit penilaian, sehingga menciptakan distribusi data yang
timpang (Abdollahpouri dkk., 2021). Ricci dkk., (2022) mengamati bahwa
kondisi ini diperparah oleh kecenderungan mayoritas algoritma
*Collaborative Filtering* (CF) yang memusatkan rekomendasi pada selera
mayoritas, sehingga sering kali mengorbankan kebaruan dan keberagaman.
Dalam analisisnya, Falk, (2019) menjelaskan bahwa sifat CF yang
content-agnostic di mana rekomendasi didasarkan pada tren perilaku
agregat turut memperkuat fenomena ini. Karena, seperti ditekankan oleh
Falk, (2019) kesamaan (*similarity*) adalah basis komputasinya, item
terpopuler secara statistik akan memiliki korelasi lebih tinggi dengan
spektrum konten yang lebih luas. Temuan dari (Abdollahpouri dkk., 2021)
bahkan menegaskan kerentanan inheren SR berbasis CF, di mana kurang dari
3% item dapat mendominasi 100% rekomendasi pada Item-CF, dan
konsentrasinya mencapai 99% pada User-CF.

Implikasi dari bias ini menjadi sangat kompleks dalam domain pariwisata,
menghasilkan konsekuensi sosial seperti fenomena overtourism dan
degradasi autentisitas destinasi (Barykin dkk., 2021 dan Solano-Barliza
dkk., 2024). Destinasi yang sudah populer menerima penguatan bias
melalui rekomendasi yang berlebihan, sehingga menciptakan konsentrasi
wisatawan yang tidak berkelanjutan. Fenomena ini berkontribusi pada
pembentukan \"daftar pendek destinasi wisata yang menarik jutaan
pelancong,\" sebuah istilah yang dikemukakan oleh Pencarelli, (2020).
Tekanan demografis yang dihasilkan dari konsentrasi massal ini bahkan
dapat menyebabkan perpindahan penduduk lokal dari pusat-pusat bersejarah
karena area tersebut bertransformasi menjadi dominasi aktivitas turistik
(Pencarelli, 2020). Ironisnya, wisatawan justru kehilangan pengalaman
otentik yang mereka cari. Pada akhirnya, seperti yang dicatat oleh
Pencarelli, (2020) kondisi ini merugikan baik penduduk maupun wisatawan
dalam jangka panjang. Menciptakan sebuah lingkaran degradasi di mana
marjinalisasi komunitas lokal secara langsung mengikis autentisitas,
sebuah poin krusial yang juga diamati oleh Ricci dkk., (2022).

Konsekuensi sosial tersebut merambat ke dalam struktur ekonomi regional.
*Popularity bias* menciptakan perbedaan pasar yang sistematis, terlihat
melalui konsentrasi pendapatan yang tidak proporsional di antara
penyedia layanan pariwisata (Abdollahpouri, 2019 dan Ricci dkk., 2022).
Sebagai analogi dari domain hiburan, data menunjukkan bahwa produk dari
hanya 3 sutradara (kurang dari 0,4% dari total kreator) dapat
mendominasi 50% dari seluruh rekomendasi (Ricci dkk., 2022). Dalam
ekosistem pariwisata, pola konsentrasi serupa menyebabkan marjinalisasi
sistematis terhadap operator pariwisata skala kecil. Yoon dan Choi,
(2023) menambahkan bahwa keterbatasan akses data untuk destinasi yang
kurang mapan semakin memperburuk siklus ini, menciptakan mekanisme yang
terus-menerus memperkuat bias algoritmik. (Ricci dkk., 2022) berargumen
bahwa kondisi ini jelas bertentangan dengan tujuan fundamental SR di
industri pariwisata, yang idealnya berfungsi mendorong diversifikasi
konsumsi dan penemuan produk *long-tail*. Oleh karena itu, penanganan
bias popularitas menuntut intervensi yang melampaui optimisasi teknis
semata, sebuah tantangan yang menuntut kerangka kerja terintegrasi,
sejalan dengan pemikiran Abdollahpouri, (2019) dan Ricci dkk., (2022),
untuk memastikan terciptanya ekosistem pariwisata yang lebih merata dan
berkelanjutan.

Analisis komprehensif terhadap popularity bias dan dampaknya yang
multidimensi mulai dari degradasi pengalaman wisatawan hingga
ketimpangan ekonomi regional mendasari urgensi penelitian ini. Fenomena
*overtourism* dan marjinalisasi destinasi *long-tail* yang
diidentifikasi dalam tinjauan ini bukan sekadar masalah teknis
algoritmik, melainkan tantangan sosio-ekonomi yang mendesak. Oleh karena
itu, penelitian ini tidak hanya bertujuan meningkatkan metrik teknis
seperti akurasi, tetapi secara eksplisit mengintegrasikan mekanisme
mitigasi bias popularitas melalui strategi diversifikasi adaptif yang
responsif terhadap dinamika kontekstual pariwisata.

## *Collaborative Filtering* dalam Sistem Rekomendasi Sektor Pariwisata

*Collaborative Filtering* (CF) merupakan metodologi fundamental yang
paling banyak diadopsi dalam sistem rekomendasi (Wang dkk., 2022) dan
telah menjadi salah satu pendekatan dominan dalam domain pariwisata
(Solano-Barliza dkk., 2024). Pendekatan ini bekerja dengan
merekomendasikan berdasarkan analisis pola perilaku pengguna dengan
preferensi serupa (Yoon dan Choi, 2023).

CF berbasis pengguna mengidentifikasi sekelompok kecil wisatawan dengan
preferensi serupa dan menggunakan pola kunjungan mereka untuk
merekomendasikan destinasi yang belum dikunjungi oleh pengguna target
(Nan dkk., 2022). Keunggulan utama CF terletak pada kemampuannya
menghasilkan rekomendasi yang dipersonalisasi meskipun kesamaan konten
antar destinasi tidak tinggi, karena metode ini sepenuhnya bergantung
pada pola interaksi pengguna-item (Yoon dan Choi, 2023). Dalam konteks
pariwisata yang kompleks, CF memainkan peran krusial dalam mencocokkan
berbagai fasilitas pariwisata seperti restoran, hotel, dan museum dengan
minat individual wisatawan, sehingga secara signifikan meningkatkan
kepuasan dan pengalaman perjalanan (Shambour dkk., 2024 dan Choi dkk.,
2021).

Namun, sistem rekomendasi berbasis CF menghadapi sejumlah keterbatasan
fundamental yang menghambat efektivitasnya dalam layanan perencanaan
perjalanan (Choi dkk., 2021). Pertama, CF sangat rentan terhadap masalah
data sparsity, terutama untuk destinasi baru atau kurang populer yang
memiliki sedikit interaksi historis (Yoon dan Choi, 2023). Kedua, sifat
*content-agnostic* CF yang hanya mengandalkan pola perilaku agregat
cenderung memperkuat popularity bias, di mana destinasi populer secara
sistematis direkomendasikan secara berlebihan (Falk, 2019 dan
Abdollahpouri dkk., 2021). Ketiga, CF tradisional tidak mampu
mengakomodasi faktor kontekstual dinamis seperti cuaca, waktu, atau
teman seperjalanan yang sangat memengaruhi keputusan wisatawan (Massimo
dan Ricci, 2022).

Keterbatasan-keterbatasan CF konvensional ini menjadi justifikasi utama
bagi penelitian ini untuk mengembangkan pendekatan hibrida yang
mengintegrasikan CF dengan teknik lain. Dengan menggabungkan kekuatan CF
dalam personalisasi dengan mekanisme *context-aware* dan strategi
diversifikasi adaptif, penelitian ini bertujuan mengatasi kelemahan
inheren CF sambil mempertahankan kemampuan personalisasinya. Pendekatan
ini menjadi fondasi bagi sistem rekomendasi yang tidak hanya akurat
tetapi juga beragam dan responsif terhadap dinamika kontekstual
pariwisata.

## *Context-Aware Recommendations* dalam Domain Pariwisata

Domain pariwisata memiliki karakteristik unik yang membedakannya dari
domain rekomendasi lain seperti *e-commerce* atau hiburan (Fararni dkk.,
2021). Keputusan seorang wisatawan sangat dipengaruhi oleh serangkaian
faktor dinamis yang melampaui preferensi historis mereka. Faktor-faktor
seperti cuaca, waktu, lokasi geografis, hingga teman seperjalanan dapat
secara fundamental mengubah jenis destinasi atau aktivitas yang
diinginkan (Yoon dan Choi, 2023). Oleh karena itu, sistem rekomendasi
pariwisata tradisional yang hanya mengandalkan interaksi *User x Item*
seringkali tidak memadai (Massimo dan Ricci, 2022). Untuk mengatasi
keterbatasan ini, *Context-Aware Recommender Systems* (CARS) menjadi
pendekatan yang sangat relevan. CARS memperluas model rekomendasi
tradisional menjadi tiga dimensi (*User x Item x Context*), dengan
tujuan memberikan rekomendasi yang tepat untuk situasi spesifik pengguna
(Suhaim dan Berri, 2021).

### Kategori Konteks dalam Pariwisata

Konteks dalam pariwisata dapat dikategorikan ke dalam beberapa dimensi
utama, yang meliputi:

1.  Konteks Lingkungan (*Environmental Context*): Faktor eksternal yang
    tidak dapat dikontrol oleh pengguna namun sangat memengaruhi
    pengalaman wisata, seperti Waktu (*Temporal*), Lokasi
    (*Spatial/Geographical*), dan Cuaca (*Weather*) (Yoon dan Choi,
    2023).

2.  Konteks Pengguna (*User Context*): Faktor-faktor yang melekat pada
    pengguna dan situasinya saat itu, seperti Konteks Sosial (teman
    seperjalanan) (Suhaim dan Berri, 2021), Konteks Demografis (Shafqat
    dan Byun, 2020), dan Konteks Emosional (*Mood*) (Bukhari dkk.,
    2025).

3.  Konteks Interaksi (*Interaction Context*): Faktor yang berkaitan
    dengan cara pengguna berinteraksi dengan sistem, seperti Perangkat
    (*Device*) (Fararni dkk., 2021) dan Tujuan Perjalanan (*Trip
    Purpose*) (Javadian Sabet dkk., 2022).

### Pendekatan Integrasi Konteks

Terdapat tiga paradigma utama untuk mengintegrasikan informasi
kontekstual ke dalam proses rekomendasi, seperti yang diidentifikasi
oleh Suhaim dan Berri, (2021):

1.  *Pre-Filtering* (Pra-Penyaringan Kontekstual): Konteks digunakan
    untuk memfilter data interaksi *sebelum* algoritma rekomendasi
    dijalankan. Pendekatan ini berisiko memperburuk masalah *data
    sparsity*.

2.  *Post-Filtering* (Pasca-Penyaringan Kontekstual): Daftar rekomendasi
    umum yang sudah jadi akan disaring atau diurutkan ulang berdasarkan
    konteks pengguna saat ini. Pendekatan ini sederhana namun berisiko
    kehilangan item yang relevan.

3.  *Contextual Modeling* (Pemodelan Kontekstual): Informasi kontekstual
    dimasukkan secara langsung sebagai fitur eksplisit ke dalam model
    prediksi. Pendekatan ini dianggap lebih canggih karena mampu
    menangkap interaksi kompleks antara pengguna, item, dan konteks .

Berdasarkan analisis keunggulan dan keterbatasan tersebut, penelitian
ini mengusulkan pendekatan hibrida yang mengombinasikan kekuatan
pemodelan kontekstual (contextual modeling) pada tahap candidate
generation dengan fleksibilitas pasca-penyaringan kontekstual
(post-filtering) pada tahap re-ranking. Pendekatan ini memastikan
informasi kontekstual tidak hanya memengaruhi pemilihan kandidat awal
tetapi juga secara dinamis menyesuaikan urutan rekomendasi final
berdasarkan kondisi *real-time* pengguna. Dengan demikian, sistem yang
dikembangkan menghasilkan rekomendasi yang tidak hanya relevan secara
situasional tetapi juga dioptimalkan untuk tujuan keberagaman dan
pemerataan destinasi wisata, sebuah kebutuhan krusial yang terabaikan
dalam pendekatan context-aware konvensional.

## Pendekatan Hibrida untuk Personalisasi

Sistem rekomendasi hibrida (*Hybrid Recommender Systems*, HRS) dirancang
untuk mengatasi keterbatasan model tunggal dengan menggabungkan dua atau
lebih teknik rekomendasi, dengan tujuan memanfaatkan keunggulan
masing-masing dan mengimbangi kelemahannya (Fararni edkk., 2021 dan
Solano-Barliza dkk., 2024). Dalam domain pariwisata, pendekatan ini
umumnya mengintegrasikan tiga komponen utama: (1) *Content-Based
Filtering* (CBF) yang memanfaatkan fitur deskriptif destinasi untuk
merekomendasikan item serupa dengan preferensi pengguna sebelumnya
(Falk, 2019), (2) *Collaborative Filtering* (CF) yang menganalisis pola
interaksi historis pengguna-item untuk menghasilkan rekomendasi personal
(Sachi Nandan Mohanty, 2020), dan (3) *Context-Aware Recommender
Systems* (CARS) yang memasukkan informasi kontekstual seperti waktu,
lokasi, atau teman perjalanan (Sachi Nandan Mohanty, 2020).

Berbagai strategi hibridisasi telah diidentifikasi dalam literatur,
seperti *weighted hybrid, switching hybrid, cascaded hybrid, dan
feature-combination hybrid* (Sachi Nandan Mohanty, 2020). Meskipun HRS
terbukti efektif mengatasi masalah cold-start dan data sparsity (Ko
dkk., 2022), implementasinya menimbulkan tantangan berupa peningkatan
kompleksitas komputasi dan kebutuhan penyetelan hiperparameter yang
cermat untuk mencapai kinerja optimal (Akhadam dkk., 2025 dan Falk,
2019).

Untuk mengatasi keterbatasan parameter statis dalam HRS konvensional,
penelitian kontemporer mulai mengadopsi teknik optimasi adaptif seperti
*Multi-Armed Bandit* (MAB) yang menyediakan kerangka kerja dinamis untuk
penyesuaian rekomendasi secara *real-time* (Qassimi dan Rakrak, 2025).
MAB memungkinkan sistem untuk belajar dan beradaptasi dari umpan balik
yang diterima secara berkelanjutan, sehingga mampu menangani dilema
eksplorasi-eksploitasi dan merespons perubahan minat pengguna yang tidak
dapat ditangani oleh metode statis tradisional (Bukhari dkk., 2025).

Dalam konteks *re-ranking*, teknik *Maximal Marginal Relevance* (MMR)
menyediakan pendekatan untuk memaksimalkan kombinasi linear antara
relevansi dan keberagaman dalam daftar rekomendasi (Ricci dkk., 2022).
Daftar kandidat yang dihasilkan oleh kombinasi CF dan CB dapat
di-re-rank menggunakan MMR untuk mencapai kompromi optimal antara
akurasi dan diversitas (Shi dkk., 2023). Parameter lambda (λ) dalam MMR
mengontrol *trade-off* ini (Abdollahpouri dkk., 2021), dan ketika
dikombinasikan dengan mekanisme pembelajaran adaptif MAB, sistem dapat
secara otomatis menyesuaikan bobot ini berdasarkan konteks dan umpan
balik pengguna (Qassimi dan Rakrak, 2025).

Penelitian ini mengadopsi arsitektur *hybrid cascaded* yang
mengintegrasikan *collaborative filtering* dan *content-based filtering*
pada tahap *candidate generation*, kemudian menerapkan re-ranking
adaptif berbasis MAB-MMR yang parameter lambda-nya dioptimasi secara
dinamis berdasarkan pemrosesan kontekstual. Pendekatan ini menjawab
kebutuhan akan sistem yang tidak hanya personal dan beragam, tetapi juga
mampu beradaptasi terhadap perubahan konteks *real-time* yang inheren
dalam domain pariwisata.

## Keberagaman dan Cakupan

Shambour dkk., (2024) mencatat bahwa evaluasi sistem rekomendasi secara
historis sangat bertumpu pada metrik akurasi prediktif, seperti *Mean
Absolute Error* (MAE) dan *Root Mean Square Error* (RMSE). MAE mengukur
selisih absolut rata-rata antara prediksi dan rating aktual, sedangkan
RMSE menjalankan fungsi serupa namun dengan memberikan bobot lebih pada
kesalahan yang besar (Falk, 2019). Namun, studi oleh Choi dkk., (2021)
menunjukkan bahwa dalam konteks pariwisata yang kompleks, metrik akurasi
tradisional ini menjadi tidak memadai.

Ricci dkk., (2022) mengidentifikasi bahwa peningkatan marginal dalam
akurasi yang dilaporkan dalam riset sering kali tidak berkorelasi dengan
persepsi kualitas pengguna di dunia nyata. Akibatnya, sebuah SR dapat
menunjukkan kinerja offline yang sangat baik, namun gagal dalam
implementasi praktis karena tidak selaras dengan ekspektasi pengguna
atau tujuan bisnis yang lebih luas (Ricci dkk., 2022). Keterbatasan ini
juga terlihat dari ketidakmampuannya untuk secara inheren mengevaluasi
rekomendasi item komposit, seperti paket tur (Choi dkk., 2021).

Bahkan, dalam beberapa aplikasi pariwisata, metrik seperti *precision*
menjadi kurang relevan karena pengguna mungkin tidak diharapkan memilih
lebih dari satu item. Fokus yang berlebihan pada akurasi juga cenderung
memperkuat *popularity bias*, yang mengakibatkan sistem merekomendasikan
item-item populer tanpa memberikan nilai tambah yang signifikan (Yalcin
dan Bilge, 2021). Dengan demikian, diperlukan paradigma evaluasi yang
lebih holistik.

Melampaui akurasi, keberagaman muncul sebagai salah satu dimensi
evaluasi yang esensial (Abdollahpouri dkk., 2020). Akhadam dkk., (2025)
mendefinisikan keberagaman sebagai lawan dari kesamaan, yang merujuk
pada variasi item dalam sebuah daftar rekomendasi. Pengukuran
keberagaman dapat dilakukan dengan menghitung jarak rata-rata
berpasangan antar semua item dalam set tersebut (Ricci dkk., 2022).
Literatur kemudian membedakan dua jenis utama: *intra-list Diversity*,
yang mengukur perbedaan item untuk seorang pengguna, dan *inter-list
Diversity*, yang menilai perbedaan antar daftar rekomendasi untuk
pengguna yang berbeda (Akhadam dkk., 2025). Pentingnya keberagaman
didasari oleh beberapa argumen.

Sistem tradisional yang memprioritaskan kesamaan secara implisit
mengabaikan keberagaman, sebuah kelalaian yang dapat menurunkan kualitas
rekomendasi final (Ricci dkk., 2022). Rekomendasi yang beragam mampu
memperkaya pengalaman pengguna seiring waktu, membantu mereka menemukan
hal baru dan mengembangkan minat (Akhadam dkk., 2025). Tanpa keberagaman
yang memadai, pengguna berisiko terperangkap dalam \"gelembung filter\"
(*filter bubble*), di mana mereka hanya disajikan konten yang familier
(Ricci dkk., 2022). Dalam konteks pariwisata, penerapan prinsip ini
berarti merekomendasikan destinasi yang bervariasi secara geografis atau
jenis aktivitas, bukan sekadar variasi minor pada lokasi yang sama
(Shafqat dan Byun, 2020).

Dimensi evaluasi krusial lainnya adalah kebaruan (*novelty*), yang
merujuk pada sejauh mana item yang direkomendasikan belum pernah atau
jarang dilihat oleh pengguna (Abdollahpouri dkk., 2021). Sementara
keberagaman berfokus pada variasi karakteristik antar item, *novelty*
memastikan pengguna terekspos pada konten atau pengalaman yang
benar-benar baru dan tidak terduga (Ricci dkk., 2022). Di domain
pariwisata, *novelty* memiliki nilai strategis tinggi karena berkaitan
dengan penemuan hidden gems destinasi non-mainstream dengan potensi
pengalaman otentik (Abdollahpouri dkk., 2020). Sistem yang efektif
menghasilkan rekomendasi baru dapat mendorong wisatawan keluar dari zona
nyaman mereka, menemukan pengalaman yang tidak terjangkau melalui
pencarian konvensional, sekaligus mengurangi *popularity bias* dengan
mengeksplorasi item-item *long-tail* yang relevan (Abdollahpouri dkk.,
2021).

Meskipun demikian, optimalisasi *novelty* menghadirkan dilema
fundamental. Sebagaimana diperingatkan oleh Falk, (2019) terlalu banyak
*novelty* dapat mengorbankan relevansi, sementara terlalu sedikit akan
membuat rekomendasi menjadi mudah ditebak. Oleh karena itu, tantangan
utamanya terletak pada penciptaan keseimbangan dinamis antara *novelty*,
keberagaman, dan relevansi. Hal ini menuntut sebuah pendekatan adaptif
yang mampu menyesuaikan proporsi ketiga dimensi tersebut berdasarkan
konteks dan preferensi individual pengguna (Ricci dkk., 2022).

Cakupan merupakan dimensi evaluasi fundamental berikutnya, yang
mengindikasikan seberapa luas jangkauan item yang mampu direkomendasikan
oleh sistem (Akhadam dkk., 2025). Konsep ini terbagi menjadi dua aspek:
*catalog coverage*, yakni proporsi item dalam keseluruhan katalog, dan
*user coverage*, atau proporsi pengguna yang dapat menerima rekomendasi
(Akhadam dkk., 2025). Fungsi utama cakupan adalah untuk mengatasi
masalah kelangkaan data (*data sparsity)* dan *cold-start* (Suhaim dan
Berri, 2021), dengan memungkinkan sistem menjangkau beragam item bahkan
saat data interaksi masih terbatas (Alfaifi, 2024).

Dalam ranah pariwisata, riset oleh Ricci dkk., (2022) menggarisbawahi
kaitan langsung antara cakupan dengan promosi destinasi *long-tail*.
Destinasi yang baru berkembang seringkali kekurangan data historis (Yoon
dan Choi, 2023), dan sistem dengan cakupan rendah akan cenderung
mengabaikan aset potensial ini dan hanya berfokus pada item populer
(Abdollahpouri dkk., 2021). Dengan demikian, peningkatan cakupan menjadi
strategi vital untuk mendistribusikan perhatian ke item-item *long-tail*
yang krusial bagi keberlanjutan ekonomi sektor pariwisata (Ricci dkk.,
2022).

Paradigma evaluasi \"*beyond accuracy*\" yang mengintegrasikan metrik
seperti keberagaman, *novelty*, dan cakupan menawarkan penilaian yang
lebih komprehensif dan holistik terhadap sistem rekomendasi pariwisata
(Choi dkk., 2021). Penelitian ini mengadopsi kerangka evaluasi
multidimensi ini sebagai fondasi untuk mengukur keberhasilan sistem
adaptif yang dikembangkan. Lebih dari sekadar evaluasi teknis,
pendekatan ini berfungsi sebagai penjaga ekosistem autentisitas
destinasi, memastikan sistem rekomendasi berperan sebagai alat
pelestarian bukan perusak terhadap keberagaman budaya dan ekonomi lokal
yang menjadi esensi dari pariwisata berkelanjutan (Ricci dkk., 2022).
Dengan demikian, metrik-metrik ini tidak hanya menjadi alat evaluasi
tetapi juga menjadi indikator dampak sosial-ekonomi dari sistem yang
dibangun.

## *Maximal Marginal Relevance* dan *Multi-Armed Bandit*

Untuk mengatasi keterbatasan sistem rekomendasi konvensional, strategi
teknis *re-ranking* telah muncul sebagai pendekatan yang valid secara
metodologis (Yalcin dan Bilge, 2021). Abdollahpouri, (2019)
mendefinisikan re-ranking sebagai rekonfigurasi sistematis terhadap
daftar kandidat rekomendasi, dengan tujuan fundamental untuk
mengoptimalkan *trade-off* antara akurasi dan keberagaman (Yalcin dan
Bilge, 2021). Pendekatan ini mengimplementasikan intervensi algoritmik
pada tahap *post-processing*, di mana item diberi bobot berbanding
terbalik dengan popularitasnya, kemudian diorganisasi ulang berdasarkan
kriteria diversifikasi (Abdollahpouri dkk., 2021).

Salah satu algoritma diversifikasi yang paling mapan adalah *Maximal
Marginal Relevance* (MMR), yang menurut Yalcin dan Bilge, (2021)
beroperasi dengan prinsip optimasi *greedy* untuk memaksimalkan
kombinasi linear antara *similarity* terhadap preferensi pengguna dan
dissimilarity terhadap item yang sudah terseleksi. Tujuan dari MMR,
seperti dijelaskan oleh Shi dkk., (2023), adalah mengoptimalkan
relevansi sambil meminimalkan redundansi. Evaluasi kandidatnya
didasarkan pada kriteria ganda: (1) tingkat relevansi terhadap
preferensi pengguna (Noorian, 2024), dan (2) tingkat keberagaman relatif
terhadap item yang sudah ada dalam set rekomendasi (Shi dkk., 2023 dan
Zhao dkk., 2025). Regulasi keseimbangan antara relevansi dan keberagaman
ini dilakukan melalui parameter lambda (λ ∈ \[0,1\]) (Yalcin dan Bilge,
2021), yang mengontrol *trade-off* antara kedua tujuan tersebut
(Abdollahpouri dkk., 2021).

Meskipun demikian, pendekatan yang mengelola *trade-off*
relevansi-diversitas seperti MMR menghadapi keterbatasan fundamental.
Menurut Shi dkk., (2023) kelemahannya berkaitan dengan asumsi parameter
statis, di mana bobot optimal diasumsikan tidak bervariasi terhadap
dinamika kontekstual. Dalam domain pariwisata yang secara inheren tidak
stabil, kondisi kontekstual seperti perubahan cuaca, transisi musim,
atau acara lokal menuntut kalibrasi ulang yang adaptif (Massimo dan
Ricci, 2022 dan Qassimi dan Rakrak, 2025). Ketika kondisi berubah,
sistem dengan parameter statis cenderung gagal beradaptasi, sehingga
berpotensi menghasilkan rekomendasi yang suboptimal (Bukhari dkk.,
2025).

Sebagai jawaban atas keterbatasan pendekatan statis, paradigma
*Multi-Armed Bandit* (MAB) muncul sebagai kemajuan evolusioner yang
menawarkan mekanisme pembelajaran adaptif dalam lingkungan dinamis
(Qassimi dan Rakrak, 2025 dan Ricci dkk., 2022). Berbeda dengan
konfigurasi parameter tetap, MAB beroperasi berdasarkan prinsip
pembelajaran berkelanjutan (Qassimi dan Rakrak, 2025), di mana sistem
secara otonom menyesuaikan strategi berdasarkan umpan balik *real-time*
(Shi dkk., 2023). Dalam arsitekturnya, setiap \"*arm*\"
merepresentasikan strategi rekomendasi yang berbeda, dengan prioritas
yang terdiferensiasi antara relevansi, kebaruan, atau pendekatan
seimbang (Shi dkk., 2023 dan Qassimi dan Rakrak, 2025).

Keunggulan komparatif MAB terletak pada kemampuan pembelajaran daring
yang memungkinkannya beradaptasi tanpa bergantung pada data historis
(Shi dkk., 2023 dan Qassimi dan Rakrak, 2025). MAB dapat
mengintegrasikan metrik diversifikasi dalam perhitungan *expected
reward*, di mana fungsi imbalannya dirancang untuk menggabungkan
kepuasan pengguna dengan ukuran peningkatan keberagaman (Shi dkk., 2023
dan Zhao dkk., 2025). Ketika konteks berubah, sistem secara otomatis
mengidentifikasi konfigurasi lengan yang optimal dan menyesuaikan
probabilitas pemilihan strateginya (Qassimi dan Rakrak, 2025 dan Bukhari
dkk., 2025).

Dalam lanskap algoritma diversifikasi yang lebih luas, pendekatan
adaptif seperti MAB menghadapi kompetisi dari metodologi alternatif.
*Determinantal Point Processes* (DPP) menawarkan model probabilistik
untuk meningkatkan keberagaman (Shi dkk., 2023), sementara pendekatan
berbasis klaster menawarkan efisiensi komputasi yang lebih baik (Suhaim
dan Berri, 2021 dan Nan dkk., 2022), namun efektivitasnya sangat
bergantung pada kualitas algoritma klastering yang digunakan
(Chalkiadakis dkk., 2023).

Penelitian ini mengadopsi pendekatan hibrida MAB-MMR yang
mengintegrasikan kekuatan kedua paradigma: ketepatan optimasi *greedy*
MMR dalam menghasilkan daftar beragam dan fleksibilitas pembelajaran
adaptif MAB dalam menyesuaikan parameter λ secara dinamis. Implementasi
ini memerlukan arsitektur yang canggih, mencakup desain fungsi imbalan
yang robust untuk menggabungkan relevansi dan diversitas, strategi
eksplorasi yang efisien untuk menghindari local optima, dan mekanisme
adaptif untuk menangani *concept drift* dalam preferensi pengguna dan
perubahan konteks (Qassimi dan Rakrak, 2025 dan Bukhari dkk., 2025).

Integrasi MAB dengan kerangka evaluasi komprehensif yang menggabungkan
metrik keberagaman, cakupan, dan *novelty* menjadi krusial untuk
memastikan sistem tidak hanya responsif terhadap perubahan konteks
tetapi juga mempertahankan keadilan distribusi rekomendasi
(Abdollahpouri dkk., 2020 dan Ricci dkk., 2022). Dengan demikian,
pendekatan MAB-MMR adaptif yang diusulkan dalam penelitian ini
menawarkan kerangka solusi yang komprehensif untuk mengatasi
kompleksitas domain rekomendasi pariwisata modern, menjembatani
kesenjangan antara personalisasi, diversifikasi, dan responsivitas
adaptif (Yoon dan Choi, 2023; Achmad dkk., 2023).

## Sistem Adaptif: Keterbatasan Pendekatan Statis

Sistem rekomendasi tradisional, yang beroperasi berdasarkan data
historis dan pemodelan statis, menunjukkan keterbatasan signifikan dalam
konteks dinamis karena kerap mengabaikan perubahan minat pengguna dari
waktu ke waktu (Wang dkk., 2022 dan Bukhari dkk., 2025)). Akibatnya,
sistem ini kesulitan merekomendasikan destinasi saat informasi tidak
mencukupi atau berubah secara *real-time* (Song dan Jiao, 2023 dan Yoon
dan Choi, 2023). Yoon dan Choi, (2023) mengidentifikasi bahwa SR
berbasis kecerdasan buatan (AI) juga memiliki keterbatasan serupa,
karena gagal merefleksikan perubahan faktor eksternal seperti suhu atau
curah hujan. Hal ini menggarisbawahi bagaimana sebagian besar model
rekomendasi yang ada masih cenderung statis dalam beradaptasi terhadap
perubahan lingkungan dan preferensi pengguna (Shi dkk., 2023 dan Bukhari
dkk., 2025).

Dalam riset pariwisata, pentingnya konteks *real-time* telah berulang
kali ditekankan oleh berbagai peneliti (Javadian Sabet dkk., 2022 dan
Qassimi dan Rakrak, 2025). Informasi situasional seperti suhu, curah
hujan, atau musim menjadi faktor penentu signifikan dalam keputusan
kunjungan dan dapat berubah seketika sesuai lokasi (Qassimi dan Rakrak,
2025 dan Shafqat dan Byun, 2020). Sebagai ilustrasi, sebuah sistem
statis mungkin merekomendasikan jalur pendakian di pagi hari, tetapi
sistem adaptif yang menerima data cuaca *real-time* akan membatalkan
rekomendasi tersebut dan menyarankan museum jika prediksi cuaca
menunjukkan akan turun hujan lebat (Qassimi dan Rakrak, 2025). Oleh
karena itu, sistem adaptif harus mampu merespons dinamika ini dengan
merefleksikan perubahan faktor eksternal dan merekomendasikan tur yang
disesuaikan dengan tipe wisatawan (Yoon dan Choi, 2023) dan Qassimi dan
Rakrak, 2025).

Pendekatan sadar konteks (*context-aware*) memperluas dimensi SR dari
dua (pengguna, item) menjadi tiga (pengguna, item, konteks), sebuah
ekspansi yang memungkinkan rekomendasi lebih akurat pada waktu dan
lokasi yang tepat (Suhaim dan Berri, 2021 dan Ricci dkk., 2022).
Pendekatan ini juga mempertimbangkan aktivitas dan bahkan kondisi
emosional pengguna (Suhaim dan Berri, 2021 dan Bukhari dkk., 2025).
Fararni dkk., (2021) mengkategorikan konteks ini ke dalam beberapa
jenis, termasuk informasi fisik (waktu, posisi, cuaca), sosial
(keberadaan orang lain), dan media interaksi (karakteristik perangkat),
sementara konteks modal seperti suasana hati menjadi pertimbangan
penting lainnya (Bukhari dkk., 2025).

Untuk mendukung sistem adaptif yang sadar konteks, arsitektur pemrosesan
kontekstual data real-time menjadi sebuah keharusan fundamental (Bukhari
dkk., 2025). Hal ini karena sistem konvensional cenderung statis dalam
memodelkan preferensi pengguna (Noorian Avval dan Harounabadi, 2023),
sedangkan pendekatan adaptif seperti pembelajaran daring sangat penting
untuk hasil yang kuat dalam skenario *real-time* (Bukhari dkk., 2025).
Berbeda dengan pemrosesan batch yang beroperasi pada data historis dalam
interval tertentu, pemrosesan kontekstual *real-time* data memungkinkan
pemrosesan informasi secara berkelanjutan seiring kedatangan data baru
(Fragkoulis dkk., 2024).

Perbedaan fundamental ini memiliki implikasi arsitektural yang
signifikan antara pendekatan statis dan dinamis (Bukhari dkk., 2025).
Dalam pendekatan tradisional berbasis batch, sistem hanya dapat
merespons perubahan setelah siklus pemrosesan berikutnya, yang bisa
memakan waktu berjam-jam atau berhari-hari karena ketergantungannya pada
data historis yang statis (Shi dkk., 2023 dan Bukhari dkk., 2025).
Sebaliknya, arsitektur pemrosesan kontekstual *real-time* memungkinkan
sistem untuk merespons perubahan konteks dalam hitungan detik, dengan
fokus pada latensi rendah dan throughput tinggi (Fragkoulis dkk., 2024).

Implementasi sistem adaptif dalam SR pariwisata memerlukan kemampuan
untuk mengintegrasikan data dari berbagai sumber. Data ini mencakup data
terstruktur seperti rating (Bukhari dkk., 2025) dan lokasi (Huang dkk.,
2020), data semi-terstruktur seperti review (Ricci dkk., 2022), serta
informasi kontekstual *real-time* seperti cuaca dan kondisi lalu lintas
(Solano-Barliza dkk., 2024). Sistem harus mampu memproses informasi
kontekstual terkini dan merespons perubahan dengan cepat (Shafqat dan
Byun, 2020) untuk memberikan rekomendasi yang relevan dengan situasi
pengguna saat itu (Fragkoulis dkk., 2024).

Namun, kemampuan integrasi data saja tidak cukup jika model di dalamnya
tidak mampu belajar dari perubahan yang terjadi (Fragkoulis dkk., 2024).
Di sinilah konsep pembelajaran adaptif atau berkelanjutan menjadi
komplemen yang vital (Ricci dkk., 2022 dan Qassimi dan Rakrak, 2025).
Sistem tidak hanya harus memproses data baru dengan cepat, tetapi juga
secara bertahap memperbarui model tanpa perlu melatih ulang dari awal
(Shi dkk., 2023 dan Fragkoulis dkk., 2024). Konsep ini memungkinkan
sistem untuk terus belajar dari pola-pola baru, mengingat preferensi
pengguna dan faktor kontekstual dapat mengalami *concept drift* pada
interval yang tidak terduga (Wang dkk., 2022 dan Shi dkk., 2023).

## Rangkuman Tinjauan Pustaka dan Posisi Penelitian

Tinjauan pustaka ini mengungkap progresi logis dari masalah fundamental
hingga celah penelitian kritis dalam ekosistem rekomendasi pariwisata
digital. Transformasi digital industri pariwisata (Barykin dkk., 2021)
telah menciptakan paradoks *information overload* yang memerlukan sistem
rekomendasi sebagai solusi (Kumar dkk., 2024). Namun, sistem rekomendasi
konvensional berbasis *Collaborative Filtering* menghadapi tantangan
sistemik berupa *popularity bias* (Abdollahpouri dkk., 2021), yang dalam
konteks pariwisata memicu fenomena overtourism dan ketimpangan ekonomi
regional yang signifikan (Pencarelli, 2020 dan Ricci dkk., 2022).

Upaya mitigasi melalui teknik diversifikasi seperti *Maximal Marginal
Relevance* (MMR) telah menunjukkan hasil positif dalam meningkatkan
keberagaman rekomendasi (Yalcin dan Bilge, 2021). Namun, pendekatan
existing memiliki keterbatasan fundamental: penggunaan parameter statis
yang gagal beradaptasi terhadap karakteristik dinamis domain pariwisata
(Shi dkk., 2023). Faktor kontekstual seperti cuaca, waktu, lokasi, dan
kondisi *real-time* lainnya sangat memengaruhi keputusan wisatawan (Yoon
dan Choi, 2023 dan Massimo dan Ricci, 2022), namun sistem tradisional
tidak mampu merespons perubahan ini secara adaptif (Bukhari dkk., 2025).

Tinjauan komprehensif mengungkap bahwa penelitian existing masih belum
efektif dalam mengintegrasikan tiga elemen krusial secara kohesif: (1)
data kontekstual *multimodal real-time*, (2) mekanisme pembelajaran
adaptif berkelanjutan, dan (3) optimasi *trade-off* antara relevansi dan
diversitas secara dinamis. Celah penelitian ini menciptakan kebutuhan
mendesak akan sistem yang sekaligus personal (Noorian Avval dan
Harounabadi, 2023), beragam (Shi dkk., 2023), dan responsif terhadap
perubahan konteks (Qassimi dan Rakrak, 2025).

Untuk mengatasi celah ini, penelitian ini mengusulkan sistem rekomendasi
pariwisata adaptif dengan tiga kontribusi utama:

1.  Integrasi Data Kontekstual *Real-time*: Arsitektur yang
    mengintegrasikan data multimodal (cuaca, lalu lintas, tren sosial
    media) untuk merespons perubahan kondisi dalam hitungan detik, bukan
    jam atau hari.

2.  Mekanisme Pembelajaran Adaptif MAB: Implementasi *Multi-Armed
    Bandit* untuk optimasi parameter lambda (λ) MMR secara dinamis
    berdasarkan umpan balik *real-time*, memungkinkan sistem
    menyesuaikan *trade-off* relevansi-diversitas sesuai konteks tanpa
    intervensi manual.

3.  Re-ranking Dinamis Berbasis MAB-MMR: Pendekatan hibrida yang
    mengombinasikan kekuatan optimasi *greedy* MMR dengan fleksibilitas
    pembelajaran berkelanjutan MAB untuk menghasilkan rekomendasi yang
    tidak hanya personal dan beragam, tetapi juga adaptif terhadap
    dinamika kontekstual pariwisata.

Kerangka kerja adaptif MAB-MMR yang diusulkan menjadi inti mekanisme
yang memungkinkan sistem mempertahankan akurasi sambil secara signifikan
meningkatkan keberagaman, cakupan destinasi *long-tail*, serta
mengurangi *popularity bias*. Dengan demikian, penelitian ini
berkontribusi pada pengembangan sistem rekomendasi yang tidak hanya
superior secara teknis tetapi juga mendukung tujuan pariwisata
berkelanjutan dan pemerataan ekonomi regional.

Alur konseptual penelitian secara lengkap disajikan pada Gambar II.1,
yang memetakan secara sistematis dari identifikasi masalah fundamental
(*popularity bias* dan *overtourism*), analisis solusi existing dan
keterbatasannya (MMR statis), hingga kerangka solusi adaptif yang
diusulkan (integrasi MAB-MMR dengan pemrosesan kontekstual *real-time*).

[]{#_Toc214882431 .anchor}Gambar II.1 Alur Konseptual Penelitian

# Metodologi Penelitian

Bab ini menguraikan metodologi penelitian yang diterapkan dalam
pengembangan sistem rekomendasi adaptif *real-time* ini. Pendekatan
*Design Science Research Methodology* (DSRM) dipilih sebagai kerangka
kerja utama. Pembahasan dalam bab ini akan mencakup setiap tahapan DSRM,
yaitu identifikasi masalah, penentuan tujuan solusi, perancangan dan
pengembangan artefak, demonstrasi, evaluasi, serta komunikasi hasil
penelitian.

## Metode Penelitian DSRM

Penelitian ini menggunakan metode DSRM. DSRM merupakan kerangka kerja
metodologis yang menyediakan tahapan terstruktur untuk memfasilitasi
penelitian yang berhubungan dengan teknologi informasi dengan prinsip
"pencarian solusi yang bertujuan" (Peffers dkk., 2007). Metode ini dapat
digunakan untuk memahami dan melakukan evaluasi. DSRM terdiri dari enam
tahapan mulai dari proses identifikasi terhadap masalah, menentukan
solusi, melakukan perancangan dan pengembangan, melakukan demonstrasi,
melakukan evaluasi, sampai dengan melakukan komunikasi seperti yang
ditampilkan pada Gambar III. 1.

![A diagram of a process AI-generated content may be
incorrect.](media/image3.png){width="5.510416666666667in"
height="2.2536209536307963in"}

[]{#_Toc214882432 .anchor}Gambar III.1 Kerangka Kerja DSRM berdasarkan
Peffers dkk (2007)

Pemilihan DSRM dalam penelitian ini didasarkan pada beberapa
pertimbangan strategis yang selaras dengan karakteristik sistem
rekomendasi adaptif yang dikembangkan. Pertama, DSRM memberikan kerangka
kerja yang terstruktur untuk menggabungkan konsep teori dengan pembuatan
sistem nyata, hal ini krusial mengingat penelitian ini mengintegrasikan
konsep teoritis *Multi-Armed Bandit* dengan aplikasi praktis dalam
domain pariwisata yang dinamis. Kedua, sifat iteratif DSRM memungkinkan
memperbaiki sistem berdasarkan feedback dari setiap tahap evaluasi,
sangat relevan dengan sistem yang dikembangkan, yang memang bersifat
adaptif dan terus belajar dari sistem yang dikembangkan. Ketiga, DSRM
mendukung evaluasi dari berbagai sisi yang mencakup aspek teknis
(akurasi, keberagaman, cakupan) dan aspek pengalaman pengguna (user
acceptance, usability), selaras dengan paradigma evaluasi \"*beyond
accuracy*\" yang telah diidentifikasi dalam tinjauan pustaka.

Berdasarkan kerangka DSRM, setiap tahapan penelitian telah diuraikan
metode pelaksanaannya secara rinci guna memastikan penelitian berjalan
secara terukur dan terencana. DSRM dipilih karena memungkinkan iterasi
desain-evaluasi untuk sistem adaptif. Misalnya, tahap \'demonstrasi\'
pada DSRM memfasilitasi uji coba prototipe dalam skenario perubahan
cuaca mendadak. Berikut kerangka penelitian yang digunakan dalam
penelitian ini sebagaimana pada Gambar III 2.

![](media/image4.png){width="7.458333333333333in"
height="3.1881944444444446in"}

[]{#_Toc214882433 .anchor}Gambar III.2 Kerangka Penelitian

## Identifikasi Masalah dan Motivasi

Penelitian ini dimulai dengan tahap tahapan pertama dalam kerangka DSRM,
proses identifikasi masalah dan motivasi telah menjadi fondasi utama
yang dibahas secara komprehensif dalam Bab I (Pendahuluan) dan diperkuat
secara teoretis dalam Bab II (Tinjauan Pustaka). Di dalam bab-bab
tersebut, telah dibangun argumen yang kuat mengenai urgensi masalah
*popularity bias* dan dampaknya terhadap ekosistem pariwisata, yang
menjadi justifikasi utama untuk penelitian ini.

### Analisis Permasalahan

Merujuk pada permasalahan fundamental *popularity bias* yang telah
diidentifikasi pada Bab I, tahap ini akan mengoperasionalkan tantangan
tersebut ke dalam analisis kebutuhan dari perspektif pemangku
kepentingan utama di ekosistem pariwisata Sumedang, yaitu wisatawan, dan
stakeholder sekunder, seperti Dinas Pariwisata serta pengelola
destinasi. Selain Dinas Pariwisata, para pelaku Usaha Kecil dan Menengah
(UKM) seperti pengelola penginapan lokal, rumah makan, dan toko
oleh-oleh juga menghadapi tantangan signifikan. Keberlangsungan usaha
mereka sangat bergantung pada distribusi wisatawan yang merata. Namun,
sistem rekomendasi konvensional cenderung menciptakan ketimpangan \'yang
kaya semakin kaya\' (*rich-get-richer effect*), di mana destinasi
populer terus-menerus direkomendasikan. Fenomena ini menyebabkan
konsentrasi aliran wisatawan, sehingga UKM yang berlokasi di sekitar
destinasi berkualitas namun tidak populer mengalami kesulitan untuk
berkembang dan berisiko menghadapi kegagalan usaha.

Berdasarkan studi literatur dan observasi, teridentifikasi tiga
permasalahan utama yang dihadapi wisatawan:

1.  Sistem rekomendasi konvensional cenderung merekomendasikan destinasi
    yang telah populer, sebuah fenomena yang dikenal sebagai *popularity
    bias*. Akibatnya, wisatawan, terutama yang memiliki pengetahuan
    terbatas tentang Sumedang, akan menerima rekomendasi yang monoton
    dan terkonsentrasi pada sejumlah kecil destinasi *mainstream*.
    Kondisi ini mengurangi kualitas pengalaman eksplorasi dan
    menyebabkan wisatawan kehilangan kesempatan untuk menemukan
    destinasi alternatif yang lebih sesuai dengan preferensi personal
    mereka.

2.  Sistem rekomendasi pada umumnya bersifat statis dan menghasilkan
    rekomendasi berdasarkan data historis tanpa mempertimbangkan konteks
    pengguna saat ini. Hal ini menimbulkan permasalahan relevansi yang
    signifikan dalam domain pariwisata yang dinamis. Perubahan kondisi
    eksternal seperti cuaca, kemacetan lalu lintas, atau jam operasional
    dapat membuat rekomendasi yang sebelumnya valid menjadi tidak
    optimal. Dampaknya adalah pengalaman wisata yang suboptimal,
    inefisiensi waktu dan biaya, serta potensi risiko bagi wisatawan.

3.  Sistem rekomendasi yang berorientasi pada akurasi cenderung
    mengabaikan item-item ini, menciptakan efek *rich-get-richer* di
    mana destinasi populer akan semakin dominan. Akibatnya, cakupan
    sistem menjadi rendah dan terjadi ketimpangan distribusi kunjungan,
    sementara wisatawan kehilangan kesempatan untuk menemukan
    tempat-tempat unik.

Dinas Pariwisata menghadapi tantangan dalam pemerataan distribusi
wisatawan untuk mencegah *overtourism* pada destinasi populer yang dapat
menyebabkan degradasi lingkungan dan penurunan kualitas pengalaman. Di
sisi lain, pengelola destinasi kurang populer kesulitan mendapatkan
visibilitas dalam ekosistem digital untuk bersaing dan menarik
pengunjung yang relevan.

Analisis di atas menyimpulkan bahwa permasalahan inti yang harus
dipecahkan oleh sistem yang diusulkan adalah sebagai berikut:

1.  *Popularity Bias:* Dominasi destinasi populer dalam rekomendasi.

2.  *Lack of Context-Awareness:* Ketidakmampuan sistem beradaptasi
    dengan kondisi *real-time*.

3.  *Low Diversity & Coverage:* Rekomendasi yang monoton dan jangkauan
    katalog yang terbatas (*long-tail problem*).

4.  *Cold-Start Problem:* Kesulitan memberikan rekomendasi relevan bagi
    pengguna baru.

5.  *Concept Drift:* Ketidakmampuan model statis beradaptasi dengan
    perubahan tren dan preferensi.

Permasalahan-permasalahan ini memerlukan solusi terintegrasi yang tidak
hanya berfokus pada akurasi, tetapi juga secara eksplisit mengoptimalkan
keberagaman, cakupan, dan adaptivitas kontekstual.

## Menentukan Solusi dari Tujuan

Berdasarkan masalah yang telah teridentifikasi, tahapan kedua DSRM
adalah menentukan tujuan dari solusi yang diusulkan. Tujuan ini telah
dirumuskan secara spesifik dan terukur dalam bentuk Rumusan Masalah dan
Tujuan ini diformulasikan, yang berangkat dari kesenjangan penelitian
(*research gap*) yang diidentifikasi pada akhir Bab II.

### Analisis Solusi

1.  *Popularity Bias*

> Bias popularitas terjadi ketika *item* populer cenderung
> direkomendasikan daripada *item long-tail* (niche), meskipun *item*
> yang terakhir mungkin menarik bagi pengguna individual (Yalcin dan
> Bilge, 2021). Tabel III.1 memuat beberapa solusi yang bisa mengurangi
> *popularity bias.*

[]{#_Toc214880948 .anchor}Tabel III.1 Solusi Alternatif Mengurangi
*Popularity Bias*

  ---------------------------------------------------------------------------------------------
              Solusi                 Deskripsi &           Pertimbangan           Tantangan
                                     Implementasi          Implementasi           Potensial
  ------------------------------ -------------------- ----------------------- -----------------
  *Post-Processing* (Re-ranking)  Penyesuaian daftar         Bersifat            Peningkatan
        (Zhao dkk., 2025)         rekomendasi akhir   *model-agnostic* (tidak   mitigasi bias
                                  dengan memberikan    tergantung pada model   terbatas karena
                                    bobot terbalik     dasar) dan fleksibel     terikat pada
                                 terhadap popularitas  (Zhao dkk., 2025). CP  hasil model dasar
                                   item. Contohnya    memberikan kinerja yang yang sudah bias.
                                 adalah *Value-aware  konsisten rendah dalam      Terdapat
                                 Ranking* (VaR) yang     *User Popularity        *trade-off*
                                    efisien dalam        Deviation* (UPD),     antara mitigasi
                                  debiasing (Yalcin    menunjukkan perlakuan      bias dan
                                 dan Bilge, 2021) dan  yang lebih adil dari    akurasi/presisi
                                     *Calibrated        perspektif pengguna      (Zhao dkk.,
                                   Popularity* (CP)    (Abdollahpouri dkk.,        2025).
                                  yang menyesuaikan      2021). AdaptedVaR    
                                   rekomendasi agar       terbukti dapat      
                                    sesuai dengan     mengurangi bias dengan  
                                  toleransi pengguna   kerugian pada akurasi  
                                 terhadap popularitas    (nDCG) yang dapat    
                                  (Zhao dkk., 2025).   diabaikan (Yalcin dan  
                                                           Bilge, 2021).      

          *In-Processing         Modifikasi algoritma  Mengatasi bias sejak    Umumnya kurang
   (Regularization/Constraint)*     standar dengan     tahap pelatihan model       efektif
     (Yalcin dan Bilge, 2021)        menambahkan        (Yalcin dan Bilge,      dibandingkan
                                    regularizer ke       2021). Pendekatan         metode
                                   fungsi objektif           berbasis           *re-ranking*
                                   untuk mengontrol     *Learning-to-Rank*     (Abdollahpouri
                                  rasio item populer  (LTR) dapat mengontrol    dkk., 2021).
                                  dan kurang populer        bias dengan             Dapat
                                  (Yalcin dan Bilge,   memprioritaskan item     mengakibatkan
                                        2021).              *long-tail*            akurasi
                                                       (Abdollahpouri dkk.,      rekomendasi
                                                              2021).          terkompromi (Zhao
                                                                                dkk., 2025).

   Solusi Berbasis Causal (Shi   Menggunakan *Causal   Kelebihan utama dari      Sulit untuk
           dkk., 2023)              Graphs* untuk      pendekatan ini adalah   memperoleh data
                                 menganalisis proses    kemampuannya untuk     yang tidak bias
                                   rekomendasi (Shi      secara eksplisit      untuk pelatihan
                                     dkk., 2023).       memodelkan hubungan   (Shi dkk., 2023).
                                                       sebab-akibat (kausal)  
                                                         (Shi dkk., 2023)     
  ---------------------------------------------------------------------------------------------

2.  *Lack of Context-Awareness*

> Sistem rekomendasi tradisional beroperasi dalam ruang dua dimensi
> (Pengguna *Item*), mengabaikan informasi kontekstual (C) seperti
> waktu, lokasi, atau status perangkat, yang dapat memengaruhi penilaian
> pengguna (Suhaim dan Berri, 2021). Tabel III.2 memuat beberapa solusi
> yang bisa mengatasi kurangnya *context-awareness*.

[]{#_Toc214880949 .anchor}Tabel III.2 Solusi Alternatif Mengatasi
Kurangnya *Context-Awareness*

  --------------------------------------------------------------------------------
       Solusi           Deskripsi &           Pertimbangan           Tantangan
                        Implementasi          Implementasi           Potensial
  ----------------- -------------------- ----------------------- -----------------
     Kontekstual        Menggunakan      Memungkinkan penggunaan  Akurasi mungkin
   *Pre-Filtering*   informasi konteks    kembali algoritma 2D   rendah jika data
   (Noorian Avval    (misalnya, waktu,    tradisional. Relatif    historis untuk
  dan Harounabadi,  musim, lokasi) untuk mudah diimplementasikan konteks spesifik
        2023)         memilih *subset*     untuk mengadaptasi     tersebut jarang
                    data pelatihan yang   sistem tradisional ke     (*sparse*).
                      relevan, sebelum       dalam konteks.         Membutuhkan
                     menerapkan sistem                             identifikasi
                       rekomendasi 2D                                 faktor
                    tradisional. Konteks                         kontekstual yang
                     yang jarang dapat                           relevan di tahap
                       digeneralisasi                                 desain.
                      (misalnya, waktu                           
                      spesifik menjadi                           
                     \'Akhir Pekan\').                           

      Pemodelan       Mengintegrasikan       Mampu menangkap     Data kontekstual
     Kontekstual       konteks secara      interaksi kompleks       sering kali
    (*Contextual     langsung ke dalam      non-linear antara         jarang
     Modeling*)     fungsi peringkat: .   pengguna, *item*, dan     (*sparse*).
    (Qassimi dan     Implementasi dapat      konteks. Dapat      Integrasi terlalu
    Rakrak, 2025)        melibatkan       meningkatkan kinerja     banyak fitur
                    dekomposisi tensor,        dan akurasi       kontekstual dapat
                     Faktorisasi Mesin,  dibandingkan pendekatan    menyebabkan
                      atau model *Deep      non-kontekstual.          masalah
                       Learning* yang                             dimensionalitas
                         diperluas.                                 dan kinerja
                                                                     menurun.

     Contextual      Menganalisis data     Model-agnostik dan       Peningkatan
   Post-Filtering        preferensi         tidak memengaruhi        kualitas
     (Suhaim dan     kontekstual untuk    pemodelan preferensi      rekomendasi
    Berri, 2021)     pengguna tertentu    dasar. Ringkas untuk     terbatas pada
                       dalam konteks       implementasi karena    hasil awal dari
                       tertentu guna        hanya membutuhkan      model dasar.
                       menemukan pola    lapisan penyesuaian di    Tidak secara
                      penggunaan item         akhir proses.          intrinsik
                    spesifik (misalnya,                            meningkatkan
                       pengguna hanya                            pemahaman sistem
                    menonton komedi pada                              tentang
                      akhir pekan) dan                              preferensi
                    kemudian menggunakan                           kontekstual.
                       pola ini untuk                            
                    menyesuaikan daftar                          
                         item yang                               
                     direkomendasikan.                           
  --------------------------------------------------------------------------------

3.  *Low Diversity & Coverage*

> Masalah ini mengacu pada rekomendasi yang monoton (Ricci dkk., 2022)
> dan rendahnya visibilitas *item long-tail* (Abdollahpouri dkk., 2021),
> yang penting untuk penemuan pengetahuan dan keadilan bagi penyedia
> konten (Abdollahpouri, 2019). Tabel III.3 memuat beberapa solusi yang
> bisa meningkatkan *Diversity* dan *coverage*.

[]{#_Toc214880950 .anchor}Tabel III.3 Solusi Alternatif Meningkatkan
*Diversity & Coverage*

  ----------------------------------------------------------------------------------
       Solusi          Deskripsi &           Pertimbangan       Tantangan Potensial
                       Implementasi          Implementasi       
  ---------------- -------------------- ----------------------- --------------------
    *Re-ranking*     Menggunakan MMR     *Model-agnostic* dan       Membutuhkan
      Berbasis      (*Maximal Marginal     *time-efficient*       *trade-off* yang
   Diversifikasi    Relevance*) untuk   (menghindari pelatihan     cermat antara
    (MMR) (Zhao       menyeimbangkan    ulang). Sangat efektif      akurasi dan
    dkk., 2025)       relevansi dan       dalam memaksimalkan       diversitas.
                      disimilaritas         diversitas dan      Peningkatan dibatasi
                    antar-*item* dalam  mengurangi redundansi.  oleh kualitas daftar
                       daftar yang                                 kandidat awal.
                    direkomendasikan.                           
                     Fungsi MMR dapat                           
                       menggunakan                              
                        parameter                               
                   *trade-off* () untuk                         
                         mengatur                               
                   keseimbangan antara                          
                        kemiripan                               
                     (relevansi) dan                            
                       diversitas.                              

    Optimalisasi   Menggunakan MOC-MAB     Mengintegrasikan      Membutuhkan desain
    Multi-Tujuan    (*Multi-Objective   diversitas langsung ke  fungsi *reward* yang
      (RL/MAB)       Contextual MAB*)   dalam pelatihan model,  kompleks. Memerlukan
    (Qassimi dan     atau kerangka RL      yang menghasilkan          evaluasi
   Rakrak, 2025)    (misalnya, DNaIR)      daftar yang lebih    multi-metrik karena
                       yang secara         stabil. Mendukung    adanya *trade-off*.
                        eksplisit         *exploration* yang    
                      mengoptimalkan    penting untuk menemukan 
                     *Diversity* dan       *item long-tail*.    
                     *Novelty* selain                           
                         akurasi.                               

   Regularization  Memasukkan kriteria   Memastikan diversitas      Membutuhkan
  Selama Pelatihan diversitas ke dalam  sejak tahap pelatihan.    pelatihan ulang
    (Zhang dkk.,   fungsi *loss* model,   Dapat meningkatkan     model yang mungkin
       2025)        seringkali sebagai  diversitas berdasarkan     kurang efisien
                     *regularization     kategori/genre *item*      dibandingkan
                   term*, untuk melatih    yang lebih sesuai     *post-processing*.
                        model agar          dengan persepsi     
                   representasi *item*         pengguna.        
                   yang beragam menjadi                         
                       lebih dekat.                             
  ----------------------------------------------------------------------------------

4.  *Cold-Start Problem*

> Kesulitan memberikan rekomendasi bagi pengguna baru (*cold visitors*)
> atau *item* baru (*cold products*) (Sachi Nandan Mohanty, 2020) karena
> tidak adanya data historis yang memadai (Shambour dkk., 2024). Tabel
> III.4 memuat beberapa solusi yang bisa menangani *cold-start problem*.

[]{#_Toc214880951 .anchor}Tabel III.4 Solusi Alternatif Mengatasi
*Cold-Start Problem*

  ----------------------------------------------------------------------------------------
        Solusi           Deskripsi &           Pertimbangan         Tantangan Potensial
                         Implementasi          Implementasi       
  ------------------ -------------------- ----------------------- ------------------------
  Pendekatan Hibrida    Menggabungkan         Mampu mengatasi       CBF rentan terhadap
      (CF + CBF)        *Collaborative      *cold-start* untuk            masalah
    (Chalkiadakis      Filtering* (CF)      *item* dan pengguna    *over-specialization*.
     dkk., 2023)            dengan              baru secara         Implementasi hibrida
                        *Content-Based         komprehensif.        memerlukan penentuan
                      Filtering* (CBF).     Pendekatan hibrida      skema kombinasi yang
                       CBF menggunakan      (*TopicSeqHybrid*)        tepat (misalnya,
                         fitur *item*         terbukti sangat         *switching* atau
                      (deskripsi *POI*)       berhasil dalam             *mixed*).
                      untuk *item* baru.     mengatasi masalah    
                        Kombinasi ini          *cold-start*.      
                     mengatasi kelemahan                          
                        model tunggal.                            

   Pemanfaatan Data    Menggunakan data     Demografi membantu       Membutuhkan upaya
       Tambahan       demografi, atribut  memprediksi preferensi       pengguna untuk
   (Demografi/Trust  pengguna awal, atau      pengguna untuk        memberikan informasi
  Network) (Shambour jaringan kepercayaan    kunjungan di masa     demografi/profil awal.
     dkk., 2024)        sosial (*trust        depan. Jaringan     Membutuhkan akuisisi dan
                      networks*) sebagai   kepercayaan terbukti    pemeliharaan jaringan
                     informasi sampingan     lebih bermanfaat     kepercayaan yang andal.
                     (*side information*) daripada hanya meminta  
                            untuk             *rating* awal.      
                       *bootstrapping*       Mengurangi upaya     
                       profil pengguna     elisitasi preferensi   
                            baru.             pengguna baru.      

        *Deep         Menggunakan model     DRLM dapat mencapai    Membutuhkan arsitektur
    Representation     *Deep Learning*     kinerja yang superior    jaringan saraf yang
   Learning* (DRLM)   untuk menghasilkan     dalam akurasi dan      canggih. Model yang
  (Huang dkk., 2020)  representasi fitur   efektivitas mengatasi  menggunakan representasi
                        yang kaya bagi    *cold-start*. Model DL      CF-based mungkin
                      pengguna/item baru   dapat dilatih secara   kehilangan kemampuannya
                      meskipun interaksi      eksplisit untuk      menangani *cold-start*
                     terbatas. Pendekatan  *cold-start* melalui      jika representasi
                       *Meta-learning*        teknik seperti       tersebut dimodifikasi
                      melatih generator         *dropout*.           selama pelatihan.
                      *embedding* untuk                           
                         *item* baru.                             
  ----------------------------------------------------------------------------------------

5.  *Concept Drift*

> Perubahan dalam hubungan antara input dan target model seiring waktu
> (Wang dkk., 2022), yang disebabkan oleh perubahan tren atau preferensi
> pengguna (Bukhari dkk., 2025). Model statis kesulitan beradaptasi
> dengan lingkungan yang dinamis (Bukhari dkk., 2025). Tabel III.5
> memuat beberapa solusi yang bisa menangani *Concept Drift*.

[]{#_Toc214880952 .anchor}Tabel III.5 Solusi Alternatif Menangani
*Concept Drift*

  ----------------------------------------------------------------------------------
       Solusi          Deskripsi &           Pertimbangan       Tantangan Potensial
                       Implementasi          Implementasi       
  ---------------- -------------------- ----------------------- --------------------
   *Reinforcement       Memodelkan      Mampu menangkap dynamic  Membutuhkan desain
   Learning* (RL)  rekomendasi sebagai     transfer of user      fungsi reward yang
    berbasis MDP    proses pengambilan      preference dan          kompleks. RL
   (Bukhari dkk.,  keputusan sekuensial  amplification effects  membutuhkan sejumlah
       2025)           (sequential       of the feedback loop   besar data interaksi
                     decision-making)    yang diabaikan model   untuk pelatihan dan
                    menggunakan Markov  statis. Mengoptimalkan   cenderung memiliki
                     Decision Process      utilitas/kepuasan    waktu pelatihan yang
                   (MDP). RL (misalnya,     jangka panjang          lebih lama.
                      DNaIR) secara            pengguna.        
                   eksplisit menangkap                          
                     transfer dinamis                           
                   preferensi pengguna.                         

   Model Temporal    Mengintegrasikan    Penting dalam konteks   Protokol evaluasi
    Sadar Waktu       konteks waktu      pariwisata (misalnya,   untuk sistem sadar
    (Wang dkk.,      (seperti musim,      rekomendasi liburan       waktu harus
       2022)       waktu dalam sehari)    musim panas versus      dirancang secara
                     ke dalam model,        musim dingin).            cermat.
                        seringkali        Pendekatan berbasis   
                       menggunakan       LSTM dapat menyeleksi  
                     arsitektur LSTM    fitur kontekstual yang  
                    (*Long Short-Term   relevan seperti jarak,  
                      Memory*) atau        waktu, dan cuaca.    
                    *Time-aware Matrix                          
                     Factorization*.                            

    *Contextual     C-MAB mengadaptasi    Ringan, Mudah, dan    Secara tradisional,
    Multi-Armed    strategi exploration   *Real-time*: C-MAB     MAB mengasumsikan
  Bandit* (C-MAB)    vs exploitation     memiliki kompleksitas   konteks/preferensi
     (Qassimi &     secara *real-time*   komputasi yang lebih   statis dari waktu ke
   Rakrak, 2025)     dan menggunakan       ringan dan sangat      waktu, sehingga
                      konteks untuk          efisien untuk          kurang mampu
                    memandu keputusan.   pembelajaran online.   memodelkan transisi
                          Model                                  keadaan sekuensial
                     *Multi-Objective                              yang kompleks
                    Contextual Bandit*                           dibandingkan MDP.
                        (MOC-MAB)                               
                     mengintegrasikan                           
                         optimasi                               
                       multi-tujuan                             
                       (*Diversity,                             
                        fairness,                               
                    relevance*) secara                          
                         dinamis.                               
  ----------------------------------------------------------------------------------

### Rancangan Solusi dan Justifikasi

Berdasarkan analisis lima masalah kemudian beberapa solusi yang
dianalisis, solusi yang paling komprehensif dan efisien adalah
mengadopsi kerangka kerja adaptif:

$$Hybrid\ (CF + CB + Context - Aware) + MMR + MAB$$

Kerangka kerja ini diadopsi untuk mengakomodasi keseimbangan antara
kompleksitas masalah, efisiensi implementasi, dan kemampuan adaptasi
*real-time* yang krusial untuk sektor pariwisata yang dinamis:

1.  Mengatasi *Cold-Start* (Hybrid CF+CB+*Context-Aware*): Penggunaan
    pendekatan hibrida (*hybrid switching* atau *mixed*) yang
    menggabungkan CF dan CBF secara efektif menangani *Cold-Start
    Problem* dan *Low Coverage*. Komponen *Context-Aware* (CARS) yang
    diimplementasikan sebagai fitur input dalam model memastikan
    personalisasi yang didasarkan pada konteks (misalnya, lokasi dan
    waktu).

2.  Menjamin Kualitas (MMR *Post-Processing*): Penggunaan MMR sebagai
    lapisan *post-processing* yang *model-agnostic* memastikan
    rekomendasi akhir tidak monoton, secara efektif mengatasi *Low
    Diversity* dengan biaya komputasi yang ringan. Strategi mitigasi
    bias (seperti CP) dapat diintegrasikan dalam MMR atau sebagai
    *post-processing* tambahan untuk mengatasi *Popularity Bias*.

3.  Adaptasi Dinamis (MAB/C-MAB): Penggunaan C-MAB (MOC-MAB) sebagai
    mesin pembelajaran *online* pusat yang adaptif mengatasi *Concept
    Drift* dan *Lack of Context-Awareness* secara dinamis. C-MAB sangat
    ringkas dan mudah diimplementasikan untuk menangani data *real-time*
    dan secara otomatis menyesuaikan *trade-off* antara tujuan yang
    bertentangan (misalnya, akurasi vs. diversitas atau keadilan).
    Kompleksitas C-MAB yang relatif lebih ringan dibandingkan MDP
    menjadikannya ideal untuk sistem pariwisata yang membutuhkan respons
    cepat.

## Perancangan dan Pengembangan

Tahap Perancangan dan Pengembangan merupakan inti dari DSRM, di mana
sistem solusi mulai dibangun secara teknis. Berdasarkan tujuan yang
telah dirumuskan pada sub-bab sebelumnya, sistem yang dikembangkan dalam
penelitian ini adalah sebuah sistem rekomendasi pariwisata adaptif
*real-time*. Sub-bab ini menyajikan spesifikasi teknis dan arsitektur
sistem.

### Spesifikasi Kebutuhan Sistem

Berdasarkan analisis permasalahan dan solusi yang telah dirumuskan,
kebutuhan sistem didetailkan menjadi spesifikasi fungsional dan
non-fungsional yang menjadi acuan implementasi. Spesifikasi ini
disesuaikan dengan scope penelitian untuk memastikan tercapainya dalam
konteks pengembangan sistem rekomendasi.

Kebutuhan Fungsional

Kebutuhan fungsional mendefinisikan fungsionalitas inti yang harus
disediakan sistem. Spesifikasi lengkap disajikan pada Tabel III.6.

[]{#_Toc214880953 .anchor}Tabel III.6 Kebutuhan Fungsional Sistem

  -----------------------------------------------------------------------
  ID      Kebutuhan Fungsional
  ------- ---------------------------------------------------------------
  KF01    Sistem harus dapat mengintegrasikan data kontekstual (minimal
          dua dari: cuaca, lalu lintas, atau tren media sosial)

  KF02    Sistem harus menghasilkan rekomendasi menggunakan model
          *hybrid* dengan mekanisme MAB-MMR

  KF03    Sistem harus dapat menerima input preferensi pengguna dan
          menghasilkan rekomendasi yang dipersonalisasi

  KF04    Sistem harus menyediakan antarmuka web untuk menampilkan
          rekomendasi destinasi beserta justifikasinya

  KF05    Sistem harus dapat menerima *feedback* pengguna (rating atau
          interaksi) untuk evaluasi
  -----------------------------------------------------------------------

Kebutuhan *Non-Fungsional*

Kebutuhan *non-fungsional* mendefinisikan standar kualitas dan batasan
operasional sistem. Spesifikasi lengkap disajikan pada Tabel III.7:

[]{#_Toc214880954 .anchor}Tabel III.7 Kebutuhan *Non-Fungsional* Sistem

+-------+--------------------------------------------------------------+
| ID    | Kebutuhan Non-Fungsional                                     |
+=======+==============================================================+
| KNF01 | *Response Time*:                                             |
|       |                                                              |
|       | - *Offline evaluation*: *Response time* tidak lebih dari     |
|       |   500ms (tanpa latency API eksternal karena menggunakan      |
|       |   *cached data*)                                             |
|       |                                                              |
|       | - *Online user testing*: *Response time* tidak lebih dari 3  |
|       |   detik untuk 90% request (mengakomodasi latency API         |
|       |   *real-time*: cuaca \~200ms, calendar \~150ms, plus         |
|       |   inferensi model \~500ms, plus network overhead \~300ms)    |
+-------+--------------------------------------------------------------+
| KNF02 | Sistem harus dapat mengoptimalkan metrik akurasi             |
|       | (Precision@K, NDCG) dan keberagaman (*Diversity, Coverage*)  |
|       | secara seimbang                                              |
+-------+--------------------------------------------------------------+
| KNF03 | Sistem harus dapat diakses melalui *web browser* dan         |
|       | memiliki target *System Usability Scale* (SUS) *score*       |
|       | minimal 70                                                   |
+-------+--------------------------------------------------------------+
| KNF04 | Sistem harus memiliki mekanisme penanganan eror yang memadai |
|       | untuk menjaga stabilitas selama pengujian                    |
+-------+--------------------------------------------------------------+
| KNF05 | Sistem harus memiliki mekanisme fallback untuk mengatasi     |
|       | kegagalan API eksternal, menggunakan data cache dengan       |
|       | timestamp maksimal 30 menit                                  |
+-------+--------------------------------------------------------------+

Spesifikasi ini menjadi blueprint untuk tahap implementasi sistem dan
baseline untuk evaluasi keberhasilan penelitian dalam menjawab rumusan
masalah yang telah dirumuskan.

### Integrasi Data dan API

Untuk merealisasikan kapabilitas adaptif sistem, penelitian ini
mengintegrasikan empat sumber data dinamis utama yang diperoleh melalui
API publik. Pemilihan sumber data ini diturunkan secara langsung dari
rumusan masalah penelitian guna menangkap konteks perjalanan yang
menyuluruh. Rincian API yang digunakan disajikan pada Tabel III.8.

[]{#_Toc214880955 .anchor}Tabel III.8 Spesifikasi Integrasi Data dan API

  -------------------------------------------------------------------------
   No.   Sumber Data      API yang       Data Point yang        Tujuan
                          Digunakan          Diambil       Penggunaan dalam
                                                                Model
  ----- ------------- ----------------- ------------------ ----------------
    1       Cuaca      OpenWeatherMap   Suhu, kelembaban,   *Context-aware
         *Real-time*         API           curah hujan,    filtering* untuk
                                         kecepatan angin,     destinasi
                                           visibility,        outdoor vs
                                          kondisi cuaca         indoor

    2   Lalu Lintas &   Data Simulasi      Kondisi lalu      Optimalisasi
          Mobilitas     (Google Maps          lintas         routing dan
                       Traffic Logic)     (Macet/Lancar)    *accessibility
                                                               scoring*

    3   Media Sosial    Data Simulasi    Trending Topic &    *Popularity
                           (Trends          Viral Tags     trend detection*
                         Injection)                        

    4    Kalender &     Calenderafic        Hari libur        *Seasonal
            Event                        nasional/daerah,  adjustment* dan
                                         festival lokal,     *event-based
                                          event musiman     recommendation
                                                              boosting*
  -------------------------------------------------------------------------

Pada tahap implementasi penelitian ini, modul integrasi untuk *Traffic*
dan *Media Sosial* menggunakan injeksi data statis yang mensimulasikan
respons API (*mocking data*). Hal ini dilakukan untuk memvalidasi logika
adaptasi algoritma *Context-Aware* terhadap variabel eksternal,
mengingat adanya batasan akses (*rate limit* dan biaya) pada API
*Enterprise* untuk kedua platform tersebut.

### Dataset Penelitian 

Untuk melatih dan mengevaluasi model, penelitian ini dirancang
menggunakan pendekatan data-driven berbasis data riil (*real-world
dataset*). Sumber data utama yang digunakan adalah ulasan publik (user
reviews) yang dihimpun dari platform Google Maps untuk berbagai
destinasi wisata di Kabupaten Sumedang.

Pengambilan data dilakukan menggunakan teknik *web scraping* untuk
mendapatkan riwayat ulasan historis yang mencakup atribut User ID,
Destination ID, Rating, dan Timestamp. Penggunaan data riil ini
bertujuan untuk memastikan bahwa model rekomendasi dilatih berdasarkan
pola preferensi wisatawan yang autentik dan perilaku perjalanan yang
sesungguhnya.

### Desain Model *Machine Learning* (MAB-MMR)

Model yang diusulkan dalam penelitian ini dirancang untuk beroperasi
sebagai sistem rekomendasi yang adaptif terhadap preferensi dan konteks.
Proses kerjanya dibagi menjadi dua langkah utama: pertama, menghasilkan
daftar kandidat destinasi yang relevan (Generasi Kandidat) dan kedua
menyempurnakan daftar tersebut secara dinamis untuk menyeimbangkan
berbagai tujuan (Optimisasi Adaptif).

Langkah 1: Generasi Kandidat dengan Model Hibrida

Pada langkah awal, sistem menggabungkan tiga jenis analisis untuk
menghitung skor relevansi awal setiap destinasi. Tiga analisis tersebut
adalah analisis tren pengguna (*Collaborative Filtering*), analisis
preferensi personal (*Content-Based*), dan analisis situasi *real-time*
(*Context-Aware*). Skor dari ketiga analisis ini kemudian digabungkan
menjadi satu skor akhir relevansi menggunakan persamaan III.1 berikut:

+-------------------------------------------------------------------------------+---------+
| $$ScoreRelevance(u,i,c) = \ \alpha CF(c) \cdot ScoreCF\ $$                    | (III.1) |
+-------------------------------------------------------------------------------+         |
| $$+ \ \alpha CB(c) \cdot ScoreCB\  + \ \alpha Context(c) \cdot ScoreContext$$ |         |
+===============================================================================+=========+

dengan:

> $ScoreRelevance(u,i,c)$: Skor akhir kecocokan sebuah destinasi untuk
> pengguna pada situasi tertentu.
>
> $\alpha CF(c) \cdot ScoreCF$: Skor dari analisis tren (seberapa cocok
> destinasi menurut pengguna lain yang seleranya mirip).
>
> $\alpha CB(c) \cdot ScoreCB$: Skor dari analisis profil pribadi
> (seberapa cocok destinasi dengan riwayat dan selera personal
> pengguna).
>
> $\alpha Context(c) \cdot ScoreContext$: Skor dari analisis kondisi
> *real-time* (seberapa ideal destinasi untuk dikunjungi saat ini juga,
> mempertimbangkan cuaca, lalu lintas, dan penganggalan).
>
> $\alpha\ $: Bobot atau \"tingkat kepentingan\" untuk setiap skor.
> Nilai ini bisa berubah-ubah; misalnya saat cuaca buruk, bobot α
> Context​ akan ditingkatkan secara otomatis.

Fungsi *composite reward* mengombinasikan 50% NDCG, 30% Diversity, dan
20% Novelty untuk menyeimbangkan tiga objektif yang saling berkompetisi.
Prioritas 50% untuk akurasi (NDCG) dipilih karena relevansi tetap
fundamental dalam domain eksplorasi, sejalan dengan temuan Shi dkk.
(2023) bahwa bobot akurasi \<40% menurunkan user engagement, sementara
\>70% gagal mencapai diversifikasi (Abdollahpouri dkk., 2020). Bobot ini
ditentukan, dengan alokasi 30% *Diversity* dan 20% *Novelty* memberikan
nilai yang cukup untuk eksplorasi tanpa mengorbankan relevansi.

Langkah 2: Optimisasi Adaptif dengan MAB-MMR

Setelah mendapatkan daftar kandidat, sistem tidak langsung
menampilkannya. Daftar tersebut dioptimasi melalui mekanisme penyesuaian
bobot dinamis yang menjadi kontribusi utama penelitian ini.

1.  Penentuan Strategi oleh MAB

> Pertama, sistem harus menentukan strategi rekomendasi yang paling
> tepat untuk situasi saat ini. Apakah harus fokus pada akurasi, atau
> lebih mementingkan keberagaman? MAB bertugas memilih parameter λ
> optimal dari 5 arms diskrit \[0.0, 0.3, 0.5, 0.7, 1.0\] yang
> merepresentasikan spektrum strategi dari \"relevansi murni\" (λ=0.0)
> hingga \"keberagaman murni\" (λ=1.0).
>
> Pemilihan 5 nilai diskrit ini didasarkan pada pertimbangan strategis:

- spektrum penuh dari relevansi murni (λ=0.0) hingga keberagaman murni
  (λ=1.0).

- interval 0.2-0.3 yang cukup diskriminatif berdasarkan eksperimen
  pendahuluan.

- efisiensi eksplorasi sejalan dengan literatur (Qassimi dan
  Rakrak, 2025) yang menunjukkan 3-7 arms sebagai optimal untuk
  *contextual bandits*.

> Proses pemilihan strategi ini menggunakan algoritma *Upper Confidence
> Bound* (UCB) yang dihitung berdasarkan persamaan III.2:

  ------------------------------------------------------------------------
  $$UCB(t,k)\  = \ \mu\hat{}(t,k)\  + \ c\sqrt{}(ln(t)/N(k))$$   (III.2)
  -------------------------------------------------------------- ---------

  ------------------------------------------------------------------------

> dengan:
>
> $UCB(t,k)$: Skor kepercayaan untuk setiap strategi k. Sistem akan
> memilih strategi dengan skor tertinggi.
>
> $\mu\hat{}(t,k)$: Rata-rata *reward* atau keberhasilan strategi k di
> masa lalu. Komponen ini merepresentasikan eksploitasi, yang
> memanfaatkan strategi dengan riwayat keberhasilan tertinggi.
>
> $c\sqrt{}(ln(t)/N(k))$: \"Bonus rasa penasaran\". Nilai bonus ini akan
> tinggi untuk strategi yang jarang dicoba. Ini adalah komponen
> eksplorasi, yang mendorong sistem untuk mencoba hal-hal baru.
>
> $t$: Jumlah total interaksi sejauh ini.
>
> $N(k)$: Seberapa sering strategi k telah dipilih

2.  Penyusunan Ulang Daftar oleh MMR (\"Lengan Eksekutor\")

> Setelah strategi (nilai λ) ditentukan oleh MAB, daftar kandidat akan
> disusun ulang. Skor final untuk setiap destinasi dihitung menggunakan
> prinsip *Maximal Marginal Relevance* (MMR) sesuai persamaan (III.3):

+-----------------------------------------------------------------------------+---------+
| $${FinalScore}_{i}\  =$$                                                    | (III.3) |
+-----------------------------------------------------------------------------+         |
| $$\ \lambda \cdot {Score}_{{prediksi}_{i}}\  - \ (1 - \lambda) \cdot maxj$$ |         |
+-----------------------------------------------------------------------------+         |
| $$q \in S\ Sim(i,j)\  + \ \gamma \cdot B{onus}_{{bias}_{i}}\ \ \ \ $$       |         |
+=============================================================================+=========+

> dengan:
>
> ${FinalScore}_{i}$: Skor akhir dari destinasi i setelah proses
> editorial.
>
> $\lambda \cdot {Score}_{{prediksi}_{i}}$: Komponen relevansi. Semakin
> tinggi nilai λ (ditentukan oleh MAB), semakin besar porsi skor dari
> prediksi awal.
>
> $(1 - \lambda) \cdot maxj \in S\ Sim(i,j)$: Komponen hukuman karena
> monoton. Skor destinasi $i$ akan dikurangi jika ia terlalu mirip
> $Sim(i,j)$dengan destinasi lain (j) yang sudah ada di dalam daftar
> rekomendasi final (S).
>
> $\gamma \cdot B{onus}_{{bias}_{i}}$: Komponen keadilan. Ini adalah
> \"bonus\" yang diberikan kepada destinasi berkualitas namun kurang
> populer (*hidden gems*) untuk membantu mereka bersaing dengan
> destinasi yang sudah sangat terkenal.

Langkah 3: Menjaga Model Tetap Relevan (Adaptasi Jangka Panjang)

Model machine learning rentan mengalami penurunan performa akibat
kadaluwarsa data. Dunia pariwisata dan selera pengguna terus berubah,
sehingga model yang dibuat hari ini mungkin tidak akan akurat lagi di
masa depan. Oleh karena itu, penelitian ini merancang agar model bisa
beradaptasi seiring waktu.

Untuk menangani perubahan preferensi pengguna (*Concept Drift*) dalam
jangka panjang, sistem dirancang dengan kapabilitas Model Retraining.
Dalam lingkup eksperimen ini, proses pembaruan model dilakukan secara
periodik (batch retraining) menggunakan data umpan balik (*feedback*)
terbaru yang dikumpulkan dari interaksi pengguna.

Mekanisme ini memastikan bahwa *latent factor* pada model *Collaborative
Filtering* tetap relevan dengan tren terbaru. Evaluasi stabilitas model
dilakukan dengan memonitor metrik *Novelty* dan *Accuracy* secara
berkala untuk menentukan kapan *retraining* diperlukan, sebagaimana
divalidasi pada analisis stabilitas di Bab IV.

### Arsitektur Aliran Data 

Arsitektur ini dirancang pada gambar III.4 untuk memproses data secara
sistematis melalui tujuh tahapan utama, guna memastikan efisiensi dan
kapabilitas pembelajaran berkelanjutan. Proses operasional sistem, dari
permintaan awal hingga penyajian rekomendasi, dieksekusi melalui alur
kerja berikut:

[]{#_Toc214882434 .anchor}Gambar III.4 Arsitektur Aliran Data

1.  Tahap 1: Pengumpulan Data: Proses dimulai dengan mengambil dua
    kategori data. Data *real-time* mencakup cuaca, lalu lintas, tren
    media sosial, dan penanggalan diambil dari API publik secara
    terjadwal dengan format yang terstruktur untuk MAB processing.
    Secara paralel, data statis meliputi profil pengguna, metadata Objek
    Daya Tarik Wisata (ODTW), dan ulasan historis diekstraksi dari basis
    data relasional.

2.  Tahap 2: Pemrosesan Data: Data mentah yang telah diakuisisi
    selanjutnya melalui tahap pra-pemrosesan yang meliputi pembersihan
    data (data cleaning) untuk menangani anomali, transformasi data, dan
    rekayasa fitur (feature engineering) untuk mengekstraksi variabel
    prediktif termasuk *contextual signals* untuk MAB *reward
    calculation*. Seluruh fitur ini kemudian diintegrasikan menjadi
    dataset terpadu yang siap digunakan untuk pemodelan.

3.  Tahap 3: Pelatihan & Pembaruan Model: Model *machine learning*
    dilatih menggunakan dataset terpadu. Arsitektur ini didesain untuk
    mendukung mekanisme pelatihan ulang secara periodik, guna memastikan
    adaptasi model terhadap pergeseran pola data.

4.  Tahap 4: Inferensi & Pembuatan Rekomendasi: Pada saat inferensi,
    model yang telah dilatih digunakan untuk menghasilkan skor prediksi
    relevansi untuk setiap destinasi bagi pengguna aktif. Berdasarkan
    skor tersebut, sejumlah destinasi dengan peringkat teratas dipilih
    sebagai himpunan kandidat rekomendasi awal.

5.  Tahap 5: Optimalisasi Adaptif dengan MAB-MMR: Tahap ini merupakan
    inti inovasi penelitian yang mengimplementasikan sistem optimalisasi
    dua lapis. Layer pertama: *Multi-Armed Bandit* (MAB) menganalisis
    kondisi kontekstual *real-time* dari Tahap 1 (cuaca, traffic, social
    trends) untuk memilih parameter λ optimal dari 5 kemungkinan nilai
    (0.0, 0.3, 0.5, 0.7, 1.0) menggunakan *Upper Confidence Bound
    policy*. Layer kedua: *Maximal Marginal Relevance* menggunakan λ
    terpilih untuk me-rerank kandidat dengan menyeimbangkan relevansi
    dan *Diversity* secara dinamis, serta mengimplementasikan modul
    koreksi bias untuk memitigasi *popularity bias* dan mempromosikan
    destinasi yang kurang terekspos.

6.  Tahap 6: Penyajian Rekomendasi & Umpan Balik: Daftar N-Top ODTW yang
    telah teroptimalkan disajikan kepada pengguna melalui sebuah
    endpoint API.

7.  Tahap 7: Siklus Pembelajaran MAB: Interaksi dikonversi menjadi
    reward signal untuk MAB. Data reward ini digunakan MAB untuk
    memperbarui estimasi performa setiap arm, menciptakan pembelajaran
    berkelanjutan yang mengoptimalkan parameter λ seiring waktu,
    sehingga membentuk sebuah siklus pembelajaran berkelanjutan.
    Penentuan bobot β dan γ dalam fungsi *composite reward* sudah
    ditetapkan sebelumnya.

8.  Untuk mendukung kapabilitas adaptif *real-time*, Arsitektur sistem
    dirancang menggunakan pendekatan Microservices berbasis
    Event-Driven, yang memprioritaskan responsivitas inferensi saat
    permintaan pengguna terjadi (*inference-time context injection*).
    Berbeda dengan pemrosesan aliran kontinu (*continuous stream
    processing*) yang memakan sumber daya besar, arsitektur ini
    menerapkan mekanisme On-Demand Contextual Retrieval.

> Dalam skema ini, data historis diproses secara *batch* untuk membentuk
> *base model*, sementara data kontekstual *real-time* (seperti cuaca
> dan waktu) diambil dan diproses secara instan melalui API Gateway
> tepat saat pengguna meminta rekomendasi. Pendekatan ini dipilih untuk
> menyeimbangkan latensi sistem agar tetap di bawah ambang batas
> toleransi pengguna, sekaligus memastikan rekomendasi selalu relevan
> dengan kondisi terkini tanpa memerlukan infrastruktur pemrosesan
> kontekstual *real-time*.

### Alur Interaksi Sistem (*Sequence Diagram*)

[]{#_Toc214882435 .anchor}Gambar III.5 Tahap 1: Permintaan Rekomendasi

Alur pertama, yang ditunjukkan pada Gambar III.5, adalah proses
permintaan rekomendasi. Alur ini diinisiasi ketika Pengguna mengakses
Antarmuka Pengguna, yang kemudian meneruskan permintaan melalui API
Gateway ke Sistem Rekomendasi. Sistem kemudian bertindak sebagai
orkestrator utama: ia memanggil Layanan Konteks untuk mengumpulkan data
*real-time* (Tahap 1-2), memanggil Optimisasi MAB untuk memilih
parameter λ optimal (Tahap 5), dan mengeksekusi Model Hibrida untuk
menghasilkan daftar rekomendasi final (Tahap 3, 4, 5).

[]{#_Toc214882436 .anchor}Gambar III.6 Tahap 6-7: Interaksi &
Pembelajaran

Kedua alur ini permintaan dan umpan balik secara bersama-sama membentuk
sebuah sistem *closed-loop* yang dirancang untuk belajar dan beradaptasi
secara kontinu.

### Desain Basis Data (ERD)

Basis data digunakan untuk menstrukturkan dan menyimpan seluruh data
yang digunakan oleh model. Berdasarkan analisis kebutuhan, sistem ini
akan mengelola beberapa entitas utama: Pengguna (User), Destinasi
(Destination), Kategori (Categories), Ulasan (Review), dan Peringkat
(Rating).

Hubungan kunci antara Pengguna dan Destinasi adalah *many-to-many*, di
mana satu pengguna dapat berinteraksi dengan banyak destinasi, dan
sebaliknya. Untuk mengimplementasikan hubungan ini secara efektif, tabel
rating dan review berfungsi sebagai tabel perantara (*junction tables*).
Setiap entri dalam tabel ini mencatat satu interaksi unik antara seorang
pengguna dengan sebuah destinasi. Struktur logis dan hubungan antar
semua entitas ini divisualisasikan secara lengkap dalam
*Entity-Relationship Diagram* (ERD) yang disajikan pada Gambar III.7.

![A diagram of a computer AI-generated content may be
incorrect.](media/image8.png){width="5.504399606299213in"
height="3.2875in"}

[]{#_Toc214882437 .anchor}Gambar III.7 *Entity-Relationship Diagram*
(ERD)

Berikut ini disajikan spesifikasi teknis untuk setiap tabel yang
menyusun basis data. Detail pada tabel-tabel di bawah ini merinci setiap
kolom, termasuk tipe data yang digunakan dan keterangan fungsionalnya,
yang berfungsi sebagai *blueprint* untuk implementasi.

[]{#_Toc214880956 .anchor}Tabel III.9 Struktur Tabel User

  -----------------------------------------------------------------------
        Nama Kolom               Tipe Data              Keterangan
  ----------------------- ----------------------- -----------------------
            Id                  SERIAL (PK)        Identifier unik untuk
                                                     setiap pengguna,
                                                   digenerate otomatis.

           Name                VARCHAR(255)       Nama lengkap pengguna.

           Email               VARCHAR(255)       Alamat email pengguna,
                                                      bersifat unik.

        Preferences            VARCHAR(255)        Menyimpan preferensi
                                                      kategori wisata
                                                     pengguna (misal:
                                                     \"Alam,Budaya\").

        Created_at               TIMESTAMP            Waktu saat akun
                                                  pengguna dibuat, terisi
                                                         otomatis.
  -----------------------------------------------------------------------

[]{#_Toc214880957 .anchor}Tabel III.10 Struktur Tabel rating

  -----------------------------------------------------------------------
        Nama Kolom               Tipe Data              Keterangan
  ----------------------- ----------------------- -----------------------
            Id                  SERIAL (PK)        Identifier unik untuk
                                                   setiap record rating.

          User_id              INTEGER (FK)          Foreign Key yang
                                                   merujuk ke users(id).

      Destination_id           INTEGER (FK)          Foreign Key yang
                                                        merujuk ke
                                                     destinations(id).

          rating                   FLOAT             Nilai rating yang
                                                    diberikan pengguna
                                                  (antara 1.0 s.d. 5.0).

        Created_at               TIMESTAMP           Waktu saat rating
                                                     diberikan, terisi
                                                         otomatis.
  -----------------------------------------------------------------------

[]{#_Toc214880958 .anchor}Tabel III.11 Struktur Tabel Destination

  -----------------------------------------------------------------------
        Nama Kolom               Tipe Data              Keterangan
  ----------------------- ----------------------- -----------------------
            Id                  SERIAL (PK)        Identifier unik untuk
                                                     setiap destinasi
                                                          (ODTW).

           Name                VARCHAR(255)        Nama resmi destinasi
                                                          wisata.

        Description                TEXT              Deskripsi lengkap
                                                    mengenai destinasi

            Lat                    FLOAT             Koordinat Lintang
                                                     (Latitude) untuk
                                                         pemetaan.

            Lon                    FLOAT              Koordinat Bujur
                                                     (Longitude) untuk
                                                         pemetaan.

          address              VARCHAR(255)           Alamat lengkap
                                                        destinasi.
  -----------------------------------------------------------------------

[]{#_Toc214880959 .anchor}Tabel III.12 Struktur Tabel
destination_categories

  -----------------------------------------------------------------------
        Nama Kolom               Tipe Data              Keterangan
  ----------------------- ----------------------- -----------------------
      Destination_id         INTEGER (PK, FK)        Foreign Key yang
                                                        merujuk ke
                                                     destinations(id).

        Category_id          INTEGER (PK, FK)        Foreign Key yang
                                                        merujuk ke
                                                      categories(id).
  -----------------------------------------------------------------------

[]{#_Toc214880960 .anchor}Tabel III.13 Struktur Tabel Categories

  -----------------------------------------------------------------------
        Nama Kolom               Tipe Data              Keterangan
  ----------------------- ----------------------- -----------------------
            Id                  SERIAL (PK)        Identifier unik untuk
                                                  setiap kategori wisata.

           Name                VARCHAR(255)        Nama kategori (e.g.,
                                                  Alam, Budaya, Kuliner,
                                                         Sejarah).

        Description            VARCHAR(255)          Deskripsi singkat
                                                     mengenai kategori
                                                         tersebut.
  -----------------------------------------------------------------------

[]{#_Toc214880961 .anchor}Tabel III.14 Struktur Tabel review

  -----------------------------------------------------------------------
        Nama Kolom               Tipe Data              Keterangan
  ----------------------- ----------------------- -----------------------
            Id                  SERIAL (PK)        Identifier unik untuk
                                                   setiap record ulasan.

          User_id              INTEGER (FK)          Foreign Key yang
                                                   merujuk ke users(id).

      Destination_id           INTEGER (FK)          Foreign Key yang
                                                        merujuk ke
                                                     destinations(id).

           Title               VARCHAR(255)         Judul singkat dari
                                                          ulasan.

          Content                  TEXT           Isi ulasan lengkap yang
                                                  ditulis oleh pengguna.

        Created_at               TIMESTAMP           Waktu saat ulasan
                                                      dibuat, terisi
                                                         otomatis.
  -----------------------------------------------------------------------

### Strategi Menangani *Cold Start*

Mengingat karakteristik dataset yang memiliki tingkat kelangkaan
(*sparsity*) tinggi, sistem dirancang dengan arsitektur hibrida yang
secara inheren tangguh (*robust*) terhadap kondisi pengguna baru
(*cold-start*). Strategi mitigasi diimplementasikan melalui tiga
pendekatan desain:

1.  Profil Berbasis Kategori (*Category-Based Profiling*):

> Sebagai langkah awal, representasi pengguna tidak dibangun berdasarkan
> ID unik semata, melainkan diperkaya dengan preferensi kategori. Sistem
> memanfaatkan metadata kategori destinasi (seperti Alam, Budaya,
> Kuliner) untuk membangun vektor profil awal. Hal ini memungkinkan
> sistem memetakan pengguna baru ke dalam klaster preferensi umum
> meskipun riwayat interaksi spesifik belum tersedia.

2.  Arsitektur Hibrida Seimbang (*Balanced Hybrid Fallback*):

> Sistem menerapkan pembobotan model hibrida seimbang ($\alpha_{CF}$ =
> 0.5, $\alpha_{CB}$ = 0.5). Dalam skenario *cold-start*, komponen
> *Collaborative Filtering* (CF) cenderung menghasilkan nilai prediksi
> nol atau netral karena ketiadaan tetangga (*neighbors*) yang valid.
> Dengan desain ini, skor rekomendasi akhir secara otomatis didominasi
> oleh komponen *Content-Based* (CB) yang tetap berfungsi optimal
> berdasarkan kesesuaian fitur item. Mekanisme ini berfungsi sebagai
> prosedur mitigasi (fallback) otomatis tanpa memerlukan penyesuaian
> parameter manual yang kompleks.

3.  *Contextual Boosting* sebagai Sinyal Tambahan:

> Untuk mengkompensasi minimnya sinyal preferensi personal, sistem
> meningkatkan peran data kontekstual real-time. Aturan *context-aware*
> (seperti cuaca dan waktu) diterapkan secara aditif pada skor kandidat
> rekomendasi. Hal ini memastikan bahwa rekomendasi yang disajikan
> kepada pengguna baru tetap terasa relevan dan cerdas karena
> disesuaikan dengan kondisi lingkungan saat itu, meskipun sistem belum
> mempelajari selera mendalam pengguna tersebut.

## Demonstrasi

Tahap Demonstrasi bertujuan untuk menunjukkan bagaimana artefak sistem
dapat digunakan untuk menyelesaikan permasalahan yang telah dirumuskan.
Dalam penelitian ini, demonstrasi akan dilakukan melalui implementasi
prototype fungsional dan aplikasi sistem pada skenario-skenario spesifik
yang merepresentasikan kondisi operasional dalam domain pariwisata
Kabupaten Sumedang.

### Skenario Demonstrasi

Demonstrasi sistem dilaksanakan melalui simulasi skenario terkontrol
yang mencerminkan kondisi operasional nyata dalam domain pariwisata
Kabupaten Sumedang. Tujuan demonstrasi adalah memvalidasi tiga
kapabilitas inti sistem adaptif: (1) personalisasi akurat dalam kondisi
normal, (2) responsivitas terhadap perubahan konteks eksternal, dan (3)
kemampuan diversifikasi untuk pemerataan distribusi.

Untuk mencapai tujuan tersebut, evaluasi akan difokuskan pada *case
study* pengguna representatif dengan tiga skenario kontekstual yang
kontras:

1.  Skenario 1 - *Baseline Performance* (Kondisi Ideal):

> Menguji kemampuan sistem mempertahankan personalisasi akurat pada
> kondisi tanpa kendala kontekstual (cuaca cerah, kepadatan normal).
> Sistem diharapkan merekomendasikan destinasi yang sesuai preferensi
> historis pengguna dengan parameter λ rendah untuk memaksimalkan
> relevansi. Validasi fokus pada akurasi pencocokan profil pengguna
> dengan karakteristik destinasi.

2.  Skenario 2 - *Context Responsiveness* (Perubahan Drastis):

> Menguji responsivitas sistem terhadap perubahan konteks lingkungan
> yang signifikan (misalnya: cuaca ekstrem, gangguan lalu lintas).
> Sistem diharapkan mampu melakukan intervensi adaptif dengan
> mengalihkan rekomendasi ke kategori alternatif yang lebih sesuai
> kondisi. Validasi fokus pada kemampuan sistem memprioritaskan
> kenyamanan dan keselamatan pengguna.

3.  Skenario 3 - *Diversity Optimization* (Kondisi Crowded):

> Menguji kemampuan sistem mendiversifikasi rekomendasi saat terjadi
> konsentrasi wisatawan tinggi. Sistem diharapkan meningkatkan parameter
> λ untuk mempromosikan destinasi alternatif yang beragam, sejalan
> dengan tujuan penelitian mencegah *overtourism*. Validasi fokus pada
> variasi geografis dan kategori destinasi yang direkomendasikan.

Pemilihan pengguna sampel dan parameter skenario spesifik (misalnya:
preferensi historis pengguna, jenis konteks yang disimulasikan) akan
didasarkan pada analisis eksplorasi data untuk memastikan
representativitas dan kemampuan validasi yang optimal.

## Evaluasi

Tahap Evaluasi bertujuan untuk memvalidasi kinerja artefak sistem dalam
memenuhi tujuan rekomendasi memenuhi tujuan yang telah ditetapkan.
Evaluasi dilakukan menggunakan metrik kuantitatif seperti akurasi,
keberagaman rekomendasi, kecepatan respons, dan stabilitas pemrosesan
data. Evaluasi kualitatif dilakukan melalui survei atau wawancara
terhadap pengguna untuk mengukur persepsi terhadap kegunaan dan kepuasan
penggunaan sistem.

Sebagai pembanding, sistem ini dievaluasi terhadap pendekatan
rekomendasi statis guna menyoroti keunggulan adaptivitas *real-time*.
Apabila hasil evaluasi menunjukkan adanya kekurangan, maka dilakukan
iterasi kembali ke tahap Perancangan dan Pengembangan untuk perbaikan.

### Evaluasi Kuantitatif

Evaluasi kuantitatif difokuskan untuk mengukur kinerja sistem secara
objektif berdasarkan rumusan masalah. Metrik yang digunakan
dikelompokkan ke dalam tiga kategori utama: Akurasi dan Relevansi,
Keberagaman dan Cakupan, serta Kebaruan.

1.  Metrik akurasi dan relevansi digunakan untuk menjawab RM1, yaitu
    memvalidasi kemampuan sistem dalam mempertahankan kualitas
    rekomendasi.

- *Precision@K*: Mengukur proporsi item relevan dalam K item teratas
  yang direkomendasikan (Ricci dkk., 2022). Metrik ini dipilih karena
  relevansinya yang lebih tinggi dibandingkan *precision* tradisional
  dalam konteks fokus pada top-K recommendations yang benar-benar
  dilihat pengguna. Dihitung dengan persamaan III.5:

+-----------------------------------------------------------------------------------+---------+
| $$Precision@K\  = \ $$                                                            | (III.5) |
+-----------------------------------------------------------------------------------+         |
| $$|\left\{ item\ relevan \right\}\  \cap \ \{ top - K\ recommendations\}|\ /\ K$$ |         |
+===================================================================================+=========+

- NDCG (*Normalized Discounted Cumulative Gain*): Mengukur kualitas
  ranking dengan mempertimbangkan posisi item relevan dalam daftar
  rekomendasi (Ricci dkk., 2022). Item relevan yang muncul di posisi
  atas mendapat skor lebih tinggi. NDCG dinormalisasi sehingga nilai
  maksimum adalah 1.0. Dihitung dengan persamaan III.6:

  ----------------------------------------------------------------
  $$NDCG@K\  = \ DCG@K\ /\ IDCG@K$$                      (III.6)
  ------------------------------------------------------ ---------

  ----------------------------------------------------------------

> dengan:
>
> DCG@K = *Discounted Cumulative Gain*
>
> IDCG@K = Ideal DCG.

2.  Metrik keberagaman dan cakupan secara langsung mengukur keberhasilan
    sistem dalam menjawab RM1 dan RM2 terkait peningkatan variasi dan
    jangkauan rekomendasi.

- Keberagaman (*Intra-List Diversity*): Mengukur seberapa bervariasi
  item-item dalam satu daftar rekomendasi yang disajikan kepada seorang
  pengguna (Akhadam dkk., 2025). Dalam penelitian ini, metrik ini
  dihitung sebagai 1 dikurangi rata-rata skor kemiripan antar item,
  sehingga nilai yang lebih tinggi merepresentasikan keberagaman yang
  lebih baik. Dihitung berdasarkan persamaan III.7:

  ---------------------------------------------------------------------------------
  $$Diversity\  = \ 1\  - \ (2/(|S|(|S| - 1)))\ *\ \sum\sum\ sim(i,j)$$   (III.7)
  ----------------------------------------------------------------------- ---------

  ---------------------------------------------------------------------------------

> dengan:
>
> S = set rekomendasi
>
> sim(i,j) = kesamaan antara item i dan j.

- Cakupan (*Catalogue Coverage*): Mengukur proporsi item dari
  keseluruhan katalog yang mampu direkomendasikan oleh sistem (Akhadam
  dkk., 2025). Nilai yang lebih tinggi menunjukkan bahwa sistem tidak
  hanya terpaku pada sebagian kecil item populer, melainkan mampu
  menjangkau lebih banyak destinasi. Dihitung dengan persamaan III.8:

+-------------------------------------------------------+---------+
| $$Coverage\  = \ | \cup \ users\ Recommendations|\ $$ | (III.8) |
+-------------------------------------------------------+         |
| $$/\ |Total\ Items|$$                                 |         |
+=======================================================+=========+

- Koefisien Gini (*Gini Coefficient*): Metrik yang mengukur
  ketidaksetaraan di seluruh distribusi frekuensi item yang
  direkomendasikan (Abdollahpouri dkk., 2021). Metrik ini sering
  digunakan untuk menilai tingkat (ketidak)setaraan paparan (*exposure*)
  item yang berbeda yang disebabkan oleh *popularity bias*
  (Abdollahpouri dkk., 2021). Penurunan nilai Gini mengindikasikan
  keberhasilan sistem dalam mengurangi popularity bias dan mempromosikan
  distribusi kunjungan yang lebih adilDihitung dengan persamaan III.9:

  --------------------------------------------------------------------------------------
  $Gini\  = \ (\sum ᵢ₌₁ⁿ\ \sum ⱼ₌₁ⁿ\ |xᵢ\  - \ xⱼ|)\ /\ (2n²\  \cdot \ \mu)$   (III.9)
  ---------------------------------------------------------------------------- ---------

  --------------------------------------------------------------------------------------

> dengan:
>
> $xᵢ,\ xⱼ$ = jumlah kali destinasi i dan j direkomendasikan
>
> $n$ = jumlah total destinasi dalam katalog
>
> $\mu$ = rata-rata jumlah rekomendasi per destinasi

3.  Metrik Kebaruan ini digunakan untuk mengevaluasi kemampuan sistem
    dalam menjawab RM3, yaitu menyajikan destinasi yang tidak terduga
    atau kurang populer.

- Kebaruan (diukur dengan *Popularity*): Diukur melalui skor popularitas
  rata-rata dari item yang direkomendasikan (Abdollahpouri dkk., 2021).
  Nilai popularitas yang lebih rendah mengindikasikan tingkat kebaruan
  yang lebih tinggi, karena hal tersebut menunjukkan sistem berhasil
  merekomendasikan item-item yang kurang terekspos. Dihitung dengan
  persamaan III.10:

  --------------------------------------------------------------------------
  $$Novelty\  = \  - \sum(log2(pop(i)))\ /\ |Recommendations|$$   (III.10)
  --------------------------------------------------------------- ----------

  --------------------------------------------------------------------------

> dengan:
>
> pop(i) = *popularity* score dari item i.

4.  Validasi Signifikansi Statistik: Untuk mengevaluasi apakah perbedaan
    kinerja antar model yang diamati bukan hanya hasil kebetulan, akan
    dilakukan uji signifikansi statistik. Karena setiap model dievaluasi
    pada himpunan pengguna yang sama, metode yang paling tepat adalah
    *Paired t-test*. Statistik $t\ $dihitung berdasarkan persamaan
    III.11.

+---------------------------------------------------------+----------+
| > $$t = \ \frac{\overline{d}}{\frac{s_{d}}{\sqrt{n}}}$$ | (III.11) |
+=========================================================+==========+

> dengan:
>
> $\overline{d}\ $= rata-rata selisih kinerja antar pasangan model
>
> $s_{d}$ = standar deviasi dari selisih tersebut
>
> $n$ adalah jumlah total sampel pengguna yang dievaluasi.
>
> Nilai $p$ \< 0.05 akan digunakan sebagai ambang batas untuk menentukan
> perbedaan yang signifikan secara statistik

5.  Analisis ini digunakan untuk menemukan solusi optimal ketika
    terdapat pertukaran (*trade-off*) antara dua metrik yang saling
    bertentangan, yaitu Akurasi $(f_{1})$ dan Keberagaman $(f_{1})$.
    Persamaan III.12 membuktukan sebuah model $A$ dikatakan mendominasi
    model $B$ jika:

+--------------------------------------------------------------------+----------+
| > $$f_{1}(A) \geq f_{1}(B){\ \bigwedge\ f}_{2}(A){\geq f}_{2}(B)$$ | (III.12) |
+====================================================================+==========+

> dengan ketaksamaan ketat pada setidaknya salah satu metrik. Himpunan
> solusi yang tidak didominasi oleh model lain membentuk Pareto
> Frontier, yang merepresentasikan pilihan efisiensi terbaik.

6.  Untuk melengkapi uji signifikansi statistik, *Cohen\'s d* akan
    dihitung untuk mengukur besarnya perbedaan praktis antar model
    (Cohen, 1988). Metrik ini memberikan interpretasi yang lebih
    substantif dibandingkan *p-value* semata, karena menunjukkan
    magnitudo perbedaan yang independen dari ukuran sampel (Ricci dkk.,
    2022). Dihitung dengan persamaan III.13

+----------------------------------------------------------------------+----------+
| > $$d = \ \frac{\overline{x_{1}} - \ \overline{x_{2}}}{S_{pooled}}$$ | (III.11) |
+======================================================================+==========+

> dengan:
>
> $\overline{x_{1}} - \ \overline{x_{2}}$ = *mean* metrik untuk dua
> model yang dibandingkan
>
> $S_{pooled}$ = *pooled standard deviation*
>
> Interpretasi mengikuti konvensi Cohen (1988):
>
> *small effect* $(d\  \approx 0.2)$, *medium effect*
> $(d\  \approx 0.5)$, *large effect* $(d\  \approx 0.8)$.

### Evaluasi Kualitatif 

bertujuan untuk menggali persepsi dan pengalaman pengguna secara
mendalam, yang tidak dapat ditangkap oleh metrik kuantitatif. Evaluasi
ini akan dilakukan melalui sesi pengujian pengguna (*user testing*).
Instrumen yang akan digunakan adalah:

1.  *System Usability Scale* (SUS): Instrumen ini terdiri dari 10
    pertanyaan standar yang dirancang untuk mengukur persepsi kemudahan
    penggunaan (*perceived ease of use atau usability*) dari prototipe
    sistem yang dibangun (Brooke, 1996). Terdapat 10 pertanyaan dengan
    responden menjawab dengan skala Likert satu hingga lima yaitu 1
    sangat tidak setuju, 2 tidak setuju, 3 netral, 4 setuju, dan 5
    sangat setuju seperti yang diperlihatkan pada Tabel III.15.

[]{#_Toc214880962 .anchor}Tabel III.15 Daftar Pernyataan *System
Usability Scale*

+----+------------------------------------------------------+---------------------------------------+
| No | Pernyataan                                           | Tanggapan                             |
|    |                                                      +-------+-------+-------+-------+-------+
|    |                                                      | 1     | 2     | 3     | 4     | 5     |
+:==:+======================================================+=======+=======+=======+=======+=======+
| 1  | Saya berpikir akan menggunakan sistem ini secara     |       |       |       |       |       |
|    | teratur                                              |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 2  | Saya merasa sistem ini terlalu rumit untuk digunakan |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 3  | Saya merasa sistem ini mudah digunakan               |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 4  | Saya memerlukan bantuan orang teknis untuk           |       |       |       |       |       |
|    | menggunakan sistem ini                               |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 5  | Berbagai fungsi dalam sistem ini terintegrasi dengan |       |       |       |       |       |
|    | baik                                                 |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 6  | Menurut saya terdapat terlalu banyak inkonsistensi   |       |       |       |       |       |
|    | dalam sistem ini                                     |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 7  | Saya membayangkan kebanyakan orang akan belajar      |       |       |       |       |       |
|    | menggunakan sistem ini dengan sangat cepat           |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 8  | Saya merasa sistem ini sangat rumit untuk digunakan  |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 9  | Saya merasa sangat percaya diri menggunakan sistem   |       |       |       |       |       |
|    | ini                                                  |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+
| 10 | Saya perlu mempelajari banyak hal sebelum dapat      |       |       |       |       |       |
|    | menggunakan sistem ini                               |       |       |       |       |       |
+----+------------------------------------------------------+-------+-------+-------+-------+-------+

> Adapun cara menghitung hasil pengukuran *system usability
> scale *yaitu:

- Untuk setiap pertanyaan pada urutan ganjil kurangi dengan nilai satu.
  Contoh pertanyaan 1 memiliki skor 4. Maka kurangi 4 dengan 1 sehingga
  skor pertanyaan 1 adalah 3.

- Untuk setiap pertanyaan pada urutan genap kurangi nilainya dari lima.
  Contoh pertanyaan 2 memiliki skor 1. Maka kurangi 5 dengan 1 sehingga
  skor pertanyaan 2 adalah 4.

- Tambahkan nilai-nilai dari pernyataan bernomor genap dan ganjil.
  Kemudian hasil penjumlahan tersebut dikalikan dengan 2,5.

Kombinasi evaluasi kuantitatif dan kualitatif ini dirancang untuk
memberikan validasi menyeluruh terhadap model MAB-MMR. Metrik
kuantitatif memastikan sistem dapat menyeimbangkan akurasi, keberagaman,
dan kebaruan secara terukur, sementara evaluasi kualitatif memvalidasi
bahwa keunggulan teknis tersebut benar-benar menghasilkan pengalaman
pengguna yang memuaskan dalam konteks penggunaan nyata. Pendekatan
evaluasi multi-dimensi ini memungkinkan penilaian komprehensif terhadap
kontribusi penelitian baik dari aspek algoritmik maupun aplikatif.

### Protokol Pengujian

Untuk mengevaluasi efektivitas model MAB-MMR yang diusulkan, penelitian
ini membandingkannya dengan sebelas konfigurasi model yang dikelompokkan
menjadi tiga kategori:

1.  Kategori 1: Baseline Fundamental (Non-Diversified)

> Kelompok ini mencakup model-model dasar yang berfokus murni pada
> relevansi tanpa mekanisme diversifikasi tambahan:

- *Popularity-Based Recommendation*: *Baseline* paling sederhana yang
  merekomendasikan destinasi berdasarkan popularitas global (frekuensi
  kunjungan) tanpa personalisasi.

- *Collaborative Filtering* (NMF): Menggunakan teknik *Non-negative
  Matrix Factorization* untuk menangkap preferensi laten pengguna
  berdasarkan interaksi historis semata.

- *Content-Based Filtering* (CB): Merekomendasikan item dengan
  menghitung skor kemiripan (*similarity*) antara vektor fitur destinasi
  (yang dibobotkan menggunakan TF-IDF pada atribut kategori) dan profil
  preferensi pengguna. Model ini berfungsi sebagai *baseline* krusial
  untuk menangani masalah *cold-start* di mana data interaksi
  kolaboratif belum tersedia.

- *Hybrid Model* (*No Context*): Mengombinasikan skor CF dan CB (bobot
  50:50) tanpa melibatkan fitur kontekstual *real-time*, digunakan untuk
  mengukur kontribusi murni dari hibridisasi.

2.  Kategori 2: *Baseline Static Diversification* (dengan Konteks)

> Kelompok ini menggunakan model Hybrid *Context-Aware* sebagai basis,
> kemudian menerapkan re-ranking MMR dengan parameter statis untuk
> memvalidasi keunggulan adaptasi dinamis (Hipotesis 1):

- Hybrid+MMR-λ0.0 (*Pure Relevance*): Fokus 100% pada akurasi (setara
  dengan model *Hybrid Context-Aware* murni).

- Hybrid+MMR-λ0.3 (*Relevance-Oriented*): Diversifikasi minimal (30%).

- Hybrid+MMR-λ0.5 (*Balanced*): *Baseline* utama dengan penyeimbangan
  moderat.

- Hybrid+MMR-λ0.7 (*Diversity-Oriented*): Prioritas pada keberagaman
  (70%).

- Hybrid+MMR-λ1.0 (*Pure Diversity*): Fokus 100% pada keberagaman
  (maksimalisasi disimilaritas).

3.  Kategori 3: Model Usulan

- Hybrid+MAB-MMR (*Proposed*): Model hybrid *context-aware* dengan
  seleksi parameter λ yang adaptif menggunakan *Multi-Armed Bandit*.

4.  Tahap 2: User testing

> Pengujian pada user dilakukan untuk memvalidasi pengalaman pengguna
> dalam kondisi operasional dengan integrasi data kontekstual
> *real-time*.

5.  Integrasi dan Triangulasi Hasil

> Hasil dari kedua tahap pengujian akan diintegrasikan dalam Bab 4 untuk
> memberikan validasi:

- Konvergensi: Bila evaluasi *offline* menunjukkan tingkat keberagaman
  rekomendasi tinggi dan pengujian pengguna mencatat kepuasan yang baik,
  maka hal ini menjadi bukti kuat efektivitas pendekatan yang diusulkan.

- Divergensi: Jika ditemukan ketidaksesuaian misalnya metrik teknis
  tinggi namun skor SUS rendah maka perbedaan tersebut akan dianalisis
  secara mendalam untuk mengidentifikasi penyebab dan implikasinya.

- Komplementaritas: Data kuantitatif menguraikan pola kinerja sistem,
  sedangkan umpan balik kualitatif memberikan konteks interpretatif
  terhadap pola tersebut.

Melalui triangulasi ini, penelitian berupaya memastikan bahwa alat ukur
benar-benar mengukur hal yang dimaksud dan bahwa hasilnya dapat
diterapkan pada kondisi lain.

## Komunikasi

Tahap *Komunikasi* merupakan fase akhir dalam DSRM yang berfokus pada
diseminasi hasil penelitian kepada komunitas akademik dan praktisi.
Komunikasi dilakukan melalui penyusunan tesis yang mendokumentasikan
seluruh proses, temuan, dan sistem secara lengkap.

# Implementasi dan Hasil Penelitian

Bab ini menyajikan dokumentasi komprehensif mengenai realisasi teknis
sistem rekomendasi adaptif yang telah dirancang pada Bab III, serta
hasil evaluasi menyeluruh terhadap kinerja sistem. Pembahasan dimulai
dengan spesifikasi lingkungan implementasi, dilanjutkan dengan detail
implementasi setiap komponen sistem, dan diakhiri dengan analisis
mendalam terhadap hasil evaluasi kuantitatif maupun kualitatif yang
menjawab rumusan masalah penelitian.

## Lingkungan Implementasi

Realisasi teknis dari seluruh proses pengembangan dan eksperimen dalam
penelitian ini didukung oleh serangkaian perangkat lunak dan pustaka
(*libraries*) yang relevan dengan domain ilmu data dan rekayasa
perangkat lunak. Pemilihan *stack* teknologi didasarkan pada
pertimbangan kompatibilitas, performa, serta dukungan komunitas yang
aktif untuk memastikan reprodusibilitas penelitian.

### Stack Teknologi

Rincian lengkap teknologi yang digunakan disajikan pada Tabel IV.1.
Pemilihan Python sebagai bahasa utama didasarkan pada ekosistem *library
machine learning* yang matang (*surprise, scikit-learn, pandas*).
FastAPI dipilih untuk API *framework*. PostgreSQL digunakan untuk
mendukung data relasional, sementara Docker memastikan *environment
consistency* untuk reprodusibilitas penelitian.

[]{#_Toc214880963 .anchor}Tabel IV.1 Stack Teknologi Penelitian

  ----------------------------------------------------------------------------
   No       Kategori         Teknologi      Versi     Peran dalam Penelitian
  ---- ------------------- -------------- --------- --------------------------
   1       Programming         Python       3.9+       Primary development
            Language                                         language

   2      ML Framework      scikit-learn    1.3.0   Implementasi CB (TF-IDF),
                                                            similarity

   3      ML Framework        surprise       \-       Implementasi CF (NMF)

   4     Data Processing       pandas       2.0.3     Data manipulation dan
                                                          preprocessing

   5     Data Processing       NumPy       1.24.3     Numerical computation

   6        Database         PostgreSQL     15.3     Relational data storage

   7      API Framework       FastAPI      0.100.0   RESTful API development

   8       Validation         Pydantic      2.0+         Request/response
                                                            validation

   9         Caching           Redis       7.0.12   Cache untuk API responses

   10   Containerization       Docker      24.0.2          Application
                                                         containerization

   11    Version Control        Git        2.41.0     Source code management

   12       Notebook        Jupyter Lab     4.0.2    Interactive development
           Environment                              

   13     Visualization      Matplotlib     3.7.2          Static plots

   14     Visualization       Seaborn      0.12.2        Statistical data
                                                          visualization
  ----------------------------------------------------------------------------

### Spesifikasi Sistem

Eksperimen dilakukan pada lingkungan komputasi dengan spesifikasi:
Processor Intel Core i5-1335U, RAM 16GB DDR5, dan Storage 512GB NVMe
SSD. Konfigurasi eksperimen menggunakan *random seed* global 42 untuk
reprodusibilitas, seperti yang didefinisikan dalam *notebook* evaluasi.

## Implementasi Sistem

Bagian ini mendokumentasikan realisasi teknis dari arsitektur sistem
yang telah dirancang pada Bab III, disesuaikan dengan implementasi
aktual pada *notebook* evaluasi evaluasi_kuantitatif_FINAL.ipynb.

### Arsitektur Sistem

Implementasi arsitektur sistem mengadopsi *microservices pattern* untuk
memastikan *scalability* dan *fault tolerance*. Arsitektur terdiri dari
tiga layer utama: (1) *Data Layer* yang mengelola database PostgreSQL,
(2) *Application Layer* yang mengimplementasikan model ML dan *business
logic*, dan (3) *Presentation Layer* yang menyediakan REST API dan
antarmuka web.

Arsitektur *pipeline* rekomendasi mengikuti desain tiga tahap yang
terintegrasi, seperti yang diilustrasikan pada Gambar IV.1. Tahap
pertama adalah *Candidate Generation*, di mana sistem mengintegrasikan
skor dari tiga komponen: *Collaborative Filtering* (NMF) untuk menangkap
pola preferensi kolaboratif, *Content-Based Filtering* (TF-IDF) untuk
*similarity* berbasis metadata kategori, dan *Context-Aware Component*
yang menambahkan *boost* aditif berdasarkan kondisi kontekstual (cuaca,
hari, kepadatan, *event*). Ketiga skor ini digabungkan untuk
menghasilkan kandidat rekomendasi awal.

Tahap kedua adalah Adaptive Optimization menggunakan *Multi-Armed
Bandit* (MAB) dengan algoritma *Upper Confidence Bound* (UCB1). MAB
bertugas memilih parameter λ optimal dari 5 *arms* diskrit \[0.0, 0.3,
0.5, 0.7, 1.0\] yang merepresentasikan spektrum strategi dari
\"relevansi murni\" (λ=0.0) hingga \"keberagaman murni\" (λ=1.0).
Pemilihan *arm* dilakukan secara dinamis berdasarkan konteks pengguna
dan *reward* historis dari setiap *arm*.

Tahap ketiga adalah Re-ranking menggunakan *Maximal Marginal Relevance*
(MMR). Dengan parameter λ yang telah dipilih oleh MAB, MMR melakukan
seleksi iteratif untuk membangun daftar final top-10 destinasi,
menyeimbangkan relevansi item dengan keberagaman (perbedaan dari item
yang sudah terpilih). *Output* akhir adalah daftar top-10 destinasi yang
dipersonalisasi dan beragam, siap disajikan kepada pengguna.

![[]{#_Toc214882438 .anchor}Gambar IV.1 Arsitektur Pipeline Rekomendasi
MAB-MMR](media/image9.png){width="5.513888888888889in"
height="2.473611111111111in"}

### Deskripsi Dataset dan Eksperimen

Berdasarkan metode akuisisi data yang dijelaskan pada Bab III, dataset
mentah melalui tahap pembersihan (*cleaning*) dan pemrosesan awal.
Dataset akhir yang valid untuk digunakan dalam eksperimen memiliki
karakteristik statistik sebagai berikut:

1.  Rentang Waktu: Data mencakup periode historis 12 tahun, mulai dari 6
    Oktober 2013 hingga 3 November 2025.

2.  Volume Data:

    - Total Destinasi: 224 ODTW

    - Total Pengguna Unik: 27.431 pengguna.

    - Total Interaksi (*Ratings*): 36.992 ulasan.

3.  Kepadatan Data (*Sparsity*): Tercatat sebesar 0.602%. Nilai ini
    mengindikasikan tingkat kelangkaan data (*sparsity*) yang tinggi,
    yang menegaskan kompleksitas permasalahan dalam sistem rekomendasi
    pariwisata.

4.  Distribusi Interaksi: Analisis distribusi menunjukkan bahwa 99,69%
    pengguna memiliki kurang dari 10 ulasan. Kondisi ini mengonfirmasi
    adanya masalah *cold-start* yang ekstrem pada dataset.

Analisis lebih lanjut dilakukan terhadap distribusi interaksi pengguna
untuk memvalidasi keberadaan fenomena *popularity bias* pada *dataset*.
Visualisasi distribusi rating per destinasi (diurutkan dari yang
terpopuler) menunjukkan pola Distribusi Pangkat (*Power Law*) yang
sangat tajam, sebagaimana terlihat pada Gambar IV.2.

![[]{#_Toc214882439 .anchor}Gambar IV.2 Distribusi Interaksi Pengguna
Asli (*Long-Tail*) pada Dataset\
Pariwisata
Sumedang](media/image10.png){alt="A graph with a red line AI-generated content may be incorrect."
width="5.513888888888889in" height="2.9902777777777776in"}

Grafik di atas mengonfirmasi ketimpangan yang ekstrem dalam data
kunjungan. Area yang diarsir merah menunjukkan dominasi *head items*, di
mana sebagian kecil destinasi populer menerima mayoritas interaksi,
sementara kurva yang melandai panjang ke kanan (*long-tail*)
merepresentasikan ratusan destinasi lain yang jarang mendapatkan
*rating*. Struktur data yang timpang ini menegaskan urgensi penerapan
algoritma yang mampu mengangkat item di area *tail* tanpa bergantung
semata pada popularitas historis.

Skema Pembagian Data (Data Splitting): Untuk keperluan evaluasi yang
realistis, dataset dibagi dengan rasio 80:

1.  *Training Set* (80%): 6.120 interaksi terawal (untuk melatih model).

2.  *Test Set* (20%): 2.331 interaksi terbaru (untuk pengujian performa
    prediksi).

3.  Populasi Evaluasi: Fokus evaluasi dibatasi pada 1.880 pengguna valid
    (memiliki ≥ 3 ratings) untuk menjamin reliabilitas pengukuran metrik
    akurasi

### Implementasi Backend dan Model

Implementasi model disesuaikan dengan *library* dan parameter yang
digunakan dalam *notebook* evaluasi untuk memastikan konsistensi data.

- *Collaborative Filtering* (CF): Diimplementasikan menggunakan
  *library* surprise dengan algoritma *Non-negative Matrix
  Factorization* (NMF). Parameter yang digunakan adalah n_factors=20
  (jumlah komponen laten) dan n_epochs=30, sesuai dengan implementasi di
  *notebook* evaluasi. Pemilihan n_factors=20 (dibandingkan nilai lebih
  tinggi seperti 50) dipilih sebagai keseimbangan antara performa dan
  kecepatan *training*, yang sangat relevan untuk skenario *cold-start*
  dengan data *sparse*.

- *Content-Based Filtering* (CB): Menggunakan TfidfVectorizer dari
  scikit-learn dengan parameter *default* untuk mengekstraksi fitur dari
  metadata kategori item. Berbeda dengan pendekatan *content-based*
  tradisional yang menggunakan deskripsi teks panjang, implementasi ini
  fokus pada kategori. Dalam skenario *cold-start* ekstrem (di mana
  99.69% pengguna memiliki \<10 *rating*), metadata kategori terbukti
  lebih informatif dan stabil daripada sinyal kolaboratif yang sangat
  *sparse*.

- *Context-Aware Component*: Mengintegrasikan data kontekstual (cuaca,
  hari, kepadatan, *event*) menggunakan logika aditif. Berbeda dengan
  *weighted sum*, pendekatan ini mengonversi bobot multiplikatif menjadi
  *boost* aditif. Sebagai contoh, aturan {\'Wisata Alam\': 1.5} pada
  kondisi *weekend* dikonversi menjadi *boost* +0.5 (1.5 - 1.0) yang
  ditambahkan ke skor relevansi. Sebaliknya, aturan {\'Wisata Alam\':
  0.5} pada kondisi hujan menjadi penalti -0.5 (0.5 - 1.0). Skor akhir
  item dihitung dengan menjumlahkan skor relevansi asli dengan total
  *boost* dari semua aturan kontekstual yang aktif. Detail lengkap
  aturan kontekstual disajikan dalam Lampiran A.2.

- *Multi-Armed Bandit* (MAB): Mengimplementasikan algoritma UCB1 (*Upper
  Confidence Bound*) standar untuk mengelola 5 *arms* yang
  merepresentasikan nilai λ berbeda: \[0.0, 0.3, 0.5, 0.7, 1.0\].
  *Reward function* yang digunakan menggabungkan tiga metrik: 50% NDCG
  (akurasi), 30% *Diversity* (keberagaman), dan 20% *Novelty*
  (kebaruan), mencerminkan prioritas sistem untuk menyeimbangkan
  *multiple objectives*.

- *Maximal Marginal Relevance* (MMR): Melakukan *re-ranking* kandidat.
  Vektor fitur untuk menghitung similaritas (keberagaman) adalah
  gabungan dari *one-hot encoding* kategori item dan skor popularitas
  item yang dinormalisasi (dengan bobot 0.3). Algoritma berjalan secara
  iteratif: pada setiap langkah, MMR memilih item dengan skor MMR
  tertinggi (relevansi tinggi DAN tidak mirip dengan item yang sudah
  dipilih), menambahkannya ke *result set*, dan melanjutkan hingga
  mencapai target k=10 item.

Detail snippet kode untuk setiap kelas model dapat ditemukan di Lampiran
A: implementasi $ProperCollaborativeRecommender$ dengan NMF (Lampiran
A.1.1), $ContextAwareComponent$ dengan logika aditif (Lampiran A.1.2),
dan $ContextualMAB$ beserta $MMRReranker\ $dengan algoritma iteratif
(Lampiran A.1.3).

Selain logika pemrosesan data, arsitektur backend diperkuat dengan
mekanisme Redis Caching Layer untuk memenuhi standar keandalan sistem
(KNF05). Data kontekstual eksternal yang bersifat dinamis (seperti cuaca
dan waktu) disimpan sementara dalam memori dengan durasi *Time-to-Live*
(TTL) 30 menit. Mekanisme ini berfungsi sebagai strategi *fallback*
otomatis: apabila API eksternal mengalami kegagalan koneksi atau latensi
tinggi (*timeout*), sistem akan menggunakan data konteks terakhir yang
tersimpan di *cache*. Hal ini menjamin layanan rekomendasi tetap
tersedia (*high availability*) dan responsif bagi pengguna meskipun
terjadi gangguan pada penyedia data pihak ketiga.

### Implementasi Antarmuka Pengguna

Antarmuka pengguna (UI) diimplementasikan sebagai *web application*
menggunakan React sebagai *framework frontend* dengan Tailwind CSS untuk
*styling*. Antarmuka ini dirancang untuk berinteraksi langsung dengan
*backend* FastAPI dan menyajikan rekomendasi yang adaptif kepada
pengguna.

Implementasi UI terdiri dari tiga komponen React utama. Komponen pertama
adalah RecommendationList, yang bertanggung jawab menampilkan daftar
rekomendasi yang diterima dari API, lengkap dengan *loading state*
(menampilkan *skeleton placeholders*) dan *error state*. Komponen kedua
adalah DestinationCard, komponen visual *reusable* untuk setiap
destinasi, yang menampilkan gambar (dengan *lazy loading*), *badge*
kategori, rating bintang, dan deskripsi singkat.

[]{#_Toc214882440 .anchor}Gambar IV.3 Tampilan Halaman Utama

## Hasil Evaluasi Kuantitatif

Sub-bab ini menyajikan hasil evaluasi kuantitatif dari eksekusi notebook
evaluasi_kuantitatif_FINAL.ipynb. Analisis berikut didasarkan pada data
yang diekstraksi dari notebook tersebut, yang mencerminkan performa
model pada dataset yang sangat sparse.

Sebagaimana dirumuskan dalam Tujuan Penelitian (Subbab I.3), evaluasi
ini dirancang untuk menjawab tiga rumusan masalah utama:

RM1**:** Kemampuan optimasi dinamis parameter $\lambda$ dalam
meningkatkan keberagaman tanpa mengorbankan akurasi.

RM2**:** Seberapa besar pengaruh integrasi data kontekstual dinamis
(cuaca dan kalender secara real-time, serta model simulasi traffic dan
social media trends).

RM3**:** Peningkatan eksposur destinasi kurang populer dibandingkan
sistem konvensional.

### Performa Model Baseline Non-Diversified (CF, CB, Hybrid) 

Untuk menjawab RM1 dan memvalidasi kebutuhan akan pendekatan hibrida
serta mekanisme diversifikasi, empat model baseline fundamental
dievaluasi sebagai titik referensi. Model-model ini mewakili pendekatan
konvensional yang tidak mengimplementasikan mekanisme diversifikasi,
sebagaimana diidentifikasi dalam analisis permasalahan (Subbab III.2.1).
Hasil evaluasi keempat model baseline disajikan pada Tabel IV.2.

[]{#_Toc214880964 .anchor}Tabel IV.2 Perbandingan Kinerja Model
*Baseline Non-Diversified*

  ------------------------------------------------------------------------------------------------
     Model      Precision@10   Recall@10   NDCG@10   *Diversity*   *Novelty*   *Catalog    *Gini
                                                                               Coverage*   Coef*
  ------------ -------------- ----------- --------- ------------- ----------- ----------- --------
   Popularity      0.0288       0.2410     0.1327      0.9111       0.3794       4.46%     0.2397

       CF          0.0045       0.0365     0.0169      0.8911       0.8625      82.14%     0.6567

       CB          0.0116       0.0954     0.0461      0.0565       0.7402      40.18%     0.5605

     Hybrid        0.0067       0.0536     0.0244      0.5801       0.8793      78.13%     0.6620
  ------------------------------------------------------------------------------------------------

1.  Analisis Model *Popularity-Based*

> Model Popularity-Based secara mengejutkan menghasilkan akurasi
> (NDCG@10 = 0.1327) tertinggi di antara semua model. Angka ini secara
> absolut mengalahkan model personalisasi yang lebih kompleks,
> menunjukkan bias yang sangat kuat dalam test set.
>
> Akar penyebab performa ini adalah dataset bias. Data uji didominasi
> oleh 10 item terpopuler dari 224 item yang ada (10/224 = 4.46%). Model
> ini pada dasarnya hanya merekomendasikan 10 item yang sama berulang
> kali kepada setiap pengguna.
>
> Paradoksnya, model ini mencatat *Diversity* (0.9111) yang tinggi dan
> Gini (0.2397) yang rendah. Metrik ini tinggi secara artifisial, bukan
> karena strategi diversifikasi, tetapi murni karena 10 item terpopuler
> tersebut kebetulan memiliki kategori yang berbeda. Metrik *Coverage*
> (4.46%) dan *Novelty* (0.3794) yang sangat rendah menunjukkan
> kegagalan total model ini dalam hal eksplorasi.
>
> Implikasinya, model ini adalah baseline yang buruk untuk mengukur
> *coverage* atau *Novelty*. Namun, ia menjadi baseline akurasi yang
> ironisnya sulit dikalahkan, yang membuktikan bahwa sifat data uji
> lebih menguntungkan popularitas daripada personalisasi.

2.  Analisis Model *Collaborative Filtering* (CF)

> Model *Collaborative Filtering* (NMF) menunjukkan kegagalan akurasi
> yang signifikan, dengan NDCG@10 hanya 0.0169. Performa ini adalah yang
> terburuk kedua, hanya sedikit di atas model acak, dan secara drastis
> lebih rendah dari *baseline Popularity* (0.1327) maupun CB (0.0461).
>
> Penyebab kegagalan ini dapat diatribusikan langsung pada dua
> karakteristik data: data *sparsity* yang ekstrem (hanya 0.602% rating
> matrix terisi) dan masalah cold-start masif (99.69% pengguna memiliki
> \< 10 rating). Tanpa data interaksi yang cukup, NMF tidak dapat
> mempelajari pola laten pengguna atau item yang bermakna.
>
> Kegagalan akurasi ini memaksa model untuk memberikan rekomendasi yang
> semi-acak, yang secara artifisial menghasilkan metrik sekunder
> tertinggi: *Diversity* (0.8911), *Novelty* (0.8625), dan *Coverage*
> (82.14%). Angka-angka ini bukanlah cerminan dari strategi eksplorasi
> yang cerdas, melainkan artefak dari ketidakmampuan total model untuk
> melakukan personalisasi.
>
> Implikasi utamanya adalah bahwa model CF murni sama sekali tidak cocok
> untuk skenario *cold-start* ekstrem seperti ini. Model ini gagal
> menemukan sinyal apa pun dari data interaksi yang sangat sedikit dan
> pada dasarnya tidak berguna dalam sistem ini.

3.  Analisis Model *Content-Based* (CB**)**

> Model *Content-Based* (CB), yang menggunakan kategori item (TF-IDF),
> menunjukkan akurasi (NDCG@10 = 0.0461) yang jauh lebih superior
> daripada CF (0.0169). Meskipun masih di bawah baseline *Popularity*,
> performanya hampir 3x lipat lebih baik daripada CF, membuktikan
> relevansinya.
>
> Ini adalah temuan kunci: dalam skenario *cold-start* ekstrem, metadata
> (kategori) jauh lebih berguna daripada data interaksi yang langka.
> Analisis dari notebook (Section 2, CELL 15.5) mendukung ini,
> menunjukkan bahwa 56.54% pengguna memang memiliki preferensi kategori
> yang konsisten (1-2 kategori), memberikan sinyal yang cukup bagi model
> CB untuk bekerja.
>
> Seperti yang diperkirakan, model ini terjebak dalam filter bubble. Ia
> menghasilkan *Diversity* (0.0565) terendah kedua dan *Coverage*
> (40.18%) yang terbatas. Model ini cenderung merekomendasikan item yang
> sangat mirip (dalam kategori yang sama) dengan apa yang sudah disukai
> pengguna, sehingga mengorbankan eksplorasi.
>
> Implikasinya, CB adalah strategi yang valid dan penting dalam skenario
> cold-start. Model ini berhasil menangkap preferensi pengguna yang
> sebenarnya, meskipun dengan konsekuensi menciptakan \"gelembung
> filter\" yang kuat dan mengorbankan penemuan item baru (*Novelty*).

4.  Analisis Model Hybrid (CF+CB+Context)

> Model Hybrid (dengan pembobotan 50/50 dan konteks) mencatat akurasi
> (NDCG@10 = 0.0244). Performa ini berada di antara CF (0.0169) dan CB
> (0.0461), namun secara signifikan lebih dekat ke performa CF yang
> buruk daripada CB yang lebih baik.
>
> Penyebab utamanya adalah pembobotan 50/50. Dalam skenario *sparsity*
> ekstrem, skor CF yang sangat rendah (mendekati nol atau acak) secara
> efektif \"menarik ke bawah\" dan merusak skor CB yang sebenarnya lebih
> relevan. Sinyal yang buruk dari CF menetralkan sinyal yang baik dari
> CB.
>
> Namun, model ini berhasil memperbaiki kelemahan utama CB. Dengan
> memasukkan komponen CF yang (meskipun tidak akurat) merekomendasikan
> secara acak, model ini mencapai *Diversity* (0.5801) dan *Coverage*
> (78.13%) yang jauh lebih sehat, memecah filter bubble yang diciptakan
> oleh CB murni.
>
> Implikasinya, model Hybrid 50/50 ini mewakili *trade-off* yang jelas:
> ia mengorbankan sebagian besar perolehan akurasi dari CB untuk
> mendapatkan eksplorasi dan coverage katalog yang jauh lebih baik. Ini
> adalah penyeimbang, meskipun tidak optimal secara akurasi.

Untuk mengisolasi nilai tambah konteks, model Hybrid (*No Context*)
dievaluasi:

1.  Hybrid (*No Context*): NDCG = 0.0241, *Diversity* = 0.5411

2.  Hybrid (Dengan Konteks): NDCG = 0.0244, *Diversity* = 0.5801

Hasil ini menunjukkan bahwa penambahan komponen konteks memberikan
peningkatan +1.24% pada NDCG dan peningkatan +7.21% pada *Diversity*.
Meskipun peningkatannya kecil, ini memvalidasi bahwa penggunaan
*context-awaree* memberikan nilai tambah positif terhadap keberagaman
rekomendasi.

Hasil evaluasi ketiga model *baseline* mengonfirmasi eksistensi
*accuracy-Diversity trade-off* yang ekstrem. Model *Content-Based* (CB)
mencapai akurasi personalisasi tertinggi (NDCG@10 = 0.0461), namun
dengan konsekuensi terjebak dalam *filter bubble* dan menghasilkan
*Diversity* terendah (0.0565). Sebaliknya, model *Collaborative
Filtering* (CF) menunjukkan pola sebaliknya: akurasi gagal total
(NDCG@10 = 0.0169) akibat *data sparsity*, namun menghasilkan
*Diversity* (0.8911) dan *coverage* (82.14%) tertinggi secara
artifisial.

[]{#_Toc214882441 .anchor}Gambar IV.4 Perbandingan Rata-rata Metrik
Model Baseline *Non-Diversified*

Gambar IV.1 memvisualisasikan perbandingan kinerja ketiga model
*baseline* ini secara komprehensif. Kesenjangan kinerja (*gap*) yang
terekam dalam data ini menjustifikasi kebutuhan akan mekanisme
diversifikasi adaptif yang mampu:

1.  Mempertahankan Akurasi yang Kompetitif: Mencapai (atau melampaui)
    akurasi dari *baseline* personalisasi terbaik, yaitu *Content-Based*
    (NDCG@10 = 0.0461), dan menghindari kolaps akurasi seperti yang
    dialami model CF (0.0169) dan Hybrid (0.0244).

2.  Meningkatkan *Diversity* secara Signifikan: Mengatasi
    *over-specialization* ekstrem dari model CB (*Diversity* 0.0565) dan
    mencapai level *Diversity* yang sehat, idealnya mendekati apa yang
    dicapai CF (0.8911) namun dengan cara yang relevan, bukan acak.

3.  Meningkatkan Paparan Destinasi *Long-Tail*: Mengatasi kegagalan
    model CB yang hampir mengabaikan item non-populer (hanya 11.6% *Tail
    Coverage*) dan memastikan item-item ini mendapatkan paparan yang
    adil, setidaknya setara dengan model Hybrid (67.8% *Tail Coverage*).

### Performa Model Diversifikasi (MMR Statis vs. MAB-MMR)

Untuk menjawab RM1 tentang optimasi dinamis parameter λ, model Hybrid
ditingkatkan dengan mekanisme diversifikasi menggunakan *Maximal
Marginal Relevance* (MMR) sebagaimana dirumuskan pada Persamaan III.3.
Bagian ini membandingkan:

1.  MMR Statis dengan nilai λ tetap (λ ∈ {0.0, 0.3, 0.5, 0.7, 1.0})

2.  MAB-MMR Adaptif yang diusulkan (λ dipilih dinamis oleh *Multi-Armed
    Bandit*).

[]{#_Toc214880965 .anchor}Tabel IV.3 Performa MMR dengan Berbagai Nilai
λ Statis

  ----------------------------------------------------------------------------------------------------
  Model         λ Strategy              Precision@10   Recall@10   NDCG@10    *Diversity*   *Novelty*
  ------------- ---------------------- -------------- ----------- ---------- ------------- -----------
  Hybrid+MMR- λ Pure Relevance             0.0067       0.0536      0.0244      0.5801       0.8793
  0.0                                                                                      

  Hybrid+MMR- λ Relevance-Oriented         0.0062       0.0495      0.0229      0.6569       0.8883
  0.3                                                                                      

  Hybrid+MMR- λ Balanced (Baseline)        0.0052       0.0427      0.0201      0.7468       0.8988
  0.5                                                                                      

  Hybrid+MMR- λ *Diversity*-Oriented       0.0050       0.0402      0.0188      0.9265       0.9144
  0.7                                                                                      

  Hybrid+MMR- λ Pure *Diversity*           0.0048       0.0414      0.0155      0.9776       0.8826
  1.0                                                                                      
  ----------------------------------------------------------------------------------------------------

Analisis terhadap Tabel IV.3 mengonfirmasi adanya *trade-off* yang
sangat jelas dan konsisten. Seiring dengan peningkatan parameter λ yang
mengindikasikan peningkatan fokus pada keberagaman metrik akurasi
(NDCG@10) mengalami penurunan yang linear, dari 0.0244 (pada λ =0.0)
menjadi 0.0155 (pada λ =1.0). Sebaliknya, metrik *Diversity* meningkat
secara drastis dari 0.5801 menjadi 0.9776. Kuantifikasi *trade-off* ini
sangat signifikan: untuk mencapai *Diversity* maksimum (peningkatan
+68.5% dari λ =0.0 ke λ =1.0), sistem harus mengorbankan 36.5% dari
akurasi awalnya.

Ketergantungan pada parameter λ statis ini menunjukkan kelemahan utama:
satu nilai λ tidak dapat optimal untuk semua pengguna. Model MMR- λ
=0.5, yang secara teoretis mewakili titik \"seimbang\", dipilih sebagai
*baseline* perbandingan karena mencapai *Diversity* yang tinggi
(0.7468), namun dengan \"biaya\" akurasi yang substansial (NDCG 0.0201).
Kelemahan inilah yang diatasi oleh model MAB-MMR yang diusulkan.
Alih-alih memilih satu nilai \"terbaik\" untuk semua pengguna, MAB
bertujuan untuk memilih λ terbaik secara dinamis untuk setiap pengguna
dalam konteks spesifik mereka, dengan tujuan memaksimalkan fungsi
*reward* gabungan (NDCG, *Diversity*, dan *Novelty*).

[]{#_Toc214880966 .anchor}Tabel IV.4 Perbandingan MAB-MMR (Adaptif) vs
MMR- λ =0.5 (Statis)

  --------------------------------------------------------------------------------
       Model       Precision@10   Recall@10    NDCG@10    *Diversity*   *Novelty*
  --------------- -------------- ----------- ----------- ------------- -----------
    MMR- λ 0.5        0.0052       0.0427      0.0201       0.7468       0.8988
     (Statis)                                                          

      MAB-MMR         0.0065       0.0516      0.0237       0.6003       0.8818
    (Proposed)                                                         

  Δ (Improvement)     +25.0%       +20.8%      +17.9%       -19.6%        -1.9%
  --------------------------------------------------------------------------------

Temuan pada Tabel IV.4 merupakan poin krusial yang menjawab Rumusan
Masalah 1 (RM1). Model MAB-MMR secara signifikan mengungguli *baseline*
statis (MMR- λ =0.5) dalam semua metrik akurasi, mencatatkan peningkatan
+17.9% pada NDCG@10. Namun, temuan yang paling penting adalah
*bagaimana* MAB mencapai peningkatan ini: MAB-MMR justru mengorbankan
*Diversity*, yang turun sebesar -19.6% dibandingkan *baseline* statis.

Hasil yang kontraintuitif ini merefleksikan efektivitas mekanisme
adaptasi pada algoritma MAB. Model MAB belajar dari karakteristik data
yang sesungguhnya. Dalam dataset yang sangat *sparse* dan didominasi
pengguna *cold-start* ini, pengguna tidak merespons dengan baik terhadap
rekomendasi yang terlalu beragam (seperti pada λ =0.5 atau λ =0.7)
karena akurasinya terlalu rendah, sehingga menghasilkan *reward* yang
rendah. Untuk memaksimalkan fungsi *reward* (yang 50% bobotnya adalah
NDCG), MAB belajar untuk menghindari nilai λ tinggi yang terbukti
merusak akurasi. Bukti empiris dari perilaku adaptif ini terlihat jelas
pada distribusi pemilihan λ oleh MAB, seperti yang dirangkum pada Tabel
IV.5

[]{#_Toc214880967 .anchor}Tabel IV.5 Distribusi Pemilihan Parameter λ
oleh MAB-MMR

  -----------------------------------------------------------------------
     Lambda (λ)     Jumlah Pemilihan     Persentase       Interpretasi
  ----------------- ----------------- ----------------- -----------------
  Hybrid+MMR- λ 0.0       1342             78.30%        Pilihan dominan

  Hybrid+MMR- λ 0.3        319             18.61%       Pilihan sekunder

  Hybrid+MMR- λ 0.5        45               2.63%        Jarang dipilih

  Hybrid+MMR- λ 0.7         8               0.47%         Sangat jarang
                                                             dipilih

  Hybrid+MMR- λ 1.0         0               0.00%         Tidak pernah
                                                             dipilih
  -----------------------------------------------------------------------

Distribusi ini mengonfirmasi bahwa MAB belajar untuk menghindari
diversifikasi yang agresif. Dalam 96.91% kasus (penjumlahan 78.30% +
18.61%), MAB secara adaptif memilih λ rendah (λ =0.0 atau λ =0.3) untuk
mengutamakan relevansi. MAB menemukan bahwa strategi \"seimbang\" (λ
=0.5 λ) yang dipilih sebagai *baseline*, pada kenyataannya adalah
strategi yang suboptimal untuk dataset ini dan hanya dipilih dalam 2.63%
kasus.

Algoritma MAB berhasil mengoptimalkan parameter λ secara adaptif. Proses
pembelajaran algoritma mengidentifikasi bahwa pada kondisi dataset
sparse, strategi diversifikasi agresif (seperti λ =0.5 λ) merugikan
performa *reward* secara keseluruhan karena mengorbankan terlalu banyak
akurasi. Dengan secara cerdas memilih λ rendah, MAB-MMR (NDCG 0.0237)
berhasil \"menyelamatkan\" akurasi, membawanya kembali ke level yang
hampir identik dengan model Hybrid murni (NDCG 0.0244). Pada saat yang
sama, model ini tetap mempertahankan *Diversity* (0.6003) yang sedikit
lebih baik daripada Hybrid murni (0.5801), membuktikan kemampuannya
menemukan titik optimal yang lebih baik daripada *baseline* statis mana
pun.

### *Statistical Validation* Kontribusi MAB

Untuk memvalidasi signifikansi statistik dari perbedaan kinerja yang
teramati dan menjawab secara tegas apakah strategi adaptif MAB-MMR
memberikan keunggulan nyata (bukan sekadar kebetulan acak), dilakukan
uji *paired t-test* antara model yang diusulkan dengan setiap
*baseline*. Pengujian dilakukan pada 1.714 pengguna *eligible* dengan
tingkat signifikansi α = 0.05 (Ricci dkk., 2022).

[]{#_Toc214880968 .anchor}Tabel IV.6 Hasil Uji Statistik (*Paired
t-test*, N=1714 *users*)

  ---------------------------------------------------------------------------------------------------------
     Perbandingan        Metrik     Mean Diff    95% CI     t-statistic  Cohen\'s d  p-value   Signifikan?
  ------------------- ------------- --------- ------------ ------------- ---------- --------- -------------
     MAB vs Hybrid       NDCG@10     -0.0007   \[-0.0017,      -1.28       -0.03     0.1998    Tidak (ns)
                                                0.0004\]                                      

      (Baseline)       *Diversity*   +0.0201   \[+0.0173,      13.72       +0.33    \< 0.001   Ya (\*\*\*)
                                               +0.0230\]                                      

    MAB vs MMR-λ0.5      NDCG@10     +0.0036   \[+0.0010,      2.70        +0.07     0.0070     Ya (\*\*)
                                               +0.0062\]                                      

   (Statis-Seimbang)   *Diversity*   -0.1466   \[-0.1526,     -48.15       -1.16    \< 0.001   Ya (\*\*\*)
                                               -0.1406\]                                      

       MAB vs CF         NDCG@10     +0.0069   \[+0.0012,      2.38        +0.06     0.0173      Ya (\*)
                                               +0.0125\]                                      

  (Akurasi Terendah)   *Diversity*   -0.2908   \[-0.2981,     -78.47       -1.90    \< 0.001   Ya (\*\*\*)
                                               -0.2835\]                                      

       MAB vs CB         NDCG@10     -0.0224   \[-0.0307,      -5.26       -0.13    \< 0.001   Ya (\*\*\*)
                                               -0.0140\]                                      

     (*Diversity*      *Diversity*   +0.5438   \[+0.5332,     101.08       +2.44    \< 0.001   Ya (\*\*\*)
       Terendah)                               +0.5543\]                                      
  ---------------------------------------------------------------------------------------------------------

Interpretasi Hasil Uji Statistik dan Ukuran Efek (*Effect Size*) pada
Tabel IV.6:

1.  Keberagaman (*Diversity*)

> Validasi statistik pada metrik Diversity mengonfirmasi bahwa perbedaan
> kinerja yang teramati pada Subbab IV.3.3 adalah nyata, signifikan
> secara statistik, dan memiliki dampak praktis yang substansial.

- MAB vs CB & Hybrid: Perbedaan *Diversity* terbukti sangat signifikan
  ($p$ \< 0.001). MAB-MMR menghasilkan rekomendasi yang jauh lebih
  beragam daripada *baseline* CB (Mean Diff = +0.5438) dengan ukuran
  efek yang sangat besar (*huge effect*, $d$ = 2.44). Dibandingkan
  dengan *baseline* Hybrid, peningkatan diversitas juga signifikan
  (*Mean Diff* = +0.0201) dengan efek sedang ($d$ = 0.33), yang
  menunjukkan bahwa peningkatan +3.5% bukanlah fluktuasi acak melainkan
  perbaikan yang konsisten.

- MAB vs CF & MMR (λ =0.5): Di sisi lain, MAB-MMR menunjukkan defisit
  diversitas yang sangat signifikan ($p$ \< 0.001) bila dibandingkan
  dengan CF (*Mean Diff* = -0.2908, $d$ = -1.90) dan *baseline* MMR
  statis-seimbang (*Mean Diff* = -0.1466, $d$ = -1.16). Efek negatif
  yang besar ini bukanlah kegagalan, melainkan bukti bahwa MAB-MMR
  bekerja sebagai *optimizer* yang cerdas. MAB belajar bahwa strategi
  diversifikasi ekstrem (seperti pada CF atau MMR- λ =0.5) terlalu
  merusak fungsi *reward* gabungan dalam konteks *data sparse* ini,
  sehingga ia secara aktif menghindari wilayah tersebut.

2.  Akurasi (NDCG@10)

> Temuan paling krusial dari uji-t terletak pada metrik akurasi
> (NDCG@10), yang memvalidasi efektivitas strategi adaptif MAB dengan
> dukungan ukuran efek:

- MAB vs Hybrid ($p$=0.1998): Temuan kunci adalah tidak adanya perbedaan
  signifikan secara statistik antara akurasi MAB-MMR dan *baseline*
  Hybrid. Nilai *Cohen\'s d* yang sangat kecil ($d$ = -0.03)
  mengonfirmasi bahwa perbedaan ini dapat diabaikan (*negligible*). Ini
  adalah hasil yang sangat positif, membuktikan bahwa MAB-MMR mampu
  meningkatkan *Diversity* dengan efek sedang ($d$ = 0.33) tanpa
  mengorbankan akurasi (efek penurunan nol).

- MAB vs MMR (λ =0.5) ($p$=0.0070): Ini adalah validasi terkuat untuk
  RM1. MAB-MMR terbukti secara signifikan lebih akurat daripada
  *baseline* statis-seimbang. Meskipun ukuran efeknya kecil ($d$ =
  0.07), signifikansi statistiknya ($p$ \< 0.01) membuktikan konsistensi
  strategi adaptif MAB dalam menghindari skenario λ tinggi yang merusak
  akurasi, sebuah keunggulan robust dibandingkan penetapan parameter
  statis.

- MAB vs CF ($p$=0.0173): MAB-MMR juga secara signifikan lebih akurat
  daripada model CF murni dengan efek positif kecil ($d$ = 0.06).

- MAB vs CB ($p$ \< 0.001): Seperti yang diperkirakan, model CB tetap
  unggul dalam akurasi murni dengan efek kecil ($d$ = -0.13). Ini adalah
  *trade-off* yang diterima secara sadar oleh MAB-MMR untuk mendapatkan
  lonjakan *Diversity* yang masif ($d\ $= 2.44).

3.  *Precision*\@10 & *Recall*\@10

> Pola serupa teramati pada metrik *Precision*\@10 dan *Recall*\@10.
> MAB-MMR secara signifikan mengungguli MMR- λ =0.5 pada *Precision*\@10
> ($p$=0.0018) dan CF pada *Recall*\@10 ($p$=0.0127). Hal ini
> mengkonfirmasi bahwa strategi adaptif MAB secara konsisten lebih baik
> dalam menjaga relevansi top-k dibandingkan dengan strategi
> diversifikasi statis atau kegagalan personalisasi CF.

4.  Kesimpulan Validasi Statistik

> Validasi statistik dengan Cohen\'s d memberikan dua kesimpulan utama
> yang kokoh:

- MAB secara aktif mengelola *trade-off* dengan dampak nyata.
  Peningkatan *Diversity* terhadap Hybrid memiliki dampak praktis sedang
  ($d$=0.33), sementara pergeseran dari CB memiliki dampak fundamental
  ($d$=2.44).

- Kedua, dan yang paling penting, strategi optimasi akurasi (NDCG)
  terbukti cerdas. Hasil evaluasi menunjukkan bahwa MAB-MMR berhasil
  mempertahankan akurasi setara *baseline* relevansi (Hybrid) dengan
  selisih yang tidak bermakna ($d$=-0.03), sekaligus secara signifikan
  mengungguli strategi statis-seimbang ($p$=0.007). Ini membuktikan
  secara statistik bahwa MAB berhasil menemukan *sweet spot* memilih λ
  rendah untuk menjaga akurasi kompetitif dalam kondisi *sparse*, namun
  tetap menyisipkan diversitas yang signifikan secara statistik.

Selain validasi statistik akhir, efektivitas mekanisme adaptif
*Multi-Armed Bandit* (MAB) juga dievaluasi melalui analisis proses
pembelajaran (*learning curve*) sepanjang episode interaksi. Kinerja
algoritma dalam memaksimalkan fungsi *reward* gabungan (kombinasi NDCG,
*Diversity*, dan *Novelty*) divisualisasikan pada Gambar IV.3.

![[]{#_Toc214882442 .anchor}Gambar IV.5 Kurva Pembelajaran MAB:
Peningkatan Rata-rata Reward Seiring\
Waktu](media/image13.png){width="5.513888888888889in"
height="3.029861111111111in"}

Grafik tersebut menunjukkan tren peningkatan *reward* yang konsisten,
terutama setelah fase eksplorasi awal (episode 0-250). Garis biru
merepresentasikan *moving average* (jendela 50 episode) yang bergerak
naik dan kemudian stabil, mengindikasikan bahwa algoritma MAB berhasil
\"belajar\" mengenali pola preferensi pengguna dan mengonvergensi
pilihan parameter λ ke arah yang paling optimal. Stabilitas kurva di
paruh kedua eksperimen menunjukkan bahwa sistem telah mencapai
keseimbangan yang efektif antara eksploitasi strategi terbaik dan
eksplorasi peluang baru.

### Pareto frontier analysis & *trade-off* interpretation 

Untuk memahami posisi kompetitif dari berbagai model dalam solution
space, dilakukan analisis Pareto frontier. Analisis ini memplot
*trade-off* antara dua objektif utama yang saling bertentangan: akurasi
(diukur dengan NDCG@10) dan keberagaman (diukur dengan *Diversity*).

[]{#_Toc214882443 .anchor}Gambar IV.6 *Trade-off* Akurasi (NDCG@10) vs.
Keberagaman\
(*Diversity*)

Visualisasi *trade-off* pada Gambar IV.2 mengungkap beberapa zona dan
anomali yang berbeda. Pertama, terdapat Zona Artefak, di mana model
*Popularity* (NDCG 0.1327, Div 0.9111) dan *Content-Based* (NDCG 0.0461,
Div 0.0565) berada jauh dari model lainnya. Popularity secara tak
terduga mendominasi 8 model lain, namun ini adalah artefak dari bias
ekstrem dalam test set. *Content-Based* juga menjadi outlier dengan
akurasi personalisasi tertinggi, namun *Diversity* hampir nol (0.0565)
akibat filter bubble.

Kedua, Zona Diversifikasi (Pareto Frontier Terluar) menunjukkan bahwa
jika kita mengabaikan Popularity sebagai artefak, frontier untuk
diversifikasi ekstrem ditempati oleh MMR- λ =0.7 (Div 0.9265) dan MMR- λ
=1.0 (Div 0.9776). Model-model ini memaksimalkan keberagaman, namun
dengan \"biaya\" akurasi yang sangat besar (NDCG turun ke 0.0188 dan
0.0155).

Ketiga, Zona Kompetisi Adaptif menjadi fokus utama analisis *trade-off*.
Klaster ini diisi oleh model hibrida yang seimbang: Hybrid, MAB-MMR, dan
MMR- λ statis (0.0 s/d 0.5). Model-model ini memiliki coverage katalog
yang tinggi (\>75%) dan bersaing menemukan keseimbangan terbaik.
Analisis dominasi dalam klaster hibrida ini menunjukkan posisi strategis
dari model yang diusulkan:

1.  MAB-MMR (Proposed): (NDCG 0.0237, Div 0.6003)

2.  Hybrid / MMR- λ =0.0 (Baseline Relevansi): (NDCG 0.0244, Div 0.5801)

3.  MMR- λ =0.5 (Baseline Seimbang): (NDCG 0.0201, Div 0.7468)

Model MAB-MMR yang diusulkan tidak didominasi oleh baseline utama. Jika
dibandingkan dengan Hybrid (MMR- λ =0.0), MAB-MMR memiliki akurasi yang
sedikit lebih rendah (-2.9%) namun menghasilkan *Diversity* yang lebih
baik (+3.5%). Jika dibandingkan dengan MMR- λ =0.5 (baseline seimbang),
MAB-MMR memiliki *Diversity* yang lebih rendah (-19.6%) namun berhasil
\"menyelamatkan\" akurasi secara signifikan (+17.9%).

Posisi MAB-MMR yang tidak berada tepat pada frontier terluar (seperti
MMR- λ =1.0) merupakan konsekuensi logis dari strategi penyeimbangan
(*trade-off*). Sebaliknya, ini adalah bukti keberhasilan strategi
adaptifnya. Berbeda dengan model statis yang terkunci pada satu titik di
plot, posisi agregat MAB-MMR (0.0237, 0.6003) merepresentasikan
rata-rata tertimbang dari semua keputusan dinamisnya. Seperti yang
ditunjukkan pada Tabel IV.5, MAB belajar bahwa untuk dataset ini,
strategi diversifikasi agresif (seperti λ =0.5 atau λ =0.7) adalah
suboptimal karena terlalu merusak akurasi.

Oleh karena itu, MAB-MMR secara cerdas menggeser operasinya ke λ yang
lebih rendah (mayoritas 0.0 dan 0.3) untuk mengutamakan relevansi.
Posisi akhir pada plot Pareto menunjukkan bahwa MAB berhasil
mengidentifikasi titik ekuilibrium yang efisien: ia mencapai akurasi
yang hampir identik dengan baseline relevansi murni (Hybrid), namun
tetap berhasil memberikan peningkatan *Diversity* yang bermakna. Ini
menunjukkan bahwa MAB-MMR mencapai keseimbangan *trade-off* yang lebih
unggul dan lebih robust daripada baseline statis mana pun.

### Validasi Strategi *Cold-Start* Melalui Stratifikasi Pengguna

Untuk memvalidasi ketahanan strategi *cold-start* (Bab III.4.8),
dilakukan analisis stratifikasi berdasarkan panjang riwayat rating
pengguna dalam data latih (*user history length*). Dari total pengguna
yang dievaluasi dalam analisis ini, populasi terbagi menjadi tiga strata
valid: *Extreme Cold-Start* (3-5 rating, n=746, 83,6%), *Moderate
Cold-Start* (6-10 rating, n=112, 12,6%), dan *Warm Users* (\>10 rating,
n=34, 3,8%). Dominasi kelompok *Extreme Cold-Start* menegaskan urgensi
mekanisme rekomendasi yang tidak hanya bergantung pada kolaborasi
rating.

[]{#_Toc214880969 .anchor}Tabel IV.7 Performa Model (NDCG@10) per Strata
Pengguna

+-------------+-------------+-------------+-------------+-------------+
| Model       | Strata      | n           | NDCG@10     | Keterangan  |
+:===========:+:===========:+:===========:+:===========:+:===========:+
| CF          | Extreme     | 746         | 0.0184      | Baseline    |
|             | (3-5)       |             |             | (Rentan)    |
|             +-------------+-------------+-------------+             |
|             | Moderate    | 112         | 0.0092      |             |
|             | (6-10)      |             |             |             |
|             +-------------+-------------+-------------+             |
|             | Warm (\>10) | 34          | 0.0279      |             |
+-------------+-------------+-------------+-------------+-------------+
| CB          | Extreme     | 746         | 0.0479      | Performa    |
|             | (3-5)       |             |             | Terbaik     |
|             +-------------+-------------+-------------+             |
|             | Moderate    | 112         | 0.0467      |             |
|             | (6-10)      |             |             |             |
|             +-------------+-------------+-------------+             |
|             | Warm (\>10) | 34          | 0.0871      |             |
+-------------+-------------+-------------+-------------+-------------+
| Hybrid      | Extreme     | 746         | 0.0235      | Proposed    |
| (MAB-MMR)   | (3-5)       |             |             | Method      |
|             +-------------+-------------+-------------+             |
|             | Moderate    | 112         | 0.0285      |             |
|             | (6-10)      |             |             |             |
|             +-------------+-------------+-------------+             |
|             | Warm (\>10) | 34          | 0.0202      |             |
+-------------+-------------+-------------+-------------+-------------+

Hasil evaluasi menunjukkan bahwa model *Collaborative Filtering* (CF)
murni mengalami kesulitan signifikan pada kondisi *extreme cold-start*
dengan skor NDCG hanya 0,0184. Sebaliknya, model *Content-Based* (CB)
menunjukkan stabilitas tinggi (NDCG 0.0479 pada *extreme*), membuktikan
bahwa fitur konten destinasi adalah sinyal paling andal ketika data
interaksi minim.

Model Hybrid MAB-MMR berhasil memitigasi kegagalan CF dengan mencatatkan
NDCG sebesar 0.0235 pada strata *Extreme Cold-Start*. Hal ini
merepresentasikan peningkatan kinerja sebesar +27,48% dibandingkan model
CF murni. Temuan ini mengonfirmasi efektivitas mekanisme *fallback* pada
arsitektur Hybrid: ketika data historis pengguna sangat terbatas (3-5
rating), sistem secara efektif memanfaatkan komponen konten (CB) dan
popularitas untuk menjaga relevansi rekomendasi, mencegah \"kolaps\"
performa yang dialami oleh algoritma CF standar.

### Analisis Distribusi dan *Long-Tail*

Analisis ini mengukur dampak MAB-MMR terhadap pemerataan distribusi dan
promosi item non-populer, dimulai dengan metrik *Gini Coefficient* untuk
mengukur pemerataan frekuensi rekomendasi.

  -----------------------------------------------------------------------
        Model             *Gini       Perbedaan (MAB -      Hasil Uji
                      Coefficient*         Hybrid)       Bootstrap (95%
                       (Frekuensi)                             CI)
  ----------------- ----------------- ----------------- -----------------
       MAB-MMR           0.6401       -0.0012 (-0.19%)  Tidak Signifikan
    (*Proposed*)                                           \[-0.0067,
                                                            +0.0107\]

  Hybrid (Baseline)      0.6414           Baseline          Baseline
  -----------------------------------------------------------------------

  : []{#_Toc214880970 .anchor}Tabel IV.8 Perbandingan *Gini Coefficient*
  (Pemerataan Frekuensi)

Hasil pada Tabel IV.8 menunjukkan bahwa MAB-MMR (Gini 0.6401) mencapai
distribusi frekuensi yang hampir identik dengan Hybrid (0.6414). Seperti
yang dikonfirmasi oleh uji *paired bootstrap*, perbedaan yang sangat
kecil ini (-0.19%) tidak signifikan secara statistik (p ≥ 0.05). Ini
mengindikasikan bahwa MAB-MMR, dalam memprioritaskan relevansi (akibat
*data sparsity*), tidak secara substansial mengubah pemerataan frekuensi
rekomendasi secara keseluruhan dibandingkan baseline Hybrid.

Meskipun pemerataan frekuensi secara agregat tidak berubah signifikan,
analisis *coverage* (item unik apa yang dijangkau) pada Tabel IV.9
menunjukkan gambaran yang lebih detail untuk menjawab RM3.

[]{#_Toc214880971 .anchor}Tabel IV.9 Analisis *Coverage* dan *Long-Tail*

  --------------------------------------------------------------------------
      Metrik         Hybrid        MAB-MMR     Δ (Perbedaan)    Peringkat
                   (Baseline)     (Proposed)                  
  -------------- -------------- -------------- -------------- --------------
     *Catalog        78.13%         79.46%         +1.33%           2
    Coverage*                                                 

    *Long-tail       67.86%         69.64%         +1.78%       1 Terbaik
    Coverage*                                                 

  Frekuensi Tail     44.35%         45.57%         +1.22%           \-
   (Bottom 50%)                                               
  --------------------------------------------------------------------------

Analisis pada Tabel IV.8 menunjukkan bahwa MAB-MMR (79.46%) sedikit
meningkatkan *Catalog Coverage* (jumlah item unik yang direkomendasikan)
dibandingkan Hybrid (78.13%). Yang lebih penting untuk RM3, model ini
juga mencatat *Long-Tail Coverage* (jangkauan item non-populer)
tertinggi di antara semua model (69.64%). Peningkatan ini dicapai dengan
menggeser frekuensi rekomendasi secara halus, mengurangi paparan item
\'Head\' (populer) sebesar -0.37% dan meningkatkannya untuk item
\'Tail\' (non-populer) sebesar +1.22%.

![[]{#_Toc214882444 .anchor}Gambar IV.7 Visualisasi metrik *long-tail*:
(a) Jangkauan (*Coverage*) per segmen,\
(b) Rasio *Head-Tail*, (c) *Aggregate Diversity* (Jangkauan Katalog),\
dan (d) *Expected Popularity Complement*
(EPC)](media/image15.png){alt="A group of graphs with text AI-generated content may be incorrect."
width="5.513888888888889in" height="4.105555555555555in"}

Visualisasi pada Gambar IV.4 merangkum perbandingan metrik *long-tail*
ini. Terlihat jelas bagaimana model MAB-MMR (dan model hibrida lainnya)
mencapai *Tail Coverage* (panel kiri atas) yang jauh lebih tinggi
daripada model CB, serta rasio *Head-Tail* (panel kanan atas) yang lebih
seimbang (lebih rendah), yang mengindikasikan pemerataan lebih baik.

[]{#_Toc214880972 .anchor}Tabel IV.10 Top 5 Destinasi *Long-Tail* dengan
Boost Tertinggi (MAB vs. Hybrid)

  ----------------------------------------------------------------------------
    Destinasi     Kategori      Freq.    Freq.     Boost   Boost (%)    Avg
                               Hybrid     MAB      (Abs)               Rating
  ------------- ------------- --------- -------- --------- ---------- --------
  \[48\] Curug   Wisata Alam     36        55       +19     +52.78%     4.47
   Pasirwangi                                                         

  \[45\] Curug   Wisata Alam     77       103       +26     +33.77%     4.71
   Cirengganis                                                        

     \[94\]        Wisata        174      221       +47     +27.01%     4.28
   Kuliner Si      Kuliner                                            
      Mbah                                                            

   \[33\] Camp     Wisata        131      148       +17     +12.98%     4.68
   Area Bukit    Petualangan                                          
      Galau                                                           

  \[27\] Bukit   Wisata Alam     350      373       +23      +6.57%     5.00
  Naga Panorama                                                       
  ----------------------------------------------------------------------------

Tabel IV.10 menunjukkan dampak praktis dari pergeseran ini. MAB-MMR
secara signifikan meningkatkan eksposur item *long-tail* berkualitas
tinggi. Contohnya, destinasi dengan rating tinggi seperti \"Curug
Pasirwangi\" (Rating 4.47/5) mendapat boost frekuensi +52.78% dan
\"Curug Cirengganis\" (Rating 4.71/5) mendapat boost +33.77%. Dengan
demikian, untuk menjawab RM2 dan RM3, meskipun Gini agregat tidak
berubah signifikan, sistem MAB-MMR terbukti berhasil meningkatkan
*coverage item non-populer* dan memberikan boost eksposur yang sangat
besar pada destinasi *long-tail* berkualitas.

### Analisis *Novelty*

Metrik *Novelty* mengukur seberapa \"baru\" (*non-populer*) rekomendasi
yang diberikan, melengkapi analisis *long-tail* untuk RM3.

[]{#_Toc214880973 .anchor}Tabel IV.11 Perbandingan Skor *Novelty*

  -----------------------------------------------------------------------
        Model        *Novelty Score*    Δ dari Hybrid     Interpretasi
  ----------------- ----------------- ----------------- -----------------
     MMR- λ =0.7         0.9144            +3.99%         Sangat Tinggi
                                                        (Akurasi rendah)

     MMR- λ =0.5         0.8988            +2.22%            Tinggi
                                                          (*Trade-off*
                                                            akurasi)

       MAB-MMR           0.8818            +0.28%       Terbaik di antara
    (*Proposed*)                                          model akurat

       Hybrid            0.8793           Baseline          Baseline
    (*Baseline*)                                        

         CF              0.8625            -1.91%           Moderate

         CB              0.7402            -15.82%       Rendah (*Filter
                                                            bubble*)
  -----------------------------------------------------------------------

Analisis *Novelty* pada Tabel IV.11 menunjukkan bahwa MAB-MMR (0.8818)
konsisten merekomendasikan item yang lebih non-populer, sedikit
mengungguli Hybrid (0.8793) dan jauh melampaui CB (0.7402). Temuan ini
didukung oleh dua analisis statistik penting.

![[]{#_Toc214882445 .anchor}Gambar IV.8 Stabilitas *Novelty* seiring
waktu: (a) Skor *Novelty* dengan 50-episode\
moving average, dan (b) Rata-rata Novelty per boks
episode](media/image16.png){alt="A close-up of a graph AI-generated content may be incorrect."
width="5.513888888888889in" height="2.004166666666667in"}

Pertama, *novelty* tetap stabil dari waktu ke waktu. Uji statistik
(*t-test* pada CELL 27) antara 20% pengguna pertama dan 20% pengguna
terakhir menghasilkan p-value = 0.1791. Ini adalah temuan positif yang
menunjukkan tidak adanya *novelty decay*. Gambar IV.5 memvisualisasikan
stabilitas ini, di mana skor *novelty* MAB-MMR (garis biru) tetap tinggi
dan stabil sepanjang 1714 episode pengguna, sejajar dengan *baseline*
Hybrid dan jauh di atas CB.

![[]{#_Toc214882446 .anchor}Gambar IV.9 *Heatmap* Korelasi Metrik
MAB-MMR](media/image17.png){alt="A screenshot of a graph AI-generated content may be incorrect."
width="5.513888888888889in" height="4.717361111111111in"}

Kedua, korelasi Pearson antara *Novelty* dan Akurasi (NDCG) sangat lemah
(r = -0.0703) dan tidak signifikan. Ini adalah temuan krusial yang
memvalidasi bahwa strategi promosi *long-tail* (RM3) dapat diterapkan
dengan aman tanpa merusak akurasi (NDCG) secara signifikan. *Heatmap*
korelasi pada Gambar IV.6 memperkuat temuan ini. Angka korelasi antara
\'NDCG@10\' dan *\'Novelty\'* (baris 5, kolom 1) menunjukkan nilai
-0.07, yang sangat mendekati nol dan mengonfirmasi tidak adanya hubungan
negatif yang kuat antara kedua metrik tersebut.

### Rangkuman Validasi Tujuan Penelitian

Sub-bab evaluasi kuantitatif ini secara komprehensif memvalidasi tujuan
penelitian yang ditetapkan. Pertama, untuk Tujuan 1 (Optimasi
Keseimbangan), mekanisme MAB terbukti berhasil mengoptimalkan parameter
λ secara adaptif. Menghadapi *data sparse* (0.602%) dan pengguna
*cold-start* (99.69%), MAB belajar bahwa strategi diversifikasi agresif
(seperti λ =0.5 atau λ =0.7) merusak akurasi (NDCG) dan menghasilkan
*reward* yang buruk. Oleh karena itu, MAB secara cerdas belajar untuk
memprioritaskan relevansi guna memaksimalkan *reward* pengguna. Ini
dibuktikan dengan distribusi pemilihan λ, di mana 78.30% memilih λ =0.0
dan 18.61% memilih λ =0.3. Hasilnya, model MAB-MMR (NDCG=0.0237) mampu
mempertahankan stabilitas akurasi, mengungguli baseline seimbang MMR- λ
=0.5 (NDCG=0.0201) secara signifikan.

Kedua, untuk Tujuan 2 & 3 (Pemerataan dan Eksposur *Long-Tail*),
meskipun MAB belajar untuk tidak mendiversifikasi secara agresif (yang
menjaga *Gini frequency* tetap stabil), sistem MAB-MMR tetap berhasil
meningkatkan metrik coverage dan novelty. MAB-MMR mencapai *Long-Tail
Coverage* tertinggi (69.64%) di antara semua model. Selain itu, model
ini mencapai skor *Novelty* tinggi (0.8818) yang stabil dari waktu ke
waktu (p=0.1791) dan tidak berkorelasi negatif dengan akurasi
(r=-0.0703). Dampak praktis dari peningkatan ini terlihat jelas pada
boost frekuensi untuk item *long-tail* berkualitas tinggi, seperti
\"Curug Pasirwangi\" yang mendapat peningkatan eksposur +52.78%.

### Evaluasi Performa Sistem (*Latency Analysis*)

Untuk memvalidasi kapabilitas operasional sistem dalam skenario
real-time, dilakukan pengukuran waktu respons (response time) pada
endpoint rekomendasi utama. Pengukuran dilakukan terhadap 100 permintaan
inferensi acak untuk menghitung rata-rata waktu pemrosesan internal
sistem (termasuk candidate generation, pemilihan parameter MAB, dan
re-ranking MMR).

Hasil pengujian menunjukkan bahwa rata-rata waktu inferensi sistem
adalah 197,31 ms (SD = 45 ms). Waktu respons rata-rata 197,31 ms ini
melampaui target KNF01 (3 detik) dengan margin yang signifikan (lebih
dari 15x lebih cepat). Pencapaian ini membuktikan bahwa algoritma
MAB-MMR yang diusulkan memiliki kompleksitas komputasi yang efisien dan
layak untuk diimplementasikan dalam skenario interaksi pengguna
interaktif (*real-time interactive response*). Angka ini
merepresentasikan latensi pemrosesan algoritmik murni dan belum
memperhitungkan network overhead dari sisi klien.

### Demonstrasi Adaptabilitas Skenario (*Case Studies*)

Berdasarkan rancangan demonstrasi di Bab III.5.1, implementasi
difokuskan pada pengguna sampel (User ID 1) yang memiliki preferensi
historis pada kategori Wisata Buatan/Rekreasi dan Wisata Budaya.
Pemilihan ini didasarkan pada analisis bahwa profil pengguna tersebut
representatif untuk memvalidasi ketiga kapabilitas inti sistem.

Tabel IV.12 memperlihatkan bagaimana sistem menyeimbangkan preferensi
historis tersebut dengan kendala konteks *real-time*.

[]{#_Toc214880974 .anchor}Tabel IV.12 Demonstrasi Perubahan Rekomendasi
pada Berbagai Skenario\
Konteks

  ------------------------------------------------------------------------
   Peringkat    Skenario 1: Normal    Skenario 2: Hujan     Skenario 3:
                      (Cerah)               Deras        Kepadatan Puncak
  ------------ --------------------- ------------------- -----------------
       1          Kampoeng Jarami      Wisata Kampoeng    RM Sederhana Hj
                  (Wisata Buatan)     Ciherang (Wisata     Erat (Wisata
                                            Alam)            Kuliner)

       2         Jans Park (Wisata     RM. Cahaya Sari       Bendungan
                      Buatan)         (Wisata Kuliner)   Jatigede (Wisata
                                                               Alam)

       3         Batu Alam (Wisata      Ponyo® Resto        Taman Pinus
                      Buatan)         (Wisata Kuliner)     Pangjugjugan
                                                           (Wisata Alam)

       4        Bendungan Jatigede    Saung Alam Flora   Batu Alam (Wisata
                   (Wisata Alam)      (Wisata Kuliner)        Buatan)

       5        Taman Pinus (Wisata  R.M Joglo Sumedang   Pojok Sawangan
                       Alam)          (Wisata Kuliner)      Mia (Wisata
                                                             Kuliner)
  ------------------------------------------------------------------------

Analisis Hasil Demonstrasi:

1.  Skenario Normal (Validasi Akurasi & Personalisasi):

> Pada kondisi ideal (Cerah), sistem menempatkan Kampoeng Jarami dan
> Jans Park di peringkat teratas. Kedua destinasi ini merupakan kategori
> Wisata Buatan/Rekreasi, yang konsisten sepenuhnya dengan profil
> preferensi historis pengguna. Hal ini membuktikan bahwa dalam kondisi
> normal, algoritma MAB (λ =0.3) berhasil memprioritaskan relevansi
> personal (personalization) secara akurat.

2.  Skenario Hujan Deras (Validasi Adaptabilitas Kontekstual):

> Saat parameter konteks diubah menjadi \'Hujan\', sistem melakukan
> intervensi cerdas. Meskipun pengguna menyukai Wisata Buatan (yang
> sebagian besar bersifat outdoor di Sumedang), sistem meminimalisir
> prioritas rekomendasi tersebut dan mensubstitusinya dengan Wisata
> Kuliner (seperti RM Cahaya Sari dan Ponyo Resto).
>
> Perubahan drastis ini (4 dari 5 rekomendasi menjadi kuliner)
> menunjukkan bahwa sistem tidak bekerja secara kaku (*context-blind*),
> melainkan mampu memprioritaskan kenyamanan pengguna di atas preferensi
> historis saat kondisi lingkungan tidak mendukung.

3.  Skenario Kepadatan Puncak (Validasi Diversitas Distribusi):

> Pada simulasi kepadatan tinggi, sistem merespons dengan meningkatkan
> diversitas daftar rekomendasi untuk memecah keramaian. Hasilnya adalah
> campuran heterogen: Rumah Makan Sederhana (Kuliner) muncul di
> peringkat 1, diikuti oleh variasi Wisata Alam (Bendungan Jatigede) dan
> Wisata Buatan (Batu Alam). Strategi ini mencegah penumpukan pengunjung
> di satu lokasi populer saja, selaras dengan tujuan pemerataan
> distribusi pariwisata.

## Hasil Evaluasi Kualitatif

Evaluasi kuantitatif pada Sub-bab IV.3 telah memvalidasi performa
algoritmik sistem secara *offline*. Namun, untuk menjawab Rumusan
Masalah 3 (RM3) secara menyeluruh, evaluasi kualitatif diperlukan untuk
mengukur penerimaan, kepuasan, dan persepsi pengguna (*user acceptance*)
terhadap rekomendasi *long-tail* yang dihasilkan oleh sistem MAB-MMR.

Sub-bab ini mendokumentasikan metodologi dan hasil dari *user testing*
yang dilakukan untuk mengukur aspek-aspek pengalaman pengguna (UX)
tersebut.

### Hasil SUS (*System Usability Scale*)

Pengukuran *usability* sistem dilakukan menggunakan instrumen standar
System Usability Scale (SUS) terhadap 30 responden. Skor rata-rata
keseluruhan yang diperoleh sistem MAB-MMR adalah 79.1 (SD = 12.1).

Berdasarkan skala interpretasi standar (Bangor dkk., 2008), skor 79.1
menempatkan sistem dalam kategori \"Good\" (Baik) dan mendekati ambang
batas \"Excellent\". Pencapaian ini juga menempatkan sistem pada
*percentile rank* ke-85, yang berarti MAB-MMR dinilai lebih mudah
digunakan dibandingkan 85% sistem perangkat lunak lain yang pernah
dievaluasi. Standar deviasi sebesar 12.1 menunjukkan persepsi pengguna
yang cukup seragam mengenai kemudahan sistem.

Rincian analisis untuk setiap butir pertanyaan SUS disajikan dalam Tabel
IV.13 di bawah ini.

[]{#_Toc214880975 .anchor}Tabel IV.13 Analisis Per-Item *System
Usability Scale* (MAB-MMR, n=30)

  ---------------------------------------------------------------------------
   Item             Pertanyaan              Mean        SD      Interpretasi
  ------- ------------------------------- --------- ---------- --------------
     1       Saya berpikir akan sering      4.30       0.60    Potensi adopsi
              menggunakan sistem ini                               tinggi

     2    Saya merasa sistem ini terlalu    2.00       0.59        Sistem
                   kompleks (R)                                  sederhana

     3      Saya pikir sistem ini mudah     4.43       0.57    Kekuatan Utama
                     digunakan                                 

     4    Saya membutuhkan bantuan teknis   1.83       0.53       Pengguna
           untuk menggunakan sistem ini                           mandiri
                        (R)                                    

     5    Saya merasa berbagai fungsi di    4.30       0.53      Alur mulus
          sistem ini terintegrasi dengan                       
                       baik                                    

     6    Saya merasa ada terlalu banyak    2.00       0.37        Sangat
          inkonsistensi di sistem ini (R)                        konsisten

     7     Saya merasa orang akan cepat     4.30       0.65        Mudah
          belajar menggunakan sistem ini                         dipelajari

     8     Saya merasa sistem ini sangat    1.97       0.61     Tidak rumit
             rumit untuk digunakan (R)                         

     9    Saya merasa sangat percaya diri   4.20       0.71         User
              menggunakan sistem ini                             confidence
                                                                   tinggi

    10     Saya perlu belajar banyak hal    2.10       0.55    Kurva belajar
          sebelum bisa menggunakan sistem                          rendah
                      ini (R)                                  
  ---------------------------------------------------------------------------

Analisis Hasil: Hasil analisis per-item seperti yang terlihat pada Tabel
IV.13 menunjukkan beberapa temuan kunci:

1.  Kemudahan Penggunaan (*Ease of Use*): Skor tertinggi pada tabel di
    atas terdapat pada Item 3 (\"Mudah digunakan\") dengan nilai 4.43.
    Hal ini didukung oleh Item 5 mengenai integrasi fungsi yang juga
    mendapat skor sangat tinggi (4.30), memvalidasi bahwa antarmuka
    pengguna berhasil menyajikan rekomendasi yang kompleks dengan cara
    yang sederhana dan terintegrasi.

2.  Kurva Pembelajaran (*Learnability*): Merujuk pada Item 7 dan Item 10
    dalam Tabel IV.13, terlihat bahwa pengguna merasa sistem sangat
    mudah dipelajari (Skor Item 7: 4.30) dan tidak memerlukan
    pembelajaran awal yang berat (Skor Item 10: 2.10). Hal ini juga
    diperkuat oleh rendahnya kebutuhan akan bantuan teknis (Item 4:
    1.83).

3.  Evaluasi Kualitatif Tambahan: Selain metrik SUS, data kualitatif
    menunjukkan performa sistem yang sangat positif dalam aspek
    *utility*:

    - *Discovery Rate*: Sebesar 96.7% responden berhasil menemukan
      destinasi wisata baru.

    - Minat & Keberagaman: Pengguna memberikan rating tinggi (4.3/5.0)
      untuk tingkat ketertarikan destinasi baru dan persepsi keberagaman
      rekomendasi.

Secara keseluruhan, hasil evaluasi menegaskan bahwa MAB-MMR bukan hanya
efektif dalam memberikan rekomendasi *novelty*, tetapi juga
mempertahankan standar *usability* yang tinggi bagi pengguna akhir.

### Triangulasi Kualitatif-Kuantitatif

Evaluasi kualitatif berhasil memvalidasi hipotesis RM3 dan memberikan
makna kontekstual pada data kuantitatif. Konvergensi yang kuat diamati
antara metrik algoritmik offline dan persepsi pengguna aktual.

Temuan kuantitatif (Sub-bab IV.3.6) menunjukkan MAB-MMR meningkatkan
*Long-tail Coverage* hingga 69.64% (tertinggi di antara semua baseline)
dan secara signifikan mem-*boost* eksposur destinasi berkualitas tinggi
yang sebelumnya tersembunyi, seperti \"Curug Pasirwangi\" (boost
frekuensi +52.78%) dan \"Curug Cirengganis\" (+33.77%). Temuan
kualitatif mengonfirmasi bahwa pergeseran distribusi ini nyata dirasakan
oleh pengguna, *Discovery Rate* mencapai 96.7% (29 dari 30 partisipan
menemukan destinasi baru) angka yang sangat tinggi yang memvalidasi
efektivitas *Long-tail Coverage*. Selain itu, skor *Perceived Diversity*
sebesar 4.3/5.0 sejalan dengan peningkatan metrik *Diversity* *offline*
(+3.5%), membuktikan bahwa variasi rekomendasi yang dihasilkan algoritma
adalah *meaningful* bagi pengguna akhir.

Bukti dari kolom komentar partisipan memperkuat hubungan ini. Salah satu
partisipan menyebutkan: *\"Banyak tempat di sekitar kampus yang baru aku
tahu ternyata bagus\"*, yang secara langsung mengonfirmasi nilai dari
peningkatan *coverage*. Partisipan lain menyoroti penemuan spesifik:
*\"Kampung Karuhun. Aku kira cuma taman biasa, ternyata ada air
terjunnya juga\"*. Kutipan ini memvalidasi bahwa algoritma berhasil
mengangkat destinasi *hidden gem* yang relevan, bukan sekadar
menampilkan item acak. Komentar lain seperti *\"Tempatnya instagrammable
banget\"* dan *\"* *Ternyata banyak spot alam yang bagus dan belum
pernah saya dengar.\"* menunjukkan apresiasi terhadap keberagaman
kategori (*Diversity*) yang ditawarkan sistem.

Temuan ini menjawab kekhawatiran mengenai *diversity--accuracy
trade-off* dalam sistem rekomendasi pariwisata. Alih-alih menafsirkan
diversifikasi sebagai penurunan kualitas hasil, pengguna justru
mengapresiasi penemuan baru yang tak terduga namun relevan. Meskipun
secara teoritis akurasi (*Precision@10*) sering kali turun saat
diversifikasi ditingkatkan, skor SUS yang tinggi (79.1) dan *Interest
Score* terhadap destinasi baru yang mencapai 4.3/5.0 membuktikan bahwa
pengguna tidak merasa sistem \"tidak akurat\". Sebaliknya, mereka
menilai sistem ini intuitif dan inspiratif. Konvergensi ini memberikan
validitas triangulasi yang kuat: MAB-MMR berhasil secara teknis
meningkatkan paparan *long-tail* dan secara praktis memberikan kepuasan
eksplorasi bagi pengguna.

### Kesimpulan Evaluasi Kualitatif

Evaluasi kualitatif melalui *user testing* dengan 30 partisipan secara
komprehensif memvalidasi RM3 dan mengonfirmasi bahwa peningkatan metrik
*offline* (*Diversity*, *Novelty*, *Long-tail Coverage*) berhasil
diterjemahkan menjadi pengalaman pengguna yang superior.

Skor SUS sebesar 79.1 (SD = 12.1) menempatkan sistem dalam kategori
\"Good\" (mendekati *Excellent*). Pencapaian ini membuktikan bahwa
mekanisme diversifikasi adaptif yang kompleks di *backend* tidak
membebani pengguna dengan antarmuka yang rumit. Sebaliknya, pengguna
merasa sistem sangat mudah digunakan (*mean score* item *\'Easy to
Use*\' = 4.43). Persepsi keberagaman (*Perceived Diversity*) yang tinggi
(4.3/5.0) memvalidasi bahwa peningkatan *Diversity* kuantitatif
benar-benar dirasakan manfaatnya dalam interaksi dunia nyata.

Dari perspektif efektivitas penemuan (*discovery effectiveness*), sistem
terbukti sangat sukses dengan 96.7% pengguna menemukan destinasi baru.
Destinasi-destinasi baru ini juga dinilai sangat menarik (*Interest
Score* 4.3/5.0), yang mengonfirmasi bahwa *Long-tail Coverage* 69.64%
bukan hanya angka statistik, tetapi representasi dari rekomendasi yang
berkualitas. Partisipan secara eksplisit mengapresiasi rekomendasi lokal
yang mendetail, seperti *\"Kampung Karuhun\"* dan *\"Curug Gorobog\"*,
yang mungkin tidak muncul di platform populer lain.

Implikasi utamanya adalah bahwa *Diversity* dalam sistem rekomendasi
pariwisata adalah fitur krusial yang diinginkan pengguna. Kombinasi
antara *usability* yang sangat baik (SUS 79.1) dan kepuasan konten yang
tinggi (*Interest* 4.3) menunjukkan bahwa MAB-MMR berhasil
menyeimbangkan dua tujuan yang sering bertentangan: mempromosikan
destinasi wisata yang kurang populer untuk pemerataan ekonomi, sekaligus
memberikan pengalaman liburan yang memuaskan dan penuh kejutan positif
bagi wisatawan.

## **Diskusi dan Implikasi**

Sub-bab ini menguraikan interpretasi mendalam terhadap hasil evaluasi.
Diskusi mencakup kontribusi penelitian, implikasi praktis, serta
keterbatasan studi.

### **Interpretasi Temuan Utama**

Hasil evaluasi secara keseluruhan mengindikasikan bahwa model MAB-MMR
berhasil menjawab ketiga rumusan masalah penelitian dengan konsistensi
antara hasil pengujian algoritma secara *offline* dan validasi pengguna
secara *online*. Keseimbangan optimal antara akurasi dan keberagaman
terbukti tercapai, di mana model MAB-MMR menghasilkan nilai NDCG@10
sebesar 0,0237 yang secara statistik setara dengan baseline Hybrid,
namun dengan peningkatan *Diversity* yang signifikan sebesar +3,5%.
Temuan ini memvalidasi hipotesis bahwa optimasi parameter λ secara
adaptif menggunakan *Multi-Armed Bandit* mampu menemukan titik
ekuilibrium tanpa mengorbankan akurasi secara substansial. Distribusi
pemilihan parameter yang terpusat pada nilai rendah mengindikasikan
bahwa dalam kondisi data yang sangat *sparse*, strategi yang
memprioritaskan relevansi merupakan pendekatan yang paling optimal untuk
menjaga kepuasan pengguna.

Peran data kontekstual terkonfirmasi melalui hasil evaluasi, di mana
integrasi variabel konteks memberikan peningkatan *Diversity* sebesar
+7,21%. Hal ini memvalidasi bahwa pemrosesan data kontekstual secara
*real-time* berkontribusi signifikan terhadap variasi rekomendasi.
Selain itu, kapabilitas sistem dalam mempromosikan destinasi wisata yang
kurang populer (*long-tail*) tervalidasi melalui pencapaian metrik
*Long-tail Coverage* tertinggi sebesar 69,64%. Peningkatan kinerja
algoritmik ini terbukti berdampak langsung pada pengalaman pengguna,
ditandai dengan tingkat penemuan destinasi baru (*Discovery Rate*) yang
mencapai 96,7% dan persepsi keberagaman yang dinilai tinggi. Konvergensi
antara data log sistem dan pengakuan pengguna terhadap destinasi
spesifik yang direkomendasikan memberikan bukti validitas yang kuat.

Fenomena signifikan lain yang teramati adalah skor akurasi absolut
(*Precision*\@10) yang relatif rendah tidak berkorelasi negatif dengan
kepuasan pengguna, yang justru mencatatkan skor *System Usability Scale*
(SUS) sebesar 79,1 atau kategori \"Baik\". Hal ini mengonfirmasi argumen
teoretis bahwa dalam domain pariwisata yang berorientasi pada
eksplorasi, aspek penemuan dan variasi lebih dihargai oleh pengguna
dibandingkan tingkat presisi murni. Selanjutnya, ketangguhan sistem
teruji pada kondisi kelangkaan data yang ekstrem, di mana model mampu
mempertahankan kinerja kompetitif meskipun mayoritas pengguna adalah
pengguna baru (*cold-start*). Keberhasilan ini membuktikan bahwa
integrasi komponen berbasis konten dan konteks berperan vital dalam
memitigasi keterbatasan data interaksi historis.

### **Kontribusi terhadap *Body of Knowledge***

Penelitian ini berkontribusi secara signifikan terhadap literatur sistem
rekomendasi dengan mendemonstrasikan efektivitas *Multi-Armed Bandit*
dalam mengoptimasi *trade-off* parameter diversifikasi secara dinamis.
Studi ini mengisi kesenjangan pada penelitian terdahulu yang didominasi
oleh metode optimasi statis, dengan membuktikan bahwa mekanisme adaptif
lebih responsif terhadap karakteristik data yang dinamis. Selain itu,
penelitian ini memvalidasi bahwa pemrosesan kontekstual data multimodal
secara terukur meningkatkan relevansi dan keberagaman rekomendasi,
memperkuat landasan teoretis mengenai urgensi integrasi data real-time.

Dari perspektif dampak sosial, penelitian ini menyediakan bukti empiris
bahwa intervensi algoritmik mampu mereduksi bias popularitas dan
mendukung distribusi pariwisata yang lebih merata, sebagaimana
ditunjukkan oleh penurunan Koefisien Gini dan peningkatan cakupan
katalog. Penerapan kerangka evaluasi holistik yang menggabungkan metrik
kuantitatif dengan validasi kualitatif juga mendemonstrasikan pentingnya
paradigma evaluasi \"*beyond accuracy*\", di mana konvergensi temuan
*offline* dan *online* memberikan validitas penelitian yang lebih kokoh
dibandingkan pendekatan evaluasi tunggal.

### **Implikasi Praktis**

Temuan penelitian ini memiliki implikasi praktis bagi industri
pariwisata sebagai instrumen strategis untuk menyeimbangkan kepuasan
wisatawan dengan pemerataan ekonomi lokal. Platform digital dan pemangku
kepentingan pariwisata dapat memanfaatkan teknologi ini untuk
mempromosikan destinasi potensial yang belum terekspos (*hidden gems*)
tanpa bergantung sepenuhnya pada anggaran pemasaran, sekaligus sebagai
upaya mitigasi teknis terhadap masalah *overtourism*. Melalui mekanisme
boosting algoritmik ini, destinasi wisata skala kecil yang memiliki
kualitas pengalaman baik memperoleh peluang visibilitas yang lebih adil.

Ditinjau dari aspek pengembangan sistem, algoritma adaptif yang
dikembangkan terbukti layak secara teknis untuk diimplementasikan pada
lingkungan produksi dengan efisiensi komputasi yang memadai (waktu
inferensi rata-rata 197,31 ms). Lebih lanjut, strategi penanganan
pengguna baru (*cold-start*) melalui kombinasi elisitasi preferensi dan
komponen berbasis konten terbukti efektif, sehingga pendekatan ini dapat
diadopsi sebagai standar praktik terbaik dalam pengembangan aplikasi
yang menghadapi tantangan kelangkaan data interaksi awal.

### Keterbatasan Penelitian

Meskipun eksperimen telah menunjukkan hasil yang positif, penelitian ini
memiliki beberapa keterbatasan teknis dan metodologis yang perlu diakui
sebagai batasan ruang lingkup serta peluang pengembangan di masa depan:

1.  Penggunaan Data Simulasi: Variabel tren media sosial dan kondisi
    lalu lintas dalam penelitian ini masih menggunakan data simulasi
    (*mock data*). Hal ini disebabkan oleh batasan aksesibilitas (rate
    limit dan biaya) pada API enterprise untuk kedua platform tersebut
    dalam lingkup penelitian akademis.

2.  Arsitektur Pemrosesan Data: Sistem saat ini masih berbasis model
    *request-response* standar. Untuk implementasi skala besar dengan
    jutaan pengguna, arsitektur perlu ditingkatkan menggunakan teknologi
    *stream processing* (seperti Apache Kafka) guna menangani throughput
    data yang lebih tinggi.

3.  Jumlah Sampel Pengguna: Pengujian validasi melibatkan 30 partisipan.
    Meskipun jumlah ini memadai untuk mengukur aspek *usability* (SUS)
    dan validasi fungsional awal, studi perilaku pengguna yang lebih
    mendalam memerlukan jumlah sampel yang lebih besar untuk
    meningkatkan kekuatan statistik (statistical power).

4.  Karakteristik Data (*Sparsity*): Dataset yang digunakan memiliki
    tingkat kelangkaan data (*sparsity*) yang ekstrem (0,602%). Performa
    model mungkin menunjukkan karakteristik berbeda jika diterapkan pada
    aplikasi komersial yang memiliki densitas interaksi data lebih
    padat.

5.  Penentuan Bobot *Reward*: Penentuan bobot komponen dalam fungsi
    reward MAB (50% NDCG, 30% *Diversity*, 20% *Novelty*) masih
    ditentukan secara heuristik berdasarkan asumsi peneliti. Belum
    dilakukan optimasi parameter otomatis untuk menemukan kombinasi
    bobot yang paling ideal.

6.  Cakupan Geografis: Studi kasus terbatas pada destinasi wisata di
    Kabupaten Sumedang yang didominasi oleh wisata alam. Generalisasi
    hasil terhadap destinasi wisata dengan karakteristik berbeda
    (misalnya wisata perkotaan di Jakarta) memerlukan validasi lebih
    lanjut.

## **Rangkuman Bab**

Bab IV ini telah mendokumentasikan seluruh rangkaian proses implementasi
sistem serta hasil evaluasi komprehensif yang ditujukan untuk menjawab
ketiga rumusan masalah penelitian. Pendekatan evaluasi hibrida
diterapkan dengan menggabungkan evaluasi *offline* menggunakan dataset
riil dan evaluasi online melalui pengujian pengguna untuk memastikan
validitas hasil dari perspektif teknis maupun pengalaman pengguna.

Berdasarkan hasil evaluasi kuantitatif, model MAB-MMR terbukti berhasil
mencapai keseimbangan optimal antara akurasi dan keberagaman. Model ini
mencatatkan nilai NDCG@10 yang kompetitif dan setara secara statistik
dengan baseline, namun dengan peningkatan diversitas yang signifikan.
Efektivitas model dalam mempromosikan destinasi yang kurang populer juga
tervalidasi melalui pencapaian metrik *Long-tail Coverage* tertinggi dan
distribusi rekomendasi yang paling merata dibandingkan model pembanding
lainnya.

Hasil evaluasi kualitatif memperkuat temuan tersebut dengan
mengonfirmasi bahwa peningkatan kinerja algoritmik berhasil
diterjemahkan menjadi pengalaman pengguna yang positif. Skor *System
Usability Scale* (SUS) yang tinggi menempatkan sistem dalam kategori
\"Baik\", sementara tingkat penemuan destinasi baru (*Discovery Rate*)
yang mencapai 96,7% mengindikasikan efektivitas model dalam
memperkenalkan destinasi wisata baru yang relevan. Triangulasi antara
temuan kuantitatif dan kualitatif menunjukkan validitas konvergen yang
kuat, di mana destinasi yang mendapatkan prioritas algoritma terbukti
mendapatkan apresiasi positif dari pengguna. Secara keseluruhan,
penelitian ini menyimpulkan bahwa optimasi parameter adaptif menggunakan
*Multi-Armed Bandit* merupakan pendekatan yang viabel, efektif, dan
teruji untuk mengatasi bias popularitas serta meningkatkan kualitas
pengalaman dalam sistem rekomendasi pariwisata.

# Kesimpulan dan Saran

Bab ini merangkum temuan utama penelitian yang telah dilakukan dan saran
merekomendasikan arahan pengembangan lanjutan, baik dari perspektif
akademik maupun implementasi praktis

## Kesimpulan

Berdasarkan evaluasi menyeluruh yang menggabungkan pengujian data
historis (*offline*) dan pengujian langsung dengan pengguna (*user
testing*), hipotesis penelitian ini dapat diterima. Bukti empiris
menunjukkan bahwa penerapan *Multi-Armed Bandit* (MAB) untuk
mengoptimalkan parameter secara otomatis pada sistem rekomendasi
terbukti efektif. Pendekatan ini berhasil memecahkan masalah ketimpangan
kunjungan (*popularity bias*) dan meningkatkan keberagaman rekomendasi,
sekaligus mempromosikan destinasi wisata berkualitas yang selama ini
kurang terekspos (*hidden gems*) tanpa mengurangi kenyamanan pengguna.

Berikut adalah rincian kesimpulan yang menjawab rumusan masalah
penelitian:

1.  Keseimbangan Adaptif antara Akurasi dan Keberagaman: Model MAB-MMR
    yang dikembangkan terbukti mampu menyesuaikan strategi rekomendasi
    secara otomatis terhadap kondisi yang dihadapi. Dalam situasi di
    mana data interaksi sangat minim (*data sparse* 0,602%) dan
    mayoritas pengguna adalah pengunjung baru, sistem secara mandiri
    memilih strategi yang mengutamakan relevansi (parameter λ rendah).
    Mekanisme adaptasi ini memberikan hasil yang efektif: sistem mampu
    mempertahankan akurasi yang setara dengan model pembanding (baseline
    Hybrid) dengan skor NDCG@10 sebesar 0,0237, namun di saat yang sama
    memberikan rekomendasi yang 3,5% lebih beragam. Hal ini membuktikan
    bahwa sistem dapat menemukan titik temu terbaik antara akurasi dan
    keberagaman tanpa intervensi manual.

2.  Kontribusi Integrasi Data Kontekstual terhadap Distribusi: Integrasi
    variabel kontekstual (seperti cuaca dan waktu) terbukti meningkatkan
    relevansi dan pemerataan rekomendasi secara terukur. Hasil evaluasi
    menunjukkan bahwa penambahan komponen konteks meningkatkan nilai
    keberagaman (*Diversity*) sebesar +7,21% dan akurasi (NDCG) sebesar
    +1,24% dibandingkan model tanpa konteks. Dari perspektif distribusi,
    sistem mencatatkan penurunan ketimpangan (Gini Coefficient 0,6401)
    dan perluasan cakupan rekomendasi. Secara spesifik, cakupan katalog
    (*Catalog Coverage*) meningkat menjadi 79,46% dan jangkauan terhadap
    destinasi *long-tail* mencapai 69,64%. Hal ini mengindikasikan bahwa
    sistem memfasilitasi pergeseran frekuensi rekomendasi dari destinasi
    populer (*Head*) menuju destinasi alternatif (*Tail*) secara
    efektif.

3.  Peningkatan Eksposur Destinasi dan Evaluasi Pengguna Implementasi
    algoritma ini berdampak langsung pada peningkatan visibilitas
    destinasi yang sebelumnya kurang terekspos. Analisis frekuensi
    menunjukkan peningkatan rekomendasi yang signifikan pada destinasi
    berkualitas tinggi namun jarang dikunjungi, seperti \"Curug
    Pasirwangi\" (+52,78%) dan \"Curug Cirengganis\" (+33,77%).

> Temuan ini sejalan dengan hasil evaluasi pengguna (n=30), yang
> mencatat tingkat penemuan destinasi baru (*Discovery Rate*) sebesar
> 96,7%. Responden juga memberikan penilaian positif terhadap variasi
> rekomendasi (*Perceived Diversity* skor 4,3/5,0) dan aspek kegunaan
> sistem, yang ditunjukkan oleh skor *System Usability Scale* (SUS)
> sebesar 79,1 (kategori \"Baik\"). Data ini mengonfirmasi bahwa upaya
> pemerataan distribusi dapat dilakukan tanpa mengurangi tingkat
> penerimaan pengguna terhadap sistem.

Secara keseluruhan, penelitian ini menyimpulkan bahwa pendekatan adaptif
yang diusulkan berhasil menjadi solusi kompromi yang optimal: sistem
mampu mendukung pemerataan ekonomi pariwisata lokal melalui algoritma,
namun tetap memastikan wisatawan mendapatkan rekomendasi liburan yang
relevan dan memuaskan.

## Saran 

Berdasarkan hasil dan temuan dalam penelitian ini, beberapa saran untuk
pengembangan dan penelitian lanjutan adalah sebagai berikut:

1.  Ekspansi Multi-Regional untuk Validasi Generalisabilitas: Dataset
    Sumedang memiliki karakteristik spesifik (78% wisata
    alam/petualangan, *sparsity* 0,602%). Generalisabilitas strategi
    adaptasi perlu divalidasi pada destinasi dengan profil berbeda.

2.  Peningkatan sample size user testing: Eksperimen dapat diperluas
    dengan jumlah partisipan yang lebih besar (n≥50 per grup) untuk
    meningkatkan statistical power, memungkinkan deteksi small to medium
    effect sizes, dan melakukan analisis subgroup yang lebih mendalam
    pada segmen pengguna yang berbeda.

3.  Eksplorasi *automated reward function tuning*: Teknik hyperparameter
    optimization atau *multi-objective evolutionary algorithms* dapat
    diteliti lebih lanjut untuk mengotomasi tuning composite reward
    function dan menemukan kombinasi bobot optimal yang berbeda untuk
    user segments atau contexts yang berbeda.

4.  Integrasi dengan *deep learning*: Pendekatan *neural collaborative
    filtering*, *variational autoencoders*, atau *graph neural networks*
    dapat dieksplorasi untuk menangkap kompleksitas preferensi pengguna
    dengan lebih baik, terutama pada dataset dengan kepadatan lebih
    tinggi, dengan tetap mempertimbangkan *trade-off* antara
    kompleksitas model dan *interpretability*.

# DAFTAR PUSTAKA

Abdollahpouri, H. (2019). Popularity bias in ranking and recommendation.
AIES 2019 - Proceedings of the 2019 AAAI/ACM Conference on AI, Ethics,
and Society, 529--530. https://doi.org/10.1145/3306618.3314309

Abdollahpouri, H., Mansoury, M., Burke, R., & Mobasher, B. (2020). The
Connection between Popularity Bias, Calibration, and Fairness in
Recommendation. RecSys 2020 - 14th ACM Conference on Recommender
Systems, 726--731. https://doi.org/10.1145/3383313.3418487

Abdollahpouri, H., Mansoury, M., Burke, R., Mobasher, B., & Malthouse,
E. (2021). User-centered evaluation of popularity bias in recommender
systems. UMAP 2021 - Proceedings of the 29th ACM Conference on User
Modeling, Adaptation and Personalization, 119--129.
https://doi.org/10.1145/3450613.3456821

Akhadam, A., Kbibchi, O., Mekouar, L., & Iraqi, Y. (2025). A Comparative
Evaluation of Recommender Systems Tools. IEEE Access.
https://doi.org/10.1109/ACCESS.2025.3541014

Alfaifi, Y. H. (2024). Recommender Systems Applications: Data Sources,
Features, and Challenges. Dalam Information (Switzerland) (Vol. 15,
Nomor 10). Multidisciplinary Digital Publishing Institute (MDPI).
https://doi.org/10.3390/info15100660

Barykin, S. E., de la Poza, E., Khalid, B., Kapustina, I. V., Kalinina,
O. V., & Iqbal, K. M. J. (2021). Tourism industry: Digital
transformation. Dalam Handbook of Research on Future Opportunities for
Technology Management Education (hlm. 414--434). IGI Global.
https://doi.org/10.4018/978-1-7998-8327-2.ch025

Booking.com. (2023). SHARES ITS 7 PREDICTIONS FOR TRAVEL IN 2024 OUT OF
AUTOPILOT AND INTO OUR BEST LIFE.

Brooke, J. (1996). SUS - A quick and dirty usability scale.

Bukhari, M., Maqsood, M., & Adil, F. (2025). An actor-critic based
recommender system with context-aware user modeling. Artificial
Intelligence Review, 58(5). https://doi.org/10.1007/s10462-025-11134-9

Chalkiadakis, G., Ziogas, I., Koutsmanis, M., Streviniotis, E.,
Panagiotakis, C., & Papadakis, H. (2023). A Novel Hybrid Recommender
System for the Tourism Domain. Algorithms, 16(4).
https://doi.org/10.3390/a16040215

Choi, I. Y., Ryu, Y. U., & Kim, J. K. (2021). A recommender system based
on personal constraints for smart tourism city. Asia Pacific Journal of
Tourism Research, 26(4), 440--453.
https://doi.org/10.1080/10941665.2019.1592765

DISPARBUDPORA. (2024). DATA  KUNJUNGAN OBJEK WISATA TAHUN 2023.

Falk, K. (2019). Practical Recommender Systems.

Fararni, K. Al, Nafis, F., Aghoutane, B., Yahyaouy, A., Riffi, J., &
Sabri, A. (2021). Hybrid recommender system for tourism based on big
data and AI: A conceptual framework. Big Data Mining and Analytics,
4(1), 47--55. https://doi.org/10.26599/BDMA.2020.9020015

Foronda-Robles, C., Galindo-Pérez-de-Azpillaga, L., & Armario-Pérez, P.
(2025). The sustainable management of overtourism via user content.
Annals of Tourism Research Empirical Insights, 6(2).
https://doi.org/10.1016/j.annale.2025.100184

Fragkoulis, M., Carbone, P., Kalavri, V., & Katsifodimos, A. (2024). A
survey on the evolution of stream processing systems. VLDB Journal,
33(2), 507--541. https://doi.org/10.1007/s00778-023-00819-8

Gotthardt, M., & Mezhuyev, V. (2022). Measuring the Success of
Recommender Systems: A PLS-SEM Approach. IEEE Access, 10, 30610--30623.
https://doi.org/10.1109/ACCESS.2022.3159652

Hoarau-Heemstra, H., Wigger, K., Olsen, J., & James, L. (2023). Cruise
tourism destinations: Practices, consequences and the road to
sustainability. Dalam Journal of Destination Marketing and Management
(Vol. 30). Elsevier Ltd. https://doi.org/10.1016/j.jdmm.2023.100820

Hu, M., Zhang, Y., Zhang, H., Lu, Y., Zuo, L., Zhuang, M., Liu, W.,
Zhang, J., & Zhang, H. (2020). How do Chinese tourists perceive
tranquillity during the tour? Tourism Management Perspectives, 34.
https://doi.org/10.1016/j.tmp.2020.100666

Huang, Z., Lin, X., Liu, H., Zhang, B., Chen, Y., & Tang, Y. (2020).
Deep Representation Learning for Location-Based Recommendation. IEEE
Transactions on Computational Social Systems, 7(3), 648--658.
https://doi.org/10.1109/TCSS.2020.2974534

Javadian Sabet, A., Shekari, M., Guan, C., Rossi, M., Schreiber, F., &
Tanca, L. (2022). THOR: A Hybrid Recommender System for the Personalized
Travel Experience. Big Data and Cognitive Computing, 6(4).
https://doi.org/10.3390/bdcc6040131

Kumar, J., Patra, B. K., Sahoo, B., & Babu, K. S. (2024). Group
recommendation exploiting characteristics of user-item and collaborative
rating of users. Multimedia Tools and Applications, 83(10),
29289--29309. https://doi.org/10.1007/s11042-023-16799-4

Massimo, D., & Ricci, F. (2022). Building effective recommender systems
for tourists. AI Magazine, 43(2), 209--224.
https://doi.org/10.1002/aaai.12057

Noorian Avval, A. A., & Harounabadi, A. (2023). A hybrid recommender
system using topic modeling and prefixspan algorithm in social media.
Complex and Intelligent Systems, 9(4), 4457--4482.
https://doi.org/10.1007/s40747-022-00958-5

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007).
A Design Science Research Methodology for Information Systems Research.
Dalam Journal of Management Information Systems (Vol. 24, Nomor 8).
http://www.tuunanen.fi.

Pencarelli, T. (2020). The digital revolution in the travel and tourism
industry. Information Technology and Tourism, 22(3), 455--476.
https://doi.org/10.1007/s40558-019-00160-3

Qassimi, S., & Rakrak, S. (2025). Multi-objective contextual bandits in
recommendation systems for smart tourism. Scientific Reports, 15(1).
https://doi.org/10.1038/s41598-025-89920-2

Ricci, F., Rokach, L., & Shapira, B. (2022). Recommender Systems
Handbook: Third Edition. Dalam Recommender Systems Handbook: Third
Edition. Springer US. https://doi.org/10.1007/978-1-0716-2197-4

Sachi Nandan Mohanty, J. M. C. S. J. A. A. E. P. G. (2020). Recommender
System with Machine Learning and Artificial Intelligence.

Shafqat, W., & Byun, Y. C. (2020). A context-aware location
recommendation system for tourists using hierarchical LSTM model.
Sustainability (Switzerland), 12(10). https://doi.org/10.3390/su12104107

Shambour, Q. Y., Abualhaj, M. M., Abu-Shareha, A. A., & Kharma, Q. M.
(2024). PERSONALIZED TOURISM RECOMMENDATIONS: LEVERAGING USER
PREFERENCES AND TRUST NETWORK. Interdisciplinary Journal of Information,
Knowledge, and Management, 19. https://doi.org/10.28945/5329

Shi, X., Liu, Q., Xie, H., Wu, D., Peng, B., Shang, M., & Lian, D.
(2023). Relieving Popularity Bias in Interactive Recommendation: A
Diversity-Novelty-Aware Reinforcement Learning Approach. ACM
Transactions on Information Systems, 42(2).
https://doi.org/10.1145/3618107

Shuvo, M. I. M., & Islam, M. J. (2024). The digital transformation of
tourism: a study of tourist behaviour and preferences in the age of
technology in Bangladesh. Research in Hospitality Management, 14(3),
236--244. https://doi.org/10.1080/22243534.2024.2419366

Siyamiyan Gorji, A., Hosseini, S., Seyfi, S., Almeida-García, F., Cortes
Macías, R., & Mena Navarro, A. (2026). 'Málaga for living, not
surviving': Resident perceptions of overtourism, social injustice and
urban governance. Journal of Destination Marketing and Management, 39.
https://doi.org/10.1016/j.jdmm.2025.101044

Solano-Barliza, A., Arregocés-Julio, I., Aarón-Gonzalvez, M.,
Zamora-Musa, R., De-La-Hoz-Franco, E., Escorcia-Gutierrez, J., &
Acosta-Coll, M. (2024). Recommender systems applied to the tourism
industry: a literature review. Dalam Cogent Business and Management
(Vol. 11, Nomor 1). Cogent OA.
https://doi.org/10.1080/23311975.2024.2367088

Song, Y., & Jiao, X. (2023). A Real-Time Tourism Route Recommendation
System Based on Multitime Scale Constraints. Mobile Information Systems,
2023. https://doi.org/10.1155/2023/4586047

Suhaim, A. Bin, & Berri, J. (2021). Context-Aware Recommender Systems
for Social Networks: Review, Challenges and Opportunities. IEEE Access,
9, 57440--57463. https://doi.org/10.1109/ACCESS.2021.3072165

UNWTO. (2021). International Tourism Highlights, 2020 Edition. Dalam
International Tourism Highlights, 2020 Edition. World Tourism
Organization (UNWTO). https://doi.org/10.18111/9789284422456

Wang, R., Wu, Z., Lou, J., & Jiang, Y. (2022). Attention-based dynamic
user modeling and Deep Collaborative filtering recommendation. Expert
Systems with Applications, 188.
https://doi.org/10.1016/j.eswa.2021.116036

World Tourism Organization. (2024). International Tourism Highlights,
2024 Edition. UN Tourism. https://doi.org/10.18111/9789284425808

Yalcin, E., & Bilge, A. (2021). Investigating and counteracting
popularity bias in group recommendations. Information Processing and
Management, 58(5). https://doi.org/10.1016/j.ipm.2021.102608

Yoon, J. H., & Choi, C. (2023). Real-Time Context-Aware Recommendation
System for Tourism. Sensors, 23(7). https://doi.org/10.3390/s23073679

Zhang, K., Cao, Q., Sun, F., Wu, Y., Tao, S., Shen, H., & Cheng, X.
(2025). Robust Recommender System: A Survey and Future Directions. ACM
Computing Surveys. https://doi.org/10.1145/3757057

Zhao, Y., Wang, Y., Liu, Y., Cheng, X., Aggarwal, C. C., & Derr, T.
(2025). Fairness and Diversity in Recommender Systems: A Survey. ACM
Transactions on Intelligent Systems and Technology, 16(1).
https://doi.org/10.1145/3664928

 

# LAMPIRAN

[]{#_Toc214880879 .anchor}Lampiran A: Detail Implementasi Teknis

Lampiran ini berisi detail teknis, *snippet* kode, dan tabel aturan
pendukung yang diringkas pada Bab IV.2.

[]{#_Toc214880880 .anchor}A.1 Snippet Kode Komponen Utama

Berikut adalah *snippet* kode yang mendefinisikan logika inti dari
komponen-komponen model yang digunakan dalam *notebook* evaluasi
evaluasi_kuantitatif_FINAL.

**A.1.1 *Collaborative Filtering* (NMF)**

\# Menggunakan library \'surprise\'

from surprise import Dataset, Reader, NMF

from surprise.model_selection import train_test_split as surprise_split

class ProperCollaborativeRecommender:

\"\"\"Collaborative Filtering using Surprise NMF.\"\"\"

def \_\_init\_\_(self, n_factors=20, n_epochs=30, random_state=42):

\# Parameter n_factors=20 dan n_epochs=30

self.nmf_model = NMF(n_factors=n_factors, n_epochs=n_epochs,
random_state=random_state)

self.trainset = None

self.is_trained = False

\# \... (logika train dan predict) \...

**A.1.2 *Context-Aware Component***

class ContextAwareComponent:

def \_\_init\_\_(self):

\# Mendefinisikan aturan bobot multiplikatif (yang akan menjadi aditif)

self.context_rules = {

\'weekend\': {

\'Wisata Alam\': 1.5, \'Wisata Keluarga\': 1.6,

\# \... (aturan \'weekend\' lainnya) \...

},

\'hujan\': {

\'Wisata Kuliner\': 1.8,

\'Wisata Budaya & Sejarah\': 1.7,

\'Wisata Alam\': 0.5, \# Konversi: 0.5 (multiplikatif) → -0.5 (aditif
boost/penalty)

\# \... (aturan \'hujan\' lainnya) \...

},

\# \... (Aturan untuk musim, waktu, kepadatan, event, viral) \...

}

def get_contextual_boost(self, recommendations, user_context,
item_categories):

boosted_recs = \[\]

for rec in recommendations:

original_score = rec\[\'score\'\]

category = item_categories.get(rec\[\'destination_id\'\], \'Other\')

\# \-\-- LOGIKA ADITIF (PENJUMLAHAN) \-\--

total_additive_boost = 0.0

\# 1. Tipe Hari

day_type = user_context.get(\'day_type\', \'weekday\')

day_weights = self.context_rules.get(day_type, {})

multiplicative_boost_day = day_weights.get(category, 1.0)

total_additive_boost += (multiplicative_boost_day - 1.0) \# misal: 1.5
-\> +0.5

\# 2. Cuaca

weather = user_context.get(\'weather\', \'cerah\')

weather_weights = self.context_rules.get(weather, {})

multiplicative_boost_weather = weather_weights.get(category, 1.0)

total_additive_boost += (multiplicative_boost_weather - 1.0) \# misal:
0.5 -\> -0.5

\# \... (logika boost lainnya untuk musim, waktu, kepadatan, dll.) \...

boosted_recs.append({

\'destination_id\': rec\[\'destination_id\'\],

\'score\': original_score + total_additive_boost \# Skor akhir = Skor
Asli + Total Boost

})

return boosted_recs

**A.1.3 MAB & MMR**

class MMRReranker:

\"\"\"Melakukan re-ranking menggunakan Maximal Marginal Relevance.\"\"\"

def \_\_init\_\_(self, item_categories, item_popularity,
popularity_weight=0.3):

self.item_vectors = {}

unique_categories = list(set(item_categories.values()))

for item_id, category in item_categories.items():

\# Vektor fitur = One-hot Kategori + Skor Popularitas (bobot 0.3)

cat_vector = \[1.0 if cat == category else 0.0 for cat in
unique_categories\]

\# \... (logika normalisasi skor popularitas) \...

pop_feature = \...

self.item_vectors\[item_id\] = np.array(cat_vector + \[pop_feature \*
self.popularity_weight\])

def rerank(self, candidates, lambda_val=0.5, k=10):

\# \... (Logika iteratif MMR) \...

\# mmr_score = (1 - lambda_val) \* relevance - lambda_val \* max_sim

\...

class ContextualMAB:

\"\"\"Mengelola pemilihan arm (lambda) menggunakan UCB1.\"\"\"

def \_\_init\_\_(self, lambda_values=None, random_state=42):

if lambda_values is None:

\# 5 Arms (Lambda) yang digunakan

self.lambda_values = \[0.0, 0.3, 0.5, 0.7, 1.0\]

else:

self.lambda_values = lambda_values

self.rng = np.random.RandomState(random_state)

\# Inisialisasi \'context_brains\' untuk menyimpan statistik per konteks

self.context_brains = {}

def select_arm(self, context_key):

\# \... (Logika UCB1 (Upper Confidence Bound)) \...

\...

def update(self, context_key, arm_index, reward):

\# \... (Logika pembaruan reward inkremental) \...

\...

[]{#_Toc214880881 .anchor}A.2 Detail Aturan Kontekstual Aditif

Logika inti dari komponen *context-aware* adalah aturan aditif. *Boost*
(atau penalti) dihitung menggunakan formula (Bobot Multiplikatif - 1.0)
dan ditambahkan ke skor relevansi asli. Tabel berikut merinci semua
aturan yang diimplementasikan.

[]{#_Toc214880976 .anchor}Tabel A.2.1 Aturan Kontekstual - Tipe Hari

  -------------------------------------------------------------------
     Kondisi             Kategori          Bobot     Boost/Penalty
                                                        Aditif
  -------------- ------------------------ ------- -------------------
     Weekend           Wisata Alam          1.5          +0.5

                     Wisata Keluarga        1.6          +0.6

                  Wisata Buatan/Rekreasi    1.6          +0.6

                      Wisata Kuliner        1.4          +0.4

                    Wisata Petualangan      1.4          +0.4

                 Wisata Budaya & Sejarah    1.1          +0.1

     Weekday     Wisata Budaya & Sejarah    1.4          +0.4

                      Wisata Religi         1.3          +0.3

                      Wisata Kuliner        1.2          +0.2

                     Wisata Kesehatan       1.4          +0.4

                       Wisata Alam          1.1          +0.1

                     Wisata Keluarga        0.8     -0.2 (Penalti)

  Libur Nasional  Wisata Buatan/Rekreasi    1.8          +0.8

                     Wisata Keluarga        1.8          +0.8

                      Wisata Kuliner        1.6          +0.6

                       Wisata Alam          1.7          +0.7

                    Wisata Petualangan      1.5          +0.5

  Libur Lebaran      Wisata Keluarga        2.0          +1.0

                  Wisata Buatan/Rekreasi    1.9          +0.9

                      Wisata Kuliner        1.7          +0.7

                       Wisata Alam          1.5          +0.5
  -------------------------------------------------------------------

[]{#_Toc214880977 .anchor}Tabel A.2.2 Aturan Kontekstual -- Cuaca

  ---------------------------------------------------------------
   Kondisi           Kategori          Bobot     Boost/Penalty
                                                    Aditif
  ---------- ------------------------ ------- -------------------
    Cerah          Wisata Alam          1.7          +0.7

                Wisata Petualangan      1.6          +0.6

                 Wisata Olahraga        1.5          +0.5

              Wisata Buatan/Rekreasi    1.4          +0.4

                 Wisata Keluarga        1.4          +0.4

                  Wisata Kuliner        1.0           0.0

             Wisata Budaya & Sejarah    0.9     -0.1 (Penalti)

   Mendung   Wisata Budaya & Sejarah    1.4          +0.4

                  Wisata Kuliner        1.3          +0.3

                 Wisata Keluarga        1.2          +0.2

                   Wisata Alam          1.2          +0.2

              Wisata Buatan/Rekreasi    1.2          +0.2

    Hujan         Wisata Kuliner        1.8          +0.8

             Wisata Budaya & Sejarah    1.7          +0.7

                 Wisata Kesehatan       1.6          +0.6

              Wisata Buatan/Rekreasi    1.2   +0.2 (Jika indoor)

                   Wisata Alam          0.5     -0.5 (Penalti)

                Wisata Petualangan      0.4     -0.6 (Penalti)

                 Wisata Olahraga        0.3     -0.7 (Penalti)
  ---------------------------------------------------------------

[]{#_Toc214880978 .anchor}Tabel A.2.3 Aturan Kontekstual - Waktu & Musim

  ---------------------------------------------------------------------
      Kondisi              Kategori          Bobot     Boost/Penalty
                                                          Aditif
  ---------------- ------------------------ ------- -------------------
        Pagi             Wisata Alam          1.3          +0.3

                       Wisata Olahraga        1.4          +0.4

                   Wisata Budaya & Sejarah    1.1          +0.1

       Siang            Wisata Kuliner        1.3          +0.3

                    Wisata Buatan/Rekreasi    1.2          +0.2

                   Wisata Budaya & Sejarah    1.2          +0.2

        Sore            Wisata Kuliner        1.4          +0.4

                         Wisata Alam          1.1          +0.1

       Malam            Wisata Kuliner        1.7          +0.7

                    Wisata Buatan/Rekreasi    1.3          +0.3

   Musim Kemarau         Wisata Alam          1.4          +0.4

                      Wisata Petualangan      1.3          +0.3

    Musim Hujan    Wisata Budaya & Sejarah    1.3          +0.3

                        Wisata Kuliner        1.2          +0.2

                         Wisata Alam          0.8     -0.2 (Penalti)
  ---------------------------------------------------------------------

[]{#_Toc214880979 .anchor}Tabel A.2.4 Aturan Kontekstual - Event, Tren,
& Kepadatan

  -------------------------------------------------------------------------
         Kondisi               Kategori          Bobot     Boost/Penalty
                                                              Aditif
  --------------------- ----------------------- ------- -------------------
       Tren: Viral         (Semua Kategori)       2.0          +1.0

     Event: Festival        Wisata Kuliner        2.2          +1.2
         Kuliner                                        

                            Wisata Keluarga       1.5          +0.5

     Event: Festival    Wisata Budaya & Sejarah   2.2          +1.2
         Budaya                                         

                            Wisata Keluarga       1.4          +0.4

    Kepadatan: Puncak      (Semua Kategori)       0.5     -0.5 (Penalti)

  Kepadatan: Sg. Ramai     (Semua Kategori)       0.7     -0.3 (Penalti)

    Kepadatan: Ramai       (Semua Kategori)       0.9     -0.1 (Penalti)

     Kepadatan: Sepi       (Semua Kategori)       1.2          +0.2

   Kepadatan: Sg. Sepi     (Semua Kategori)       1.3          +0.3
  -------------------------------------------------------------------------
