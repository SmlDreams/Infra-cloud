const button = document.getElementById('callApi');
const responseDiv = document.getElementById('response');

button.addEventListener('click', async () => {
    responseDiv.textContent = "Chargement...";
    try {
        const res = await fetch('http://api-test-mgmt.azure-api.net/hello'); // Remplace par l'URL de ton API
        if (!res.ok) throw new Error("Erreur lors de l'appel API");
        const data = await res.json();
        responseDiv.textContent = `Réponse API: ${JSON.stringify(data)}`;
    } catch (err) {
        responseDiv.textContent = `Erreur: ${err.message}`;
    }
});
