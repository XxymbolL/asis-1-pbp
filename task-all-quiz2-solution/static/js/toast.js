(() => {
    const region = document.querySelector("#toast-region");

    window.showToast = (message) => {
        if (!region) {
            return;
        }

        const toast = document.createElement("div");
        const text = document.createElement("p");
        const closeButton = document.createElement("button");

        toast.className = "toast";
        text.textContent = message;
        closeButton.type = "button";
        closeButton.className = "plain-button";
        closeButton.textContent = "Tutup";
        closeButton.addEventListener("click", () => toast.remove());

        toast.append(text, closeButton);
        region.replaceChildren(toast);
    };
})();
