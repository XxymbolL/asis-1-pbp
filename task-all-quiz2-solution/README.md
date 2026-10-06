# Solusi Kuis 2: Authentication, Session, dan JavaScript

Folder ini berisi solusi referensi untuk `task-all-quiz2`. Jalankan proyek dengan langkah yang sama seperti starter:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

Untuk Windows, aktifkan environment dengan `env\Scripts\activate`.

## Jawaban implementasi

1. Register, login, dan logout berada di `main/views.py`. Navbar pada `templates/base.html` memakai `user.is_authenticated` untuk menampilkan aksi yang sesuai.
2. Login menulis cookie `last_login`, logout menghapusnya, dan `show_account` dilindungi oleh `login_required`.
3. `static/js/sessions.js` mengambil data dari endpoint JSON, melakukan debounce pencarian, serta merender data memakai `document.createElement` dan `textContent`.
4. Halaman sesi memakai elemen `dialog` untuk form dan `static/js/toast.js` untuk pesan singkat yang dapat ditutup.
5. `create_session_ajax` menerima POST yang sudah terautentikasi, mengembalikan JSON, lalu JavaScript memperbarui daftar tanpa reload halaman.

## Pertanyaan

1. `login()` menyimpan identitas pengguna pada session Django. Browser menyimpan ID session dalam cookie, lalu `SessionMiddleware` mengambil session itu pada request berikutnya. `AuthenticationMiddleware` membaca data session dan mengisi `request.user`, sehingga view dan template dapat mengetahui pengguna yang sedang login.
2. Cookie `last_login` hanya informasi tampilan yang berada di browser dan dapat diubah pengguna. Django harus memakai session autentikasi dan data server untuk menentukan apakah pengguna benar-benar sudah login.
3. CSRF token membuktikan bahwa request POST berasal dari halaman yang dibuka dari aplikasi Django. Saat `fetch` mengirim data yang mengubah server, token tersebut tetap perlu dikirim agar Django dapat menolak request lintas situs yang tidak sah.
4. `textContent` memperlakukan nilai dari JSON sebagai teks biasa. Jika respons memuat karakter seperti tag HTML atau skrip, browser tidak akan menjalankannya. `innerHTML` dapat menafsirkan nilai tersebut sebagai markup dan membuka risiko XSS jika data tidak tepercaya.
