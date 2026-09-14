Nama : Aisyah Zayyana Hanifah

NPM : 2506609132

Kelas : PBP F

Link PWS: https://aisyah-zayyana-myportofolio.pws.cs.ui.ac.id


## Deskripsi
Website portofolio pribadi yang dibuat sebagai bagian dari Tugas PBP. Website ini menampilkan profil dan pengalaman.

## Features

- Personal profile
- Experience section
- Education section
- Responsive desktop/mobile layout
- Semantic HTML5 structure
- Social media links


## Tech Stack

- Python 3
- Django
- HTML5
- CSS3
- Git & GitHub


## Project Structure

myportfolio/
├── main/
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_education.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── portofolio/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
├── templates/
│   ├── education.html
│   ├── experience.html
│   └── index.html
├── manage.py
├── requirements.txt
└── README.md


## Local Setup

### 1. Clone repository
git clone <repository-url>
cd myportfolio
### 2. Create virtual environment
python3 -m venv venv
### 3. Activate virtual environment
macOS/Linux:
source venv/bin/activate
Windows:
venv\Scripts\activate
### 4. Install dependencies
pip install -r requirements.txt
### 5. Run Django
python manage.py runserver

Website dapat diakses melalui:
http://127.0.0.1:8000/


## Development Progress

### Tutorial 0

- Membuat Django project.
- Menghubungkan repository dengan GitHub.
- Melakukan deployment awal ke PWS.

### Tutorial 1

- Membuat halaman profile.
- Menambahkan semantic HTML.
- Mengatur static files.
- Membuat responsive layout dasar.

### Tugas 1

- Menambahkan Experience section.
- Mengubah layout Experience menggunakan CSS Grid.
- Menambahkan media query untuk mobile.
- Menguji tampilan pada desktop dan mobile.
- Memperbaiki semantic HTML dan accessibility.
- Memperbarui dokumentasi dan AI disclosure.

### Tutorial 2

- Membuat aplikasi `main` pada proyek Django.
- Mengimplementasikan konsep Model-View-Template (MVT).
- Membuat model `Experience` untuk menyimpan data pengalaman.
- Menghubungkan model dengan view dan template.
- Membuat halaman Experience yang menampilkan data secara dinamis.
- Mengonfigurasi routing menggunakan `urls.py` pada project dan aplikasi.
- Menambahkan navigasi antarhalaman menggunakan Django Template Language (DTL).
- Membuat unit tests untuk menguji halaman, model, routing, dan kondisi data.

### Tugas 2

- Menambahkan Education section menggunakan konsep Model-View-Template (MVT).
- Membuat model `Education` untuk menyimpan data pendidikan.
- Membuat migration untuk model `Education`.
- Menambahkan halaman Education dengan data dari database.
- Menambahkan URL dan navbar untuk halaman Education.
- Menambahkan empty state ketika belum ada data pendidikan.
- Menambahkan unit tests untuk page Education.

## Refleksi

### Tugas 1
> 1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

**Jawaban:**

