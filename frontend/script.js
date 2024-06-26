document.getElementById('transfer-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const currentSquad = document.getElementById('current-squad').value.split(',').map(name => name.trim());
    const budget = parseFloat(document.getElementById('budget').value);
    const features = document.getElementById('features').value.split(',').map(Number);

    if (features.length !== 27 || features.some(isNaN) || isNaN(budget)) {
        alert('Please enter exactly 27 numeric features and a valid budget.');
        return;
    }

    const payload = {
        current_squad: currentSquad,
        budget: budget,
        features: features
    };

    const response = await fetch('http://127.0.0.1:5000/suggest_transfers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        const result = await response.json();
        let suggestionsHtml = '<h3>Suggested Transfers:</h3>';
        result.suggestions.forEach(suggestion => {
            suggestionsHtml += `
                <div>
                    <p><strong>Out:</strong> ${suggestion['Player Out']} (${suggestion['Out Team']})</p>
                    <p><strong>In:</strong> ${suggestion['Player In']} (${suggestion['In Team']})</p>
                    <p><strong>Predicted Score In:</strong> ${suggestion['Predicted Score In']}</p>
                    <p><strong>Predicted Score Out:</strong> ${suggestion['Predicted Score Out']}</p>
                    <p><strong>Remaining Budget:</strong> £${suggestion['Remaining Budget'].toFixed(1)}</p>
                </div>
            `;
        });
        document.getElementById('result').innerHTML = suggestionsHtml;
    } else {
        document.getElementById('result').innerText = `Error: ${response.statusText}`;
    }
});
