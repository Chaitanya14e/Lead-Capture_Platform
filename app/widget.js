(function () {
    const script = document.currentScript;

    if (!script) {
        console.error("Widget script could not determine itself.");
        return;
    }

    const params = new URLSearchParams(script.src.split("?")[1]);
    const publicKey = params.get("widget");

    if (!publicKey) {
        console.error("Widget public key is missing.");
        return;
    }

    const API_BASE = new URL(script.src).origin;

    async function loadWidget() {
        try {
            const response = await fetch(
                `${API_BASE}/widgets/public/${publicKey}/config`
            );

            if (!response.ok) {
                throw new Error("Unable to load widget configuration.");
            }

            const config = await response.json();

            renderWidget(config);
        } catch (error) {
            console.error("Widget failed to load:", error);
        }
    }

    function renderWidget(config) {
        const container = document.createElement("div");

        container.id = "flyrank-widget";

        container.innerHTML = `
            <div style="
                max-width: 400px;
                padding: 24px;
                border: 1px solid #ddd;
                border-radius: 12px;
                font-family: Arial, sans-serif;
                background: #ffffff;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            ">
                <h2 style="
                    margin-top: 0;
                    margin-bottom: 8px;
                ">
                    ${escapeHtml(config.name)}
                </h2>

                ${
                    config.description
                        ? `<p style="color:#666;">${escapeHtml(config.description)}</p>`
                        : ""
                }

                <form id="flyrank-widget-form">

                    <input
                        type="text"
                        name="name"
                        placeholder="Your name"
                        required
                        maxlength="100"
                        style="
                            width:100%;
                            box-sizing:border-box;
                            padding:10px;
                            margin-bottom:10px;
                        "
                    />

                    <input
                        type="email"
                        name="email"
                        placeholder="Your email"
                        required
                        maxlength="255"
                        style="
                            width:100%;
                            box-sizing:border-box;
                            padding:10px;
                            margin-bottom:10px;
                        "
                    />

                    <textarea
                        name="message"
                        placeholder="Your message"
                        required
                        maxlength="5000"
                        rows="5"
                        style="
                            width:100%;
                            box-sizing:border-box;
                            padding:10px;
                            margin-bottom:10px;
                        "
                    ></textarea>

                    <input
                        type="text"
                        name="website"
                        tabindex="-1"
                        autocomplete="off"
                        style="
                            position:absolute;
                            left:-9999px;
                        "
                    />

                    <button
                        type="submit"
                        style="
                            width:100%;
                            padding:11px;
                            border:none;
                            border-radius:6px;
                            background:#111827;
                            color:white;
                            cursor:pointer;
                        "
                    >
                        Submit
                    </button>

                    <p
                        id="flyrank-widget-status"
                        style="margin-bottom:0;"
                    ></p>

                </form>
            </div>
        `;

        document.body.appendChild(container);

        const form = document.getElementById("flyrank-widget-form");
        const status = document.getElementById("flyrank-widget-status");

        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(form);

            const payload = {
                widget_id: config.id,
                idempotency_key: crypto.randomUUID(),
                name: formData.get("name"),
                email: formData.get("email"),
                message: formData.get("message"),
                honeypot: formData.get("website")
            };

            status.textContent = "Submitting...";

            try {
                const response = await fetch(
                    `${API_BASE}/submissions`,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(payload)
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.detail || "Submission failed."
                    );
                }

                status.textContent = "Thanks! Your message was submitted.";

                form.reset();

            } catch (error) {
                status.textContent = error.message;
            }
        });
    }

    function escapeHtml(value) {
        const div = document.createElement("div");
        div.textContent = value ?? "";
        return div.innerHTML;
    }

    loadWidget();
})();