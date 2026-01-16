document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById("tracker");
    const summaryRow = document.getElementById("summary-row");

    function updatePersonWiseCount() {
        const totalCols = table.rows[1].cells.length - 1;
        const counts = new Array(totalCols).fill(0);

        for (let i = 2; i < table.rows.length - 1; i++) {
            let row = table.rows[i];
            for (let j = 1; j <= totalCols; j++) {
                if (row.cells[j].innerText.trim() === "✔️") {
                    counts[j - 1]++;
                }
            }
        }

        for (let k = 0; k < totalCols; k++) {
            summaryRow.cells[k + 1].innerText = counts[k];
        }
    }

    function saveData() {
        for (let i = 2; i < table.rows.length - 1; i++) {
            let row = table.rows[i];
            for (let j = 1; j < row.cells.length; j++) {
                let key = `cell-${i}-${j}`;
                let value = row.cells[j].innerText.trim();
                localStorage.setItem(key, value);
            }
        }
    }

    function loadData() {
        for (let i = 2; i < table.rows.length - 1; i++) {
            let row = table.rows[i];
            for (let j = 1; j < row.cells.length; j++) {
                let key = `cell-${i}-${j}`;
                let value = localStorage.getItem(key);
                if (value === "✔️") {
                    row.cells[j].innerText = "✔️";
                    row.cells[j].style.color = "green";
                } else if (value === "❌") {
                    row.cells[j].innerText = "❌";
                    row.cells[j].style.color = "red";
                } else {
                    row.cells[j].innerText = "";
                    row.cells[j].style.color = "black";
                }
            }
        }
    }

    // Add click handler to every cell
    for (let i = 2; i < table.rows.length - 1; i++) {
        let row = table.rows[i];
        for (let j = 1; j < row.cells.length; j++) {
            row.cells[j].addEventListener("click", function () {
                let current = this.innerText.trim();
                if (current === "") {
                    this.innerText = "✔️";
                    this.style.color = "green";
                } else if (current === "✔️") {
                    this.innerText = "❌";
                    this.style.color = "red";
                } else {
                    this.innerText = "";
                    this.style.color = "black";
                }
                saveData();
                updatePersonWiseCount();
            });
        }
    }

    loadData();              // Load saved ✔️❌ from storage
    updatePersonWiseCount(); // Initial count
});