Pada Tutorial, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<main>`, `<section>`, dan `<footer>` yang sudah tersedia pada template yang diberikan. Elemen-elemen tersebut membantu membagi struktur halaman berdasarkan fungsinya, sehingga konten website menjadi lebih terorganisir dan mudah dipahami. Pada Tugas 1, saya menambahkan elemen `<article>` untuk memisahkan setiap pengalaman secara individual. Saya juga menggunakan `<details>` dan `<summary>` untuk menampilkan informasi tambahan yang dapat dibuka dan ditutup oleh pengguna. Penggunaan elemen-elemen tersebut membantu saya menyusun konten dengan lebih terstruktur serta menambahkan interaksi sederhana tanpa menggunakan JavaScript.

> 2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

**Jawaban:**

Ketika mengatur CSS agar tetap responsive, tantangan yang saya temukan adalah menentukan layout yang sesuai untuk setiap section. Dalam menentukan elemen yang perlu diubah posisi atau ukurannya, saya mempertimbangkan hierarki informasi dan fokus utama yang ingin ditampilkan kepada pengguna. Elemen yang ingin lebih dahulu dilihat akan diprioritaskan posisinya dan ukurannya disesuaikan dengan ruang yang tersedia. Misalnya pada bagian Profile, foto ditempatkan setelah nama pada tampilan mobile agar tetap terlihat sebelum pengguna membaca informasi lainnya. Untuk bagian Experience, saya memilih layout horizontal agar kartu dapat ditampilkan dengan ukuran yang sesuai dan dapat digeser pada layar yang lebih kecil.

> 3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

**Jawaban:**

Karena website yang dibuat masih berupa static web, informasi pada portofolio masih harus ditulis langsung di dalam HTML dan membuat proses mengelola informasi menjadi kurang fleksibel. Pada iterasi selanjutnya, saya ingin menambahkan fungsionalitas dinamis agar informasi dapat ditambah atau diperbarui dengan lebih mudah tanpa harus mengubah isi HTML secara langsung.

**AI Disclosure**
Saya menggunakan ChatGPT sebagai alat bantu selama proses pengerjaan Tugas 1. AI digunakan untuk mendiskusikan alternatif desain dan layout, menjelaskan konsep HTML dan CSS yang belum saya pahami (seperti penggunaan `<details>` dan `<summary>` yang saya gunakan pada section Experience), serta membantu mengevaluasi dan melakukan troubleshooting pada kode.

Saya tetap memahami, memilih, dan mengimplementasikan perubahan pada kode secara manual. Setiap saran dari AI saya pertimbangkan kembali berdasarkan kebutuhan desain dan ketentuan tugas.


### Tugas 2

> 1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada *browser*. Dalam jawabanmu, jelaskan peran `urls.py` proyek, `urls.py` aplikasi, *view*, model, dan *template*.

**Jawaban:**

Dalam website portofolio ini, ketika pengguna memilih menu Education pada navbar, *browser* mengirimkan *request* ke URL `/education/`. *Request* tersebut pertama kali diterima oleh `portofolio/urls.py`. Dari sana, request diteruskan ke `main/urls.py` menggunakan `include()`. Selanjutnya, `main/urls.py` mencocokkan URL `/education/` dengan *view* `show_education`.

Di dalam *view* `show_education`, data pendidikan diambil dari model `Education` menggunakan `Education.objects.all()`. Data tersebut kemudian dimasukkan ke dalam *context* dan dikirim ke *template* `education.html`. Template menggunakan Django Template Language (DTL) untuk melakukan loop pada data pendidikan dan menampilkannya satu per satu. Setelah template diproses oleh Django menjadi HTML, hasilnya dikirim kembali ke *browser* dan halaman Education ditampilkan kepada pengguna.

> 2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam *template*? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

**Jawaban:**

Menurut saya, data lebih baik disimpan pada model karena isi data dan tampilan website menjadi lebih terpisah. Misalnya, dalam portofolio saya, kalau data pendidikan atau pengalaman ditulis langsung di dalam *template*, setiap kali ingin menambah atau mengubah informasi saya harus mengubah kode HTML-nya juga. Dengan menggunakan model, saya cukup mengubah data yang ada di database tanpa perlu mengubah struktur *template*.

Hal ini membuat website lebih mudah dikelola, terutama ketika jumlah data semakin banyak. Template juga bisa digunakan kembali untuk menampilkan data yang berbeda. Selain itu, jika nantinya ingin menambahkan fitur lain yang menggunakan data yang telah disimpan, data tersebut sudah tersimpan dengan struktur yang jelas sehingga lebih mudah untuk dikembangkan.

> 3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

**Jawaban:**

`makemigrations` digunakan untuk membuat file migration setelah terdapat perubahan pada model. File tersebut berisi perubahan yang perlu dilakukan pada struktur database. Sementara itu, `migrate` digunakan untuk menerapkan perubahan yang ada di file migration tersebut ke database.

Pada Tugas 2, saya menambahkan model `Education` dengan beberapa field seperti `institution`, `degree`, `description`, `thumbnail`, `started_at`, dan `ended_at`. Setelah model dibuat, saya menjalankan `makemigrations` sehingga Django membuat file `0002_education.py`. Setelah itu, saya menjalankan `migrate` untuk menerapkan perubahan tersebut ke database. Dengan begitu, model `Education` dapat digunakan untuk menyimpan dan mengambil data pendidikan pada website.

**AI Disclosure**

Saya menggunakan ChatGPT sebagai alat bantu selama proses pengerjaan Tugas 2. AI digunakan untuk membantu memahami konsep Model-View-Template (MVT), mendiskusikan CSS yang saya perlukan tapi belum saya ketahui, serta membantu melakukan troubleshooting pada kode.

Saya tetap memahami, memilih, dan mengimplementasikan perubahan pada kode secara manual. Setiap saran dari AI saya pertimbangkan kembali berdasarkan kebutuhan proyek dan ketentuan tugas.