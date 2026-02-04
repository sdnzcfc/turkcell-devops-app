# Turkcell DevOps Case – Observability & Logging Platform

Bu proje, Turkcell DevOps ekibinin verdiği case kapsamında;
gerçek bir production ortamında karşılaşılabilecek **loglama, gözlemlenebilirlik (observability), reverse proxy, HTTPS, metrik toplama ve log rotation** ihtiyaçlarını birebir simüle edecek şekilde tasarlanmıştır.

Amaç:  
> “Yeni bir sunucuya sadece `git pull` + `docker compose up -d` diyerek,
hiç README okumadan bile sistemin ayağa kalkabilmesi.”

---

## 🧱 Mimari Genel Bakış

Sistem aşağıdaki bileşenlerden oluşur:

- **FastAPI App**
  - API ve basit Web GUI
  - Gelen request’leri log dosyasına yazar
  - Prometheus formatında metrik üretir

- **Nginx**
  - Reverse proxy
  - HTTPS terminasyonu (TLS)
  - `/`, `/grafana`, `/prometheus` path routing
  - Docker DNS resolver ile scale edilebilir yapı

- **Prometheus**
  - FastAPI uygulamasından metrik toplar
  - 6 aya kadar veri saklama (retention)

- **Grafana**
  - Prometheus’tan gelen metrikleri görselleştirir
  - Dashboard ve datasource provisioning ile otomatik kurulum

- **Logrotate**
  - Uygulama loglarını periyodik olarak döndürür
  - 10MB üstü log dosyalarını rotate eder
  - Eski logları sıkıştırır ve sınırlar

Tüm sistem **Docker Compose** ile orkestre edilmiştir.

---

## 📁 Klasör Yapısı

```text
.
├── app/                    # FastAPI uygulaması
│   ├── main.py              # API + web endpointleri
│   ├── metrics.py           # Prometheus metrik tanımları
│   └── requirements.txt
│
├── docker/
│   └── Dockerfile           # FastAPI için image build
│
├── nginx/
│   ├── conf.d/app.conf      # Reverse proxy + HTTPS config
│   └── certs/               # SSL sertifikaları
│
├── prometheus/
│   └── prometheus.yml       # Aktif kullanılan Prometheus config
│
├── grafana/
│   ├── dashboards/          # JSON dashboard tanımları
│   └── provisioning/
│       ├── datasources/     # Prometheus datasource tanımı
│       └── dashboards/      # Dashboard provisioning
│
├── logrotate/
│   └── app-requests         # Logrotate kural dosyası
│
├── logs/
│   └── app/                 # Host üzerinde tutulan app logları
│
└── docker-compose.yml
