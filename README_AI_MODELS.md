# Sistem Konfigurasi AI Models

## Overview

Sistem ini memungkinkan admin untuk mengatur model AI, cost kuota, dan API keys melalui panel admin Django.

## Fitur

- ✅ Konfigurasi model AI dari database
- ✅ Cost kuota yang dapat diatur per model
- ✅ API keys yang dapat diatur per model
- ✅ Status aktif/nonaktif per model
- ✅ Panel admin untuk mengelola konfigurasi

## Setup Awal

### 1. Jalankan Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Setup Data Awal

```bash
python manage.py setup_ai_models
```

### 3. Konfigurasi API Keys

1. Buka panel admin Django
2. Pergi ke "AI Model Configurations"
3. Edit setiap model dan isi API key yang sesuai:
   - **Gemini**: Masukkan API key Google AI
   - **GPT-3.5**: Masukkan API key OpenAI
   - **GPT-4.1**: Masukkan API key OpenAI

## Struktur Database

### Model: AiModelConfig

```python
class AiModelConfig(models.Model):
    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quota_cost = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Penggunaan di Views

### 1. Mengambil Cost dari Database

```python
try:
    model_config = AiModelConfig.objects.get(model_name=model_choice)
    quota_cost = model_config.quota_cost
except AiModelConfig.DoesNotExist:
    quota_cost = 5 # Default cost
```

### 2. Mengambil API Key dari Database

```python
try:
    model_config = AiModelConfig.objects.get(model_name=model_choice)
    API_KEY = model_config.api_key
    if not API_KEY:
        return JsonResponse({"error": "API key tidak tersedia"}, status=500)
except AiModelConfig.DoesNotExist:
    return JsonResponse({"error": "Model tidak ditemukan"}, status=400)
```

### 3. Mengirim Data ke Template

```python
def get_ai_models_data():
    try:
        models = AiModelConfig.objects.filter(is_active=True).order_by('quota_cost')
        return models
    except:
        return []

# Di view
ai_models = get_ai_models_data()
context = {
    'ai_models': ai_models,
    'ai_models_json': json.dumps({...}),
    'ai_models_cost_json': json.dumps({...})
}
```

## Template Usage

### Dropdown Options

```html
<select id="modelSelect">
  {% if ai_models %} {% for model in ai_models %}
  <option
    value="{{ model.model_name }}"
    data-cost="{{ model.quota_cost }}"
    {%
    if
    forloop.first
    %}selected{%
    endif
    %}
  >
    {{ model.display_name }} - {{ model.quota_cost }} Kuota
  </option>
  {% endfor %} {% else %}
  <!-- Fallback options -->
  {% endif %}
</select>
```

### JavaScript Data

```javascript
const modelDescriptions = JSON.parse("{{ ai_models_json|escapejs }}");
const modelCost = JSON.parse("{{ ai_models_cost_json|escapejs }}");
```

## Admin Panel

### Akses Admin Panel

1. Buka `/admin/`
2. Login dengan akun admin
3. Pergi ke "AI Model Configurations"

### Fitur Admin Panel

- ✅ List view dengan filter dan search
- ✅ Edit model satu per satu
- ✅ Toggle status aktif/nonaktif
- ✅ Update cost kuota
- ✅ Update API keys
- ✅ View timestamps

## Keuntungan Sistem Ini

1. **Fleksibilitas**: Admin dapat mengubah cost dan API keys tanpa deploy ulang
2. **Keamanan**: API keys tersimpan di database, bukan hardcoded
3. **Skalabilitas**: Mudah menambah model AI baru
4. **Monitoring**: Timestamps untuk tracking perubahan
5. **Fallback**: Sistem tetap berjalan meski data database kosong

## Troubleshooting

### Error: "Model AI tidak ditemukan"

- Pastikan model sudah disetup dengan `python manage.py setup_ai_models`
- Cek apakah model aktif di admin panel

### Error: "API key tidak tersedia"

- Isi API key di admin panel untuk model yang digunakan
- Pastikan API key valid dan aktif

### Error: "Kuota tidak cukup"

- Cek cost model di admin panel
- Pastikan user memiliki kuota yang cukup

## Next Steps

1. **Implementasi OpenAI API**: Tambahkan logika untuk GPT-3.5 dan GPT-4.1
2. **Rate Limiting**: Tambahkan sistem rate limiting per model
3. **Usage Tracking**: Track penggunaan per model
4. **Cost Optimization**: Sistem untuk memilih model terbaik berdasarkan cost
5. **Admin Notifications**: Notifikasi saat API key expired atau error
