# Kuis 2: Authentication, Session, dan JavaScript

Proyek Ruang Belajar ini sudah menyelesaikan materi sebelumnya. Halaman profil, daftar sesi, form sesi biasa, serta endpoint JSON `/api/sessions/` dapat digunakan sebagai titik awal.

## Tugas 1: Register, Login, dan Logout

Tambahkan autentikasi berbasis session menggunakan autentikasi bawaan Django.

Buat halaman register dengan `UserCreationForm` pada `/register/` dan named route `main:register`. Buat pula halaman login dengan `AuthenticationForm` pada `/login/` dan named route `main:login`. Setelah register atau login berhasil, pengguna diarahkan ke halaman daftar sesi.

Tambahkan route `main:logout` pada `/logout/`. Ubah navbar agar pengunjung melihat Masuk dan Daftar, sedangkan pengguna login melihat Akun, username, dan Keluar.

## Tugas 2: Cookie Login dan Halaman Akun

Saat login berhasil, simpan cookie `last_login` dengan nilai waktu login yang dapat dibaca manusia serta masa berlaku paling sedikit satu hari. Hapus cookie tersebut saat logout.

Buat halaman `/account/` dengan named route `main:show_account`. Halaman ini hanya dapat dibuka pengguna yang sudah login, lalu menampilkan username dan nilai cookie `last_login`. Jika cookie belum tersedia, tampilkan penjelasan bahwa waktu login belum tercatat.

## Tugas 3: Daftar Sesi dari Fetch API

Refactor halaman `/sessions/` agar daftar sesi diambil dari endpoint JSON yang sudah tersedia, bukan dari perulangan template Django.

Tambahkan input pencarian topik. Ketika pengguna mengetik, panggil `/api/sessions/?topic=...` menggunakan `fetch` dan debounce. Render kartu sesi memakai DOM API seperti `document.createElement` dan `textContent`, bukan `innerHTML`. Sediakan kondisi loading, kosong, dan error yang memberi pengguna langkah berikutnya. Pertahankan urutan waktu sesi dan formatkan waktu menggunakan `Intl.DateTimeFormat` berbahasa Indonesia.

## Tugas 4: Dialog Tambah Sesi dan Toast

Pada halaman daftar sesi, pengguna login dapat membuka form Tambah sesi melalui elemen HTML `<dialog>`. Pengunjung diarahkan ke halaman Masuk. Dialog harus dapat dibuka dengan keyboard dan ditutup melalui tombol Batal atau Escape.

Buat komponen toast pada berkas JavaScript terpisah. Toast menerima pesan teks, diumumkan melalui live region, dapat ditutup, dan tidak memakai animasi berulang. Semua kontrol harus tetap dapat digunakan melalui keyboard.

## Tugas 5: Tambah Sesi dengan AJAX

Buat endpoint POST `/sessions/add-ajax/` dengan named route `main:create_session_ajax`. Endpoint menerima `SessionForm` dan hanya dapat digunakan pengguna login. Data valid mengembalikan JSON status 201 beserta pesan sukses. Form tidak valid mengembalikan status 400 dan detail error dalam JSON.

Kirim form dialog menggunakan `fetch`, `FormData`, dan CSRF token. Selama request berlangsung, nonaktifkan tombol simpan serta tampilkan status. Saat berhasil, tutup dan kosongkan dialog, tampilkan toast, lalu muat ulang daftar menggunakan fungsi fetch. Saat gagal, tampilkan error tanpa menghapus isian pengguna.

## Penilaian setiap nomor

| Skor | Kriteria |
| --- | --- |
| 1 | Ada usaha implementasi, tetapi kode error atau proyek tidak dapat dijalankan. |
| 2 | Sebagian kebutuhan nomor dikerjakan dan README diisi. |
| 3 | Seluruh kebutuhan nomor dikerjakan, tetapi belum ada test. |
| 3.5 | Seluruh kebutuhan nomor dikerjakan dan terdapat test yang relevan, tetapi test dibuat setelah implementasi. |
| 4 | Seluruh kebutuhan nomor dikerjakan dengan TDD. Riwayat Git memperlihatkan test gagal dibuat sebelum implementasi, lalu implementasi membuat test lulus. |

Untuk nomor JavaScript, test Django boleh digunakan untuk memeriksa endpoint, respons JSON, otorisasi, atau markup yang menjadi kontrak JavaScript.

## Pertanyaan

Jawab pada bagian Jawaban di bawah ini.

1. Jelaskan bagaimana `login()` Django membuat pengguna tetap terautentikasi ketika membuka request berikutnya. Sebutkan peran session, cookie, middleware, dan `request.user`.
2. Mengapa cookie `last_login` pada tugas ini tidak boleh dipakai sebagai sumber kebenaran autentikasi pengguna?
3. Jelaskan alasan penggunaan CSRF token ketika JavaScript mengirim `fetch` POST ke Django.
4. Mengapa data dari respons JSON sebaiknya dimasukkan ke halaman menggunakan `textContent`, bukan `innerHTML`?

## Jawaban

1. 
2. 
3. 
4. 
