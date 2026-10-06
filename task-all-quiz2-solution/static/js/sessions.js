(() => {
    const results = document.querySelector("#session-results");
    const searchInput = document.querySelector("#session-search");
    const loading = document.querySelector("#session-loading");
    const error = document.querySelector("#session-error");
    const dialog = document.querySelector("#session-dialog");
    const openDialogButton = document.querySelector("#open-session-dialog");
    const closeDialogButton = document.querySelector("#close-session-dialog");
    const cancelDialogButton = document.querySelector("#cancel-session-dialog");
    const form = document.querySelector("#session-ajax-form");
    const formStatus = document.querySelector("#session-form-status");
    let debounceTimer;

    if (!results) {
        return;
    }

    const formatDate = (value) => new Intl.DateTimeFormat("id-ID", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Jakarta",
    }).format(new Date(value));

    const createSessionRow = (session) => {
        const fields = session.fields;
        const row = document.createElement("article");
        const timeWrapper = document.createElement("div");
        const time = document.createElement("time");
        const body = document.createElement("div");
        const level = document.createElement("p");
        const title = document.createElement("h2");
        const description = document.createElement("p");
        const duration = document.createElement("p");

        row.className = "session-row";
        timeWrapper.className = "session-time";
        time.dateTime = fields.scheduled_at;
        time.textContent = formatDate(fields.scheduled_at);
        body.className = "session-body";
        level.className = "session-level";
        level.textContent = fields.level === "basic" ? "Dasar" : fields.level === "intermediate" ? "Menengah" : "Lanjutan";
        title.textContent = fields.topic;
        description.textContent = fields.description;
        duration.className = "session-duration";
        duration.textContent = `${fields.duration_minutes} menit`;

        timeWrapper.append(time);
        body.append(level, title, description);
        row.append(timeWrapper, body, duration);
        return row;
    };

    const showEmptyState = (message) => {
        const state = document.createElement("div");
        const title = document.createElement("h2");
        const text = document.createElement("p");

        state.className = "empty-state";
        title.textContent = "Tidak ada sesi yang cocok.";
        text.textContent = message;
        state.append(title, text);
        results.replaceChildren(state);
    };

    const loadSessions = async (topic = "") => {
        const endpoint = new URL(results.dataset.apiUrl, window.location.origin);
        if (topic) {
            endpoint.searchParams.set("topic", topic);
        }

        loading.hidden = false;
        error.hidden = true;
        try {
            const response = await fetch(endpoint, { headers: { Accept: "application/json" } });
            if (!response.ok) {
                throw new Error("Request daftar sesi gagal.");
            }
            const sessions = await response.json();
            if (!sessions.length) {
                showEmptyState(topic ? "Ubah kata pencarian atau tambahkan sesi baru." : "Tambahkan sesi baru untuk mengisi jadwal belajar.");
                return;
            }
            results.replaceChildren(...sessions.map(createSessionRow));
        } catch (requestError) {
            results.replaceChildren();
            error.hidden = false;
        } finally {
            loading.hidden = true;
        }
    };

    searchInput?.addEventListener("input", () => {
        window.clearTimeout(debounceTimer);
        debounceTimer = window.setTimeout(() => loadSessions(searchInput.value.trim()), 300);
    });

    openDialogButton?.addEventListener("click", () => dialog.showModal());
    closeDialogButton?.addEventListener("click", () => dialog.close());
    cancelDialogButton?.addEventListener("click", () => dialog.close());

    form?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = form.querySelector('button[type="submit"]');
        const formData = new FormData(form);

        submitButton.disabled = true;
        formStatus.textContent = "Menyimpan sesi.";
        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    Accept: "application/json",
                },
            });
            const payload = await response.json();
            if (!response.ok) {
                const firstField = Object.keys(payload.errors || {})[0];
                const firstError = firstField ? payload.errors[firstField][0].message : "Data sesi belum dapat disimpan.";
                throw new Error(firstError);
            }
            form.reset();
            dialog.close();
            formStatus.textContent = "";
            window.showToast(payload.message);
            loadSessions(searchInput?.value.trim());
        } catch (requestError) {
            formStatus.textContent = requestError.message || "Koneksi gagal. Periksa jaringan lalu coba lagi.";
        } finally {
            submitButton.disabled = false;
        }
    });

    loadSessions();
})();
