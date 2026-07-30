# RAG Project Skeleton

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# isi .env dengan API key lo
```

Taruh dataset lo (.txt / .md) di `data/raw/`.

## Jalankan

```bash
# 1. Ingest dataset -> embed -> simpan ke ChromaDB
python ingest.py

# 2. Test retrieval doang (opsional, buat debug)
python retriever.py

# 3. Test full pipeline via CLI
python main.py
```

## Ganti konfigurasi

Semua setting (embedding mode, model generation, chunk size, top-k) ada di `config.py`.

- `EMBEDDING_MODE = "local"` -> pakai sentence-transformers, gratis, jalan di CPU.
- `EMBEDDING_MODE = "gemini"` -> pakai Gemini embedding API, butuh `GEMINI_API_KEY`.
- `GENERATION_PROVIDER = "gemini"` atau `"deepseek"` -> pilih LLM buat generate jawaban.

## Next steps

- Ganti `chunk_text()` di `ingest.py` dengan splitter yang lebih pintar (misal per-paragraf/per-heading)
  kalau chunking fixed-size mulai terasa motong konteks secara aneh.
- Tambah loader untuk `.pdf` / `.docx` di `load_raw_files()` kalau dataset lo bukan cuma txt/md.
- Kalau udah stabil, tinggal import `rag_pipeline.ask()` di handler Telegram bot lo yang sudah ada.
