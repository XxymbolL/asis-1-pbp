# Latihan Django: Ruang Belajar

## Tugas 1: Django Initial Project, HTML5, dan CSS3

Halaman `/` saat ini hanya merender `index.html` tanpa tampilan yang lengkap.

Lengkapi `index.html` sebagai halaman profil fasilitator Ruang Belajar. Gunakan elemen semantik `header`, `nav`, `main`, `section`, dan `footer`. Halaman minimal menampilkan nama, program studi, bio singkat, NPM, serta satu tautan email.

Daftarkan folder `static/` pada konfigurasi proyek dan hubungkan `static/css/style.css` menggunakan tag `{% static %}`. Lengkapi stylesheet yang tersedia dengan custom properties, Flexbox atau Grid, dan media query agar halaman tetap terbaca pada layar kecil.

## Tugas 2: Implementasi Model-View-Template

Daftarkan aplikasi `main` pada `INSTALLED_APPS`, lalu pindahkan routing halaman utama dari level proyek ke `main/urls.py`. Buat view `show_main` untuk halaman profil dan gunakan named route `main:show_main` pada navigasi.

Buat model `Session` pada aplikasi `main` dengan ketentuan berikut:

- `id` menggunakan UUID sebagai primary key dan dibuat otomatis.
- `topic` menyimpan teks dengan panjang maksimal 120 karakter.
- `description` menyimpan teks panjang.
- `level` hanya menerima `basic`, `intermediate`, atau `advanced`. Label yang tampil adalah `Dasar`, `Menengah`, dan `Lanjutan`.
- `scheduled_at` menyimpan tanggal dan waktu pelaksanaan.
- `duration_minutes` menyimpan bilangan bulat positif dengan nilai awal 60.
- Representasi string objek mengembalikan nilai `topic`.

Buat dan terapkan migration setelah model selesai.

Tambahkan view `show_sessions` yang mengambil seluruh objek `Session`, mengurutkannya berdasarkan `scheduled_at`, lalu mengirimkannya ke `session_list.html` melalui context bernama `session_list`.

Template `session_list.html` beserta stylesheet-nya sudah tersedia. Kamu tidak perlu mengubah struktur HTML tersebut. Perhatikan bahwa template mengharapkan context bernama `session_list` dan membaca field model sesuai ketentuan di atas.

Daftarkan halaman sesi pada path `/sessions/` dengan named route `main:show_sessions`. Tambahkan tautan `Sesi` pada navigasi bersama di `base.html` menggunakan tag `{% url %}`. Jika alur MVT benar, template akan menampilkan seluruh objek atau teks `Belum ada sesi belajar.` ketika database kosong.

### optional

Tulis unit test yang memeriksa sedikitnya empat hal berikut:

1. Named route halaman sesi dapat diakses dan memakai `session_list.html`.
2. Data model muncul pada response halaman sesi.
3. Pesan kondisi kosong muncul ketika tidak ada sesi.
4. Representasi string model sama dengan topik sesi.

## Tugas 3: Form dan Data Delivery

Buat `SessionForm` berbasis `ModelForm` untuk seluruh field `Session` selain `id`. Buat view `create_session` yang menampilkan form pada GET, menyimpan data valid pada POST, lalu mengarahkan pengguna ke `main:show_sessions`.

Template `session_form.html` sudah tersedia. Daftarkan path `/sessions/add/` dengan named route `main:create_session`, lalu tambahkan tautan `Tambah sesi` pada halaman daftar sesi.

Tambahkan view `get_sessions_json` yang mengembalikan seluruh sesi dalam format JSON. Gunakan parameter query `topic` untuk memfilter topik dengan `icontains`. Daftarkan endpoint pada `/api/sessions/` dengan named route `main:get_sessions_json`.

### optional

Tulis unit test untuk form valid, kondisi form tidak valid, dan response JSON dengan filter `topic`.

## Pertanyaan

Jawab pada bagian Jawaban di bawah ini.

1. Jelaskan alur request untuk `/sessions/` melalui `ruang_belajar/urls.py`, `main/urls.py`, view, model, context, dan template.
2. Apa perbedaan fungsi `makemigrations` dan `migrate` pada model `Session`?
3. Mengapa form memakai CSRF token dan kapan response JSON lebih tepat digunakan daripada HTML?

## Jawaban

Tulis jawabanmu di sini.
