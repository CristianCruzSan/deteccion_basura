document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.querySelector('input[type="file"]');
    formData.append("file", fileInput.files[0]);

    const resultadosDiv = document.getElementById("resultados");
    resultadosDiv.innerHTML = "<p class='text-info'>Procesando imagen, espera...</p>";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Error en la predicción");

        const data = await response.json();

        if (data.detecciones.length === 0) {
            resultadosDiv.innerHTML = "<p class='text-warning'>No se detectó basura en la imagen.</p>";
            return;
        }

        resultadosDiv.innerHTML = "<h5>Resultados:</h5>";
        data.detecciones.forEach(det => {
            resultadosDiv.innerHTML += `<p><strong>${det.clase}</strong> - Confianza: ${(det.confianza * 100).toFixed(1)}%</p>`;
        });

    } catch (error) {
        resultadosDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
    }
});
